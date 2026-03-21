import streamlit as st
from utils.styles import apply_custom_css

st.set_page_config(
    page_title="Typhoon Impact Dashboard (2020-2024)",
    page_icon="🌪️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global premium CSS
apply_custom_css()

# ==========================================
# Sidebar Global Controls
# ==========================================
with st.sidebar:
    st.title("⚙️ Configuration")
    st.markdown("Use these controls to filter the data across all views.")
    st.divider()

    # Year Range Slider
    st.subheader("📅 Timeframe")
    selected_years = st.slider(
        "Select Year Range",
        min_value=2020,
        max_value=2024,
        value=(2020, 2024)
    )

    # Region Dropdown
    st.subheader("📍 Geography")
    regions = ["All Regions", "NCR", "CAR", "Region I", "Region II", "Region III", 
               "Region IV-A", "Region IV-B", "Region V", "Region VI", "Region VII", 
               "Region VIII", "Region IX", "Region X", "Region XI", "Region XII", 
               "Region XIII", "BARMM"]
    selected_region = st.selectbox("Filter by Region", regions, index=0)

    # Primary Metric Selector
    st.subheader("📈 Primary Metric")
    metrics = ["Severity Factor", "Total Cost", "Affected Families", "Casualties"]
    selected_metric = st.selectbox("Metric to Analyze", metrics, index=0)

    st.divider()
    
    # Export Capabilities
    st.subheader("📥 Export & Reports")
    st.button("⬇ Download Current CSV Data", use_container_width=True)
    st.button("📄 Generate PDF Summary Report", use_container_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Data sources: DOST-PAGASA & PSA")

# ==========================================
# Main Content Area
# ==========================================
st.title("🌪️ Philippine Typhoon Socio-Economic Impact (2020–2024)")
st.markdown("A decision support dashboard designed to optimize disaster recovery and budget allocation through evidence-based planning.")
st.write("") # Spacer

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
