import streamlit as st
import pandas as pd
import altair as alt

def render_trend_analyzer(df, selected_years, selected_region):
    st.header("Trend Analyzer")
    st.markdown("Assess if typhoon impacts are intensifying and compare damage trajectories across regions.")
    st.write("") 
    
    # -------------------------------------------------------------
    # Region Selection Syncing
    # -------------------------------------------------------------
    # If the sidebar provides a single region, use it. Otherwise, force a local choice.
    if selected_region == "All Regions":
        regions_list = sorted(list(df['region'].dropna().unique()))
        if not regions_list:
            st.warning("No regions found to analyze.")
            return
        local_region = st.selectbox("Select a Region to Analyze", regions_list, help="Trend variance across provinces requires a specific region.")
    else:
        local_region = selected_region
        st.info(f"**Focusing on {local_region}** (as selected in the Sidebar).")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Filter dataset for time and exact region
    mask = (df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1]) & (df['region'] == local_region)
    region_df = df[mask].copy()

    if region_df.empty:
        st.warning(f"No typhoon data found for {local_region} between {selected_years[0]} and {selected_years[1]}.")
        return

    # -------------------------------------------------------------
    # Area 1: Regional Vulnerability Trend Line Chart (Altair)
    # -------------------------------------------------------------
    st.subheader("Regional Vulnerability Trend")
    st.caption("Annual aggregate cost displaying the mean across provinces. Shaded band represents the standard deviation (variance) among provinces within the region.")
    
    # Standardize missing numericals
    cost_cols = ['cost_total', 'cost_agri', 'cost_infra']
    for col in cost_cols:
        if col not in region_df.columns:
            region_df[col] = 0.0
            
    # For Altair, we want year as discrete categorical or continuous time. Year is integer, we'll keep it integer for axis.
    # Group by year and province so we can compute STD across provinces for each year
    trend_data = region_df.groupby(['year', 'province'])[cost_cols].sum().reset_index()

    # Create a long-form dataframe for altair
    trend_melt = trend_data.melt(id_vars=['year', 'province'], value_vars=cost_cols, 
                                 var_name='Cost Type', value_name='Amount (\u20b1)')
                                 
    # Map names for better readability
    trend_melt['Cost Type'] = trend_melt['Cost Type'].replace({
        'cost_total': 'Total Cost',
        'cost_agri': 'Agricultural Cost',
        'cost_infra': 'Infrastructure Cost'
    })

    # Line Chart: Mean
    line = alt.Chart(trend_melt).mark_line(point=True).encode(
        x=alt.X('year:O', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('mean(Amount (\u20b1)):Q', title='Average Cost (\u20b1) per Province'),
        color=alt.Color('Cost Type:N', legend=alt.Legend(title="Metric")),
        tooltip=['year:O', 'Cost Type:N', alt.Tooltip('mean(Amount (\u20b1)):Q', title='Mean', format=',.0f')]
    )

    # Error Band: Standard Deviation (extent='stdev')
    band = alt.Chart(trend_melt).mark_errorband(extent='stdev', opacity=0.15).encode(
        x='year:O',
        y=alt.Y('Amount (\u20b1):Q', title='Average Cost (\u20b1) per Province'),
        color='Cost Type:N'
    )

    trend_chart = (band + line).properties(height=450)
    st.altair_chart(trend_chart, use_container_width=True)

    st.divider()

    # -------------------------------------------------------------
    # Area 2: Province Benchmarking
    # -------------------------------------------------------------
    st.subheader("Province Benchmarking")
    st.caption("Side-by-side comparative bar chart evaluating selected provinces metrics and outliers over the filtered timeframe.")
    
    col_sel, col_metric = st.columns([2, 1])
    
    # Identify unique provinces in region
    provinces_list = sorted(list(region_df['province'].dropna().unique()))
    
    default_provs = provinces_list[:4] if len(provinces_list) >= 4 else provinces_list
    
    with col_sel:
        bench_provs = st.multiselect("Select Provinces (Max 6)", provinces_list, default=default_provs, max_selections=6)
        
    with col_metric:
        bench_metrics = ['Total Cost (\u20b1)', 'Agricultural Cost (\u20b1)', 'Infrastructure Cost (\u20b1)', 
                         'Severity Factor (Cost per Family)', 'Total Affected Families', 'Casualties']
        selected_bench_metric = st.selectbox("Compare Metric", bench_metrics)

    if not bench_provs:
        st.info("Select at least one province to benchmark.")
        return
        
    # Aggregate data by province across the selected years
    bench_data = region_df[region_df['province'].isin(bench_provs)].groupby('province').sum(numeric_only=True).reset_index()
    
    # Calculate derived metrics if needed
    if 'casualties' not in bench_data.columns:
        bench_data['casualties'] = bench_data.get('dead', 0) + bench_data.get('injured/ill', 0) + bench_data.get('missing', 0)
    
    # Safeguard div by 0 for Severity
    affected_fam = bench_data.get('affected_families', 0).replace(0, 1)
    bench_data['Severity Factor (Cost per Family)'] = bench_data.get('cost_total', 0) / affected_fam
    
    # Map selection to actual columns
    col_map = {
        'Total Cost (\u20b1)': 'cost_total',
        'Agricultural Cost (\u20b1)': 'cost_agri',
        'Infrastructure Cost (\u20b1)': 'cost_infra',
        'Severity Factor (Cost per Family)': 'Severity Factor (Cost per Family)',
        'Total Affected Families': 'affected_families',
        'Casualties': 'casualties'
    }
    y_col = col_map[selected_bench_metric]
    
    # Ensure column exists
    if y_col not in bench_data.columns:
        bench_data[y_col] = 0.0

    # Altair bar chart for clearer benchmark spacing
    bar = alt.Chart(bench_data).mark_bar().encode(
        x=alt.X('province:N', title='Province', axis=alt.Axis(labelAngle=0, labelOverlap=False)),
        y=alt.Y(f'{y_col}:Q', title=selected_bench_metric),
        color=alt.Color('province:N', legend=None),
        tooltip=['province:N', alt.Tooltip(f'{y_col}:Q', format=',.2f')]
    ).properties(height=450)

    # Text labels on bars using 'short' format for large numbers
    text = bar.mark_text(
        align='center',
        baseline='bottom',
        dy=-5  # Nudges text up so it doesn't overlap the top of the bar
    ).encode(
        text=alt.Text(f'{y_col}:Q', format='.2s') # Short format e.g. 1.2M
    )

    st.altair_chart(bar + text, use_container_width=True)
