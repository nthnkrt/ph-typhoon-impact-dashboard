import pandas as pd
from fpdf import FPDF
import io

def generate_global_pdf_report(df: pd.DataFrame, region: str, years: tuple, dpwh_context: str = "") -> bytes:
    """
    Generates a high-level Comprehensive Executive Summary PDF for the entire dashboard view.
    Includes granular damage subsets (agri, infra, housing), the severity factor, and the worst-hit provinces.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="Typhoon Socio-Economic Impact - Executive Summary", ln=True, align='C')
    pdf.ln(5)
    
    # Data Validation / Completeness Context
    unique_provinces = df['province'].nunique() if not df.empty and 'province' in df.columns else 0
    total_records = len(df)
    
    # Metadata Block
    pdf.set_font("Arial", 'I', 11)
    pdf.cell(0, 6, txt=f"Geography: {region} (Covers {unique_provinces} unique provinces / {total_records} impact records)", ln=True)
    pdf.cell(0, 6, txt=f"Timeframe: {years[0]} - {years[1]}", ln=True)
    if dpwh_context:
        pdf.cell(0, 6, txt=f"Administrative Context: {dpwh_context}", ln=True)
    pdf.ln(8)
    
    # Ensure columns exist safely
    casualties = int(df.get('dead', 0).sum() + df.get('injured/ill', 0).sum() + df.get('missing', 0).sum())
    affected_fam = int(df.get('affected_families', 0).sum())
    
    total_cost = df.get('cost_total', 0).sum()
    agri_cost = df.get('cost_agri', 0).sum()
    infra_cost = df.get('cost_infra', 0).sum()
    house_cost = df.get('cost_house', 0).sum()
    
    # Calculate Severity Factor (Cost per Affected Family)
    # Hsiang & Anttila-Hughes (2014) dictates severity of typhoon based on micro-economic loss
    severity_factor = total_cost / affected_fam if affected_fam > 0 else 0.0
    
    # ---------------------------------------------------------
    # Humanitarian Aggregates Section
    # ---------------------------------------------------------
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Humanitarian Impact Overview", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 7, txt=f"Total Casualties (Dead/Injured/Missing): {casualties:,}", ln=True)
    pdf.cell(0, 7, txt=f"Total Affected Families: {affected_fam:,}", ln=True)
    pdf.ln(4)
    
    # ---------------------------------------------------------
    # Economic Breakdown & Severity Section
    # ---------------------------------------------------------
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Economic Loss & Sub-Sector Breakdown", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 7, txt=f"Cumulative Economic Loss: PHP {total_cost:,.2f}", ln=True)
    
    # Indented Sub-breakdowns
    pdf.set_font("Arial", '', 11)
    pdf.cell(10) # Indent
    pdf.cell(0, 6, txt=f"- Infrastructure Damage: PHP {infra_cost:,.2f}", ln=True)
    pdf.cell(10)
    pdf.cell(0, 6, txt=f"- Agricultural Damage: PHP {agri_cost:,.2f}", ln=True)
    pdf.cell(10)
    pdf.cell(0, 6, txt=f"- Housing Damage: PHP {house_cost:,.2f}", ln=True)
    
    pdf.ln(4)
    
    # The Severity Factor Policy Note
    pdf.set_font("Arial", 'BI', 12)
    pdf.cell(0, 8, txt=f"Calculated Severity Factor: PHP {severity_factor:,.2f} per Affected Family", ln=True)
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 5, txt="* Note: High severity factors indicate severe household-level financial burdens that historically lead to long-term community poverty (Hsiang & Anttila-Hughes). Priority interventions are recommended here.", align='L')
    pdf.ln(8)
    
    # ---------------------------------------------------------
    # Top 5 Most Devastated Provinces Segment
    # ---------------------------------------------------------
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, txt="Top 5 Most Devastated Provinces (By Total Economic Loss)", ln=True)
    
    if not df.empty:
        # Group geographically
        prov_summary = df.groupby('province')['cost_total'].sum().sort_values(ascending=False).head(5)
        pdf.set_font("Arial", '', 11)
        
        for rank, (prov_name, cost) in enumerate(prov_summary.items(), 1):
            if cost > 0:
                pdf.cell(0, 7, txt=f"{rank}. {prov_name} - PHP {cost:,.2f}", ln=True)
            else:
                pdf.cell(0, 7, txt=f"{rank}. {prov_name} - No Economic Data", ln=True)
    else:
        pdf.set_font("Arial", 'I', 11)
        pdf.cell(0, 7, txt="No province data available for this criteria.", ln=True)
        
    pdf.ln(12)
    
    # Footer Stamp
    pdf.set_font("Arial", 'I', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, txt="* Generated automatically by the Philippine Typhoon Impact Dashboard.", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')
