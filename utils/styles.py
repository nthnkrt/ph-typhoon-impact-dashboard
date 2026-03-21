import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Modern font & generic styles */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Inter', sans-serif;
        }

        /* Metric styling for premium look */
        div[data-testid="stMetric"] {
            background-color: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 15px 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Value color */
        div[data-testid="stMetricValue"] {
            font-size: 2.2rem;
            font-weight: 700;
        }

        /* Cleaner Tabs padding */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            padding: 10px 0;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        }

        .stTabs [data-baseweb="tab"] {
            height: 48px;
            white-space: pre-wrap;
            border-radius: 6px 6px 0 0;
            padding-top: 10px;
            padding-bottom: 10px;
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(255, 255, 255, 0.08);
            border-bottom-color: #4CAF50 !important;
        }
        
        /* Placeholder styling class for charts */
        .chart-placeholder {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            border: 1px dashed rgba(255, 255, 255, 0.2);
            padding: 24px;
            color: rgba(255, 255, 255, 0.7);
            font-size: 1.1rem;
            font-weight: 500;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
