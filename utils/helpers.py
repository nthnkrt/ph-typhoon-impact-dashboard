import pandas as pd
import streamlit as st

@st.cache_data
def load_placeholder_data():
    """
    Returns placeholder data architecture until real data is ingested.
    """
    # This matches the requested data schema in Section 3.1
    columns = [
        "Province", "Region", "Year", "Cyclone_Category", 
        "Affected_Families", "Cost_Agri", "Cost_Infra", 
        "Cost_Private", "Cost_Housing", "Casualties", "Damaged_Houses"
    ]
    df = pd.DataFrame(columns=columns)
    return df
