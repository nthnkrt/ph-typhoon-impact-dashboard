import streamlit as st
import pandas as pd

def render_recommendations(df, selected_years, selected_region):
    st.header("Recommendations & Methodology")
    st.markdown("This section provides decision-ready recommendations derived from the analytical models and outlines the transparency of our data processes.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Actionable Recommendations")
        
        st.markdown('''
        #### Proposed Action
        The DPWH and NDRRMCs must reallocate rapid-response infrastructure recovery budgets toward Tier 1 and Tier 2 High-Priority provinces. The strategic goal is to reduce secondary socio-economic deterioration by establishing immediate access to isolated communities, prioritizing regions with the highest sustained economic and infrastructural damages relative to their population.
        
        #### Target Areas & Evidence
        **Primary Targets (Tier 1 & 2):** Provinces systematically identified in the **Priority Planner**. These areas exhibit:
        1. **High Severity Factors:** Disproportionate total casualty count and massive infrastructure/agricultural damage.
        2. **Consistent Impact:** High recurrence of extreme impacts within the observed timeframe.
        *Use the "Priority Planner" tab to generate the localized dynamic target list based on your current filter configurations.*
        
        #### Suggested Interventions
        - **Pre-Positioning:** Deploy DPWH Quick Response Assets (heavy equipment, temporary bridge components) to designated Tier 1 hubs prior to the wet season.
        - **Budget Alignment:** Shift unused contingent funds to provinces where DPWH Historical Budget Average Ranks mismatch their Empirical Severity needs.
        
        #### Feasibility Assumptions & Scenarios
        - **Standard Budget Scenario:** Funds are sufficient to cover tier 1 to tier 3. Prioritization runs strictly on the highest Severity Factor.
        - **Constrained Budget Scenario:** Severe resource limits. Focus strictly shifts to structural damage indicators, explicitly isolating and acting only upon top 10% highest casualty-density and heavily isolated areas.
        ''')

        st.subheader("Measurable Success Metrics")
        st.info("""
        1. **Response Time Reduction:** Ensure at least 80% of Tier 1 national road networks are cleared and passable within 48 hours post-impact.
        2. **Budget Alignment Gap:** Reduce the variance between the empirical Priority Ranking (from this dashboard) and the DPWH allocated Post-Typhoon Budget Ranking by 30% year-over-year.
        3. **Affected Family Access:** Decrease the number of days affected families remain without supply lines by establishing preemptive logistic hubs in all Tier 1 and Tier 2 identified provinces.
        """)

        st.subheader("Limitations and Risks")
        st.warning("""
        - **Reporting Lags:** Damage assessments (NDRRMC/PSA) often experience delays. The real-time estimates may under-represent actual ground realities immediately following a typhoon.
        - **Unseen Vulnerabilities:** The model relies on historical damage proxy data; it does not fully encapsulate rapid environmental topological changes (e.g., sudden landslides not in historical datasets).
        """)

    with col2:
        st.subheader("Methodology & Transparency")
        with st.container(border=True):
            st.markdown("### Data Sources")
            st.markdown("""
            - **DOST-PAGASA:** Historical cyclone routing and meteorological categorization.
            - **PSA (Philippine Statistics Authority):** Baseline provincial population, demography, and socio-economic data.
            - **NDRRMC / DSWD:** Disaster incident reports on casualties, affected families, agricultural and infrastructure damage.
            - **DPWH:** Historical budget alignment proxies (where available).
            """)

            st.markdown("### Processing Notes")
            st.markdown(f"""
            - **Time Coverage:** {selected_years[0]} - {selected_years[1]} (Adjustable via sidebar).
            - **Geographic Level:** Provincial and Regional aggregates.
            - **Missing Values:** Missing monetary values are imputed as `0.00` if the province reported zero incidents, or excluded from averaging dynamically to prevent zero-bias.
            - **Severity Factor Calculation:** A composite index normalized strictly between `0.00` and `1.00`, blending Cost, Casualties, and Affected Families evenly weighted unless explicitly offset in modeling menus.
            """)

            st.markdown("### Generative AI Disclosure")
            st.caption("No generative AI tools were used for data fabrication. **Gemini 3.1 Pro via Antigravity plugin** was utilized explicitly for coding and debugging errors when persisting. Outputs have been manually verified for code integration and logic soundness.")
