import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Irish Agri-Food Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    trade_balance = pd.read_csv('trade_balance_ie.csv')
    cap_eff       = pd.read_csv('cap_eff.csv')
    merged_export = pd.read_csv('merged_export_1.csv')
    eu_ml         = pd.read_csv('eu_exports_interpolated.csv')
    return trade_balance, cap_eff, merged_export, eu_ml

trade_balance_ie, cap_eff, merged_export_1, eu_ml_interpolated = load_data()

with st.sidebar:
    st.title('Irish Agri-Food Dashboard')
    st.markdown('---')
    year_list = sorted(merged_export_1['Year'].unique(), reverse=True)
    selected_year = st.selectbox('Select Year', year_list)
    country_list = sorted([c for c in merged_export_1['Country'].unique() if c != 'Ireland'])
    selected_country = st.selectbox('Compare Ireland with:', country_list,
                                    index=country_list.index('Germany') if 'Germany' in country_list else 0)
    st.markdown('---')
    st.markdown('''
    **Data Sources:**
    - CSO Ireland (TSM10)
    - Eurostat Agricultural Trade
    - EU Budget 2000–2024

    **Student:** 2026004
    **CCT College Dublin**
    ''')

st.markdown("### Ireland Agricultural Sector Overview")

ie_year = merged_export_1[(merged_export_1['Country'] == 'Ireland') & (merged_export_1['Year'] == selected_year)]
ie_prev = merged_export_1[(merged_export_1['Country'] == 'Ireland') & (merged_export_1['Year'] == selected_year - 1)]

col_kpi = st.columns(4)
with col_kpi[0]:
    val  = float(ie_year['Export Value (EUR Million)'].values[0]) if len(ie_year) > 0 else 0
    prev = float(ie_prev['Export Value (EUR Million)'].values[0]) if len(ie_prev) > 0 else 0
    st.metric('Export Value', f'€{val:,.0f}M', f'{val-prev:+.0f}M vs prev year')
with col_kpi[1]:
    cap = float(ie_year['CAP Budget (EUR Million)'].values[0]) if len(ie_year) > 0 else 0
    st.metric('CAP Budget', f'€{cap:,.0f}M')
with col_kpi[2]:
    eff = float(ie_year['CAP Efficiency'].values[0]) if len(ie_year) > 0 else 0
    st.metric('CAP Efficiency', f'{eff:.2f}x', '€ exported per €1 CAP')
with col_kpi[3]:
    tb = trade_balance_ie[trade_balance_ie['Year'] == selected_year]['Balance (Euro Million)'].sum()
    st.metric('Total Trade Balance', f'€{tb:,.0f}M')

st.markdown('---')

col1, col2 = st.columns(2)
with col1:
    st.markdown('#### Trade Balance by Country')
    fig_tb = px.choropleth(
        trade_balance_ie[trade_balance_ie['Year'] == selected_year],
        locations='Countries and Territories',
        locationmode='country names',
        color='Balance (Euro Million)',
        scope='europe',
        color_continuous_scale='RdYlGn',
        title=f"Ireland's Agricultural Trade Balance {selected_year}"
    )
    fig_tb.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=380)
    st.plotly_chart(fig_tb, use_container_width=True)

with col2:
    st.markdown('#### CAP Efficiency by Country')
    fig_cap = px.choropleth(
        cap_eff[cap_eff['Year'] == selected_year],
        locations='Country',
        locationmode='country names',
        color='CAP Efficiency',
        scope='europe',
        color_continuous_scale='RdYlGn',
        title=f'CAP Efficiency {selected_year}'
    )
    fig_cap.update_layout(margin=dict(l=0, r=0, t=40, b=0), height=380)
    st.plotly_chart(fig_cap, use_container_width=True)

st.markdown('---')

st.markdown(f'#### Ireland vs {selected_country} — CAP Budget & Export Value')
ireland_data = merged_export_1[merged_export_1['Country'] == 'Ireland']
country_data = merged_export_1[merged_export_1['Country'] == selected_country]

fig_comp = make_subplots(specs=[[{"secondary_y": True}]])
fig_comp.add_trace(go.Scatter(x=ireland_data['Year'], y=ireland_data['CAP Budget (EUR Million)'],
    name='Ireland — CAP', mode='lines+markers', line=dict(color='#1D9E75', width=2)), secondary_y=False)
fig_comp.add_trace(go.Scatter(x=ireland_data['Year'], y=ireland_data['Export Value (EUR Million)'],
    name='Ireland — Exports', mode='lines+markers', line=dict(color='#1D9E75', width=2, dash='dot')), secondary_y=True)
fig_comp.add_trace(go.Scatter(x=country_data['Year'], y=country_data['CAP Budget (EUR Million)'],
    name=f'{selected_country} — CAP', mode='lines+markers', line=dict(color='#7F77DD', width=2)), secondary_y=False)
fig_comp.add_trace(go.Scatter(x=country_data['Year'], y=country_data['Export Value (EUR Million)'],
    name=f'{selected_country} — Exports', mode='lines+markers', line=dict(color='#7F77DD', width=2, dash='dot')), secondary_y=True)
fig_comp.add_vline(x=2020, line_dash='dot', line_color='gray', annotation_text='COVID / Brexit')
fig_comp.update_yaxes(title_text='CAP Budget (€M)', secondary_y=False)
fig_comp.update_yaxes(title_text='Export Value (€M)', secondary_y=True)
fig_comp.update_layout(height=420, plot_bgcolor='white', yaxis=dict(gridcolor='rgba(0,0,0,0.05)'))
st.plotly_chart(fig_comp, use_container_width=True)
