import spacy
import re
from typing import Dict, List

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined skill list
SKILL_SET = {"python", "java", "c++", "machine learning", "deep learning", "sql", "flask", "django"}

def extract_name(doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

def extract_email(text):
    email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}", text)
    return email[0] if email else None

def extract_phone(text):
    phone = re.findall(r"\+?\d[\d -]{8,12}\d", text)
    return phone[0] if phone else None

def extract_skills(text: str) -> List[str]:
    text = text.lower()
    return [skill for skill in SKILL_SET if skill in text]

def extract_experience(text: str) -> str:
    exp_match = re.findall(r'(\d+)\s+years?', text.lower())
    return exp_match[0] + " years" if exp_match else "Not mentioned"

def process_resume(text: str) -> Dict:
    doc = nlp(text)

    return {
        "name": extract_name(doc),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "experience": extract_experience(text),
    }
