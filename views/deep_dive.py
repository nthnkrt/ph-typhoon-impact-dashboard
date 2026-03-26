import streamlit as st
from utils.components import render_chart_placeholder
from utils.components import render_time_plot
from utils.components import render_pie_chart

def render_deep_dive(df, selected_years, selected_region):
    st.header("Province Deep Dive")
    st.markdown("Explore the complete impact history and primary types of damage for a specific province.")
    st.write("")

    # Province selection
    col_sel, col_space = st.columns([1, 2])
    with col_sel:
        # Example: showing selection inside standard container
        # TODO: clean province data; some are mislabelled or are not provinces
        province_choice = st.selectbox("Select Province to Analyze", sorted(df['province'].unique().tolist()), key="dd_province")

    st.markdown("<br>", unsafe_allow_html=True)

    # Province Profile Card (KPIs)
    st.subheader("Province Profile")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("Total Incidents", "--")
    with kpi2:
        st.metric("Total Cost (₱)", "--")
    with kpi3:
        st.metric("Total Affected", "--")
    with kpi4:
        st.metric("Total Casualties", "--")
    
    st.markdown("<br>", unsafe_allow_html=True)

    col_line, col_pie = st.columns([2, 1], gap="large")

    with col_line:
        col_title, col_metric = st.columns([2, 1])
        with col_title:
            st.subheader("Monthly Trend")
        with col_metric:
            metric_choice = st.selectbox("Display Metric", ["TOTAL COST", "AFFECTED PERSONS", "DAMAGED HOUSES"], label_visibility="collapsed", key="dd_metric")
            
        st.caption(f"Multi-line chart showing trends over time ({selected_years[0]} - {selected_years[1]}) for {metric_choice}.")
        render_time_plot(df, province_choice, metric_choice)

    with col_pie:
        st.subheader("Damage Breakdown")
        st.caption("Proportional breakdown of COST OF DAMAGE (Agri, Infra, Private, Housing).")
        st.write("") # Align with line chart dropdown space
        st.write("")
        render_pie_chart(df, province_choice)