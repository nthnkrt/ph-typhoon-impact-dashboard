# Philippine Typhoon Socio-Economic Impact Dashboard (2020–2024)

A decision support dashboard designed to optimize disaster recovery and budget allocation based on the "A Provincial Analysis of Typhoon Severity and Socio-Economic Impact in the Philippines (2020 to 2024)" study. 

The dashboard provides actionable insights through the Composite Provincial Risk Score and Severity Factor.

## Setup Instructions

1. **Create a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Dashboard:**
   ```bash
   streamlit run app.py
   ```

## Project Structure
* `app.py`: Main entrypoint containing global sidebar controls and top-level navigation.
* `views/`: Contains the specific Python files to render the 4 main application views:
  * `overview.py`: Geospatial Risk Mapping and High-level KPIs.
  * `deep_dive.py`: Province specific analysis, monthly trends, and damage breakdowns.
  * `priority_planner.py`: Budget simulation and actionable intervention checklists.
  * `trend_analyzer.py`: Multi-year forecasting and inter-province benchmarking.
* `data/`: Location for raw and processed datasets (CSV, GeoJSON).
* `utils/`: Helper functions and data ingestion logic.