import streamlit as st

def render_priority_planner(selected_years, selected_region):
    st.header("Priority Planner")
    st.markdown("Simulate budget allocation and determine priority provinces for infrastructure investment and disaster recovery.")

    # Settings Row
    with st.expander("Priority Configuration", expanded=True):
        col_budget, col_weights = st.columns([1, 2])
        
        with col_budget:
            st.subheader("Budget Constraints")
            st.number_input("Available Budget (₱ Millions)", min_value=0, value=1000, step=100, key="budget_input")
        
        with col_weights:
            st.subheader("Priority Weighting")
            w1, w2, w3 = st.columns(3)
            with w1:
                st.slider("Human Impact Weight", 0.0, 1.0, 0.5, key="w_human")
            with w2:
                st.slider("Economic Impact Weight", 0.0, 1.0, 0.3, key="w_econ")
            with w3:
                st.slider("Housing Destruction Weight", 0.0, 1.0, 0.2, key="w_house")

    st.divider()

    # Results Section
    st.subheader("Recommended Priority Ranking")
    st.info("Table displaying: Province, Risk Score, Estimated Repair Cost, Recommended Action based on Tier.")
    st.container(height=300, border=True)

    st.subheader("Actionable Checklist")
    st.markdown("""
    * **Tier 1 (Highest Priority):** Structural retrofitting of evacuation centers and bridges.
    * **Tier 2 (High Priority):** Develop warning flash-flood and clear drainage systems.
    * **Tier 3 (Medium Priority):** Administer regular drills in flood-prone areas.
    """)
