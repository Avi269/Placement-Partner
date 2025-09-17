from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import json
import logging
import tempfile
from .models import Resume, JobDescription, CoverLetter, OfferLetter, SkillGapReport
from .serializers import (
    ResumeSerializer, JobDescriptionSerializer, CoverLetterSerializer,
    OfferLetterSerializer, SkillGapReportSerializer,
    ResumeUploadSerializer, JobMatchSerializer, CoverLetterGenerateSerializer,
    OfferLetterAnalyzeSerializer, ATSOptimizeSerializer
)
from .utils import (
    parse_resume_file, optimize_resume_for_ats,
    calculate_user_readiness_score, extract_skills_from_text, generate_cover_letter_with_gemini,
    analyze_offer_letter_with_gemini,
    calculate_job_fit_with_gemini,
    get_learning_resources_with_gemini,
    extract_text_from_file,
)

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @action(detail=False, methods=['post'])
    def upload(self, request):
        """Upload and parse resume"""
        serializer = ResumeUploadSerializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.save(user=request.user)
            
            # Parse the uploaded file if provided
            if resume.file:
                file_path = resume.file.path
                parsed_data = parse_resume_file(file_path)
                
                # Update resume with parsed data
                resume.parsed_text = parsed_data.get('parsed_text', '')
                resume.name = parsed_data.get('name', '')
                resume.email = parsed_data.get('email', '')
                resume.phone = parsed_data.get('phone', '')
                resume.extracted_skills = parsed_data.get('skills', [])
                resume.education = parsed_data.get('education', [])
                resume.experience = parsed_data.get('experience', [])
                
                # If no skills found, try to extract from text
                if not resume.extracted_skills and resume.parsed_text:
                    resume.extracted_skills = extract_skills_from_text(resume.parsed_text)
                
                resume.save()
            elif resume.parsed_text and not resume.extracted_skills:
                # Extract skills from provided text
                resume.extracted_skills = extract_skills_from_text(resume.parsed_text)
                resume.save()
            
            return Response(ResumeSerializer(resume).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate ATS-optimized resume"""
        serializer = ATSOptimizeSerializer(data=request.data)
        if serializer.is_valid():
            resume = get_object_or_404(Resume, id=serializer.validated_data['resume_id'])
            
            job_description_text = ""
            if 'job_description_id' in serializer.validated_data:
                jd = get_object_or_404(JobDescription, id=serializer.validated_data['job_description_id'])
                job_description_text = jd.text
            
            # Optimize resume for ATS
            optimized_text = optimize_resume_for_ats(resume.parsed_text, job_description_text)
            
            return Response({
                'resume_id': resume.id,
                'optimized_text': optimized_text,
                'original_text': resume.parsed_text
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JobDescriptionViewSet(viewsets.ModelViewSet):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CoverLetterViewSet(viewsets.ModelViewSet):
    queryset = CoverLetter.objects.all()
    serializer_class = CoverLetterSerializer

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate cover letter"""
        serializer = CoverLetterGenerateSerializer(data=request.data)
        if serializer.is_valid():
            resume = get_object_or_404(Resume, id=serializer.validated_data['resume_id'])
            jd = get_object_or_404(JobDescription, id=serializer.validated_data['job_description_id'])
            custom_prompt = serializer.validated_data.get('custom_prompt', '')
            
            # Generate cover letter using AI
            cover_letter_text = generate_cover_letter_with_gemini(
                resume.parsed_text, 
                jd.text, 
                custom_prompt
            )
            
            # Save cover letter
            cover_letter = CoverLetter.objects.create(
                resume=resume,
                job_description=jd,
                generated_text=cover_letter_text
            )
            
            return Response(CoverLetterSerializer(cover_letter).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OfferLetterViewSet(viewsets.ModelViewSet):
    queryset = OfferLetter.objects.all()
    serializer_class = OfferLetterSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @action(detail=False, methods=['post'])
    def explain(self, request):
        """Analyze offer letter"""
        serializer = OfferLetterAnalyzeSerializer(data=request.data)
        if serializer.is_valid():
            offer_letter = serializer.save(user=request.user)
            
            # Extract text from file or use provided text
            offer_text = offer_letter.text or ""
            if offer_letter.file:
                offer_text = extract_text_from_file(offer_letter.file.path)
            
            # Analyze offer letter using AI
            analysis = analyze_offer_letter_with_gemini(offer_text)
            
            # Update offer letter with analysis
            offer_letter.explanation = analysis.get('explanation', '')
            offer_letter.risk_flags = analysis.get('risk_flags', [])
            offer_letter.ctc = analysis.get('ctc', '')
            offer_letter.probation_period = analysis.get('probation_period', '')
            offer_letter.notice_period = analysis.get('notice_period', '')
            offer_letter.save()
            
            return Response(OfferLetterSerializer(offer_letter).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SkillGapReportViewSet(viewsets.ModelViewSet):
    queryset = SkillGapReport.objects.all()
    serializer_class = SkillGapReportSerializer

    @action(detail=False, methods=['post'])
    def match(self, request):
        """Match resume with job description and calculate fit score"""
        serializer = JobMatchSerializer(data=request.data)
        if serializer.is_valid():
            resume = get_object_or_404(Resume, id=serializer.validated_data['resume_id'])
            jd = get_object_or_404(JobDescription, id=serializer.validated_data['job_description_id'])
            
            # Calculate job fit
            fit_score, missing_skills, matching_skills = calculate_job_fit_with_gemini(
                resume.extracted_skills, 
                jd.required_skills + jd.preferred_skills
            )
            
            # Get learning resources for missing skills
            suggested_resources = get_learning_resources_with_gemini(missing_skills)
            
            # Save skill gap report
            skill_gap_report = SkillGapReport.objects.create(
                resume=resume,
                job_description=jd,
                fit_score=fit_score,
                missing_skills=missing_skills,
                matching_skills=matching_skills,
                suggested_resources=suggested_resources
            )
            
            return Response(SkillGapReportSerializer(skill_gap_report).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def gaps(self, request):
        """Get missing skills and learning resources"""
        resume_id = request.query_params.get('resume_id')
        jd_id = request.query_params.get('job_description_id')
        
        if resume_id and jd_id:
            try:
                skill_gap_report = SkillGapReport.objects.get(
                    resume_id=resume_id,
                    job_description_id=jd_id
                )
                return Response({
                    'missing_skills': skill_gap_report.missing_skills,
                    'suggested_resources': skill_gap_report.suggested_resources,
                    'fit_score': skill_gap_report.fit_score
                })
            except SkillGapReport.DoesNotExist:
                return Response({'error': 'Skill gap report not found'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'error': 'resume_id and job_description_id are required'}, status=status.HTTP_400_BAD_REQUEST)


# Additional API views
@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    return Response({
        'resume_upload': '/resume/upload/',
        'resume_generate': '/resume/generate/',
        'cover_letter': '/cover-letter/generate/',
        'job_match': '/skill-gap-report/match/',
        'skills_gaps': '/skill-gap-report/gaps/',
        'offer_explain': '/offer-letter/explain/',
        'user_profile': '/user-profile/profile/',
    })

# Template Views
def home(request):
    """Home page view"""
    return render(request, 'core/home.html')

@csrf_exempt
def resume_upload_view(request):
    if request.method == 'GET':
        # Render the resume upload page
        return render(request, 'core/resume_upload.html')

    elif request.method == 'POST':
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return JsonResponse({"success": False, "message": "No file uploaded."})

        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resume_file.name)[-1]) as temp_file:
                for chunk in resume_file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            # Parse resume
            parsed_data = parse_resume_file(temp_file_path)

            # Delete temp file
            os.remove(temp_file_path)

            return JsonResponse({
                "success": True,
                "data": parsed_data
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": "Error processing resume.",
                "error": str(e)
            })

    else:
        return JsonResponse({"success": False, "message": "Invalid request method."})

@csrf_exempt
def job_matching_view(request):
    if request.method == 'GET':
        return render(request, 'core/job_matching.html')  # Load the HTML page on GET

    elif request.method == 'POST':
        try:
            data = request.POST
            jd_text = data.get("description", "")

            # TODO: Fetch skills from session or temp Resume (for now hardcoded or fetched by latest)
            resume = Resume.objects.last()
            if not resume:
                return JsonResponse({"success": False, "message": "No resume found"})

            fit_score, matching_skills, missing_skills = calculate_job_fit_with_gemini(
                resume.extracted_skills,
                jd_text  # ✅ send full JD to Gemini
            )

            return JsonResponse({
                "success": True,
                "fit_score": fit_score,
                "skills_match": fit_score,  # Optional
                "experience_match": 0,
                "education_match": 0,
                "matching_skills": matching_skills,
                "missing_skills": missing_skills,
                "recommendations": {
                    "skills_to_develop": missing_skills,
                    "learning_resources": get_learning_resources_with_gemini(missing_skills)
                }
            })

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    else:
        return JsonResponse({"success": False, "message": "Invalid method"})

def cover_letter_view(request):
    """Render the cover letter page and handle AJAX generation."""
    if request.method == 'POST':
        # Extract form data
        job_title = request.POST.get('job_title', '')
        company_name = request.POST.get('company_name', '')
        jd_text = request.POST.get('job_description', '')
        resume_text = request.POST.get('resume_text', '')
        custom_prompt = request.POST.get('custom_prompt', '')

        try:
            # Generate cover letter via Gemini helper
            cover_letter = generate_cover_letter_with_gemini(
                resume_text=resume_text,
                jd_text=jd_text,
                custom_prompt=custom_prompt
            )
        except ValidationError as e:
            message = str(e)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': message})
            messages.error(request, message)
            return redirect('cover_letter')
        except Exception as e:
            logging.exception("Error generating cover letter")
            message = f"Unexpected error generating cover letter: {e}"
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': message})
            messages.error(request, "An unexpected error occurred while generating the cover letter.")
            return redirect('cover_letter')

        # AJAX success response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'cover_letter': cover_letter})

        # Non-AJAX success path
        messages.success(request, 'Cover letter generated successfully!')
        return render(request, 'core/cover_letter.html', {'cover_letter': cover_letter})

    # GET request: simply render the template
    return render(request, 'core/cover_letter.html')

@csrf_exempt
def offer_analysis_view(request):
    if request.method == "GET":
        return render(request, "core/offer_analysis.html")

    elif request.method == "POST":
        try:
            offer_text = ""
            offer_file = request.FILES.get("file")
            if offer_file:
                # Save file to temp
                ext = os.path.splitext(offer_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp:
                    for chunk in offer_file.chunks():
                        temp.write(chunk)
                    temp_path = temp.name

                try:
                    offer_text = extract_text_from_file(temp_path)
                finally:
                    os.remove(temp_path)

            elif "text" in request.POST:
                offer_text = request.POST.get("text", "").strip()

            if not offer_text:
                return JsonResponse({"success": False, "message": "No offer letter text or file provided."})

            # Call Gemini-based analysis
            analysis = analyze_offer_letter_with_gemini(offer_text)

            return JsonResponse({
                "success": True,
                "ctc": analysis.get("ctc", ""),
                "probation_period": analysis.get("probation_period", ""),
                "notice_period": analysis.get("notice_period", ""),
                "risk_flags": analysis.get("risk_flags", []),
                "explanation": analysis.get("summary", "Analysis complete."),
                "negotiation_points": analysis.get("negotiation_points", []),
                "questions_to_ask": analysis.get("questions_to_ask", []),
                "compensation_analysis": analysis.get("compensation_analysis", ""),
                "terms_analysis": analysis.get("terms_analysis", "")
            })

        except Exception as e:
            logging.exception("Offer analysis error")
            return JsonResponse({"success": False, "message": f"Analysis failed: {e}"})

    else:
        return JsonResponse({"success": False, "message": "Only POST allowed."})

def dashboard(request):
    """Dashboard view"""
    return render(request, 'core/dashboard.html')

def profile(request):
    """User profile view"""
    return render(request, 'core/profile.html')