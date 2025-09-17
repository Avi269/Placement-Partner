#!/usr/bin/env python3
"""
Simple test script to verify API endpoints
Run this after starting the Django server
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_api_root():
    """Test the API root endpoint"""
    print("Testing API root...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API root working")
            print(f"Available endpoints: {response.json()}")
        else:
            print(f"❌ API root failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API root error: {e}")

def test_job_description_creation():
    """Test creating a job description"""
    print("\nTesting job description creation...")
    try:
        data = {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "text": "We are looking for a Python developer with Django experience. Skills required: Python, Django, SQL, JavaScript. Preferred: React, AWS, Docker.",
            "required_skills": ["Python", "Django", "SQL", "JavaScript"],
            "preferred_skills": ["React", "AWS", "Docker"]
        }
        response = requests.post(f"{BASE_URL}/job-description/", json=data)
        if response.status_code == 201:
            print("✅ Job description created")
            return response.json()['id']
        else:
            print(f"❌ Job description creation failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Job description creation error: {e}")
    return None

def test_resume_creation():
    """Test creating a resume (without file upload)"""
    print("\nTesting resume creation...")
    try:
        data = {
            "parsed_text": "John Doe\nSoftware Engineer\nPython, Django, React\n5 years experience in web development",
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "123-456-7890",
            "extracted_skills": ["Python", "Django", "React", "JavaScript"],
            "education": [{"degree": "BS Computer Science", "university": "Tech University"}],
            "experience": [{"title": "Software Engineer", "company": "Previous Corp", "duration": "3 years"}]
        }
        response = requests.post(f"{BASE_URL}/resume/", json=data)
        if response.status_code == 201:
            print("✅ Resume created")
            return response.json()['id']
        else:
            print(f"❌ Resume creation failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Resume creation error: {e}")
    return None

def test_job_matching(resume_id, jd_id):
    """Test job matching functionality"""
    print("\nTesting job matching...")
    try:
        data = {
            "resume_id": resume_id,
            "job_description_id": jd_id
        }
        response = requests.post(f"{BASE_URL}/job/match/", json=data)
        if response.status_code == 201:
            result = response.json()
            print("✅ Job matching successful")
            print(f"Fit score: {result['fit_score']}%")
            print(f"Missing skills: {result['missing_skills']}")
            print(f"Matching skills: {result['matching_skills']}")
        else:
            print(f"❌ Job matching failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Job matching error: {e}")

def test_cover_letter_generation(resume_id, jd_id):
    """Test cover letter generation"""
    print("\nTesting cover letter generation...")
    try:
        data = {
            "resume_id": resume_id,
            "job_description_id": jd_id,
            "custom_prompt": "Emphasize my Python and Django experience"
        }
        response = requests.post(f"{BASE_URL}/cover-letter/generate/", json=data)
        if response.status_code == 201:
            result = response.json()
            print("✅ Cover letter generated")
            print(f"Cover letter preview: {result['generated_text'][:100]}...")
        else:
            print(f"❌ Cover letter generation failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Cover letter generation error: {e}")

def test_offer_letter_analysis():
    """Test offer letter analysis"""
    print("\nTesting offer letter analysis...")
    try:
        data = {
            "text": "Dear John Doe, We are pleased to offer you the position of Software Engineer at Tech Corp. Your CTC will be $80,000 per annum. Probation period: 6 months. Notice period: 60 days."
        }
        response = requests.post(f"{BASE_URL}/offer/explain/", json=data)
        if response.status_code == 201:
            result = response.json()
            print("✅ Offer letter analysis successful")
            print(f"CTC: {result['ctc']}")
            print(f"Probation: {result['probation_period']}")
            print(f"Notice: {result['notice_period']}")
            print(f"Risk flags: {result['risk_flags']}")
        else:
            print(f"❌ Offer letter analysis failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Offer letter analysis error: {e}")

def main():
    """Run all tests"""
    print("🚀 Testing Placement Partner API")
    print("=" * 50)
    
    # Test API root
    test_api_root()
    
    # Test job description creation
    jd_id = test_job_description_creation()
    
    # Test resume creation
    resume_id = test_resume_creation()
    
    if jd_id and resume_id:
        # Test job matching
        test_job_matching(resume_id, jd_id)
        
        # Test cover letter generation
        test_cover_letter_generation(resume_id, jd_id)
    
    # Test offer letter analysis
    test_offer_letter_analysis()
    
    print("\n" + "=" * 50)
    print("✅ API testing completed!")
    print(f"📖 API Documentation: {BASE_URL}/")
    print(f"🔧 Admin Interface: http://localhost:8000/admin/")

if __name__ == "__main__":
    main() 