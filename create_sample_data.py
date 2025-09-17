#!/usr/bin/env python3
"""
Script to create sample data for the Placement Partner application
Run this after starting the Django server
"""

import os
import django
import requests
import json

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_partner.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Resume, JobDescription, CoverLetter, OfferLetter, SkillGapReport, UserProfile

BASE_URL = "http://localhost:8000/api"

def create_sample_users():
    """Create sample users"""
    print("Creating sample users...")
    
    # Create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'testuser@example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Created user: {user.username}")
    else:
        print(f"✅ User already exists: {user.username}")
    
    return user

def create_sample_job_descriptions():
    """Create sample job descriptions"""
    print("\nCreating sample job descriptions...")
    
    jobs_data = [
        {
            "title": "Senior Python Developer",
            "company": "TechCorp Solutions",
            "text": "We are seeking a Senior Python Developer with 5+ years of experience in Django, Flask, and REST APIs. Must have strong knowledge of SQL, PostgreSQL, and cloud platforms like AWS. Experience with React, Docker, and CI/CD pipelines is preferred.",
            "required_skills": ["Python", "Django", "Flask", "SQL", "PostgreSQL", "REST APIs"],
            "preferred_skills": ["React", "AWS", "Docker", "CI/CD", "Kubernetes"]
        },
        {
            "title": "Frontend Developer",
            "company": "WebFlow Inc",
            "text": "Join our team as a Frontend Developer! We need someone with strong JavaScript skills, React experience, and knowledge of modern CSS frameworks. Experience with TypeScript, Redux, and responsive design is a plus.",
            "required_skills": ["JavaScript", "React", "HTML", "CSS", "Responsive Design"],
            "preferred_skills": ["TypeScript", "Redux", "Next.js", "Tailwind CSS", "GraphQL"]
        },
        {
            "title": "Data Scientist",
            "company": "Analytics Pro",
            "text": "We're looking for a Data Scientist with expertise in Python, machine learning, and statistical analysis. Must have experience with pandas, numpy, scikit-learn, and data visualization tools. Knowledge of deep learning frameworks is preferred.",
            "required_skills": ["Python", "Machine Learning", "Statistics", "Pandas", "NumPy", "Scikit-learn"],
            "preferred_skills": ["TensorFlow", "PyTorch", "Deep Learning", "SQL", "Big Data"]
        }
    ]
    
    created_jobs = []
    for job_data in jobs_data:
        try:
            response = requests.post(f"{BASE_URL}/job-description/", json=job_data)
            if response.status_code == 201:
                job = response.json()
                created_jobs.append(job['id'])
                print(f"✅ Created job: {job_data['title']} at {job_data['company']}")
            else:
                print(f"❌ Failed to create job: {job_data['title']}")
        except Exception as e:
            print(f"❌ Error creating job: {e}")
    
    return created_jobs

def create_sample_resumes():
    """Create sample resumes"""
    print("\nCreating sample resumes...")
    
    resumes_data = [
        {
            "parsed_text": """John Doe
Software Engineer
john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe

EXPERIENCE
Senior Developer, TechCorp (2020-2023)
- Developed REST APIs using Django and Flask
- Worked with PostgreSQL and Redis databases
- Implemented CI/CD pipelines with Jenkins
- Led team of 3 junior developers

Junior Developer, StartupXYZ (2018-2020)
- Built web applications using Python and JavaScript
- Used React for frontend development
- Collaborated with cross-functional teams

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2018

SKILLS
Python, Django, Flask, JavaScript, React, SQL, PostgreSQL, Git, Docker, AWS""",
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "(555) 123-4567",
            "extracted_skills": ["Python", "Django", "Flask", "JavaScript", "React", "SQL", "PostgreSQL", "Git", "Docker", "AWS"],
            "education": [{"degree": "BS Computer Science", "university": "University of Technology", "year": "2018"}],
            "experience": [
                {"title": "Senior Developer", "company": "TechCorp", "duration": "2020-2023"},
                {"title": "Junior Developer", "company": "StartupXYZ", "duration": "2018-2020"}
            ]
        },
        {
            "parsed_text": """Jane Smith
Frontend Developer
jane.smith@email.com | (555) 987-6543 | linkedin.com/in/janesmith

EXPERIENCE
Frontend Developer, WebFlow Inc (2021-2023)
- Built responsive web applications using React and TypeScript
- Implemented state management with Redux
- Optimized performance and accessibility
- Mentored junior developers

UI/UX Designer, DesignStudio (2019-2021)
- Created user interfaces and prototypes
- Used Figma and Adobe Creative Suite
- Conducted user research and testing

EDUCATION
Bachelor of Arts in Design
Design Institute, 2019

SKILLS
JavaScript, React, TypeScript, Redux, HTML, CSS, Figma, Adobe Creative Suite, User Research""",
            "name": "Jane Smith",
            "email": "jane.smith@email.com",
            "phone": "(555) 987-6543",
            "extracted_skills": ["JavaScript", "React", "TypeScript", "Redux", "HTML", "CSS", "Figma", "Adobe Creative Suite"],
            "education": [{"degree": "BA Design", "university": "Design Institute", "year": "2019"}],
            "experience": [
                {"title": "Frontend Developer", "company": "WebFlow Inc", "duration": "2021-2023"},
                {"title": "UI/UX Designer", "company": "DesignStudio", "duration": "2019-2021"}
            ]
        }
    ]
    
    created_resumes = []
    for resume_data in resumes_data:
        try:
            response = requests.post(f"{BASE_URL}/resume/", json=resume_data)
            if response.status_code == 201:
                resume = response.json()
                created_resumes.append(resume['id'])
                print(f"✅ Created resume for: {resume_data['name']}")
            else:
                print(f"❌ Failed to create resume for: {resume_data['name']}")
        except Exception as e:
            print(f"❌ Error creating resume: {e}")
    
    return created_resumes

def create_sample_offer_letters():
    """Create sample offer letters"""
    print("\nCreating sample offer letters...")
    
    offers_data = [
        {
            "text": """Dear John Doe,

We are pleased to offer you the position of Senior Python Developer at TechCorp Solutions.

Position: Senior Python Developer
Department: Engineering
Start Date: March 1, 2024
Location: San Francisco, CA (Hybrid)

Compensation:
- Annual Salary: $120,000
- Signing Bonus: $10,000
- Equity: 0.1% of company shares
- Benefits: Health, dental, vision, 401(k) with 4% match

Terms and Conditions:
- Probation Period: 3 months
- Notice Period: 30 days
- Non-compete: 12 months after termination
- Confidentiality: Permanent

Please review this offer and respond within 7 days.

Best regards,
HR Team
TechCorp Solutions"""
        },
        {
            "text": """Dear Jane Smith,

Congratulations! We are excited to offer you the Frontend Developer position at WebFlow Inc.

Position: Frontend Developer
Department: Product Development
Start Date: February 15, 2024
Location: Remote

Compensation Package:
- Base Salary: $95,000 per annum
- Performance Bonus: Up to 15% of base salary
- Stock Options: 500 shares vesting over 4 years
- Benefits: Comprehensive health coverage, unlimited PTO

Employment Terms:
- Probation: 6 months
- Notice Period: 60 days
- Intellectual Property: All work belongs to company
- Non-disclosure: 2 years after employment

We look forward to having you on our team!

Best regards,
Talent Acquisition
WebFlow Inc"""
        }
    ]
    
    created_offers = []
    for offer_data in offers_data:
        try:
            response = requests.post(f"{BASE_URL}/offer/explain/", json=offer_data)
            if response.status_code == 201:
                offer = response.json()
                created_offers.append(offer['id'])
                print(f"✅ Created offer letter analysis")
            else:
                print(f"❌ Failed to create offer letter analysis")
        except Exception as e:
            print(f"❌ Error creating offer letter: {e}")
    
    return created_offers

def create_sample_user_profiles():
    """Create sample user profiles"""
    print("\nCreating sample user profiles...")
    
    try:
        user = User.objects.get(username='testuser')
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'readiness_score': 75.0,
                'total_applications': 15,
                'interviews_attended': 8,
                'offers_received': 2
            }
        )
        
        if created:
            print(f"✅ Created user profile for {user.username}")
        else:
            print(f"✅ User profile already exists for {user.username}")
            
    except Exception as e:
        print(f"❌ Error creating user profile: {e}")

def run_job_matching_tests(resume_ids, job_ids):
    """Run job matching tests with sample data"""
    print("\nRunning job matching tests...")
    
    for resume_id in resume_ids:
        for job_id in job_ids:
            try:
                data = {
                    "resume_id": resume_id,
                    "job_description_id": job_id
                }
                response = requests.post(f"{BASE_URL}/job/match/", json=data)
                if response.status_code == 201:
                    result = response.json()
                    print(f"✅ Job matching: Resume {resume_id} vs Job {job_id} - Fit: {result['fit_score']}%")
                else:
                    print(f"❌ Job matching failed for Resume {resume_id} vs Job {job_id}")
            except Exception as e:
                print(f"❌ Error in job matching: {e}")

def run_cover_letter_tests(resume_ids, job_ids):
    """Run cover letter generation tests"""
    print("\nRunning cover letter generation tests...")
    
    for resume_id in resume_ids[:1]:  # Test with first resume
        for job_id in job_ids[:1]:    # Test with first job
            try:
                data = {
                    "resume_id": resume_id,
                    "job_description_id": job_id,
                    "custom_prompt": "Emphasize my technical skills and leadership experience"
                }
                response = requests.post(f"{BASE_URL}/cover-letter/generate/", json=data)
                if response.status_code == 201:
                    result = response.json()
                    print(f"✅ Cover letter generated for Resume {resume_id} and Job {job_id}")
                else:
                    print(f"❌ Cover letter generation failed")
            except Exception as e:
                print(f"❌ Error in cover letter generation: {e}")

def main():
    """Main function to create all sample data"""
    print("🚀 Creating Sample Data for Placement Partner")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("❌ Django server is not running. Please start it with: python manage.py runserver")
            return
    except:
        print("❌ Django server is not running. Please start it with: python manage.py runserver")
        return
    
    # Create sample data
    user = create_sample_users()
    job_ids = create_sample_job_descriptions()
    resume_ids = create_sample_resumes()
    offer_ids = create_sample_offer_letters()
    create_sample_user_profiles()
    
    # Run tests with sample data
    if resume_ids and job_ids:
        run_job_matching_tests(resume_ids, job_ids)
        run_cover_letter_tests(resume_ids, job_ids)
    
    print("\n" + "=" * 60)
    print("✅ Sample data creation completed!")
    print(f"📊 Created: {len(job_ids)} jobs, {len(resume_ids)} resumes, {len(offer_ids)} offer letters")
    print(f"🔗 API Documentation: {BASE_URL}/")
    print(f"🔧 Admin Interface: http://localhost:8000/admin/")
    print(f"👤 Admin Login: admin/admin or demo/demo")

if __name__ == "__main__":
    main() 