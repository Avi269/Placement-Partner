from rest_framework import serializers
from .models import Resume, JobDescription, CoverLetter, OfferLetter, SkillGapReport
from accounts.serializers import UserSerializer

class ResumeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Resume
        fields = '__all__'
        read_only_fields = ['parsed_text', 'extracted_skills', 'education', 'experience', 'name', 'email', 'phone']

class JobDescriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = JobDescription
        fields = '__all__'

class CoverLetterSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(read_only=True)
    job_description = JobDescriptionSerializer(read_only=True)
    
    class Meta:
        model = CoverLetter
        fields = '__all__'

class OfferLetterSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = OfferLetter
        fields = '__all__'
        read_only_fields = ['explanation', 'risk_flags', 'ctc', 'probation_period', 'notice_period']

class SkillGapReportSerializer(serializers.ModelSerializer):
    resume = ResumeSerializer(read_only=True)
    job_description = JobDescriptionSerializer(read_only=True)
    
    class Meta:
        model = SkillGapReport
        fields = '__all__'
        read_only_fields = ['fit_score', 'missing_skills', 'matching_skills', 'suggested_resources']

# Special serializers for specific API endpoints
class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['file', 'parsed_text', 'name', 'email', 'phone', 'extracted_skills', 'education', 'experience']
        extra_kwargs = {
            'file': {'required': False},
            'parsed_text': {'required': False},
            'name': {'required': False},
            'email': {'required': False},
            'phone': {'required': False},
            'extracted_skills': {'required': False},
            'education': {'required': False},
            'experience': {'required': False},
        }

class JobMatchSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    job_description_id = serializers.IntegerField()

class CoverLetterGenerateSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    job_description_id = serializers.IntegerField()
    custom_prompt = serializers.CharField(required=False, allow_blank=True)

class OfferLetterAnalyzeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferLetter
        fields = ['file', 'text']
        extra_kwargs = {
            'file': {'required': False},
            'text': {'required': False},
        }

class ATSOptimizeSerializer(serializers.Serializer):
    resume_id = serializers.IntegerField()
    job_description_id = serializers.IntegerField(required=False) 