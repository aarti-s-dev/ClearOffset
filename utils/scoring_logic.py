# utils/scoring_logic.py

def calculate_integrity_score(row):
    """
    Calculates a score based on GHG Protocol principles:
    - High Permanence: Geologic/Technical (1000+ years)
    - Medium Permanence: Biological/Nature-based (10-100 years)
    - Additionality: Penalizing older vintages (pre-2020)
    """
    score = 0
    
    # 1. Permanence Scoring
    tech_removals = ['Direct Air Capture', 'Mineralization', 'Enhanced Weathering']
    nature_removals = ['Forestry', 'Mangrove', 'Afforestation']
    
    if any(tech in row['type'] for tech in tech_removals):
        score += 10
    elif any(nature in row['type'] for nature in nature_removals):
        score += 6  # Mangroves/Forests have high biodiversity co-benefits
    else:
        score += 3  # Avoidance projects (like Wind/Solar)
        
    # 2. Vintage Penalty (Additionality Check)
    # The older the credit, the more likely the project would have happened anyway
    if row['vintage'] < 2020:
        score -= 4
    elif row['vintage'] >= 2023:
        score += 1  # Bonus for high-demand "Fresh" vintages
        
    return score
