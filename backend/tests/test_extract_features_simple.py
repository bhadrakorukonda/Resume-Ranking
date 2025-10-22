"""
Pytest tests for extract_features() function with synthetic inputs
"""

import pytest
from nlp import extract_features, normalize_features


class TestExtractFeaturesSynthetic:
    """Test extract_features function with synthetic inputs"""
    
    def test_extract_features_basic_resume(self):
        """Test extract_features with basic resume text"""
        resume_text = """
        John Doe
        Software Engineer
        
        Experience: 3 years of software development
        Skills: Python, JavaScript, React, SQL
        Education: Bachelor in Computer Science
        Projects: E-commerce website, Mobile app, Data analysis tool
        
        Worked at TechCorp from 2020-2023
        """
        
        job_description = "Python developer with React experience and SQL knowledge"
        
        features = extract_features(resume_text, job_description)
        
        # Check all required features are present
        required_features = ['skill_match', 'jd_alignment', 'exp_years', 'projects', 'education']
        for feature in required_features:
            assert feature in features
            assert isinstance(features[feature], (int, float))
        
        # Check reasonable ranges
        assert 0.0 <= features['skill_match'] <= 1.0
        assert 0.0 <= features['jd_alignment'] <= 1.0
        assert features['exp_years'] >= 0.0
        assert features['projects'] >= 0.0
        assert 0.0 <= features['education'] <= 5.0
    
    def test_extract_features_no_job_description(self):
        """Test extract_features without job description"""
        resume_text = """
        Software Developer
        2 years experience
        Skills: Python, JavaScript
        Education: Bachelor degree
        Projects: Web application
        """
        
        features = extract_features(resume_text, "")
        
        # All features should be present
        required_features = ['skill_match', 'jd_alignment', 'exp_years', 'projects', 'education']
        for feature in required_features:
            assert feature in features
        
        # JD alignment should be 0 without job description
        assert features['jd_alignment'] == 0.0
        
        # Skill match should be 0 without job description
        assert features['skill_match'] == 0.0
    
    def test_extract_features_empty_resume(self):
        """Test extract_features with empty resume text"""
        resume_text = ""
        job_description = "Python developer"
        
        features = extract_features(resume_text, job_description)
        
        # Should return zero features
        expected_features = {
            'skill_match': 0.0,
            'jd_alignment': 0.0,
            'exp_years': 0.0,
            'projects': 0.0,
            'education': 0.0
        }
        
        for feature, expected_value in expected_features.items():
            assert features[feature] == expected_value
    
    def test_extract_features_minimal_resume(self):
        """Test extract_features with minimal resume text"""
        resume_text = "John Doe"
        job_description = "Software Engineer"
        
        features = extract_features(resume_text, job_description)
        
        # Should handle minimal input gracefully
        required_features = ['skill_match', 'jd_alignment', 'exp_years', 'projects', 'education']
        for feature in required_features:
            assert feature in features
            assert isinstance(features[feature], (int, float))


class TestNormalizeFeaturesSynthetic:
    """Test normalize_features function with synthetic inputs"""
    
    def test_normalize_features_typical(self):
        """Test normalize_features with typical feature values"""
        features = {
            'skill_match': 0.8,
            'jd_alignment': 0.7,
            'exp_years': 5.0,  # Should be normalized
            'projects': 8.0,   # Should be normalized
            'education': 4.0   # Should be normalized
        }
        
        normalized = normalize_features(features)
        
        # Check all features are present
        required_features = ['skill_match', 'jd_alignment', 'exp_years', 'projects', 'education']
        for feature in required_features:
            assert feature in normalized
        
        # Check normalized values are in 0-1 range
        for feature, value in normalized.items():
            assert 0.0 <= value <= 1.0
        
        # Check that already normalized features remain the same
        assert normalized['skill_match'] == 0.8
        assert normalized['jd_alignment'] == 0.7
    
    def test_normalize_features_zero_values(self):
        """Test normalize_features with zero values"""
        features = {
            'skill_match': 0.0,
            'jd_alignment': 0.0,
            'exp_years': 0.0,
            'projects': 0.0,
            'education': 0.0
        }
        
        normalized = normalize_features(features)
        
        # All values should be 0.0
        for feature, value in normalized.items():
            assert value == 0.0
    
    def test_normalize_features_extreme_values(self):
        """Test normalize_features with extreme values"""
        features = {
            'skill_match': 1.0,
            'jd_alignment': 0.0,
            'exp_years': 50.0,  # Very high experience
            'projects': 100.0,  # Very many projects
            'education': 5.0    # PhD level
        }
        
        normalized = normalize_features(features)
        
        # All values should be in 0-1 range
        for feature, value in normalized.items():
            assert 0.0 <= value <= 1.0
        
        # Extreme values should be capped at 1.0
        assert normalized['exp_years'] == 1.0
        assert normalized['projects'] == 1.0
        assert normalized['education'] == 1.0


if __name__ == '__main__':
    pytest.main([__file__])
