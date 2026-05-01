import requests
from pathlib import Path

def fetch_data(study_dir_name: str):
    base_dir = Path(study_dir_name)
    raw_dir = base_dir / "raw_data"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    url = "https://clinicaltrials.gov/api/v2/studies?query.cond=hypertension&pageSize=100&format=csv"
    print(f"Fetching data from {url}...")
    
    response = requests.get(url)
    response.raise_for_status()
    
    out_file = raw_dir / "trials.csv"
    with open(out_file, "wb") as f:
        f.write(response.content)
        
    print(f"Data saved to {out_file}")
