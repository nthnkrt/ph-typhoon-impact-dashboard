import streamlit as st
from utils.styles import apply_custom_css
from utils.data_loader import load_data, load_dpwh_data
from utils.reports import generate_global_pdf_report
import pandas as pd

st.set_page_config(
    page_title="Typhoon Impact Dashboard (2020-2024)",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global premium CSS
apply_custom_css()

df = load_data()

# ==========================================
# Sidebar Global Controls
# ==========================================
with st.sidebar:
    st.title("Configuration")
    st.markdown("Use these controls to filter the data across all views.")
    st.divider()

    # Year Range Slider
    st.subheader("Timeframe")
    selected_years = st.slider(
        "Select Year Range",
        min_value=2020,
        max_value=2024,
        value=(2020, 2024)
    )

    # Region Dropdown
    st.subheader("Geography")
    regions = ["All Regions", "NCR", "CAR", "Region I", "Region II", "Region III", 
               "Region IV-A", "Region IV-B", "Region V", "Region VI", "Region VII", 
               "Region VIII", "Region IX", "Region X", "Region XI", "Region XII", 
               "Region XIII", "BARMM"]
    selected_region_ui = st.selectbox("Filter by Region", regions, index=0)
    
    region_mapping = {
        "All Regions": "All Regions",
        "NCR": "NCR", "CAR": "CAR", "Region I": "I", "Region II": "II",
        "Region III": "III", "Region IV-A": "CALABARZON", "Region IV-B": "MIMAROPA",
        "Region V": "V", "Region VI": "VI", "Region VII": "VII", "Region VIII": "VIII",
        "Region IX": "IX", "Region X": "X", "Region XI": "XI", "Region XII": "XII",
        "Region XIII": "CARAGA", "BARMM": "BARMM"
    }
    selected_region = region_mapping.get(selected_region_ui, selected_region_ui)

    # Primary Metric Selector
    st.subheader("Primary Metric")
    metrics = ["Severity Factor", "Total Cost", "Affected Families", "Casualties"]
    selected_metric = st.selectbox("Metric to Analyze", metrics, index=0)

    st.divider()
    
    # Export Capabilities
    st.subheader("Export & Reports")
    
    # 1. Filter the dataset based on current sidebar limits
    mask = (df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])
    global_df = df[mask].copy()
    if selected_region != "All Regions":
        global_df = global_df[global_df['region'] == selected_region]
        
    # 2. Extract DPWH Rank context dynamically
    dpwh_context = ""
    if selected_region != "All Regions":
        dpwh_df = load_dpwh_data()
        if not dpwh_df.empty:
            rank_cols = [f"Rank_{y}" for y in range(selected_years[0], selected_years[1]+1) if f"Rank_{y}" in dpwh_df.columns]
            if not rank_cols:
                rank_cols = [col for col in dpwh_df.columns if col.startswith('Rank_')] 
            avg_rank = dpwh_df[dpwh_df['Region'] == selected_region][rank_cols].mean(axis=1)
            if not avg_rank.empty and not pd.isna(avg_rank.iloc[0]):
                dpwh_context = f"DPWH Average Budget Rank: {avg_rank.iloc[0]:.1f}"

    # 3. CSV Dataset Downloader 
    csv_bytes = global_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Current CSV Data",
        data=csv_bytes,
        file_name='executive_typhoon_data.csv',
        mime='text/csv',
        use_container_width=True
    )
    
    # 4. Executive PDF Generator Button
    try:
        pdf_bytes = generate_global_pdf_report(global_df, selected_region, selected_years, dpwh_context)
        st.download_button(
            label="Generate PDF Summary Report",
            data=pdf_bytes,
            file_name="Executive_Summary_Report.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Failed to compile PDF: {e}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Data sources: DOST-PAGASA & PSA")

# ==========================================
# Main Content Area
# ==========================================
st.title("Philippine Typhoon Socio-Economic Impact (2020–2024)")
st.markdown("""
**Stakeholder:** Department of Public Works and Highways (DPWH) & National Disaster Risk Reduction Management Councils (NDRRMC)  
**Decision Question:** How should post-typhoon infrastructure rehabilitation and recovery budgets be prioritized and allocated across Philippine provinces to maximize socio-economic recovery?  
**Decision Output:** 5-Tier Provincial Priority Ranking for Budget Allocation
""")
st.write("") # Spacer

# Navigation
if 'nav_radio_target' in st.session_state:
    st.session_state.nav_radio = st.session_state.nav_radio_target
    del st.session_state.nav_radio_target

if 'nav_radio' not in st.session_state or st.session_state.nav_radio is None:
    st.session_state.nav_radio = "Overview Dashboard"

# Use st.pills for a modern, minimalist, and clean navigation bar
selected_tab = st.pills(
    "Navigation", 
    ["Overview Dashboard", "Province Deep Dive", "Priority Planner", "Trend Analyzer", "Recommendations & Methodology"],
    selection_mode="single",
    label_visibility="collapsed",
    key="nav_radio"
)

if selected_tab is None:
    selected_tab = "Overview Dashboard"
    
if selected_tab == "Overview Dashboard":
    from views import overview
    overview.render_overview(df, selected_years, selected_region, selected_metric)

elif selected_tab == "Province Deep Dive":
    from views import deep_dive
    deep_dive.render_deep_dive(df, selected_years, selected_region)

elif selected_tab == "Priority Planner":
    from views import priority_planner
    priority_planner.render_priority_planner(df, selected_years, selected_region)

elif selected_tab == "Trend Analyzer":
    from views import trend_analyzer
    trend_analyzer.render_trend_analyzer(df, selected_years, selected_region)

elif selected_tab == "Recommendations & Methodology":
    from views import recommendations
    recommendations.render_recommendations(df, selected_years, selected_region)
