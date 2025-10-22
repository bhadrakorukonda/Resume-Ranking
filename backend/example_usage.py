#!/usr/bin/env python3
"""
Example usage of Resume Ranker API
"""

import requests
import json
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_weights():
    """Test weights endpoints"""
    print("Testing weights endpoints...")
    
    # Get current weights
    response = requests.get(f"{BASE_URL}/weights")
    print(f"GET /weights - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()
    
    # Create new weights
    new_weights = {
        "name": "Custom Weights",
        "skill_match": 0.4,
        "jd_alignment": 0.3,
        "exp_years": 0.15,
        "projects": 0.1,
        "education": 0.05
    }
    
    response = requests.post(
        f"{BASE_URL}/weights",
        json=new_weights,
        headers={"Content-Type": "application/json"}
    )
    print(f"POST /weights - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_upload():
    """Test resume upload"""
    print("Testing resume upload...")
    
    # Create a sample PDF file for testing
    sample_pdf_path = "sample_resume.pdf"
    if not os.path.exists(sample_pdf_path):
        print(f"Creating sample PDF: {sample_pdf_path}")
        # Create a minimal PDF file
        with open(sample_pdf_path, 'wb') as f:
            f.write(b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(John Doe - Software Engineer) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF\n')
    
    # Upload resume
    with open(sample_pdf_path, 'rb') as f:
        files = {'resume': (sample_pdf_path, f, 'application/pdf')}
        data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1-555-0123',
            'job_description': 'Software Engineer with Python and React experience'
        }
        
        response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
    
    print(f"POST /upload - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_ranking():
    """Test candidate ranking"""
    print("Testing candidate ranking...")
    
    # Rank candidates with default weights
    response = requests.post(
        f"{BASE_URL}/rank",
        json={},
        headers={"Content-Type": "application/json"}
    )
    print(f"POST /rank - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_candidates():
    """Test candidate endpoints"""
    print("Testing candidate endpoints...")
    
    # Get all candidates
    response = requests.get(f"{BASE_URL}/candidates")
    print(f"GET /candidates - Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def main():
    """Main function"""
    print("Resume Ranker API - Example Usage")
    print("=" * 50)
    
    try:
        test_health()
        test_weights()
        test_upload()
        test_ranking()
        test_candidates()
        
        print("All tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:5000")
        print("Run: python app.py")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
