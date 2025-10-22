from resume_parser import process_resume

# Read your sample resume text
with open("sample_resume.txt", "r", encoding="utf-8") as f:
    resume_text = f.read()

# Run the parser
parsed_data = process_resume(resume_text)

# Print results
print("\n--- Parsed Resume Data ---")
for key, value in parsed_data.items():
    print(f"{key}: {value}")
