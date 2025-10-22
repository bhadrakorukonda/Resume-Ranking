# Resume Ranker Backend

A Flask-based backend service for ranking resumes using TOPSIS (Technique for Order Preference by Similarity to Ideal Solution) with NLP-based feature extraction.

## Features

- **Resume Processing**: Extract text from PDF resumes using PyPDF2
- **NLP Features**: Extract skills, experience, projects, and education using spaCy
- **Job Description Alignment**: Calculate similarity using rapidfuzz
- **TOPSIS Ranking**: Multi-criteria decision making for candidate ranking
- **Weight Management**: Configurable weights for different criteria
- **RESTful API**: Clean API endpoints for all operations

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Download spaCy Model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

The server will start on `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /health` - Check service health

### Weights Management
- `GET /weights` - Get all weight configurations
- `POST /weights` - Create new weight configuration

### Resume Upload
- `POST /upload` - Upload resume PDF with job description
  - Form data: `resume` (file), `job_description` (text), `name`, `email`, `phone`

### Candidate Ranking
- `POST /rank` - Rank all candidates using TOPSIS
  - JSON body: `weights` (optional) or `weights_id` (optional)

### Candidate Management
- `GET /candidates` - Get all candidates
- `GET /candidates/<id>` - Get specific candidate
- `DELETE /candidates/<id>` - Delete candidate

## Configuration

Default weights and feature order are defined in `config.py`:

```python
DEFAULT_WEIGHTS = {
    'skill_match': 0.25,
    'jd_alignment': 0.30,
    'exp_years': 0.20,
    'projects': 0.15,
    'education': 0.10
}
```

## Testing

Run tests with:
```bash
python -m pytest tests/
```

## Database

The application uses SQLite with SQLAlchemy ORM. The database file (`resume_ranker.db`) will be created automatically on first run.

## File Structure

```
backend/
├── app.py              # Flask application
├── config.py           # Configuration settings
├── db.py              # Database setup
├── models.py          # SQLAlchemy models
├── nlp.py             # NLP feature extraction
├── mcdm.py            # TOPSIS implementation
├── requirements.txt   # Python dependencies
├── tests/             # Test files
└── uploads/           # Uploaded PDF files
```
