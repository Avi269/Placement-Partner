# Placement Partner - Django Backend

A comprehensive Django REST API backend for a placement assistance application that helps students and job seekers with resume optimization, cover letter generation, job matching, and offer letter analysis.

## 🚀 Features

### Core Modules
- **Resume & Cover Letter Generator**
  - Upload and parse resumes (PDF/DOCX)
  - Extract skills, education, and experience
  - Generate job-specific cover letters using AI
  - ATS-optimized resume generation

- **Offer Letter Explainer**
  - Upload or paste offer letters
  - AI-powered analysis and risk assessment
  - Extract key terms (CTC, probation, notice period)
  - Flag problematic clauses

- **Job Fit & Skill Gap Analyzer**
  - Compare resume with job descriptions
  - Calculate job-fit percentage
  - Identify missing skills
  - Suggest learning resources

- **User Profile Management**
  - Track application progress
  - Calculate readiness scores
  - Monitor interview and offer statistics

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4 + Django REST Framework
- **Database**: SQLite (development)
- **File Processing**: pyresparser, pdfminer.six, python-docx
- **NLP**: spaCy
- **AI Integration**: Mock functions (ready for Gemini Pro integration)
- **CORS**: django-cors-headers

## 📋 API Endpoints

### Resume Management
- `POST /api/resume/upload/` - Upload and parse resume
- `POST /api/resume/generate/` - Generate ATS-optimized resume
- `GET /api/resume/` - List all resumes
- `GET /api/resume/{id}/` - Get specific resume

### Job Descriptions
- `POST /api/job-description/` - Create job description
- `GET /api/job-description/` - List job descriptions
- `GET /api/job-description/{id}/` - Get specific job description

### Cover Letters
- `POST /api/cover-letter/generate/` - Generate cover letter
- `GET /api/cover-letter/` - List cover letters
- `GET /api/cover-letter/{id}/` - Get specific cover letter

### Job Matching & Skill Analysis
- `POST /api/job/match/` - Match resume with job description
- `GET /api/skills/gaps/` - Get missing skills and resources
- `GET /api/skill-gap-report/` - List skill gap reports

### Offer Letter Analysis
- `POST /api/offer/explain/` - Analyze offer letter
- `GET /api/offer-letter/` - List offer letters
- `GET /api/offer-letter/{id}/` - Get specific offer letter

### User Profile
- `GET /api/user/profile/` - Get user readiness score
- `GET /api/user-profile/` - List user profiles

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Placement_Partner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### Access Points
- **API Root**: http://localhost:8000/api/
- **Admin Interface**: http://localhost:8000/admin/
- **API Documentation**: Available through Django REST Framework browsable API

## 📝 Usage Examples

### Upload Resume
```bash
curl -X POST http://localhost:8000/api/resume/upload/ \
  -F "file=@resume.pdf"
```

### Generate Cover Letter
```bash
curl -X POST http://localhost:8000/api/cover-letter/generate/ \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_description_id": 1,
    "custom_prompt": "Emphasize my leadership experience"
  }'
```

### Job Matching
```bash
curl -X POST http://localhost:8000/api/job/match/ \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": 1,
    "job_description_id": 1
  }'
```

### Analyze Offer Letter
```bash
curl -X POST http://localhost:8000/api/offer/explain/ \
  -F "file=@offer_letter.pdf"
```

## 🏗️ Project Structure

```
Placement_Partner/
├── core/                    # Main application
│   ├── models.py           # Database models
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # API views
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin interface
│   └── utils.py            # Utility functions
├── placement_partner/       # Project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL config
│   └── wsgi.py             # WSGI config
├── media/                  # Uploaded files
├── manage.py               # Django management
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## 🔧 Configuration

### Environment Variables
- `DEBUG`: Set to `True` for development
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: List of allowed hosts

### File Upload Settings
- Resume files: `media/resumes/`
- Offer letters: `media/offer_letters/`
- Supported formats: PDF, DOCX, DOC

## 🤖 AI Integration

The backend includes mock AI functions that can be easily replaced with actual Gemini Pro API integration:

- `mock_generate_cover_letter()` - Cover letter generation
- `mock_analyze_offer_letter()` - Offer letter analysis
- `mock_calculate_job_fit()` - Job matching algorithm
- `mock_get_learning_resources()` - Learning resource suggestions

## 🧪 Testing

Run the development server and test endpoints using:
- Django REST Framework browsable API
- Postman or similar API testing tools
- curl commands

## 📊 Database Models

- **Resume**: Stores parsed resume data and extracted information
- **JobDescription**: Job posting details and requirements
- **CoverLetter**: Generated cover letters with context
- **OfferLetter**: Analyzed offer letters with risk assessment
- **SkillGapReport**: Job matching results and skill analysis
- **UserProfile**: User progress tracking and readiness scores

## 🔒 Security Features

- CORS configuration for cross-origin requests
- File upload validation
- Admin interface for data management
- Input sanitization and validation

## 🚀 Deployment

For production deployment:
1. Set `DEBUG = False`
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables
5. Set up proper CORS settings
6. Integrate with actual AI services

## 📞 Support

For questions or issues:
1. Check the API documentation at `/api/`
2. Review the admin interface at `/admin/`
3. Check Django logs for debugging

## 📄 License

This project is developed for educational and demonstration purposes. 