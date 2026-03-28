import pandas as pd

def load_dpwh_data() -> pd.DataFrame:
    file_path = "data/DATA101-DPWH-Budget-Allocation.xlsx"
    df_excel = pd.read_excel(file_path, header=None)
    start_idx = df_excel[df_excel[2] == 'Without Central Office'].index[0]
    
    # Header row is the row after 'Without Central Office'
    header_row = start_idx + 1
    
    # Data rows are the next 17 rows
    df_alloc = df_excel.iloc[header_row+1:header_row+18, 2:8].copy()
    df_alloc.columns = ['Region', '2020', '2021', '2022', '2023', '2024']
    
    # Clean region names
    region_map = {
        'NCR': 'NCR', 'CAR': 'CAR', 'REGION I': 'I', 'REGION II': 'II', 'REGION III': 'III',
        'REGION IV-A': 'CALABARZON', 'REGION IV-B': 'MIMAROPA', 'REGION V': 'V',
        'REGION VI': 'VI', 'REGION VII': 'VII', 'REGION VIII': 'VIII', 'REGION IX': 'IX',
        'REGION X': 'X', 'REGION XI': 'XI', 'REGION XII': 'XII', 'REGION XIII': 'CARAGA',
        'BARMM': 'BARMM'
    }
    df_alloc['Region'] = df_alloc['Region'].str.strip().str.upper().map(region_map).fillna(df_alloc['Region'])
    
    return df_alloc

print(load_dpwh_data())
