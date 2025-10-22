import os
from pathlib import Path

# Database configuration
DATABASE_URL = 'sqlite:///resume_ranker.db'

# Default weights for TOPSIS
DEFAULT_WEIGHTS = {
    'skill_match': 0.25,
    'jd_alignment': 0.30,
    'exp_years': 0.20,
    'projects': 0.15,
    'education': 0.10
}

# Feature order for consistent processing
FEATURE_ORDER = ['skill_match', 'jd_alignment', 'exp_years', 'projects', 'education']

# Benefit mask - True for benefit criteria (higher is better), False for cost criteria
BENEFIT_MASK = {
    'skill_match': True,
    'jd_alignment': True,
    'exp_years': True,
    'projects': True,
    'education': True
}

# File upload configuration
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf'}

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Create upload directory if it doesn't exist
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
