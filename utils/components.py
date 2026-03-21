import streamlit as st

def render_chart_placeholder(height: int, text: str):
    """
    Renders a designed placeholder container to indicate where data visualizations will go.
    Makes it cleaner and easier to replace later with `st.plotly_chart`.
    """
    with st.container(border=True, height=height):
        # We use a markdown with custom class (requires custom css to be loaded)
        st.markdown(f'<div class="chart-placeholder" style="height: {height-40}px;">{text}</div>', unsafe_allow_html=True)
