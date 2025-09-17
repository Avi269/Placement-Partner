from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'resume', views.ResumeViewSet, basename='resume')
router.register(r'job-description', views.JobDescriptionViewSet, basename='job-description')
router.register(r'cover-letter', views.CoverLetterViewSet, basename='cover-letter')
router.register(r'offer-letter', views.OfferLetterViewSet, basename='offer-letter')
router.register(r'skill-gap-report', views.SkillGapReportViewSet, basename='skill-gap-report')

# URL patterns
urlpatterns = [
    # Template Views
    path('', views.home, name='home'),
    path('resume/', views.resume_upload_view, name='resume_upload'),
    path('job-matching/', views.job_matching_view, name='job_matching'),
    path('cover-letter/', views.cover_letter_view, name='cover_letter'),
    path('offer-analysis/', views.offer_analysis_view, name='offer_analysis'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),

    # API root
    path('api/', views.api_root, name='api-root'),

    # Include router URLs
    path('api/', include(router.urls)),

    # Custom URL patterns for specific endpoints
    path('api/resume/upload/', views.ResumeViewSet.as_view({'post': 'upload'}), name='resume-upload'),
    path('api/resume/generate/', views.ResumeViewSet.as_view({'post': 'generate'}), name='resume-generate'),
    path('api/cover-letter/', views.CoverLetterViewSet.as_view({'post': 'generate'}), name='cover-letter-generate'),
    path('api/job/match/', views.SkillGapReportViewSet.as_view({'post': 'match'}), name='job-match'),
    path('api/skills/gaps/', views.SkillGapReportViewSet.as_view({'get': 'gaps'}), name='skills-gaps'),
    path('api/offer/explain/', views.OfferLetterViewSet.as_view({'post': 'explain'}), name='offer-explain'),
] 