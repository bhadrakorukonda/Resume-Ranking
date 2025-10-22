import PyPDF2
import spacy
import re
from rapidfuzz import fuzz
from typing import Dict, List, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load spaCy model (you may need to download it: python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load("en_core_web_sm")
except (OSError, Exception) as e:
    logger.warning(f"spaCy model 'en_core_web_sm' not found or error loading: {e}. Please install it with: python -m spacy download en_core_web_sm")
    nlp = None

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file using PyPDF2"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
        return ""

def extract_skills(text: str) -> List[str]:
    """Extract skills from resume text using spaCy NER and keyword matching"""
    if not nlp:
        return extract_skills_fallback(text)
    
    doc = nlp(text)
    skills = set()
    
    # Common technical skills keywords
    skill_keywords = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'django', 'flask',
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'docker', 'kubernetes', 'aws', 'azure',
        'git', 'github', 'gitlab', 'jenkins', 'ci/cd', 'agile', 'scrum', 'machine learning',
        'data science', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'r',
        'tableau', 'power bi', 'excel', 'vba', 'html', 'css', 'bootstrap', 'jquery',
        'rest api', 'graphql', 'microservices', 'linux', 'unix', 'bash', 'powershell'
    ]
    
    # Extract from NER
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'TECH']:
            skills.add(ent.text.lower())
    
    # Extract from keywords
    text_lower = text.lower()
    for keyword in skill_keywords:
        if keyword in text_lower:
            skills.add(keyword)
    
    # Extract from noun phrases that might be skills
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower().strip()
        if len(chunk_text) > 2 and any(char.isalpha() for char in chunk_text):
            if any(skill in chunk_text for skill in skill_keywords):
                skills.add(chunk_text)
    
    return list(skills)

def extract_skills_fallback(text: str) -> List[str]:
    """Fallback skill extraction without spaCy"""
    skill_keywords = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'django', 'flask',
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'docker', 'kubernetes', 'aws', 'azure',
        'git', 'github', 'gitlab', 'jenkins', 'ci/cd', 'agile', 'scrum', 'machine learning',
        'data science', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'r',
        'tableau', 'power bi', 'excel', 'vba', 'html', 'css', 'bootstrap', 'jquery',
        'rest api', 'graphql', 'microservices', 'linux', 'unix', 'bash', 'powershell'
    ]
    
    text_lower = text.lower()
    skills = []
    for keyword in skill_keywords:
        if keyword in text_lower:
            skills.append(keyword)
    
    return skills

def extract_experience_years(text: str) -> float:
    """Extract years of experience from resume text"""
    # Patterns to match experience duration
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'experience[:\s]*(\d+)\+?\s*years?',
        r'(\d+)\+?\s*years?\s*in\s*',
        r'(\d+)\+?\s*years?\s*of\s*',
    ]
    
    max_years = 0
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                years = float(match)
                max_years = max(max_years, years)
            except ValueError:
                continue
    
    # Look for date ranges
    date_patterns = [
        r'(\d{4})\s*[-–]\s*(\d{4})',
        r'(\d{4})\s*[-–]\s*present',
        r'(\d{4})\s*[-–]\s*now',
    ]
    
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                if len(match) == 2:
                    start_year, end_year = match
                    if end_year.lower() in ['present', 'now', 'current']:
                        end_year = '2024'  # Current year
                    years = float(end_year) - float(start_year)
                    max_years = max(max_years, years)
            except ValueError:
                continue
    
    return min(max_years, 50)  # Cap at 50 years

def extract_projects(text: str) -> int:
    """Count number of projects mentioned in resume"""
    project_indicators = [
        'project', 'projects', 'portfolio', 'github', 'gitlab', 'repository',
        'developed', 'built', 'created', 'implemented', 'designed'
    ]
    
    text_lower = text.lower()
    project_count = 0
    
    # Count explicit project mentions
    for indicator in project_indicators:
        count = text_lower.count(indicator)
        project_count += count
    
    # Look for numbered projects
    numbered_projects = re.findall(r'project\s*#?\d+', text_lower)
    project_count += len(numbered_projects)
    
    # Look for bullet points that might be projects
    bullet_points = re.findall(r'[•\-\*]\s*.*(?:project|developed|built|created)', text_lower)
    project_count += len(bullet_points)
    
    return min(project_count, 20)  # Cap at 20 projects

def extract_education_level(text: str) -> float:
    """Extract education level and convert to numeric score"""
    education_scores = {
        'phd': 5.0,
        'doctorate': 5.0,
        'ph.d': 5.0,
        'master': 4.0,
        'mba': 4.0,
        'ms': 4.0,
        'ma': 4.0,
        'bachelor': 3.0,
        'bachelor\'s': 3.0,
        'bs': 3.0,
        'ba': 3.0,
        'btech': 3.0,
        'b.e': 3.0,
        'b.tech': 3.0,
        'associate': 2.0,
        'diploma': 2.0,
        'certificate': 1.0,
        'certification': 1.0,
        'high school': 1.0,
        'secondary': 1.0
    }
    
    text_lower = text.lower()
    max_score = 0
    
    for degree, score in education_scores.items():
        if degree in text_lower:
            max_score = max(max_score, score)
    
    return max_score

def calculate_skill_match(resume_skills: List[str], job_skills: List[str]) -> float:
    """Calculate skill match score between resume and job description"""
    if not resume_skills or not job_skills:
        return 0.0
    
    # Convert to lowercase for comparison
    resume_skills_lower = [skill.lower() for skill in resume_skills]
    job_skills_lower = [skill.lower() for skill in job_skills]
    
    # Calculate intersection
    matched_skills = set(resume_skills_lower) & set(job_skills_lower)
    
    # Calculate match ratio
    match_ratio = len(matched_skills) / len(job_skills_lower) if job_skills_lower else 0
    
    return min(match_ratio, 1.0)

def calculate_jd_alignment(resume_text: str, job_description: str) -> float:
    """Calculate job description alignment using rapidfuzz"""
    if not resume_text or not job_description:
        return 0.0
    
    # Calculate various similarity metrics
    ratio = fuzz.ratio(resume_text, job_description) / 100.0
    partial_ratio = fuzz.partial_ratio(resume_text, job_description) / 100.0
    token_sort_ratio = fuzz.token_sort_ratio(resume_text, job_description) / 100.0
    token_set_ratio = fuzz.token_set_ratio(resume_text, job_description) / 100.0
    
    # Use the maximum of all ratios
    max_ratio = max(ratio, partial_ratio, token_sort_ratio, token_set_ratio)
    
    return min(max_ratio, 1.0)

def extract_features(resume_text: str, job_description: str = "") -> Dict[str, float]:
    """Extract all features from resume text and job description"""
    features = {}
    
    # Extract skills
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description) if job_description else []
    
    # Calculate features
    features['skill_match'] = calculate_skill_match(resume_skills, job_skills)
    features['jd_alignment'] = calculate_jd_alignment(resume_text, job_description)
    features['exp_years'] = extract_experience_years(resume_text)
    features['projects'] = float(extract_projects(resume_text))
    features['education'] = extract_education_level(resume_text)
    
    return features

def normalize_features(features: Dict[str, float]) -> Dict[str, float]:
    """Normalize features to 0-1 range"""
    normalized = {}
    
    # Normalize experience years (assuming 0-20 years range)
    normalized['exp_years'] = min(features['exp_years'] / 20.0, 1.0)
    
    # Normalize projects (assuming 0-10 projects range)
    normalized['projects'] = min(features['projects'] / 10.0, 1.0)
    
    # Normalize education (assuming 0-5 range)
    normalized['education'] = features['education'] / 5.0
    
    # These are already normalized
    normalized['skill_match'] = features['skill_match']
    normalized['jd_alignment'] = features['jd_alignment']
    
    return normalized
