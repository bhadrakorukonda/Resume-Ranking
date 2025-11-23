import requests

# Test ranking with default weights
default_weights = {
    'skill_match': 0.25,
    'jd_alignment': 0.30,
    'exp_years': 0.20,
    'projects': 0.15,
    'education': 0.10
}

response = requests.post('http://localhost:5000/rank', json={'weights': default_weights})
result = response.json()
print('=== Ranking Results ===')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    print(f'Message: {result.get("message")}')
    print(f'Total Candidates: {result.get("total_candidates")}')

    print('\n=== Ranked Candidates ===')
    for candidate in result.get('ranked_candidates', []):
        print(f'Rank {candidate["rank"]}: {candidate["name"]} (Score: {candidate["topsis_score"]:.3f})')
        print(f'  Features: Skill Match: {candidate["skill_match"]:.2f}, JD Alignment: {candidate["jd_alignment"]:.2f}')
else:
    print(f'Error: {result.get("error")}')