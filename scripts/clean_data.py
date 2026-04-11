import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
input_file = os.path.join(project_root, 'data', 'typhoon_data.csv')

# Code by @fatimasulit
df = pd.read_csv(input_file)
print(df.head())

# remove other years
df = df[(df['year'] >= 2020) & (df['year'] <= 2024)]
print(df['year'].unique())

# check region names
df['region'].unique()
print(df['region'].unique())

# check province names
df['province'].unique()
print(df['province'].unique())

# find provinces with multiple regions
province_region_check = df.groupby('province')['region'].nunique()
problem_provinces = province_region_check[province_region_check > 1]

#show mismatched rows
mismatches = df[df['province'].isin(problem_provinces.index)] \
    .sort_values(['province', 'year'])

pd.set_option('display.max_rows', None)
print(mismatches)

# export first cleaned dataset
df.to_csv(os.path.join(project_root, 'data', 'cleaned_step1.csv'), index=False)

# cleaning (Maguindanao del Norte and Maguindanao del Sur combined into Maguindanao)
df['province'] = df['province'].replace({
    "Maguindanao del Norte": "Maguindanao",
    "Maguindanao del Sur": "Maguindanao"
})
print(df['province'].unique())

# export second cleaned dataset
df.to_csv(os.path.join(project_root, 'data', 'cleaned_step2.csv'), index=False)

# Fix: do not sort without breakdown under a single region
df['region'] = df.groupby('province')['region'].transform(
    lambda x: x if x.name == 'without breakdown' else x.mode()[0]
)

# check (problem_provinces should now be empty)
province_region_check = df.groupby('province')['region'].nunique()
problem_provinces = province_region_check[province_region_check > 1]
print(problem_provinces)

# export third cleaned dataset
df.to_csv(os.path.join(project_root, 'data', 'cleaned_step3.csv'), index=False)

print(df[df['region'] == 'NCR'])

# Set paths correctly relative to this script in scripts/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
input_file = os.path.join(project_root, 'data', 'cleaned_step3.csv')
output_file = os.path.join(project_root, 'data', 'final_dashboard_data.csv')

# Load the data
df = pd.read_csv(input_file)

# 1. Fix the 'IIII' typo
df.loc[df['region'] == 'IIII', 'region'] = 'IV'

# 2. Consolidate NCR cities into 'Metro Manila'
ncr_cities = [
    'Caloocan', 'Las Piñas', 'Makati', 'Malabon', 'Mandaluyong', 
    'Manila', 'Marikina', 'Muntinlupa', 'Navotas', 'Parañaque', 
    'Pasay', 'Pasig', 'Pateros', 'Quezon City', 'San Juan', 
    'Taguig', 'Valenzuela', 'without breakdown'
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

# Assign BARMM provinces to BARMM
barmm_provs = [
    'Basilan', 'Lanao del Sur', 'Maguindanao', 'Tawi-tawi'
]
df.loc[(df['province'].isin(barmm_provs)), 'region'] = 'BARMM'

# 4. Group by and sum the numeric columns
numeric_cols = [
    'dead', 'injured/ill', 'missing', 'affected_families', 'affected_persons', 
    'dmg_house_totally', 'dmg_house_partial', 'cost_agri', 'cost_infra', 
    'cost_house', 'cost_priv', 'cost_others', 'cost_total'
]
final_df = df.groupby(['province', 'region', 'year'], as_index=False)[numeric_cols].sum()

# 5. Export the final dataset
final_df.to_csv(output_file, index=False)
print("Success: data/final_dashboard_data.csv strictly updated!")