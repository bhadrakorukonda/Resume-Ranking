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
    """Extract text from PDF file using pdfplumber (better than PyPDF2) with fallback to PyPDF2"""
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
            
            # Clean up the extracted text
            if text:
                # Replace multiple spaces with single space
                text = ' '.join(text.split())
                return text.strip()
    except ImportError:
        logger.warning("pdfplumber not available, falling back to PyPDF2")
    except Exception as e:
        logger.warning(f"pdfplumber extraction failed: {e}, falling back to PyPDF2")
    
    # Fallback to PyPDF2
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
            
            # Clean up common PDF extraction issues
            if text:
                text = text.replace('\n', ' ')  # Replace newlines with spaces
                text = ' '.join(text.split())  # Remove extra whitespace
                
                # Fix common PDF extraction artifacts where spaces appear in the middle of words
                # Pattern to fix single characters separated by spaces (like "F ull-Stac k" -> "Full-Stack")
                text = re.sub(r'(\w)\s+(\w)', lambda m: m.group(1) + m.group(2) if len(m.group(1)) == 1 or len(m.group(2)) == 1 else m.group(1) + ' ' + m.group(2), text)
                
                return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF {pdf_path}: {str(e)}")
    
    return ""

def extract_skills(text: str) -> List[str]:
    """Extract skills from resume text using improved keyword matching"""
    if not text:
        return []
    
    # Common technical skills keywords (expanded and cleaned)
    skill_keywords = [
        'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'django', 'flask',
        'sql', 'postgresql', 'mysql', 'mongodb', 'redis', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
        'git', 'github', 'gitlab', 'jenkins', 'ci/cd', 'agile', 'scrum', 'kanban',
        'machine learning', 'deep learning', 'neural networks', 'nlp', 'computer vision', 'tensorflow', 'pytorch', 'scikit-learn',
        'data science', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'tableau', 'power bi',
        'html', 'css', 'bootstrap', 'tailwind', 'jquery', 'sass', 'less',
        'rest api', 'graphql', 'microservices', 'linux', 'unix', 'bash', 'powershell',
        'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'kotlin', 'swift',
        'spring', 'hibernate', '.net', 'asp.net', 'laravel', 'rails',
        'android', 'ios', 'react native', 'flutter', 'ionic',
        'opencv', 'keras', 'fastai', 'hugging face', 'spacy', 'nltk'
    ]
    
    text_lower = text.lower()
    skills = set()
    
    # Extract from keywords with better matching
    for keyword in skill_keywords:
        if keyword in text_lower:
            skills.add(keyword)
    
    # Filter out skills that are too short or contain spaces in wrong places
    filtered_skills = []
    for skill in skills:
        # Remove skills that are too short or contain weird characters
        if len(skill) >= 3 and not any(char in skill for char in ['\n', '\t', '\r']):
            # Remove skills that look like fragments (contain spaces in middle in weird ways)
            if ' ' not in skill or len(skill.split()) <= 4:  # Allow multi-word skills up to 4 words
                filtered_skills.append(skill)
    
    return sorted(list(set(filtered_skills)))

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

def extract_name(text: str) -> str:
    """Extract candidate name from resume text"""
    if not text:
        return "Unknown"
    
    # First, try to find name at the very beginning of the text
    first_line = text.split('\n')[0].strip()
    words = first_line.split()
    
    # Look for 2-3 words that could be a name (capitalized)
    for i in range(len(words)):
        for j in range(i+1, min(i+4, len(words)+1)):
            candidate_name = ' '.join(words[i:j])
            # Check if it looks like a name (2-3 words, starts with capital letters)
            name_words = candidate_name.split()
            if 2 <= len(name_words) <= 3:
                if all(word[0].isupper() for word in name_words if word):
                    # Make sure it's not a common phrase
                    if not any(phrase in candidate_name.lower() for phrase in ['engineer', 'developer', 'scientist', 'analyst', 'manager']):
                        return candidate_name.title()
    
    # Fallback: look for name patterns in the text
    lines = text.split('\n')[:10]  # Check first 10 lines
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip lines that are clearly not names
        skip_indicators = ['email', 'phone', 'address', 'linkedin', 'github', 'education', 'experience', 'skills', 'projects']
        if any(indicator in line.lower() for indicator in skip_indicators):
            continue
            
        # Look for name-like patterns (2-4 words, title case or all caps)
        words = line.split()
        if 2 <= len(words) <= 4:
            # Check if it looks like a name (starts with capital letters)
            if all(word[0].isupper() for word in words if word):
                # Filter out common resume headers
                if not any(header in line.lower() for header in ['resume', 'cv', 'curriculum vitae', 'professional summary']):
                    return line.title()
    
    # Fallback: try to find name near email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        # Look for name before email in the same line or nearby
        email_start = email_match.start()
        text_before_email = text[:email_start]
        lines_before = text_before_email.split('\n')[-3:]  # Last 3 lines before email
        
        for line in reversed(lines_before):
            line = line.strip()
            words = line.split()
            if 2 <= len(words) <= 4 and all(word[0].isupper() for word in words if word):
                return line.title()
    
    return "Unknown"

def extract_email(text: str) -> str:
    """Extract email address from resume text"""
    if not text:
        return ""
    
    # Email regex pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(email_pattern, text)
    
    if matches:
        return matches[0]  # Return first email found
    
    return ""

def extract_phone(text: str) -> str:
    """Extract phone number from resume text"""
    if not text:
        return ""
    
    # Phone number patterns
    phone_patterns = [
        r'\+\d{1,3}[\s\-\.]?\d{3,4}[\s\-\.]?\d{3,4}[\s\-\.]?\d{3,4}',  # +91 8639448680
        r'\d{3}[\s\-\.]\d{3}[\s\-\.]\d{4}',  # 123-456-7890
        r'\d{10,12}',  # 8639448680
    ]
    
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # Clean up the phone number
            clean_phone = re.sub(r'[^\d+\-\.\s]', '', match).strip()
            if len(clean_phone.replace(' ', '').replace('-', '').replace('.', '')) >= 10:
                return clean_phone
    
    return ""

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
