import pandas as pd
import requests
import os
from dotenv import load_dotenv
from utils.scoring_logic import calculate_integrity_score

# Load API keys from .env file
load_dotenv()
CARBONMARK_API_URL = "https://api.carbonmark.com/projects" # Example endpoint
# Uses python-dotenv to keep your API keys safe

def get_carbon_data():
    """
    Simulates fetching data from an API. 
    In production, you'd use: requests.get(URL, headers={'Authorization': f'Bearer {API_KEY}'})
    """
    # Mock data for demonstration
    raw_data = [
        {'name': 'Amazon Reforest', 'type': 'Forestry', 'vintage': 2018, 'registry': 'Verra'},
        {'name': 'Iceland DAC', 'type': 'Direct Air Capture', 'vintage': 2024, 'registry': 'Puro.earth'},
        {'name': 'Kenya Cookstoves', 'type': 'Cookstove', 'vintage': 2021, 'registry': 'Gold Standard'},
        {'name': 'Oman Mineralization', 'type': 'Mineralization', 'vintage': 2025, 'registry': 'Verra'},
        {'name': 'SeaTrees Mangrove', 'type': 'Mangrove', 'vintage': 2022, 'registry': 'Verra'}
    ]
    return pd.DataFrame(raw_data)

def main():
    print("🚀 Initializing Carbon Credit Integrity Scraper...")
    
    # 1. Ingest
    df = get_carbon_data()
    
    # 2. Score
    print("⚖️ Applying GHG Protocol Scoring Logic...")
    df['integrity_score'] = df.apply(calculate_integrity_score, axis=1)
    
    # 3. Rank
    df = df.sort_values(by='integrity_score', ascending=False)
    
    # 4. Output
    print("\n--- Top 5 High-Integrity Projects for Corporate Buyers ---")
    print(df.head(5))
    
    # Save results
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/integrity_rankings.csv', index=False)
    print("\n✅ Results saved to data/integrity_rankings.csv")

if __name__ == "__main__":
    main()
