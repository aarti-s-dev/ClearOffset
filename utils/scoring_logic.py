# utils/scoring_logic.py
from datetime import datetime

def calculate_integrity_score(row):
    """
    Weighted Scoring Algorithm v1.0
    Factors: Permanence (60%), Vintage Decay & Additionality (40%)
    """
    current_year = datetime.now().year
    
    # --- 1. PERMANENCE SCORE (Scale 1-10) ---
    # High: Geologic (DAC, Mineralization) = 10
    # Medium: Blue Carbon/Bio (Mangroves, Peat) = 7
    # Low: Standard Forestry = 5
    # Very Low: Renewable Energy Avoidance = 2
    
    perm_map = {
        'Direct Air Capture': 10,
        'Mineralization': 10,
        'Enhanced Weathering': 10,
        'Mangrove': 7,
        'Peatland': 7,
        'Forestry': 5,
        'Afforestation': 5,
        'Wind': 2,
        'Solar': 2
    }
    
    # Default to 3 if type is unknown
    p_score = perm_map.get(row['type'], 3)
    
    # --- 2. VINTAGE DECAY & ADDITIONALITY (Scale 1-10) ---
    # Additionality Filter: Renewables older than 5 years are often 'non-additional'
    age = current_year - row['vintage']
    v_score = 10  # Start at perfect 10
    
    # Apply Decay: -1.5 points for every year older than 5 years
    if age > 5:
        decay_years = age - 5
        v_score -= (decay_years * 1.5)
    
    # Additionality "Floor": Ensure score doesn't go below 1
    v_score = max(v_score, 1)

    # --- 3. FINAL WEIGHTED CALCULATION ---
    # 60% Weight on Permanence, 40% on Vintage/Additionality
    final_rating = (p_score * 0.6) + (v_score * 0.4)
    
    return round(final_rating, 1)
