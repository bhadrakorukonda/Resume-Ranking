import numpy as np
from sklearn.preprocessing import MinMaxScaler

def topsis(data, weights):
    # Normalize the data
    scaler = MinMaxScaler()
    norm_data = scaler.fit_transform(data)

    # Apply weights
    weighted = norm_data * weights

    # Calculate ideal best and worst
    ideal_best = np.max(weighted, axis=0)
    ideal_worst = np.min(weighted, axis=0)

    # Calculate distances
    dist_best = np.linalg.norm(weighted - ideal_best, axis=1)
    dist_worst = np.linalg.norm(weighted - ideal_worst, axis=1)

    # Calculate TOPSIS score
    scores = dist_worst / (dist_best + dist_worst)
    return scores

# ---- Sample candidate matrix ----
# Each row is a candidate
# Format: [Skill Match %, Experience (years), Degree Level, Certifications]
candidates = np.array([
    [70, 2, 3, 1],
    [90, 5, 2, 0],
    [80, 3, 3, 2],
])

# Weight for each criterion (must sum to 1 or will be normalized)
weights = np.array([0.4, 0.3, 0.2, 0.1])

# Run TOPSIS
scores = topsis(candidates, weights)

# Display results
ranks = scores.argsort()[::-1]
print("\n--- Ranking ---")
for i in ranks:
    print(f"Candidate {i+1}: Score = {scores[i]:.3f}")
