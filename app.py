import streamlit as st
from utils.styles import apply_custom_css
from utils.data_loader import load_data

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
    st.button("Download Current CSV Data", use_container_width=True)
    st.button("Generate PDF Summary Report", use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Data sources: DOST-PAGASA & PSA")

# ==========================================
# Main Content Area
# ==========================================
st.title("Philippine Typhoon Socio-Economic Impact (2020–2024)")
st.markdown("A decision support dashboard designed to optimize disaster recovery and budget allocation through evidence-based planning.")
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
    ["Overview Dashboard", "Province Deep Dive", "Priority Planner", "Trend Analyzer"], 
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
