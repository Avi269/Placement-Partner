# 📚 Placement Partner - API Documentation

## 🚀 Base URL
```
http://localhost:8000/api/
```

## 📋 API Endpoints Overview

| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/` | GET | API root with endpoint list | ✅ |
| `/resume/upload/` | POST | Upload and parse resume | ✅ |
| `/resume/generate/` | POST | Generate ATS-optimized resume | ✅ |
| `/resume/` | GET | List all resumes | ✅ |
| `/resume/{id}/` | GET | Get specific resume | ✅ |
| `/job-description/` | POST | Create job description | ✅ |
| `/job-description/` | GET | List job descriptions | ✅ |
| `/job-description/{id}/` | GET | Get specific job description | ✅ |
| `/cover-letter/generate/` | POST | Generate cover letter | ✅ |
| `/cover-letter/` | GET | List cover letters | ✅ |
| `/cover-letter/{id}/` | GET | Get specific cover letter | ✅ |
| `/job/match/` | POST | Match resume with job description | ✅ |
| `/skills/gaps/` | GET | Get missing skills and resources | ✅ |
| `/offer/explain/` | POST | Analyze offer letter | ✅ |
| `/offer-letter/` | GET | List offer letters | ✅ |
| `/offer-letter/{id}/` | GET | Get specific offer letter | ✅ |
| `/user/profile/` | GET | Get user readiness score | ✅ |
| `/user-profile/` | GET | List user profiles | ✅ |

---

## 🔍 Detailed Endpoint Documentation

### 1. API Root
**GET** `/api/`

Returns a list of all available API endpoints.

**Response:**
```json
{
  "resume_upload": "/resume/upload/",
  "resume_generate": "/resume/generate/",
  "cover_letter": "/cover-letter/generate/",
  "job_match": "/skill-gap-report/match/",
  "skills_gaps": "/skill-gap-report/gaps/",
  "offer_explain": "/offer-letter/explain/",
  "user_profile": "/user-profile/profile/"
}
```

---

### 2. Resume Management

#### Upload and Parse Resume
**POST** `/api/resume/upload/`

Upload a resume file or provide resume data for parsing.

**Request (File Upload):**
```bash
curl -X POST http://localhost:8000/api/resume/upload/ \
  -F "file=@resume.pdf"
```

**Request (JSON Data):**
```json
{
  "parsed_text": "John Doe\nSoftware Engineer\nPython, Django, React\n5 years experience",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123-456-7890",
  "extracted_skills": ["Python", "Django", "React", "JavaScript"],
  "education": [
    {
      "degree": "BS Computer Science",
      "university": "Tech University",
      "year": "2018"
    }
  ],
  "experience": [
    {
      "title": "Software Engineer",
      "company": "TechCorp",
      "duration": "2020-2023"
    }
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "file": null,
  "parsed_text": "John Doe\nSoftware Engineer...",
  "extracted_skills": ["Python", "Django", "React", "JavaScript"],
  "education": [...],
  "experience": [...],
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "123-456-7890",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### Generate ATS-Optimized Resume
**POST** `/api/resume/generate/`

Generate an ATS-optimized version of a resume.

**Request:**
```json
{
  "resume_id": 1,
  "job_description_id": 1
}
```

**Response:**
```json
{
  "resume_id": 1,
  "optimized_text": "John Doe\nSoftware Engineer\nPython, Django, React, JavaScript...",
  "original_text": "John Doe\nSoftware Engineer..."
}
```

#### List Resumes
**GET** `/api/resume/`

**Response:**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "extracted_skills": ["Python", "Django", "React"],
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 3. Job Description Management

#### Create Job Description
**POST** `/api/job-description/`

**Request:**
```json
{
  "title": "Senior Python Developer",
  "company": "TechCorp Solutions",
  "text": "We are seeking a Senior Python Developer with 5+ years of experience...",
  "required_skills": ["Python", "Django", "SQL", "JavaScript"],
  "preferred_skills": ["React", "AWS", "Docker"]
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Senior Python Developer",
  "company": "TechCorp Solutions",
  "text": "We are seeking a Senior Python Developer...",
  "required_skills": ["Python", "Django", "SQL", "JavaScript"],
  "preferred_skills": ["React", "AWS", "Docker"],
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### List Job Descriptions
**GET** `/api/job-description/`

**Response:**
```json
[
  {
    "id": 1,
    "title": "Senior Python Developer",
    "company": "TechCorp Solutions",
    "required_skills": ["Python", "Django", "SQL"],
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

---

### 4. Cover Letter Generation

#### Generate Cover Letter
**POST** `/api/cover-letter/generate/`

**Request:**
```json
{
  "resume_id": 1,
  "job_description_id": 1,
  "custom_prompt": "Emphasize my leadership experience and technical skills"
}
```

**Response:**
```json
{
  "id": 1,
  "resume": {
    "id": 1,
    "name": "John Doe"
  },
  "job_description": {
    "id": 1,
    "title": "Senior Python Developer"
  },
  "generated_text": "Dear Hiring Manager,\n\nI am writing to express my strong interest...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 5. Job Matching & Skill Analysis

#### Match Resume with Job Description
**POST** `/api/job/match/`

**Request:**
```json
{
  "resume_id": 1,
  "job_description_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "resume": {
    "id": 1,
    "name": "John Doe"
  },
  "job_description": {
    "id": 1,
    "title": "Senior Python Developer"
  },
  "fit_score": "85.50",
  "missing_skills": ["Kubernetes", "CI/CD"],
  "matching_skills": ["Python", "Django", "SQL", "JavaScript"],
  "suggested_resources": [
    {
      "skill": "Kubernetes",
      "resources": [
        {
          "title": "Learn Kubernetes",
          "url": "https://example.com/learn-kubernetes",
          "type": "course"
        }
      ]
    }
  ],
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Missing Skills and Resources
**GET** `/api/skills/gaps/?resume_id=1&job_description_id=1`

**Response:**
```json
{
  "missing_skills": ["Kubernetes", "CI/CD"],
  "suggested_resources": [...],
  "fit_score": "85.50"
}
```

---

### 6. Offer Letter Analysis

#### Analyze Offer Letter
**POST** `/api/offer/explain/`

**Request (File Upload):**
```bash
curl -X POST http://localhost:8000/api/offer/explain/ \
  -F "file=@offer_letter.pdf"
```

**Request (Text):**
```json
{
  "text": "Dear John Doe,\n\nWe are pleased to offer you the position of Senior Python Developer...\n\nCompensation:\n- Annual Salary: $120,000\n- Probation Period: 3 months\n- Notice Period: 30 days"
}
```

**Response:**
```json
{
  "id": 1,
  "file": null,
  "text": "Dear John Doe,\n\nWe are pleased to offer you...",
  "explanation": "This is a standard offer letter with typical terms and conditions.",
  "risk_flags": [
    "Standard probation period",
    "Typical notice period requirements"
  ],
  "ctc": "$120,000 per annum",
  "probation_period": "3 months",
  "notice_period": "30 days",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### 7. User Profile Management

#### Get User Readiness Score
**GET** `/api/user/profile/?user_id=1`

**Response:**
```json
{
  "user": "testuser",
  "readiness_score": "75.00",
  "total_applications": 15,
  "interviews_attended": 8,
  "offers_received": 2
}
```

---

## 🔧 Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid data provided",
  "details": {
    "field_name": ["This field is required."]
  }
}
```

### 404 Not Found
```json
{
  "error": "Resource not found"
}
```

### 415 Unsupported Media Type
```json
{
  "detail": "Unsupported media type \"application/json\" in request."
}
```

---

## 📝 Usage Examples

### Complete Workflow Example

1. **Upload Resume**
```bash
curl -X POST http://localhost:8000/api/resume/upload/ \
  -F "file=@my_resume.pdf"
```

2. **Create Job Description**
```bash
curl -X POST http://localhost:8000/api/job-description/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer",
    "company": "TechCorp",
    "text": "We are looking for a Python developer...",
    "required_skills": ["Python", "Django", "SQL"],
    "preferred_skills": ["React", "AWS"]
  }'
```

3. **Generate Cover Letter**
```bash
curl -X POST http://localhost:8000/api/cover-letter/generate/ \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_description_id": 1,
    "custom_prompt": "Emphasize my technical skills"
  }'
```

4. **Match Resume with Job**
```bash
curl -X POST http://localhost:8000/api/job/match/ \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_description_id": 1
  }'
```

5. **Analyze Offer Letter**
```bash
curl -X POST http://localhost:8000/api/offer/explain/ \
  -F "file=@offer_letter.pdf"
```

---

## 🛠️ Testing

### Test Script
Run the included test script to verify all endpoints:
```bash
python test_api.py
```

### Sample Data
Populate the database with sample data:
```bash
python create_sample_data.py
```

---

## 🔐 Authentication

Currently, the API uses `AllowAny` permissions for development. For production:

1. Add authentication classes to settings
2. Implement JWT or session-based authentication
3. Add permission classes to views
4. Configure proper CORS settings

---

## 📊 Rate Limiting

For production deployment, consider implementing:
- API rate limiting
- Request throttling
- Usage quotas

---

## 🚀 Production Considerations

1. **Database**: Migrate to PostgreSQL
2. **File Storage**: Use cloud storage (AWS S3, etc.)
3. **Caching**: Implement Redis for performance
4. **Monitoring**: Add logging and metrics
5. **Security**: Enable HTTPS, add authentication
6. **AI Integration**: Replace mock functions with actual Gemini Pro API

---

## 📞 Support

For questions or issues:
1. Check the API documentation at `/api/`
2. Review the admin interface at `/admin/`
3. Check Django logs for debugging
4. Run test scripts to verify functionality 