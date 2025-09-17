import re
import json
import os
from typing import Dict, List, Tuple, Optional
import spacy
from pyresparser import ResumeParser
import docx2txt
from pdfminer.high_level import extract_text
from django.conf import settings
from django.core.exceptions import ValidationError, ImproperlyConfigured
import google.generativeai as genai
from time import sleep

# Load environment variables
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ImproperlyConfigured(
        "Missing Gemini API key—please set GEMINI_API_KEY (or GOOGLE_API_KEY) in your environment."
    )

# Configure Gemini client
try:
    genai.configure(api_key=API_KEY)
    GEMINI_MODEL = "gemini-1.5-flash"  # Updated model name
except Exception as e:
    raise ImproperlyConfigured(f"Failed to configure Gemini client: {str(e)}")

# Try to import magic for file validation
MAGIC_AVAILABLE = False
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    pass

# Load spaCy model
try:
    NLP = spacy.load("en_core_web_sm")
except OSError:
    raise ImproperlyConfigured("spaCy English model not found. Please install it with: python -m spacy download en_core_web_sm")

def validate_file_type(file_path: str, allowed_types: Optional[List[str]] = None) -> bool:
    """Validate file type using magic numbers or extension"""
    allowed_types = allowed_types or getattr(settings, 'ALLOWED_FILE_TYPES', ['pdf', 'docx', 'doc'])
    
    try:
        file_extension = os.path.splitext(file_path)[1][1:].lower()
        
        if not MAGIC_AVAILABLE:
            return file_extension in allowed_types
        
        # Use magic for MIME type validation
        mime = magic.from_file(file_path, mime=True)
        
        # MIME type mapping
        valid_mime_types = {
            'pdf': 'application/pdf',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'doc': 'application/msword'
        }
        
        return (file_extension in allowed_types and 
                mime == valid_mime_types.get(file_extension))
    except Exception:
        return False

def validate_file_size(file_path: str, max_size: Optional[int] = None) -> bool:
    """Validate file size"""
    max_size = max_size or getattr(settings, 'MAX_UPLOAD_SIZE', 10 * 1024 * 1024)  # 10MB
    
    try:
        return os.path.getsize(file_path) <= max_size
    except Exception:
        return False

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent security issues"""
    filename = os.path.basename(filename)
    return re.sub(r'[^\w\-_\.]', '', filename)

def generate_with_retry(prompt: str, max_retries: int = 3, **kwargs):
    """Helper function with retry logic for Gemini API calls"""
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel(GEMINI_MODEL)
            response = model.generate_content(prompt, **kwargs)
            if response.text:
                return response
            raise ValueError("Empty response from API")
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            sleep(2 ** attempt)  # Exponential backoff

def generate_cover_letter_with_gemini(
    resume_text: str,
    jd_text: str,
    custom_prompt: str = ""
) -> str:
    """Generate a cover letter using Gemini model."""
    if not resume_text or not jd_text:
        raise ValidationError("Both resume text and job description are required.")
    
    try:
        prompt = (
            "You are a professional career assistant. Generate a compelling, tailored cover letter.\n\n"
            f"Resume excerpt:\n{resume_text[:1000]}\n\n"
            f"Job Description excerpt:\n{jd_text[:1000]}\n\n"
            f"Additional instructions: {custom_prompt[:500]}"
        )
        
        response = generate_with_retry(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=512,
            )
        )
        return response.text.strip()
    except Exception as e:
        raise ValidationError(f"Failed to generate cover letter: {str(e)}")

def analyze_offer_letter_with_gemini(offer_text: str) -> Dict:
    """Analyze an offer letter and extract structured data."""
    if not offer_text:
        raise ValidationError("Offer letter text is required.")
    
    try:
        prompt = (
            "You are an HR analyst AI. Carefully analyze this job offer letter and return ONLY valid JSON with the following keys:\n"
            "- ctc (string)\n"
            "- probation_period (string)\n"
            "- notice_period (string)\n"
            "- risk_flags (list of strings identifying concerning terms, if any)\n"
            "- summary (string): concise summary of the offer\n"
            "- compensation_analysis (string): analysis of salary, perks, and fairness\n"
            "- terms_analysis (string): analysis of working hours, notice, legal issues, etc.\n"
            "- negotiation_points (list of strings): key terms that could be improved\n"
            "- questions_to_ask (list of strings): important things the candidate should clarify\n\n"
            f"Offer Letter:\n{offer_text[:2000]}"
        )
        
        response = generate_with_retry(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=600,
            )
        )

        # Remove ```json code block wrapper if present
        raw = response.text.strip()
        if raw.startswith("```") and raw.endswith("```"):
            lines = raw.splitlines()
            raw = "\n".join(lines[1:-1]).strip()

        return json.loads(raw)

    except json.JSONDecodeError as e:
        # Fallback default structure if Gemini response fails
        return {
            "ctc": "Not detected",
            "probation_period": "Not detected",
            "notice_period": "Not detected",
            "risk_flags": ["Could not analyze offer letter due to format issues."],
            "summary": "The system was unable to extract structured details from the offer letter.",
            "compensation_analysis": "Not available.",
            "terms_analysis": "Not available.",
            "negotiation_points": [],
            "questions_to_ask": []
        }

    except Exception as e:
        raise ValidationError(f"Failed to analyze offer letter: {str(e)}")

def calculate_job_fit_with_gemini(
    resume_skills: List[str],
    jd_text: str
) -> Tuple[float, List[str], List[str]]:
    """Let Gemini analyze job fit based on raw JD and resume skills."""
    try:
        prompt = f"""
You are an expert in HR skill analysis.

Compare the following resume skills with the provided job description.
Return JSON with:
- fit_score (0–100),
- matching_skills (list of strings),
- missing_skills (list of strings)

Resume Skills:
{resume_skills}

Job Description:
{jd_text}
"""
        response = generate_with_retry(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.0,
                max_output_tokens=300
            )
        )

        raw = response.text.strip()

        if raw.startswith("```") and raw.endswith("```"):
            lines = raw.splitlines()
            raw = "\n".join(lines[1:-1]).strip()

        data = json.loads(raw)

        return (
            float(data.get("fit_score", 0)),
            data.get("matching_skills", []),
            data.get("missing_skills", [])
        )
    except Exception as e:
        raise ValidationError(f"Failed to calculate job fit: {str(e)}")

def get_learning_resources_with_gemini(missing_skills: List[str]) -> List[Dict]:
    """Get learning resources for missing skills."""
    if not isinstance(missing_skills, list):
        raise ValidationError("Missing skills must be provided as a list")

    cleaned_skills = [s.lower().strip() for s in missing_skills if s]
    if not cleaned_skills:
        return []

    try:
        prompt = (
            "For these missing skills, list up to three high-quality learning resources per skill. "
            "Return ONLY valid JSON array with items containing: "
            "skill (string) and resources (array of {title, url, type}).\n\n"
            f"Missing Skills: {cleaned_skills}"
        )

        response = generate_with_retry(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=300,
            )
        )
        return json.loads(response.text.strip())
    except Exception:
        # Fallback to basic resources
        return [
            {
                "skill": skill,
                "resources": [
                    {
                        "title": f"Learn {skill.title()}",
                        "url": f"https://example.com/learn-{skill}",
                        "type": "course"
                    },
                    {
                        "title": f"{skill.title()} Tutorial",
                        "url": f"https://example.com/{skill}-tutorial",
                        "type": "tutorial"
                    }
                ]
            }
            for skill in cleaned_skills[:5]  # Limit to 5 skills
        ]
    

def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF, DOCX, or DOC files."""
    ext = os.path.splitext(file_path)[1][1:].lower()
    
    try:
        if ext == 'pdf':
            return extract_text(file_path)
        elif ext in ['docx', 'doc']:
            return docx2txt.process(file_path)
        else:
            raise ValidationError(f"Unsupported file type: {ext}")
    except Exception as e:
        raise ValidationError(f"Failed to extract text: {str(e)}")
    

def parse_resume_file(file_path):
    text = extract_text_from_file(file_path)

    prompt = f"""
You are an AI resume parser. Extract the following fields from the resume:
- name
- email
- phone
- education (as a list of strings)
- experience (as a list of strings)
- skills (as a list of short strings, only technical or job-relevant skills)
- parsed_text (raw cleaned text)

Return the response as valid JSON like this:
{{
  "name": "...",
  "email": "...",
  "phone": "...",
  "education": ["..."],
  "experience": ["..."],
  "skills": ["..."],
  "parsed_text": "..."
}}

Resume:
{text}
    """

    try:
        # Get Gemini response (already working in your code)
        response = generate_with_retry(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.0,
                max_output_tokens=1024,
            )
        ).text.strip()

        # ✅ Strip triple-backtick wrappers if present
        # This handles: ```json\n{...}\n```
        match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", response)
        cleaned = match.group(1) if match else response

        return json.loads(cleaned)

    except json.JSONDecodeError as e:
        raise ValidationError(f"Gemini responded with invalid JSON: {response}")
    except Exception as e:
        raise ValidationError(f"Error parsing resume with Gemini: {str(e)}")


def extract_skills_from_text(text: str) -> List[str]:
    """Extract skills from text using NLP and pattern matching."""
    if not text:
        return []
    
    try:
        doc = NLP(text.lower())
        skills = set()
        
        # Skill patterns
        patterns = [
            r'\b(python|java|javascript|react|angular|vue|node\.?js|django|flask|spring)\b',
            r'\b(sql|mongodb|postgresql|mysql|aws|azure|gcp|docker|kubernetes|git|jenkins)\b',
            r'\b(agile|scrum|html|css|bootstrap|jquery|ajax|rest|api|json|xml|soap|graphql)\b',
            r'\b(machine learning|ml|ai|deep learning|neural networks|tensorflow|pytorch|scikit-learn)\b',
            r'\b(project management|leadership|communication|problem solving|analytical thinking)\b'
        ]
        
        # Pattern matching
        for pattern in patterns:
            skills.update(re.findall(pattern, text.lower()))
        
        # Noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) <= 3:
                skills.add(chunk.text.lower())
        
        return sorted(skills)[:20]  # Return sorted and limited list
    except Exception as e:
        raise ValidationError(f"Failed to extract skills: {str(e)}")

def optimize_resume_for_ats(resume_text: str, job_description: str = "") -> str:
    """Optimize resume text for Applicant Tracking Systems."""
    try:
        if not resume_text:
            return ""
            
        if not job_description:
            return resume_text
            
        job_keywords = extract_skills_from_text(job_description)
        resume_skills = extract_skills_from_text(resume_text)
        missing_keywords = [kw for kw in job_keywords if kw not in resume_skills]
        
        if missing_keywords:
            return f"{resume_text}\n\nAdditional Skills: {', '.join(missing_keywords[:5])}"
        return resume_text
    except Exception as e:
        raise ValidationError(f"Failed to optimize resume: {str(e)}")

def calculate_user_readiness_score(user_profile) -> float:
    """Calculate a readiness score based on user's job search activity."""
    try:
        score = 20.0  # Base score
        
        # Applications submitted
        score += min(user_profile.total_applications * 2, 20)
        
        # Interviews attended
        score += min(user_profile.interviews_attended * 5, 30)
        
        # Offers received
        score += min(user_profile.offers_received * 10, 30)
        
        return min(score, 100.0)
    except Exception as e:
        raise ValidationError(f"Failed to calculate readiness score: {str(e)}")