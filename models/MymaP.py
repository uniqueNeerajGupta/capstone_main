import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="GARMANDI | Visualizer", page_icon="🏘️", layout="wide")

# --- GARMANDI UI INJECTION ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Outfit:wght@300;600&display=swap');
    [data-testid="stAppViewContainer"] {
        background: #020202;
        background-image: radial-gradient(circle at 2% 2%, #0a1a15 0%, #000 100%);
    }
    .main-title {
        font-family: 'Cinzel', serif; font-size: 3rem; text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #D4AF37 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 10px;
    }
    h3 { color: #D4AF37 !important; font-family: 'Outfit', sans-serif; letter-spacing: 2px; margin-top: 30px;}
    .metric-card {
        background: rgba(212, 175, 55, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.2);
        padding: 20px; border-radius: 10px; text-align: center;
    }
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# DATA LOADING
# -----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('data_viz1.csv', index_col=0) 
    df_new = pd.read_csv('gurgaon_properties_missing_value_imputation.csv', index_col=0)
    cols = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    return df, df_new

df, df_new = load_data()

# --- SIDEBAR FILTERS (New UI Element) ---
st.sidebar.markdown("<h2 style='color:#D4AF37; font-family:Cinzel;'>FILTERS</h2>", unsafe_allow_html=True)
sector_list = ['All'] + sorted(df['sector'].unique().tolist())
selected_sector = st.sidebar.selectbox("Select Sector", sector_list)

if selected_sector != 'All':
    df = df[df['sector'] == selected_sector]

# -----------------------------------
# PAGE HEADER
# -----------------------------------
st.markdown('<h1 class="main-title">GEOSPATIAL CORE</h1>', unsafe_allow_html=True)

# --- TOP METRICS (New UI Element) ---
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"<div class='metric-card'><p style='color:gray;margin:0;'>TOTAL ASSETS</p><h2 style='color:white;margin:0;'>{len(df)}</h2></div>", unsafe_allow_html=True)
with m2:
    st.markdown(f"<div class='metric-card'><p style='color:gray;margin:0;'>AVG. PRICE</p><h2 style='color:#D4AF37;margin:0;'>₹{df['price'].mean():.2f} Cr</h2></div>", unsafe_allow_html=True)
with m3:
    st.markdown(f"<div class='metric-card'><p style='color:gray;margin:0;'>AVG. SQFT RATE</p><h2 style='color:white;margin:0;'>₹{df['price_per_sqft'].mean():,.0f}</h2></div>", unsafe_allow_html=True)

st.markdown("<hr style='border: 0.5px solid rgba(212,175,55,0.2);'>", unsafe_allow_html=True)

# -----------------------------------
# 1️⃣ Average Prices by Sector
# -----------------------------------
st.markdown("### 📊 Average Property Metrics by Sector")

cols_to_group = ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']
group_df = df.groupby('sector')[cols_to_group].mean().reset_index()

fig = px.scatter_mapbox(
    group_df, lat="latitude", lon="longitude",
    color="price_per_sqft", size="built_up_area",
    color_continuous_scale="Viridis", 
    zoom=10, mapbox_style="carto-darkmatter",
    hover_name="sector",
    hover_data={"price": True, "price_per_sqft": True, "built_up_area": True}
)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# 2️⃣ Property Price Distribution (FIXED COLOR SCALE)
# -----------------------------------
st.markdown("### 💰 Property Price Distribution")

fig1 = px.scatter_mapbox(
    df, lat="latitude", lon="longitude",
    color="price", size="built_up_area",
    color_continuous_scale="YlOrBr", # FIXED ERROR HERE
    hover_name="sector", mapbox_style="carto-darkmatter",
    zoom=10
)
fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------------
# 3️⃣ Heatmap
# -----------------------------------
st.markdown("### 🔥 Price Density Heatmap")
sector_avg = df.groupby('sector')[['price_per_sqft', 'latitude', 'longitude']].mean().reset_index()

fig2 = px.density_mapbox(
    sector_avg, lat='latitude', lon='longitude', z='price_per_sqft',
    radius=30, mapbox_style="carto-darkmatter",
    color_continuous_scale="Inferno", zoom=10
)
fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------
# 4️⃣ Raw Map
# -----------------------------------
st.markdown("### 🗺️ All Property Locations")
st.map(df)

# -----------------------------------
# FOOTER
# -----------------------------------
st.markdown("<br><hr style='opacity:0.1;'><p style='text-align:center; color:gray;'>✨ GARMANDI DATA ENGINE | NEERAJ</p>", unsafe_allow_html=True)