import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Modern font & generic styles */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            color: #E2E8F0; /* Tailwind slate-200 */
        }

        /* Metric styling for premium look */
        div[data-testid="stMetric"] {
            background-color: #1E293B; /* Tailwind slate-800 */
            border-radius: 8px;
            padding: 16px 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid #334155; /* Tailwind slate-700 */
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            border-color: #3B82F6; /* Tailwind blue-500 */
        }

        /* Value color */
        div[data-testid="stMetricValue"] {
            font-size: 2.2rem;
            font-weight: 700;
            color: #F8FAFC; /* Tailwind slate-50 */
        }

        div[data-testid="stMetricLabel"] {
            font-size: 0.9rem;
            font-weight: 500;
            color: #94A3B8; /* Tailwind slate-400 */
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Cleaner Tabs padding */
        .stTabs [data-baseweb="tab-list"] {
            gap: 16px;
            padding: 8px 0;
            border-bottom: 1px solid #334155;
        }

        .stTabs [data-baseweb="tab"] {
            height: 48px;
            white-space: pre-wrap;
            border-radius: 6px 6px 0 0;
            padding-top: 10px;
            padding-bottom: 10px;
            font-weight: 500;
            color: #94A3B8;
            transition: color 0.15s ease, background-color 0.15s ease;
        }

        .stTabs [aria-selected="true"] {
            background-color: transparent;
            color: #3B82F6 !important;
            border-bottom: 2px solid #3B82F6 !important;
        }
        
        /* Placeholder styling class for charts */
        .chart-placeholder {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            width: 100%;
            background-color: #0F172A; /* Tailwind slate-900 */
            border-radius: 8px;
            border: 1px dashed #475569; /* Tailwind slate-600 */
            padding: 24px;
            color: #64748B; /* Tailwind slate-500 */
            font-size: 1.1rem;
            font-weight: 500;
            text-align: center;
        }

        /* Expander headers */
        .streamlit-expanderHeader {
            font-weight: 600;
            color: #E2E8F0;
        }
        
        /* General inputs and buttons styling overrides for a more cohesive look */
        .stButton button {
            border-radius: 6px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        </style>
    """, unsafe_allow_html=True)
