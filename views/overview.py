import streamlit as st
from utils.components import render_chart_placeholder
from utils.components import render_choropleth_map
from utils.components import render_top_provinces

def render_overview(df, selected_years, selected_region, selected_metric):
    st.header("Overview Dashboard")
    st.markdown("Identify which provinces have been most impacted and where severity is concentrated.", help="Data is filtered by the Configuration sidebar.")
    st.write("") # spacer

    # Filter data based on sidebar configuration
    if not df.empty:
        filtered_df = df[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]
        if selected_region != "All Regions":
            filtered_df = filtered_df[filtered_df['region'] == selected_region]
        
        # Calculate KPIs
        total_incidents = f"{len(filtered_df):,}"
        total_affected = f"{int(filtered_df['affected_persons'].sum()):,}"
        total_cost = f"₱{filtered_df['cost_total'].sum():,.2f}"
        total_casualties = f"{int(filtered_df[['dead', 'injured/ill', 'missing']].sum().sum()):,}"
    else:
        filtered_df = df
        total_incidents, total_affected, total_cost, total_casualties = "--", "--", "--", "--"

    # KPI Cards row - Using native columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Total Incidents", value=total_incidents, delta="Filtered")
    with col2:
        st.metric(label="Total Affected Persons", value=total_affected, delta="Filtered")
    with col3:
        st.metric(label="Total Cost of Damage (₱)", value=total_cost, delta="Filtered")
    with col4:
        st.metric(label="Total Casualties", value=total_casualties, delta="Filtered")

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Visualizations Row
    col_map, col_chart = st.columns([3, 2], gap="large")
    
    with col_map:
        st.subheader("Geospatial Risk Mapping")
        st.caption("Choropleth map of the Philippines showing provinces colored by the selected metric.")
        render_choropleth_map(filtered_df, selected_metric)

    with col_chart:
        st.subheader(f"Top 15 Provinces by {selected_metric}")
        st.caption("Horizontal bar chart ranking the top 15 most impacted provinces.")
        render_top_provinces(filtered_df, selected_metric)