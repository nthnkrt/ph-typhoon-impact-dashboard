import streamlit as st

def render_overview(selected_years, selected_region, selected_metric):
    st.header("Overview Dashboard")
    st.markdown("Identify which provinces have been most impacted and where severity is concentrated.")

    # KPI Cards row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Incidents", value="--")
    with col2:
        st.metric(label="Total Affected Persons", value="--")
    with col3:
        st.metric(label="Total Cost of Damage (₱)", value="--")
    with col4:
        st.metric(label="Total Casualties", value="--")

    st.divider()

    # Main Visualizations Row
    col_map, col_chart = st.columns([3, 2])
    
    with col_map:
        st.subheader("Geospatial Risk Mapping")
        st.info("Choropleth map of the Philippines showing provinces colored by the selected metric.")
        # Placeholder for Map plotly figure implementation
        st.container(height=400, border=True)

    with col_chart:
        st.subheader(f"Top 15 Provinces by {selected_metric}")
        st.info("Horizontal bar chart ranking the top 15 most impacted provinces.")
        # Placeholder for Ranked Bar Chart
        st.container(height=400, border=True)
