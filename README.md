# Philippine Typhoon Socio-Economic Impact Dashboard (2020–2024)

A decision support dashboard designed to optimize disaster recovery and budget allocation based on the "A Provincial Analysis of Typhoon Severity and Socio-Economic Impact in the Philippines (2020 to 2024)" study. 

The dashboard provides actionable insights through the Composite Provincial Risk Score, Severity Factor, interactive variance modeling, and strict data engineering pipelines.

## Setup Instructions

1. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Standardize Raw Data (Optional ETL pipeline run):**
   If you download new raw Excel or tabular records, you can route them through the ETL scripts to ensure normalization format is maintained dynamically:
   ```bash
   python scripts/clean_data.py
   python scripts/clean_dpwh_data.py
   ```

4. **Run the Dashboard:**
   ```bash
   streamlit run app.py
   ```

## Project Architecture
* `app.py`: Main entrypoint container executing global sidebar controls, configuration syncing, and top-level sub-view routing.
* `views/`: The presentation logic rendering the 4 main application modules independently:
  * `overview.py`: Geospatial Risk Mapping and High-level KPIs dynamically reacting to the sidebar queries.
  * `deep_dive.py`: Province-specific granular analysis, monthly impact trends, and individual severity damage components.
  * `priority_planner.py`: Mathematical budget simulation engine. Computes structural allocations ensuring zero-drift budgets, links composite tier categories natively, and supports `.PDF` / `.CSV` report generation exports.
  * `trend_analyzer.py`: Multi-year variance forecasting mapping region standard deviations (Altair rendering) combined with 6-stage inter-province benchmarking.
* `scripts/`: Offline Data Transformation utilities managing heavy Extract-Transform-Load (ETL) tasks without burdening Streamlit initialization (`clean_data.py`, `clean_dpwh_data.py`).
* `data/`: Protected static storage location for flat-schema dependencies and outputs (`final_dashboard_data.csv`, `cleaned_dpwh_budget.csv`) alongside geographic configurations (`gadm41_PHL_shp`).
* `utils/`: Core processing layers housing CSS templating and explicit mapping loaders caching memory states globally (`data_loader.py`, `styles.py`).