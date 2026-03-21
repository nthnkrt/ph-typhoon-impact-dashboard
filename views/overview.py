import streamlit as st
from utils.components import render_chart_placeholder

def render_overview(selected_years, selected_region, selected_metric):
    st.header("Overview Dashboard")
    st.markdown("Identify which provinces have been most impacted and where severity is concentrated.", help="Data is filtered by the Configuration sidebar.")
    st.write("") # spacer

    # KPI Cards row - Using native columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Incidents", value="--", delta="Filtered")
    with col2:
        st.metric(label="Total Affected Persons", value="--", delta="Filtered")
    with col3:
        st.metric(label="Total Cost of Damage (₱)", value="--", delta="Filtered")
    with col4:
        st.metric(label="Total Casualties", value="--", delta="Filtered")

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Visualizations Row
    col_map, col_chart = st.columns([3, 2], gap="large")
    
    with col_map:
        st.subheader("🗺️ Geospatial Risk Mapping")
        st.caption("Choropleth map of the Philippines showing provinces colored by the selected metric.")
        render_chart_placeholder(height=500, text=f"Choropleth Map for {selected_metric}")

    with col_chart:
        st.subheader(f"📊 Top 15 Provinces by {selected_metric}")
        st.caption("Horizontal bar chart ranking the top 15 most impacted provinces.")
        render_chart_placeholder(height=500, text="Ranked Horizontal Bar Chart")
