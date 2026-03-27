import pandas as pd

# Load the data
df = pd.read_csv("cleaned_step3.csv")

# 1. Fix the 'IIII' typo
df.loc[df['region'] == 'IIII', 'region'] = 'IV'

# 2. Consolidate NCR cities into 'Metro Manila'
ncr_cities = [
    'Caloocan', 'Las Piñas', 'Makati', 'Malabon', 'Mandaluyong', 
    'Manila', 'Marikina', 'Muntinlupa', 'Navotas', 'Parañaque', 
    'Pasay', 'Pasig', 'Pateros', 'Quezon City', 'San Juan', 
    'Taguig', 'Valenzuela'
]
df.loc[(df['region'] == 'NCR') & (df['province'].isin(ncr_cities)), 'province'] = 'Metro Manila'

# 3. Map independent cities back to their provinces
city_to_province = {
    'Angeles': 'Pampanga',
    'Dagupan': 'Pangasinan',
    'Olongapo': 'Zambales',
    'Naga': 'Camarines Sur',
    'Cotabato City': 'Maguindanao',
    'Davao City': 'Davao del Sur'
}
df['province'] = df['province'].replace(city_to_province)

# 4. Group by and sum the numeric columns
numeric_cols = [
    'dead', 'injured/ill', 'missing', 'affected_families', 'affected_persons', 
    'dmg_house_totally', 'dmg_house_partial', 'cost_agri', 'cost_infra', 
    'cost_house', 'cost_priv', 'cost_others', 'cost_total'
]
final_df = df.groupby(['province', 'region', 'year'], as_index=False)[numeric_cols].sum()

# 5. Export the final dataset
final_df.to_csv("final_dashboard_data.csv", index=False)
print("Success: final_dashboard_data.csv created!")