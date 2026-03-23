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

def render_chart_placeholder(height: int, text: str):
    """
    Renders a designed placeholder container to indicate where data visualizations will go.
    Makes it cleaner and easier to replace later with `st.plotly_chart`.
    """
    with st.container(border=True, height=height):
        # We use a markdown with custom class (requires custom css to be loaded)
        st.markdown(f'<div class="chart-placeholder" style="height: {height-40}px;">{text}</div>', unsafe_allow_html=True)

# TODO: I'll clean this up
def render_choropleth_map(df, selected_metric):
    """
    Renders choropleth map
    """
    provinces = gpd.GeoDataFrame.from_file(os.path.join("data", "gadm41_PHL_shp", "gadm41_PHL_1.shp"))
    # Other grouping levels; placing here if needed for future use
    # country = gpd.GeoDataFrame.from_file(os.path.join("data", "gadm41_PHL_shp", "gadm41_PHL_0.shp"))
    # cities = gpd.GeoDataFrame.from_file(os.path.join("data", "gadm41_PHL_shp", "gadm41_PHL_2.shp"))
    # barangay = gpd.GeoDataFrame.from_file(os.path.join("data", "gadm41_PHL_shp", "gadm41_PHL_3.shp"))

    # Sort by province
    df = df.groupby('province', as_index=False).sum().drop(columns=['region', 'year'])
    df = df[['province', 'cost_total', 'affected_families']]

    # Calculate for severity
    df['severity'] = df['cost_total']/(df['affected_families'] + 1) # Avoid division by 0

    # Merge with map
    merged_df = pd.merge(provinces, df, left_on='NAME_1', right_on='province', how='left')
    k = 1600
    cmap = 'Reds'
    figsize=(12,12)
    scheme = 'Quantiles'

    fig, ax = plt.subplots(1, 1, figsize=figsize, facecolor='#b2e2e1')

    if(selected_metric == "Severity Factor"):
        selected_metric = 'severity'
    elif(selected_metric == "Total Cost"):
        selected_metric = 'cost_total'
    elif(selected_metric == "Affected Families"):
        selected_metric = 'affected_families'
    # TODO: For casualties, is this total dead + injured/ill + missing?

    merged_df.plot(column=selected_metric, cmap=cmap, ax=ax,
                      scheme=scheme, k=k, legend=False, 
                      missing_kwds={"color": "lightgrey"}) # Color for missing data
    
    ax.axis('off')

    vmin, vmax = merged_df['severity'].min(), merged_df['severity'].max()
    vcenter = merged_df['severity'].mean()

    if vmin < vcenter < vmax:
        divnorm = colors.TwoSlopeNorm(vmin=vmin, vcenter=vcenter, vmax=vmax)
    else:
        divnorm = colors.Normalize(vmin=vmin, vmax=vmax)

    cbar = plt.cm.ScalarMappable(norm=divnorm, cmap=cmap)
    fig.colorbar(cbar, ax=ax, orientation="vertical", fraction=0.036, pad=0.04)

    st.pyplot(fig)

# TODO: I'll clean this up (2)
def render_top_provinces(df, selected_metric):
    df = df.groupby(['province', 'region'], as_index=False).sum().drop(columns=['year'])
    df = df[['province', 'cost_total', 'affected_families']]
    df['severity'] = df['cost_total']/(df['affected_families'] + 1)
    df = df[(df['province'] != 'without breakdown') & (df['province'] != 'Special Geographic Areas') &
            (df['province'] != 'IIII')]

    if(selected_metric == "Severity Factor"):
        metric_idx = 'severity'
    elif(selected_metric == "Total Cost"):
        metric_idx = 'cost_total'
    elif(selected_metric == "Affected Families"):
        metric_idx = 'affected_families'
    # TODO: For casualties, is this total dead + injured/ill + missing?

    df_top = df.sort_values(metric_idx, ascending=False).head(15)
    print(df_top)
    print(df_top)
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.barplot(
        data=df_top, 
        y='province', 
        x=metric_idx, 
        ax=ax, 
        color="red", 
        legend=False
    )

    ax.set_title(f"Top 15 Provinces by {selected_metric}", fontsize=14, pad=20)
    ax.set_xlabel(selected_metric)
    ax.set_ylabel("")
    sns.despine(left=True, bottom=True)

    st.pyplot(fig)