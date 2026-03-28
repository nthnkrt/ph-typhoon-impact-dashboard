import pandas as pd

with open('explore.txt', 'w') as f:
    df_excel = pd.read_excel('data/DATA101-DPWH-Budget-Allocation.xlsx', header=None)
    f.write(f"Shape: {df_excel.shape}\n")
    f.write(df_excel.head(30).to_string())