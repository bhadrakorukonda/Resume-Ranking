import requests
import json

# Test ranking with default weights
default_weights = {
    'skill_match': 0.25,
    'jd_alignment': 0.30,
    'exp_years': 0.20,
    'projects': 0.15,
    'education': 0.10
}

response = requests.post('http://localhost:5000/rank', json={'weights': default_weights})
print('=== Ranking with Default Weights ===')
result = response.json()
print(f'Status: {response.status_code}')
if response.status_code == 200:
    print(f'Message: {result.get("message")}')
    print(f'Total Candidates: {result.get("total_candidates")}')
    print('Weights Used:', json.dumps(result.get('weights_used'), indent=2))

    print()
    print('=== Ranked Candidates ===')
    for candidate in result.get('ranked_candidates', []):
        print(f'Rank {candidate["rank"]}: {candidate["name"]} (Score: {candidate["topsis_score"]:.3f})')
else:
    print(f'Error: {result.get("error")}')