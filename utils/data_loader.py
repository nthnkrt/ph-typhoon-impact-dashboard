import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Loads and caches the main dataset for the dashboard.
    
    INTEGRATION INSTRUCTIONS FOR DATA VISUALIZER:
    1. Place your cleaned CSV file (e.g., 'cleaned_typhoon_data.csv') into the `data/` folder.
    2. Read it here using `pd.read_csv('data/cleaned_typhoon_data.csv')`.
    3. Perform any final global data type conversions here.
    4. Return the dataframe.
    """
    # Example placeholder:
    # file_path = os.path.join("data", "cleaned_typhoon_data.csv")
    # if os.path.exists(file_path):
    #     return pd.read_csv(file_path)
    
    # Returning an empty dataframe for the prototype structure

    file_path = "final_dashboard_data.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, engine="python")
        if 'dmg_house_totally' in df.columns and 'dmg_house_partial' in df.columns:
            df['damaged_houses'] = df['dmg_house_totally'] + df['dmg_house_partial']
        return df

    return pd.DataFrame()