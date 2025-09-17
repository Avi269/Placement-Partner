from django.db import models
from django.conf import settings
import uuid
import os

def resume_file_path(instance, filename):
    """Generate file path for resume uploads"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('resumes', filename)

def offer_letter_file_path(instance, filename):
    """Generate file path for offer letter uploads"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('offer_letters', filename)

class Resume(models.Model):
    """Model for storing resume information"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=resume_file_path, null=True, blank=True)
    parsed_text = models.TextField(blank=True)
    extracted_skills = models.JSONField(default=list, blank=True)
    education = models.JSONField(default=list, blank=True)
    experience = models.JSONField(default=list, blank=True)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume - {self.name or 'Unknown'}"

class JobDescription(models.Model):
    """Model for storing job descriptions"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    required_skills = models.JSONField(default=list, blank=True)
    preferred_skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class CoverLetter(models.Model):
    """Model for storing generated cover letters"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    generated_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cover Letter for {self.job_description.title}"

class OfferLetter(models.Model):
    """Model for storing offer letter analysis"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=offer_letter_file_path, null=True, blank=True)
    text = models.TextField(blank=True)
    explanation = models.TextField(blank=True)
    risk_flags = models.JSONField(default=list, blank=True)
    ctc = models.CharField(max_length=100, blank=True)
    probation_period = models.CharField(max_length=100, blank=True)
    notice_period = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer Letter Analysis - {self.created_at.strftime('%Y-%m-%d')}"

class SkillGapReport(models.Model):
    """Model for storing skill gap analysis results"""
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    fit_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    missing_skills = models.JSONField(default=list, blank=True)
    matching_skills = models.JSONField(default=list, blank=True)
    suggested_resources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Skill Gap Report - {self.fit_score}% fit"

