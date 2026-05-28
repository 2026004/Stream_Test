# dashboard_ca2.py
# Basado en: streamlit_app.py y uber.py (Prof. David McQuaid, CCT)
# Referencia: https://docs.streamlit.io/

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#######################
# Page configuration
st.set_page_config(
    page_title="🇮🇪 Irish Agri-Food Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

#######################
# Load data desde GitHub raw
# Basado en patrón de uber.py del profesor:
# DATA_URL = ('https://s3-us-west-2.amazonaws.com/...')

BASE_URL = 'https://github.com/2026004/Stream_Test'


@st.cache_data
def load_data():
    trade_balance = pd.read_csv(BASE_URL + 'trade_balance_ie.csv')
    cap_eff = pd.read_csv(BASE_URL + 'cap_eff.csv')
    merged_export = pd.read_csv(BASE_URL + 'merged_export_1.csv')
    eu_ml = pd.read_csv(BASE_URL + 'eu_exports_interpolated.csv')
    return trade_balance, cap_eff, merged_export, eu_ml


trade_balance_ie, cap_eff, merged_export_1, eu_ml_interpolated = load_data()

#######################
# Sidebar
with st.sidebar:
    st.title('🌾 Irish Agri-Food Dashboard')
    st.markdown('---')

    year_list = sorted(merged_export_1['Year'].unique(), reverse=True)
    selected_year = st.selectbox('Select Year', year_list)

    country_list = sorted([c for c in merged_export_1['Country'].unique()
                           if c != 'Ireland'])
    selected_country = st.selectbox('Compare Ireland with:', country_list,
                                    index=country_list.index('Germany')
                                    if 'Germany' in country_list else 0)
    st.markdown('---')
    st.markdown('''
    **Data Sources:**
    - CSO Ireland (TSM10)
    - Eurostat Agricultural Trade
    - EU Budget 2000–2024

    **Student:** 2026004  
    **CCT College Dublin**
    ''')

#######################
# KPIs — mismo patrón st.metric() de streamlit_app.py del profesor
st.markdown("### 🇮🇪 Ireland Agricultural Sector Overview")

ie_year = merged_export_1[
    (merged_export_1['Country'] == 'Ireland') &
    (merged_export_1['Year'] == selected_year)]
ie_prev = merged_export_1[
    (merged_export_1['Country'] == 'Ireland') &
    (merged_export_1['Year'] == selected_year - 1)]

col_kpi = st.columns(4)

with col_kpi[0]:
    val = ie_year['Export Value (EUR Million)'].values[0] if len(ie_year) > 0 else 0
    prev = ie_prev['Export Value (EUR Million)'].values[0] if len(ie_prev) > 0 else 0
