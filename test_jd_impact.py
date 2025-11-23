import sys
sys.path.append('backend')
from nlp import extract_text_from_pdf, extract_features, normalize_features
import os

# Test with different job descriptions
pdf_file = 'backend/uploads/20251124_004939_Bhadra_Korukonda.pdf'
text = extract_text_from_pdf(pdf_file)

job_descriptions = [
    'Python Developer with Machine Learning experience',
    'AI Engineer with NLP and Full Stack skills',
    'Software Engineer',
    ''
]

for jd in job_descriptions:
    print(f'\n=== Job Description: "{jd}" ===')
    features = extract_features(text, jd)
    normalized = normalize_features(features)
    print('Features:', {k: round(v, 3) for k, v in normalized.items()})