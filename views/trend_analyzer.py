import streamlit as st

def render_trend_analyzer(selected_years, selected_region):
    st.header("Trend Analyzer")
    st.markdown("Assess if typhoon impacts are intensifying and compare damage trajectories across regions.")

    if selected_region == "All Regions":
        st.warning("Trend Analysis is most effective when filtering by a specific Region. Please select one in the Sidebar.")

    col_trend, col_comp = st.columns(2)

    with col_trend:
        st.subheader("Regional Vulnerability Trend")
        st.info("Line chart showing annual aggregate cost with error bands representing variance across provinces.")
        st.container(height=400, border=True)

    with col_comp:
        st.subheader("Province Benchmarking")
        # Multi-select placeholder
        st.multiselect("Select Provinces to Compare (Max 6)", ["Prov A", "Prov B", "Prov C", "Prov D"], default=["Prov A", "Prov B"])
        st.info("Side-by-side bar chart comparing selected provinces.")
        st.container(height=330, border=True)
