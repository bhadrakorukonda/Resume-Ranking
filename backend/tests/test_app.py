import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock

from app import app, init_db
from models import Candidate, Weights
from db import get_db

class TestResumeRankerAPI(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and database"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['DATABASE_URL'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        
        # Initialize test database
        with self.app.app_context():
            init_db()
    
    def tearDown(self):
        """Clean up after tests"""
        pass
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
    
    def test_get_weights(self):
        """Test getting weights"""
        response = self.client.get('/weights')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('weights', data)
        self.assertIn('default_weights', data)
    
    def test_create_weights(self):
        """Test creating new weights"""
        weights_data = {
            'name': 'Test Weights',
            'skill_match': 0.3,
            'jd_alignment': 0.3,
            'exp_years': 0.2,
            'projects': 0.1,
            'education': 0.1
        }
        
        response = self.client.post('/weights', 
                                  data=json.dumps(weights_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('weights', data)
    
    def test_create_weights_invalid(self):
        """Test creating weights with invalid data"""
        invalid_weights = {
            'name': 'Invalid Weights',
            'skill_match': 0.5,
            'jd_alignment': 0.5,
            'exp_years': 0.5,
            'projects': 0.5,
            'education': 0.5
        }
        
        response = self.client.post('/weights',
                                  data=json.dumps(invalid_weights),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_rank_candidates_no_candidates(self):
        """Test ranking when no candidates exist"""
        response = self.client.post('/rank',
                                  data=json.dumps({}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    @patch('app.extract_text_from_pdf')
    @patch('app.extract_features')
    def test_upload_resume(self, mock_extract_features, mock_extract_text):
        """Test resume upload"""
        # Mock the extraction functions
        mock_extract_text.return_value = "Sample resume text"
        mock_extract_features.return_value = {
            'skill_match': 0.8,
            'jd_alignment': 0.7,
            'exp_years': 3.0,
            'projects': 5.0,
            'education': 4.0
        }
        
        # Create a mock PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n')
            tmp_file.flush()
            
            with open(tmp_file.name, 'rb') as f:
                response = self.client.post('/upload', data={
                    'resume': (f, 'test.pdf'),
                    'name': 'Test Candidate',
                    'email': 'test@example.com',
                    'job_description': 'Software Engineer position'
                })
        
        # Clean up
        os.unlink(tmp_file.name)
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('candidate_id', data)
        self.assertIn('features', data)
    
    def test_upload_resume_no_file(self):
        """Test upload without file"""
        response = self.client.post('/upload')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_upload_resume_invalid_file_type(self):
        """Test upload with invalid file type"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp_file:
            tmp_file.write(b'This is not a PDF')
            tmp_file.flush()
            
            with open(tmp_file.name, 'rb') as f:
                response = self.client.post('/upload', data={
                    'resume': (f, 'test.txt'),
                    'name': 'Test Candidate'
                })
        
        # Clean up
        os.unlink(tmp_file.name)
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()
