import streamlit as st
import pandas as pd
import numpy as np
from utils.data_loader import load_dpwh_data
import base64
from fpdf import FPDF

def min_max_norm(series: pd.Series) -> pd.Series:
    """Safe min-max normalization enforcing exactly [0.0, 1.0]"""
    if series.empty:
        return series
    
    # Fill na to 0
    series = series.fillna(0)
    
    s_min = series.min()
    s_max = series.max()
    
    # Check if constant
    if s_max == s_min:
        return pd.Series(np.zeros(len(series)), index=series.index)
        
    norm_series = (series - s_min) / (s_max - s_min)
    return norm_series.clip(0.0, 1.0) # hard enforce bounds

def assign_tier(score):
    if score >= 0.81: return 1
    elif score >= 0.61: return 2
    elif score >= 0.41: return 3
    elif score >= 0.21: return 4
    else: return 5

def generate_pdf(df_ranked, actions_map):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="Priority Planner - DPWH Action Plan", ln=True, align='C')
    pdf.ln(5)

    tiers = sorted(df_ranked['Tier'].unique())
    for tier in tiers:
        pdf.set_font("Arial", style='B', size=12)
        tier_label = f"Tier {tier}"
        if tier == 1: tier_label = "Tier 1: Highest priority*"
        elif tier == 2: tier_label = "Tier 2: High priority*"
        elif tier == 3: tier_label = "Tier 3: Medium priority"
        elif tier == 4: tier_label = "Tier 4: Low priority"
        elif tier == 5: tier_label = "Tier 5: Lowest priority"
        
        pdf.cell(200, 10, txt=tier_label, ln=True)
        pdf.set_font("Arial", size=11)
        
        # Actions
        for act in actions_map.get(tier, []):
            pdf.multi_cell(0, 7, txt=f"- {act}")
            
        provinces = df_ranked[df_ranked['Tier'] == tier]['Province'].tolist()
        pdf.set_font("Arial", style='I', size=10)
        pdf.multi_cell(0, 7, txt=f"Applicable Provinces: {', '.join(provinces)}")
        pdf.ln(5)

    return pdf.output(dest='S').encode('latin-1')

def render_priority_planner(df, selected_years, selected_region):
    st.header("Priority Planner")
    st.markdown("Simulate budget allocation and determine priority provinces for infrastructure investment and disaster recovery.")
    
    # Pre-filter by years
    mask = (df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])
    filtered_df = df[mask].copy()
    
    # -------------------------------------------------------------
    # Severity Score vs DPWH Budget Comparison (Regional Level)
    # -------------------------------------------------------------
    st.subheader("DPWH Historical Allocation vs. Data Severity")
    st.markdown("Comparing the internal DPWH Regional Allocation Ranking (Average 2020-2024) to the normalized Severity Score per Region. *The more vulnerable a region is, the more budget that DPWH should allocate.*")
    
    # Group by region for severity
    reg_df = filtered_df.groupby('region')[['cost_total', 'affected_families']].sum().reset_index()
    # Handle division by zero
    reg_df['affected_families'] = reg_df['affected_families'].replace(0, 1)
    reg_df['severity_raw'] = reg_df['cost_total'] / reg_df['affected_families']
    
    if len(reg_df) > 0:
        reg_df['Severity Score'] = min_max_norm(reg_df['severity_raw'])
        # Sort by severity to establish a data-driven rank (1 = highest severity)
        reg_df['Data Severity Rank'] = reg_df['Severity Score'].rank(ascending=False, method='min')
    else:
        reg_df['Severity Score'] = 0
        reg_df['Data Severity Rank'] = 0
    
    # Load Pre-Cleaned DPWH data
    dpwh_df = load_dpwh_data()
    
    # Use selected year or average over all available if range
    if not dpwh_df.empty:
        dpwh_df = dpwh_df[dpwh_df['Region'] != 'CENTRAL OFFICE']
        rank_cols = [f"Rank_{y}" for y in range(selected_years[0], selected_years[1]+1) if f"Rank_{y}" in dpwh_df.columns]
        if not rank_cols:
            rank_cols = [col for col in dpwh_df.columns if col.startswith('Rank_')] # fallback
        dpwh_df['DPWH Allocation Avg Rank'] = dpwh_df[rank_cols].mean(axis=1)
        
        # Merge
        comparison_df = pd.merge(reg_df[['region', 'Severity Score', 'Data Severity Rank']], 
                                 dpwh_df[['Region', 'DPWH Allocation Avg Rank']], 
                                 left_on='region', right_on='Region', how='inner')
        # Filter by region if requested
        if selected_region != "All Regions":
            comparison_df = comparison_df[comparison_df['region'] == selected_region]

        if not comparison_df.empty:
            st.dataframe(comparison_df[['region', 'Severity Score', 'Data Severity Rank', 'DPWH Allocation Avg Rank']]
                         .sort_values('Severity Score', ascending=False)
                         .style.format({'Severity Score': '{:.2f}', 'Data Severity Rank': '{:.0f}', 'DPWH Allocation Avg Rank': '{:.1f}'}),
                         use_container_width=True, hide_index=True)
            
            # Simple bar chart comparison
            chart_data = comparison_df[['region', 'Data Severity Rank', 'DPWH Allocation Avg Rank']].set_index('region')
            st.bar_chart(chart_data)
        else:
            st.info("No comparative DPWH budget data available for the chosen filters.")
    else:
        st.info("DPWH dataset could not be loaded.")
        
    st.divider()

    # Apply Region Filter for Province Drilldown
    if selected_region != "All Regions":
        filtered_df = filtered_df[filtered_df['region'] == selected_region]

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
        return

    # -------------------------------------------------------------
    # Province Level Priority Settings
    # -------------------------------------------------------------
    with st.expander("Priority Configuration", expanded=True):
        col_budget, col_weights = st.columns([1, 2], gap="large")
        with col_budget:
            st.subheader("Budget Constraints")
            budget = st.slider("Available Budget (₱ Millions)", min_value=10, max_value=5000, value=1000, step=10)
        
        with col_weights:
            st.subheader("Priority Weighting")
            st.caption("Adjust to emphasize different impact factors in the Composite Risk Score.")
            w1, w2, w3 = st.columns(3)
            with w1:
                w_human = st.slider("Human Impact", 0.0, 1.0, 0.5, key="w_human")
            with w2:
                w_econ = st.slider("Economic Impact", 0.0, 1.0, 0.3, key="w_econ")
            with w3:
                w_house = st.slider("Housing Damage", 0.0, 1.0, 0.2, key="w_house")
                
    # Normalize weights so they always sum to 1.0
    total_w = w_human + w_econ + w_house
    if total_w == 0:
        w_human, w_econ, w_house = 0.33, 0.33, 0.34
    else:
        w_human, w_econ, w_house = w_human/total_w, w_econ/total_w, w_house/total_w

    # Calculate Province Scores
    prov_df = filtered_df.groupby('province').sum(numeric_only=True).reset_index()
    
    # Handle possible missing cols
    if 'casualties' not in prov_df.columns:
        prov_df['casualties'] = prov_df.get('dead', 0) + prov_df.get('injured/ill', 0) + prov_df.get('missing', 0)
    if 'damaged_houses' not in prov_df.columns:
        prov_df['damaged_houses'] = prov_df.get('dmg_house_totally', 0) + prov_df.get('dmg_house_partial', 0)
        
    # Safe calc for economic
    econ_cols = [c for c in ['cost_agri', 'cost_infra', 'cost_house', 'cost_priv', 'cost_others'] if c in prov_df.columns]
    prov_df['economic_calc'] = prov_df[econ_cols].sum(axis=1) if econ_cols else prov_df.get('cost_total', 0)

    # Sub-scores
    human_val = min_max_norm(prov_df['casualties'] + prov_df['affected_families'])
    econ_val = min_max_norm(prov_df['economic_calc'])
    house_val = min_max_norm(prov_df['damaged_houses'])
    
    # Priority Score Combine
    prov_df['raw_score'] = (w_human * human_val) + (w_econ * econ_val) + (w_house * house_val)
    prov_df['Priority Score'] = min_max_norm(prov_df['raw_score'])
    
    # Tiers
    prov_df['Tier'] = prov_df['Priority Score'].apply(assign_tier)
    
    # Budget Allocation (Proportional based on Priority Score)
    total_score = prov_df['Priority Score'].sum()
    if total_score > 0:
        # We calculate iteratively to ensure exact 0% variance on budget
        allocations = (prov_df['Priority Score'] / total_score) * budget
        alloc_list = np.floor(allocations).to_list() # Start safely with floor
        remainder = budget - sum(alloc_list)
        
        # Distribute the rounded remainder down to top scores strictly
        sorted_indices = prov_df['Priority Score'].sort_values(ascending=False).index
        idx = 0
        while remainder > 0 and idx < len(sorted_indices):
            alloc_list[sorted_indices[idx]] += 1
            remainder -= 1
            idx += 1
            
        prov_df['Estimated Repair Cost (₱M)'] = alloc_list
    else:
        # Equal split guaranteeing exact bounds
        base_alloc = budget // len(prov_df)
        alloc_list = [base_alloc] * len(prov_df)
        remainder = budget - sum(alloc_list)
        for i in range(remainder): alloc_list[i] += 1
        prov_df['Estimated Repair Cost (₱M)'] = alloc_list

    # Recommendations 
    rec_map = {
        1: "Retrofit centers & bridges, impl. flood control",
        2: "Clear drainage, build shelters",
        3: "Contingency review & center inspection",
        4: "Monitor drainage, literacy campaigns",
        5: "Maintain data updates"
    }
    
    actions_full_map = {
        1: ["Structural retrofitting of evacuation centers and local bridges.",
            "Train officials and inform citizens through seminars in every barangay on disaster preparedness.",
            "Ensure each LGU has sufficient manpower, vehicles, and equipment for transportation (e.g., heavy-transport assets) and communication.",
            "Actual implementation of flood control programs (e.g., drainage, sediment control, rainwater storage projects)."],
        2: ["Develop warning flash-flood and other water-related disaster plans.",
            "Allocate budget for clearing drainage systems.",
            "Increase emergency shelter infrastructure."],
        3: ["Administer regular drills in flood-prone areas or damage zones.",
            "Conduct annual inspections of evacuation centers.",
            "Review disaster contingency plans."],
        4: ["Monitor the cleanliness of drainage and flood-related structures.",
            "Continue disaster literacy campaigns."],
        5: ["Maintain periodic data updates to ensure the severity score remains stable."]
    }

    prov_df['Recommended Action'] = prov_df['Tier'].map(rec_map)
    res_df = prov_df[['province', 'Priority Score', 'Tier', 'Estimated Repair Cost (₱M)', 'Recommended Action']].copy()
    res_df = res_df.rename(columns={'province': 'Province'}).sort_values('Priority Score', ascending=False)
    
    # -------------------------------------------------------------
    # Results & Exports Display
    # -------------------------------------------------------------
    st.subheader("Recommended Priority Ranking")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.download_button(
            label="Download CSV Results",
            data=res_df.to_csv(index=False).encode('utf-8'),
            file_name='priority_ranking.csv',
            mime='text/csv',
            use_container_width=True
        )
    with col2:
        try:
            pdf_bytes = generate_pdf(res_df, actions_full_map)
            st.download_button(
                label="Generate PDF Summary Report",
                data=pdf_bytes,
                file_name="DPWH_Action_Plan.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Failed to generate PDF: {e}")
            
    # Table Formatting
    st.dataframe(
        res_df.style.format({
            'Priority Score': '{:.2f}',
            'Estimated Repair Cost (₱M)': '₱{:.0f}'
        }).background_gradient(subset=['Priority Score'], cmap="Reds"),
        use_container_width=True,
        hide_index=True,
        height=350
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # -------------------------------------------------------------
    # Dynamic Actionable Checklist
    # -------------------------------------------------------------
    st.subheader("Actionable Checklist")
    tiers_present = sorted(res_df['Tier'].unique())
    
    with st.container(border=True):
        if not tiers_present:
            st.info("No actionable tiers found.")
        else:
            for tier in tiers_present:
                label_tier = f"Tier {tier}"
                if tier == 1: label_tier = "Tier 1: Highest priority* (Score 0.81 - 1.00)"
                elif tier == 2: label_tier = "Tier 2: High priority* (Score 0.61 - 0.80)"
                elif tier == 3: label_tier = "Tier 3: Medium priority (Score 0.41 - 0.60)"
                elif tier == 4: label_tier = "Tier 4: Low priority (Score 0.21 - 0.40)"
                elif tier == 5: label_tier = "Tier 5: Lowest priority (Score 0.00 - 0.20)"
                
                st.markdown(f"**{label_tier}**")
                for act in actions_full_map[tier]:
                    st.markdown(f"- {act}")
                    
                prov_list = res_df[res_df['Tier'] == tier]['Province'].tolist()
                st.caption(f"*Applies to: {', '.join(prov_list)}*")
                st.write("")
