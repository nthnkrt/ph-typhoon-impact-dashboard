import streamlit as st

st.set_page_config(
    page_title="Typhoon Impact Dashboard (2020-2024)",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Global Controls
st.sidebar.title("Configuration & Filters")
st.sidebar.markdown("Use these controls to filter the data across all views.")

# Year Range Slider
selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=2020,
    max_value=2024,
    value=(2020, 2024)
)

# Region Dropdown
regions = ["All Regions", "NCR", "CAR", "Region I", "Region II", "Region III", "Region IV-A", "Region IV-B", "Region V", "Region VI", "Region VII", "Region VIII", "Region IX", "Region X", "Region XI", "Region XII", "Region XIII", "BARMM"]
selected_region = st.sidebar.selectbox("Filter by Region", regions, index=0)

# Primary Metric Selector
metrics = ["Severity Factor", "Total Cost", "Affected Families", "Casualties"]
selected_metric = st.sidebar.selectbox("Primary Metric", metrics, index=0)

st.sidebar.divider()
st.sidebar.subheader("Export & Reports")
st.sidebar.button("⬇ Download Current CSV Data")
st.sidebar.button("📄 Generate PDF Summary Report")

# Main Content Area
st.title("🌪️ Philippine Typhoon Socio-Economic Impact (2020–2024)")
st.markdown("A decision support dashboard designed to optimize disaster recovery and budget allocation.")

# Navigation / Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview Dashboard", 
    "🔍 Province Deep Dive", 
    "🚨 Priority Planner", 
    "📈 Trend Analyzer"
])

with tab1:
    from views import overview
    overview.render_overview(selected_years, selected_region, selected_metric)

with tab2:
    from views import deep_dive
    deep_dive.render_deep_dive(selected_years, selected_region)

with tab3:
    from views import priority_planner
    priority_planner.render_priority_planner(selected_years, selected_region)

with tab4:
    from views import trend_analyzer
    trend_analyzer.render_trend_analyzer(selected_years, selected_region)
