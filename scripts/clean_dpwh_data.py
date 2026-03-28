import pandas as pd
import os

def clean_dpwh_excel(input_path: str, output_path: str):
    """
    Extracts the 'Without Central Office' sub-table from the DPWH Budget Allocation Excel file
    and normalizes region names, then saves to a flat CSV.
    """
    if not os.path.exists(input_path):
        print(f"Error: Could not find {input_path}")
        return

    df_excel = pd.read_excel(input_path, header=None)
    
    # Locate 'Without Central Office' section precisely
    matches = df_excel[df_excel[2] == 'Without Central Office']
    if matches.empty:
        print("Error: Could not find 'Without Central Office' string in column C (index 2).")
        return
        
    start_idx = matches.index[0]
    header_row = start_idx + 1
    
    # We slice out the 17 regions + the headers
    df_alloc = df_excel.iloc[header_row+1:header_row+18, 2:8].copy()
    df_alloc.columns = ['Region', '2020', '2021', '2022', '2023', '2024']
    
    # Establish a reliable region map against the shapefile defaults
    region_map = {
        'NCR': 'NCR', 'CAR': 'CAR', 'REGION I': 'I', 'REGION II': 'II', 'REGION III': 'III',
        'REGION IV-A': 'CALABARZON', 'REGION IV-B': 'MIMAROPA', 'REGION V': 'V',
        'REGION VI': 'VI', 'REGION VII': 'VII', 'REGION VIII': 'VIII', 'REGION IX': 'IX',
        'REGION X': 'X', 'REGION XI': 'XI', 'REGION XII': 'XII', 'REGION XIII': 'CARAGA',
        'BARMM': 'BARMM'
    }
    
    df_alloc['Region'] = df_alloc['Region'].astype(str).str.strip().str.upper().map(region_map).fillna(df_alloc['Region'])
    
    # Ensure numerical columns are technically floats/ints and rounded
    for col in ['2020', '2021', '2022', '2023', '2024']:
        df_alloc[col] = pd.to_numeric(df_alloc[col], errors='coerce')
    
    # Ensure out directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_alloc.to_csv(output_path, index=False)
    print(f"Successfully processed {input_path} -> {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    in_file = os.path.join(project_root, 'data', 'DATA101-DPWH-Budget-Allocation.xlsx')
    out_file = os.path.join(project_root, 'data', 'cleaned_dpwh_budget.csv')
    clean_dpwh_excel(in_file, out_file)
