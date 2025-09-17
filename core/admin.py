from django.contrib import admin
from .models import Resume, JobDescription, CoverLetter, OfferLetter, SkillGapReport

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'email', 'parsed_text']
    readonly_fields = ['parsed_text', 'extracted_skills', 'education', 'experience']

@admin.register(JobDescription)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'company', 'text']

@admin.register(CoverLetter)
class CoverLetterAdmin(admin.ModelAdmin):
    list_display = ['resume', 'job_description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['resume__name', 'job_description__title']

@admin.register(OfferLetter)
class OfferLetterAdmin(admin.ModelAdmin):
    list_display = ['ctc', 'probation_period', 'notice_period', 'created_at']
    list_filter = ['created_at']
    search_fields = ['text', 'explanation']
    readonly_fields = ['explanation', 'risk_flags', 'ctc', 'probation_period', 'notice_period']

@admin.register(SkillGapReport)
class SkillGapReportAdmin(admin.ModelAdmin):
    list_display = ['resume', 'job_description', 'fit_score', 'created_at']
    list_filter = ['created_at', 'fit_score']
    search_fields = ['resume__name', 'job_description__title']
    readonly_fields = ['fit_score', 'missing_skills', 'matching_skills', 'suggested_resources']
