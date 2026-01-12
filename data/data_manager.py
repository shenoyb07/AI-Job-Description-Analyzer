import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'job_descriptions.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(analysis_result):
    data = load_data()
    analysis_result['timestamp'] = datetime.now().isoformat()
    analysis_result['id'] = len(data) + 1
    data.append(analysis_result)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    return analysis_result
