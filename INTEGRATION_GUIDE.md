# Dashboard Integration Guide

Hello! This guide is written for the Data/Visualization Engineer who will be integrating the actual data models and plotly prototypes into the Streamlit dashboard structure.

As the app engineer, I have completely styled and structured the UI. The dashboard is entirely separated into clean views and components. All you need to do is connect your data and replace the placeholders.

## 1. Where to Load Your Data
I've created a centralized data loading function at `utils/data_loader.py`. 
- Place your cleaned `.csv` datasets in the `data/` folder.
- Modify `utils.data_loader.load_data()` to load your dataset.
- The dataframe (`df`) loaded here is automatically passed to **every single view**.

## 2. Integrating Your Charts
Currently, the charts are visually mocked using a function from `utils/components.py` called `render_chart_placeholder()`. 

To plug in your interactive Plotly graphs, go to the corresponding view files in the `views/` folder (`overview.py`, `deep_dive.py`, etc.). 

**Example Change:**
*Before (My code)*:
```python
render_chart_placeholder(height=500, text=f"Choropleth Map for {selected_metric}")
```
*After (Your code)*:
```python
# 1. You can filter the 'df' using the selected_years and selected_region parameters
filtered_df = df[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]

# 2. Generate your plotly figure
fig = create_choropleth_map(filtered_df, selected_metric) 

# 3. Render it in streamlit!
st.plotly_chart(fig, use_container_width=True)
```

## 3. Connecting the KPI Cards
In the views, you'll see KPI metrics written like:
```python
st.metric(label="Total Incidents", value="--", delta="Filtered")
```
Just calculate the values dynamically from `df` and replace the `"--"` string with your variable (e.g., `f"{total_incidents:,}"`).

Everything should already be styled cleanly because of the `utils/styles.py` global CSS injector! Let me know if you need any UI refinements.
