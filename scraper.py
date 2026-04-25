# scraper.py
import pandas as pd
import os
from dotenv import load_dotenv
from utils.scoring_logic import calculate_integrity_score

# Load API keys from .env file (for future live integration)
load_dotenv()

def get_carbon_data(simulate=True):
    """
    Fetches carbon project data.
    Set simulate=True to use high-fidelity mock data (Reliable for Portfolios).
    Set simulate=False to connect to a live REST API.
    """
    if simulate:
        # High-fidelity mock data representing diverse VCM (Voluntary Carbon Market) sectors
        raw_data = [
            {'name': 'Icelandic Rock Injection', 'type': 'Mineralization', 'vintage': 2025, 'registry': 'Puro.earth'},
            {'name': 'Sky-High Direct Air', 'type': 'Direct Air Capture', 'vintage': 2024, 'registry': 'Puro.earth'},
            {'name': 'Amazon Basin Protection', 'type': 'Forestry', 'vintage': 2017, 'registry': 'Verra'},
            {'name': 'Sundarbans Mangrove Restoration', 'type': 'Mangrove', 'vintage': 2022, 'registry': 'Verra'},
            {'name': 'Sub-Saharan Clean Stoves', 'type': 'Cookstove', 'vintage': 2021, 'registry': 'Gold Standard'},
            {'name': 'Great Plains Wind Expansion', 'type': 'Wind', 'vintage': 2016, 'registry': 'Verra'}
        ]
        return pd.DataFrame(raw_data)
    else:
        # Placeholder for future live API integration (e.g., Carbonmark or Verra API)
        # url = "https://api.example-carbon-registry.com/v1/projects"
        # response = requests.get(url)
        # return pd.DataFrame(response.json())
        pass

def calculate_portfolio_stats(df):
    """Generates corporate-level insights for ESG reporting."""
    stats = {
        'avg_integrity': df['integrity_rating'].mean(),
        'high_quality_count': len(df[df['integrity_rating'] >= 7.0]),
        'risk_count': len(df[df['integrity_rating'] < 4.0])
    }
    return stats

def main():
    print("🚀 Initializing ClearOffset: Carbon Credit Integrity Scraper...")
    
    # 1. Ingest (Simulation Mode enabled for portfolio stability)
    df = get_carbon_data(simulate=True)
    
    # 2. Score
    print("⚖️ Executing Weighted Integrity Algorithm (Permanence 60% | Vintage 40%)...")
    df['integrity_rating'] = df.apply(calculate_integrity_score, axis=1)
    
    # 3. Analyze Portfolio
    stats = calculate_portfolio_stats(df)
    
    # 4. Rank & Output
    df = df.sort_values(by='integrity_rating', ascending=False)
    
    print("\n" + "="*50)
    print("📊 CORPORATE PORTFOLIO INSIGHTS")
    print(f"Portfolio Health Rating:  {stats['avg_integrity']:.1f}/10")
    print(f"High-Integrity Credits:   {stats['high_quality_count']}")
    print(f"High-Risk (Flagged):      {stats['risk_count']}")
    print("="*50)
    
    print("\n--- Top 5 Ranked Projects by Integrity ---")
    print(df[['name', 'type', 'vintage', 'integrity_rating']].head(5))
    
    # Save results to local 'data' directory
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/integrity_rankings.csv', index=False)
    print(f"\n✅ Analysis saved to data/integrity_rankings.csv")

if __name__ == "__main__":
    main()
