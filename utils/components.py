import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import seaborn as sns
import geopandas as gpd
import descartes
import mapclassify
import geoplot
import plotly.express as px
import plotly.graph_objects as go

# NOTE: ...placed this to avoid unnecessary repetition across functions
metric_mapping = {
    "Severity Factor": "severity",
    "Total Cost": "cost_total",
    "Affected Families": "affected_families",
    "Casualties": "casualties"
}

def render_chart_placeholder(height: int, text: str):
    """
    Renders a designed placeholder container to indicate where data visualizations will go.
    Makes it cleaner and easier to replace later with `st.plotly_chart`.
    """
    with st.container(border=True, height=height):
        # We use a markdown with custom class (requires custom css to be loaded)
        st.markdown(f'<div class="chart-placeholder" style="height: {height-40}px;">{text}</div>', unsafe_allow_html=True)

@st.cache_data
def load_map_polygons():
    provinces = gpd.GeoDataFrame.from_file(os.path.join("data", "gadm41_PHL_shp", "gadm41_PHL_1.shp"))
    provinces['geometry'] = provinces.geometry.simplify(tolerance=0.01, preserve_topology=True)
    return provinces

# TODO: Clean up dataset errors
# TODO: Handle NCR
# TODO: Define casualties
def render_choropleth_map(df, selected_metric):
    """
    Renders choropleth map
    """
    provinces = load_map_polygons()
    
    df = df.groupby(['province', 'region'], as_index=False).sum(numeric_only=True)
    df = df[~df['province'].isin(['without breakdown', 'Special Geographic Areas', 'IIII'])]
    
    # Severity Formula: Norm(Total cost of damage / Total affected families)
    raw_severity = df['cost_total'] / (df['affected_families'] + 1)
    if not raw_severity.empty and raw_severity.max() != raw_severity.min():
        df['severity'] = (raw_severity - raw_severity.min()) / (raw_severity.max() - raw_severity.min())
    else:
        df['severity'] = 1.0 if not raw_severity.empty and raw_severity.max() > 0 else 0.0
        
    merged_df = pd.merge(provinces, df, left_on='NAME_1', right_on='province', how='left')
    merged_df = merged_df.set_index('NAME_1')

    col = metric_mapping.get(selected_metric, "severity")
    
    # Explicitly bound the continuous color scale ranges
    if selected_metric == "Severity Factor":
        color_range = [0.0, 1.0]
    else:
        max_val = df[col].max() if not df[col].empty else 1.0
        color_range = [0.0, max_val if max_val > 0 else 1.0]

    fig = px.choropleth(
        merged_df,
        geojson=merged_df.geometry,
        locations=merged_df.index, 
        color=col,
        range_color=color_range,
        color_continuous_scale="Reds",
        labels={col: selected_metric},
        hover_name=merged_df.index 
    )

    # Establish grey map trace for unselected provinces, adding it to the figure
    grey_trace = go.Choropleth(
        geojson=provinces.__geo_interface__,
        locations=provinces['NAME_1'],
        featureidkey="properties.NAME_1",
        z=[0]*len(provinces),
        colorscale=[[0, '#e8e8e8'], [1, '#e8e8e8']],
        showscale=False,
        marker_line_color='white',
        marker_line_width=0.5,
        hoverinfo='skip',
        showlegend=False
    )
    
    # Add the grey trace to the figure 
    fig.add_trace(grey_trace)
    
    # Reorder the traces so the grey map is at index 0 (the bottom layer)
    # fig.data is now (main_trace, grey_trace), so we swap them
    fig.data = (fig.data[1], fig.data[0])

    # Now fig.data[1] is the main colored trace, update its hover template
    fig.data[1].hovertemplate = "<b>%{hovertext}</b><br>" + selected_metric + ": %{z:,.2f}<extra></extra>"

    fig.update_geos(
        visible=False,
        projection_type='mercator',
        fitbounds="locations", 
        lataxis_range=[4.5, 21.5], # quick fix but could be more clean
        lonaxis_range=[114.0, 127.0],
        resolution=50,
        showcountries=False
    )

    fig.update_layout(
        height=850,
        margin={"r":0,"t":0,"l":0,"b":0},
        dragmode="pan",
        modebar_remove=['autoscale', 'select', 'lasso2d'],
        geo=dict(bgcolor='#b2e2e1'),
        coloraxis_colorbar=dict(
            title=selected_metric,
            thickness=15,
            len=0.3,
            x=0.02,
            y=0.2
        )
    )

    # Allow click selection for navigation
    event = st.plotly_chart(fig, use_container_width=True, on_select="rerun", selection_mode=("points",))
    return event

# TODO: CLean up dataset errors
# TODO: Define casualties
def render_top_provinces(df, selected_metric):
    """
    Renders bar chart of top 15 provinces by selected metric
    """
    df = df.groupby(['province', 'region'], as_index=False).sum(numeric_only=True)
    # Strip dataset defects before min-max evaluations
    df = df[~df['province'].isin(['without breakdown', 'Special Geographic Areas', 'IIII'])]

    raw_severity = df['cost_total'] / (df['affected_families'] + 1)
    if not raw_severity.empty and raw_severity.max() != raw_severity.min():
        df['severity'] = (raw_severity - raw_severity.min()) / (raw_severity.max() - raw_severity.min())
    else:
        df['severity'] = 1.0 if not raw_severity.empty and raw_severity.max() > 0 else 0.0

    metric_idx = metric_mapping.get(selected_metric, "severity")

    df_top = df.sort_values(metric_idx, ascending=True).tail(15)

    fig = px.bar(
        df_top,
        x=metric_idx,
        y='province',
        orientation='h',
        text_auto='.2f',
        labels={metric_idx: selected_metric, "province": ""},
        template="plotly_white",
        color_discrete_sequence=["#0065fb"]
    )

    dynamic_height = max(150, 100 + len(df_top) * 35)

    fig.update_layout(
        bargap=0.1, 
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True),
        height=dynamic_height,
        margin=dict(l=10, r=20, t=50, b=10),
        hovermode="closest"
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# TODO: CLean up dataset errors
def render_time_plot(df, province, metric):
    metric_mapping = {
        "TOTAL COST": "cost_total",
        "AFFECTED PERSONS": "affected_families",
        "DAMAGED HOUSES": "damaged_houses"
    }
    
    col = metric_mapping.get(metric, metric)
    province_df = df[df['province'] == province]

    # NOTE: Represent metrics during years without records as 0
    # TODO: add explicit description in website about how we handle years without records
    # as having 0 cost
    full_years = pd.DataFrame({'year': range(2020, 2025)})
    merged_df = pd.merge(full_years, province_df, on='year', how='left')
    merged_df[col] = merged_df[col].fillna(0)

    fig = px.line(
        merged_df,
        x='year',
        y=col,
        markers=True,
        template="plotly_white",
        labels={col: metric, "year": "Year"},
        color_discrete_sequence=["#0065fb"]
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis=dict(
            tickmode='linear',
            tick0=2020,
            dtick=1, 
            type='linear',
            rangeslider=dict(visible=False)
        ),
        yaxis=dict(
            fixedrange=False,
            tickformat=",.0f"
        ),
        margin=dict(l=10, r=10, t=20, b=10),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

# TODO: CLean up dataset errors
def render_pie_chart(df, province):
    df = df[(df['province'] == province) & (df['year'] >= 2021)]

    if df.empty:
        st.info(f"No cost breakdown available for {province}.")
        return

    total_costs_df = df[['cost_agri', 'cost_infra', 'cost_house', 
                            'cost_priv', 'cost_others']].sum()

    pie_df = pd.DataFrame({
        "Category": [
            "Agricultural Cost", 
            "Infrastructure Cost", 
            "House Cost", 
            "Private Cost", 
            "Others"
        ],
        "Value": [
            total_costs_df['cost_agri'], 
            total_costs_df['cost_infra'], 
            total_costs_df['cost_house'], 
            total_costs_df['cost_priv'], 
            total_costs_df['cost_others']
        ]
    })

    pie_df = pie_df[pie_df['Value'] > 0]

    if pie_df.empty:
        st.warning("No damage costs for this province.")
        return

    fig = px.pie(
        pie_df,
        values='Value',
        names='Category',
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r,
        template="plotly_white"
    )

    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Amount: ₱%{value:,.2f}<br>Percentage: %{percent}<extra></extra>",
        textinfo='percent+label',
        textposition='inside'
    )

    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", xanchor="center"),
        height=450,
        xaxis=dict(fixedrange=True),
        yaxis=dict(fixedrange=True)
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})