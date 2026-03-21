import streamlit as st
from utils.components import render_chart_placeholder

def render_priority_planner(df, selected_years, selected_region):
    st.header("Priority Planner")
    st.markdown("Simulate budget allocation and determine priority provinces for infrastructure investment and disaster recovery.")
    st.write("") # spacer

    # Settings Row
    with st.expander("Priority Configuration", expanded=True):
        col_budget, col_weights = st.columns([1, 2], gap="large")
        
        with col_budget:
            st.subheader("Budget Constraints")
            # Improved number input with better default and label hiding if needed
            budget = st.number_input("Available Budget (₱ Millions)", min_value=0, value=1000, step=100, key="budget_input")
            st.caption(f"Simulating allocations up to: **₱{budget:,.0f}M**")
        
        with col_weights:
            st.subheader("Priority Weighting")
            st.caption("Adjust the sliders to change weighting significance over the final Composite Risk Score.")
            w1, w2, w3 = st.columns(3)
            with w1:
                st.slider("Human Impact", 0.0, 1.0, 0.5, key="w_human", help="Weight based on casualties and affected persons.")
            with w2:
                st.slider("Economic Impact", 0.0, 1.0, 0.3, key="w_econ", help="Weight considering infrastructure and agriculture costs.")
            with w3:
                st.slider("Housing Damage", 0.0, 1.0, 0.2, key="w_house", help="Weight focused purely on housing destruction.")

    st.markdown("<br>", unsafe_allow_html=True)

    # Results Section
    st.subheader("Recommended Priority Ranking")
    st.caption("Table displaying: Province, Risk Score, Estimated Repair Cost, Recommended Action based on Tier.")
    
    # Placeholder for the data table
    render_chart_placeholder(height=350, text="Interactive Data Table of Ranked Provinces")

    st.markdown("<br>", unsafe_allow_html=True)

    # Actionable Checklist styled nicely
    col_check_title, col_check_btn = st.columns([4, 1])
    with col_check_title:
        st.subheader("Actionable Checklist")
    with col_check_btn:
        st.button("Export PDF Action Plan", use_container_width=True)

    with st.container(border=True):
        st.markdown("""
        **Tier 1 (Highest Priority): Score 0.81 - 1.00** 
        - Structural retrofitting of evacuation centers and local bridges.
        - Train officials and inform citizens through seminars in every barangay on disaster preparedness.
        - Ensure each LGU has sufficient manpower, vehicles, and equipment for transportation (e.g., heavy-transport assets) and communication.
        - Actual implementation of flood control programs (e.g., drainage, sediment control, rainwater storage projects).  

        **Tier 2 (High Priority): Score 0.61 - 0.80**
        - Develop warning flash-flood and other water-related disaster plans.
        - Allocate budget for clearing drainage systems.
        - Increase emergency shelter infrastructure.

        **Tier 3 (Medium Priority): Score 0.41 - 0.60**
        - Administer regular drills in flood-prone areas or damage zones.  
        - Conduct annual inspections of evacuation centers.
        - Review disaster contingency plans. 
        """)
