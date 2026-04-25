# scraper.py
import pandas as pd
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from utils.scoring_logic import calculate_integrity_score

# Load API keys from .env file (for future live integration)
load_dotenv()

def get_carbon_data(simulate=True):
    """
    Fetches carbon project data.
    Set simulate=True to use high-fidelity mock data.
    """
    if simulate:
        raw_data = [
            {'name': 'Icelandic Rock Injection', 'type': 'Mineralization', 'vintage': 2025, 'registry': 'Puro.earth'},
            {'name': 'Sky-High Direct Air', 'type': 'Direct Air Capture', 'vintage': 2024, 'registry': 'Puro.earth'},
            {'name': 'Amazon Basin Protection', 'type': 'Forestry', 'vintage': 2017, 'registry': 'Verra'},
            {'name': 'Sundarbans Mangrove Restoration', 'type': 'Mangrove', 'vintage': 2022, 'registry': 'Verra'},
            {'name': 'Sub-Saharan Clean Stoves', 'type': 'Cookstove', 'vintage': 2021, 'registry': 'Gold Standard'},
            {'name': 'Great Plains Wind Expansion', 'type': 'Wind', 'vintage': 2016, 'registry': 'Verra'}
        ]
        return pd.DataFrame(raw_data)
    return pd.DataFrame()

def calculate_portfolio_stats(df):
    """ Generates corporate-level insights for ESG reporting."""
    stats = {
        'avg_integrity': df['integrity_rating'].mean(),
        'high_quality_count': len(df[df['integrity_rating'] >= 7.0]),
        'risk_count': len(df[df['integrity_rating'] < 4.0])
    }
    return stats

def generate_visualizations(df):
    """Creates a horizontal benchmarking chart of project integrity."""
    print("📊 Generating Integrity Benchmarking Chart...")
    
    # Sort by rating so the highest rated projects are at the top of the chart
    df_sorted = df.sort_values('integrity_rating', ascending=True)
    
    # Color logic: Green (High), Yellow (Medium), Red (Risk)
    colors = []
    for score in df_sorted['integrity_rating']:
        if score >= 7.0: colors.append('#2ecc71')
        elif score >= 5.0: colors.append('#f1c40f')
        else: colors.append('#e74c3c')

    plt.figure(figsize=(10, 6))
    bars = plt.barh(df_sorted['name'], df_sorted['integrity_rating'], color=colors)
    
    # Chart Styling
    plt.xlabel('Integrity Rating (Scale 1-10)')
    plt.title('ClearOffset: Carbon Project Integrity Benchmarking')
    plt.xlim(0, 10)
    plt.axvline(x=7.0, color='gray', linestyle='--', alpha=0.5, label='High-Integrity Threshold')
    
    # Add text labels to the end of each bar
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height()/2, f'{width:.1f}', va='center', fontweight='bold')

    plt.tight_layout()
    
    # Save the chart to the data folder
    os.makedirs('data', exist_ok=True)
    plt.savefig('data/integrity_benchmark.png')
    plt.close() # Close plot to free up memory

def main():
    print("🚀 Initializing ClearOffset: Carbon Credit Integrity Scraper...")
    
    # 1. Ingest
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
    
    # 5. Visualize
    generate_visualizations(df)
    
    # 6. Save results
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/integrity_rankings.csv', index=False)
    print(f"\n✅ Analysis Complete. Results and Chart saved to /data folder.")

if __name__ == "__main__":
    main()
