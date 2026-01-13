import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# --- 1. PAGE CONFIG (Consistent with Main Site) ---
st.set_page_config(page_title="GARMANDI | Market Pulse", layout="wide", initial_sidebar_state="collapsed")

# --- 2. GARMANDI LUXURY STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Outfit:wght@300;600&display=swap');

    [data-testid="stAppViewContainer"] {
        background: #020202;
        background-image: radial-gradient(circle at 2% 2%, #0a1a15 0%, #000 100%);
    }

    .analysis-header {
        font-family: 'Cinzel', serif;
        font-size: 3rem;
        letter-spacing: 10px;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }

    /* Metric Cards */
    [data-testid="stMetricValue"] { color: #D4AF37 !important; font-family: 'Outfit'; font-size: 2rem !important; }
    [data-testid="stMetricLabel"] { color: rgba(255,255,255,0.6) !important; letter-spacing: 2px; }

    /* Glass Panels for Charts */
    .chart-container {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(212, 175, 55, 0.1);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. DATA ENGINE ---
@st.cache_data
def load_data():
    df = pd.read_csv('gurgaon_properties_missing_value_imputation.csv', index_col=0)
    num_cols = ['price','price_per_sqft','built_up_area','luxury_score','bedRoom','bathroom']
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    return df, num_cols

df, num_cols = load_data()

# --- 4. HEADER ---
st.markdown('<h1 class="analysis-header">MARKET PULSE</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#D4AF37; letter-spacing:5px; font-size:0.7rem; margin-bottom:40px;">// REAL-TIME SECTOR INTELLIGENCE</p>', unsafe_allow_html=True)

# --- 5. TOP HUD (FILTERS & KPI) ---
with st.container():
    col_f1, col_f2, col_f3, col_f4 = st.columns([1, 1, 1, 1])
    with col_f1:
        selected_sector = st.selectbox("🎯 TARGET SECTOR", sorted(df['sector'].dropna().unique()))
    
    filtered_df = df[df['sector'] == selected_sector]
    
    with col_f2:
        st.metric("AVG VALUATION", f"₹{filtered_df['price'].mean():.2f} Cr")
    with col_f3:
        st.metric("SQFT ALPHA", f"₹{filtered_df['price_per_sqft'].mean():,.0f}")
    with col_f4:
        st.metric("LUXURY INDEX", f"{filtered_df['luxury_score'].mean():.1f}/100")

st.markdown("<br>", unsafe_allow_html=True)

# --- 6. CHART STYLING OVERRIDE ---
def apply_dark_theme(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#cbd5e1",
        title_font_family="Cinzel",
        title_font_color="#D4AF37",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
    )
    return fig

# --- 7. TABS (The Garmandi Way) ---
tab1, tab2, tab3 = st.tabs(["🏛️ SECTOR OVERVIEW", "💎 LUXURY DYNAMICS", "📊 CORRELATION MATRIX"])

with tab1:
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        sector_avg = df.groupby('sector')['price'].mean().reset_index().sort_values('price', ascending=False).head(15)
        fig1 = px.bar(sector_avg, x='sector', y='price', title="TOP 15 SECTORS BY VALUATION",
                     color_continuous_scale=['#0a1a15', '#D4AF37'])
        st.plotly_chart(apply_dark_theme(fig1), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig2 = px.scatter(df, x='built_up_area', y='price', color='luxury_score',
                         title="AREA VS PRICE (COLOR: LUXURY SCORE)",
                         color_continuous_scale='Viridis')
        st.plotly_chart(apply_dark_theme(fig2), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fig4 = px.violin(df, x='bedRoom', y='luxury_score', color='bedRoom', box=True,
                    title="BEDROOM COUNT VS LUXURY SCORE DISTRIBUTION")
    st.plotly_chart(apply_dark_theme(fig4), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("Neural Connectivity Matrix")
    corr = df[num_cols].corr()
    
    fig_corr = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.index,
        y=corr.columns,
        colorscale=[[0, '#020202'], [0.5, '#0a3d31'], [1, '#D4AF37']],
        zmin=-1, zmax=1
    ))
    fig_corr.update_layout(height=500)
    st.plotly_chart(apply_dark_theme(fig_corr), use_container_width=True)

# --- FOOTER ---
st.markdown("<br><p style='text-align:center; color:rgba(212,175,55,0.3); font-size:0.7rem;'>GARMANDI QUANTITATIVE TERMINAL // AUTH_ID: NEERAJ_OS</p>", unsafe_allow_html=True)
