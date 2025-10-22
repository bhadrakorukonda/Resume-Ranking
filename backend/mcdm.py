import numpy as np
from typing import List, Dict, Tuple
from config import FEATURE_ORDER, BENEFIT_MASK

def topsis(decision_matrix: np.ndarray, weights: np.ndarray, benefit_mask: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
    
    Args:
        decision_matrix: 2D array where rows are alternatives and columns are criteria
        weights: 1D array of weights for each criterion
        benefit_mask: 1D boolean array where True indicates benefit criteria (higher is better)
    
    Returns:
        Tuple of (scores, rankings) where scores are TOPSIS scores and rankings are 1-based rankings
    """
    # Step 1: Normalize the decision matrix
    # Calculate the sum of squares for each column
    sum_squares = np.sum(decision_matrix ** 2, axis=0)
    # Avoid division by zero
    sum_squares = np.where(sum_squares == 0, 1, sum_squares)
    normalized_matrix = decision_matrix / np.sqrt(sum_squares)
    
    # Step 2: Apply weights
    weighted_matrix = normalized_matrix * weights
    
    # Step 3: Determine ideal and negative ideal solutions
    ideal_solution = np.zeros(weighted_matrix.shape[1])
    negative_ideal_solution = np.zeros(weighted_matrix.shape[1])
    
    for j in range(weighted_matrix.shape[1]):
        if benefit_mask[j]:
            # For benefit criteria, ideal is maximum, negative ideal is minimum
            ideal_solution[j] = np.max(weighted_matrix[:, j])
            negative_ideal_solution[j] = np.min(weighted_matrix[:, j])
        else:
            # For cost criteria, ideal is minimum, negative ideal is maximum
            ideal_solution[j] = np.min(weighted_matrix[:, j])
            negative_ideal_solution[j] = np.max(weighted_matrix[:, j])
    
    # Step 4: Calculate separation measures
    # Distance to ideal solution
    ideal_distances = np.sqrt(np.sum((weighted_matrix - ideal_solution) ** 2, axis=1))
    
    # Distance to negative ideal solution
    negative_ideal_distances = np.sqrt(np.sum((weighted_matrix - negative_ideal_solution) ** 2, axis=1))
    
    # Step 5: Calculate relative closeness to ideal solution
    # Avoid division by zero
    total_distances = ideal_distances + negative_ideal_distances
    total_distances = np.where(total_distances == 0, 1, total_distances)
    
    scores = negative_ideal_distances / total_distances
    
    # Step 6: Rank alternatives (higher score = better rank)
    rankings = np.argsort(scores)[::-1] + 1  # +1 for 1-based ranking
    
    return scores, rankings

def rank_candidates(candidates_data: List[Dict], weights: Dict[str, float]) -> List[Dict]:
    """
    Rank candidates using TOPSIS method
    
    Args:
        candidates_data: List of candidate dictionaries with feature scores
        weights: Dictionary of weights for each feature
    
    Returns:
        List of candidate dictionaries with added ranking information
    """
    if not candidates_data:
        return []
    
    # Extract feature vectors in the correct order
    decision_matrix = []
    for candidate in candidates_data:
        feature_vector = [
            candidate.get('skill_match', 0.0),
            candidate.get('jd_alignment', 0.0),
            candidate.get('exp_years', 0.0),
            candidate.get('projects', 0.0),
            candidate.get('education', 0.0)
        ]
        decision_matrix.append(feature_vector)
    
    decision_matrix = np.array(decision_matrix)
    
    # Create weight vector in the correct order
    weight_vector = np.array([
        weights.get('skill_match', 0.0),
        weights.get('jd_alignment', 0.0),
        weights.get('exp_years', 0.0),
        weights.get('projects', 0.0),
        weights.get('education', 0.0)
    ])
    
    # Create benefit mask
    benefit_mask = np.array([
        BENEFIT_MASK['skill_match'],
        BENEFIT_MASK['jd_alignment'],
        BENEFIT_MASK['exp_years'],
        BENEFIT_MASK['projects'],
        BENEFIT_MASK['education']
    ])
    
    # Apply TOPSIS
    scores, rankings = topsis(decision_matrix, weight_vector, benefit_mask)
    
    # Add ranking information to candidates
    ranked_candidates = []
    for i, candidate in enumerate(candidates_data):
        candidate_copy = candidate.copy()
        candidate_copy['topsis_score'] = float(scores[i])
        candidate_copy['rank'] = int(rankings[i])
        ranked_candidates.append(candidate_copy)
    
    # Sort by rank
    ranked_candidates.sort(key=lambda x: x['rank'])
    
    return ranked_candidates

def calculate_weights_sum(weights: Dict[str, float]) -> float:
    """Calculate sum of weights to check if they sum to 1.0"""
    return sum(weights.values())

def normalize_weights(weights: Dict[str, float]) -> Dict[str, float]:
    """Normalize weights so they sum to 1.0"""
    total = calculate_weights_sum(weights)
    if total == 0:
        # If all weights are zero, return equal weights
        return {key: 1.0 / len(weights) for key in weights}
    
    return {key: value / total for key, value in weights.items()}

def validate_weights(weights: Dict[str, float]) -> Tuple[bool, str]:
    """
    Validate weights dictionary
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(weights, dict):
        return False, "Weights must be a dictionary"
    
    # Check if all required features are present
    required_features = set(FEATURE_ORDER)
    provided_features = set(weights.keys())
    
    if required_features != provided_features:
        missing = required_features - provided_features
        extra = provided_features - required_features
        error_msg = f"Missing features: {missing}. Extra features: {extra}"
        return False, error_msg
    
    # Check if all values are numeric and non-negative
    for feature, weight in weights.items():
        if not isinstance(weight, (int, float)):
            return False, f"Weight for {feature} must be numeric"
        if weight < 0:
            return False, f"Weight for {feature} must be non-negative"
    
    # Check if weights sum to approximately 1.0 (allow small floating point errors)
    total = calculate_weights_sum(weights)
    if abs(total - 1.0) > 1e-6:
        return False, f"Weights must sum to 1.0, got {total:.6f}"
    
    return True, ""

def get_feature_statistics(candidates_data: List[Dict]) -> Dict[str, Dict[str, float]]:
    """
    Calculate statistics for each feature across all candidates
    
    Returns:
        Dictionary with feature statistics (mean, std, min, max)
    """
    if not candidates_data:
        return {}
    
    statistics = {}
    
    for feature in FEATURE_ORDER:
        values = [candidate.get(feature, 0.0) for candidate in candidates_data]
        if values:
            statistics[feature] = {
                'mean': float(np.mean(values)),
                'std': float(np.std(values)),
                'min': float(np.min(values)),
                'max': float(np.max(values)),
                'count': len(values)
            }
        else:
            statistics[feature] = {
                'mean': 0.0,
                'std': 0.0,
                'min': 0.0,
                'max': 0.0,
                'count': 0
            }
    
    return statistics
