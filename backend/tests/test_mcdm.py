import unittest
import numpy as np

from mcdm import (
    topsis,
    rank_candidates,
    calculate_weights_sum,
    normalize_weights,
    validate_weights,
    get_feature_statistics
)

class TestMCDMFunctions(unittest.TestCase):
    
    def test_topsis_basic(self):
        """Test basic TOPSIS functionality"""
        # Simple test case with 2 alternatives and 2 criteria
        decision_matrix = np.array([
            [1.0, 2.0],
            [2.0, 1.0]
        ])
        weights = np.array([0.5, 0.5])
        benefit_mask = np.array([True, True])
        
        scores, rankings = topsis(decision_matrix, weights, benefit_mask)
        
        self.assertEqual(len(scores), 2)
        self.assertEqual(len(rankings), 2)
        self.assertTrue(np.all(scores >= 0))
        self.assertTrue(np.all(scores <= 1))
    
    def test_topsis_benefit_vs_cost(self):
        """Test TOPSIS with benefit and cost criteria"""
        decision_matrix = np.array([
            [1.0, 2.0],  # High benefit, high cost
            [2.0, 1.0]   # Low benefit, low cost
        ])
        weights = np.array([0.5, 0.5])
        benefit_mask = np.array([True, False])  # First is benefit, second is cost
        
        scores, rankings = topsis(decision_matrix, weights, benefit_mask)
        
        self.assertEqual(len(scores), 2)
        self.assertTrue(np.all(scores >= 0))
        self.assertTrue(np.all(scores <= 1))
    
    def test_rank_candidates(self):
        """Test candidate ranking"""
        candidates_data = [
            {
                'id': 1,
                'name': 'Candidate 1',
                'skill_match': 0.8,
                'jd_alignment': 0.7,
                'exp_years': 0.6,
                'projects': 0.5,
                'education': 0.4
            },
            {
                'id': 2,
                'name': 'Candidate 2',
                'skill_match': 0.6,
                'jd_alignment': 0.8,
                'exp_years': 0.7,
                'projects': 0.6,
                'education': 0.5
            }
        ]
        
        weights = {
            'skill_match': 0.3,
            'jd_alignment': 0.3,
            'exp_years': 0.2,
            'projects': 0.1,
            'education': 0.1
        }
        
        ranked = rank_candidates(candidates_data, weights)
        
        self.assertEqual(len(ranked), 2)
        self.assertIn('topsis_score', ranked[0])
        self.assertIn('rank', ranked[0])
        self.assertTrue(ranked[0]['rank'] <= ranked[1]['rank'])
    
    def test_rank_candidates_empty(self):
        """Test ranking with empty candidate list"""
        ranked = rank_candidates([], {})
        self.assertEqual(len(ranked), 0)
    
    def test_calculate_weights_sum(self):
        """Test weights sum calculation"""
        weights = {
            'skill_match': 0.3,
            'jd_alignment': 0.3,
            'exp_years': 0.2,
            'projects': 0.1,
            'education': 0.1
        }
        
        total = calculate_weights_sum(weights)
        self.assertAlmostEqual(total, 1.0, places=6)
    
    def test_normalize_weights(self):
        """Test weight normalization"""
        weights = {
            'skill_match': 3.0,
            'jd_alignment': 3.0,
            'exp_years': 2.0,
            'projects': 1.0,
            'education': 1.0
        }
        
        normalized = normalize_weights(weights)
        total = calculate_weights_sum(normalized)
        self.assertAlmostEqual(total, 1.0, places=6)
    
    def test_normalize_weights_zero_sum(self):
        """Test normalization with zero sum weights"""
        weights = {
            'skill_match': 0.0,
            'jd_alignment': 0.0,
            'exp_years': 0.0,
            'projects': 0.0,
            'education': 0.0
        }
        
        normalized = normalize_weights(weights)
        total = calculate_weights_sum(normalized)
        self.assertAlmostEqual(total, 1.0, places=6)
        
        # All weights should be equal
        for weight in normalized.values():
            self.assertAlmostEqual(weight, 0.2, places=6)
    
    def test_validate_weights_valid(self):
        """Test validation of valid weights"""
        weights = {
            'skill_match': 0.3,
            'jd_alignment': 0.3,
            'exp_years': 0.2,
            'projects': 0.1,
            'education': 0.1
        }
        
        is_valid, error_msg = validate_weights(weights)
        self.assertTrue(is_valid)
        self.assertEqual(error_msg, "")
    
    def test_validate_weights_invalid_sum(self):
        """Test validation of weights with invalid sum"""
        weights = {
            'skill_match': 0.5,
            'jd_alignment': 0.5,
            'exp_years': 0.5,
            'projects': 0.5,
            'education': 0.5
        }
        
        is_valid, error_msg = validate_weights(weights)
        self.assertFalse(is_valid)
        self.assertIn('sum to 1.0', error_msg)
    
    def test_validate_weights_missing_features(self):
        """Test validation with missing features"""
        weights = {
            'skill_match': 0.5,
            'jd_alignment': 0.5
        }
        
        is_valid, error_msg = validate_weights(weights)
        self.assertFalse(is_valid)
        self.assertIn('Missing features', error_msg)
    
    def test_validate_weights_negative_values(self):
        """Test validation with negative values"""
        weights = {
            'skill_match': -0.3,
            'jd_alignment': 0.3,
            'exp_years': 0.2,
            'projects': 0.1,
            'education': 0.1
        }
        
        is_valid, error_msg = validate_weights(weights)
        self.assertFalse(is_valid)
        self.assertIn('non-negative', error_msg)
    
    def test_get_feature_statistics(self):
        """Test feature statistics calculation"""
        candidates_data = [
            {
                'skill_match': 0.8,
                'jd_alignment': 0.7,
                'exp_years': 0.6,
                'projects': 0.5,
                'education': 0.4
            },
            {
                'skill_match': 0.6,
                'jd_alignment': 0.8,
                'exp_years': 0.7,
                'projects': 0.6,
                'education': 0.5
            }
        ]
        
        stats = get_feature_statistics(candidates_data)
        
        self.assertIn('skill_match', stats)
        self.assertIn('jd_alignment', stats)
        self.assertIn('exp_years', stats)
        self.assertIn('projects', stats)
        self.assertIn('education', stats)
        
        for feature, stat_dict in stats.items():
            self.assertIn('mean', stat_dict)
            self.assertIn('std', stat_dict)
            self.assertIn('min', stat_dict)
            self.assertIn('max', stat_dict)
            self.assertIn('count', stat_dict)
            self.assertEqual(stat_dict['count'], 2)
    
    def test_get_feature_statistics_empty(self):
        """Test statistics with empty data"""
        stats = get_feature_statistics([])
        self.assertEqual(len(stats), 0)

if __name__ == '__main__':
    unittest.main()
