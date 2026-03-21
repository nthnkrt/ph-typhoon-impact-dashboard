import streamlit as st
from utils.components import render_chart_placeholder

def render_trend_analyzer(df, selected_years, selected_region):
    st.header("📈 Trend Analyzer")
    st.markdown("Assess if typhoon impacts are intensifying and compare damage trajectories across regions.")
    st.write("") # spacer

    if selected_region == "All Regions":
        st.warning("⚠️ Trend Analysis is most effective when filtering by a specific Region. Please select one in the Sidebar.")

    st.markdown("<br>", unsafe_allow_html=True)

    col_trend, col_comp = st.columns(2, gap="large")

    with col_trend:
        st.subheader("📊 Regional Vulnerability Trend")
        st.caption("Line chart showing annual aggregate cost with error bands representing variance across provinces.")
        render_chart_placeholder(height=500, text="Regional Trend Line Chart with Error Bands")

    with col_comp:
        col_title, col_sel = st.columns([1, 1])
        with col_title:
            st.subheader("⚖️ Benchmarking")
        with col_sel:
            # Multi-select placeholder
            st.multiselect("Select Provinces (Max 6)", ["Prov A", "Prov B", "Prov C", "Prov D"], default=["Prov A", "Prov B"], label_visibility="collapsed")
            
        st.caption("Side-by-side comparative bar chart evaluating selected provinces metrics and outliers.")
        st.write("")
        render_chart_placeholder(height=450, text="Side-by-side Province Comparison Bar Chart")
