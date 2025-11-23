from nlp import extract_text_from_pdf
import os

# Test text extraction on uploaded PDFs
pdf_files = [
    'uploads/20251124_004939_Bhadra_Korukonda.pdf',
    'uploads/20251124_004940_Bhadras_Resume-hackerresume.pdf',
    'uploads/20251124_005025_Bhadra_Korukonda_EA.pdf'
]

for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        print(f'\n=== Testing {pdf_file} ===')
        text = extract_text_from_pdf(pdf_file)
        print(f'Extracted text length: {len(text)}')
        print(f'First 300 characters: {repr(text[:300])}')
        print(f'Contains "python": {"python" in text.lower()}')
        print(f'Contains "experience": {"experience" in text.lower()}')
        print(f'Contains "skills": {"skills" in text.lower()}')
    else:
        print(f'File {pdf_file} not found')