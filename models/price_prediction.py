import streamlit as st
import pickle
import numpy as np
import pandas as pd

# -----------------------------------
# 1. PAGE CONFIG
# -----------------------------------
st.set_page_config(page_title="GARMANDI | Predictor", page_icon="💰", layout="wide")

# -----------------------------------
# 2. PREMIUM UI CSS
# -----------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Source+Code+Pro&family=Outfit:wght@300;600&display=swap');

[data-testid="stAppViewContainer"] {
    background: #020202;
    background-image: radial-gradient(circle at 2% 2%, #0a1a15 0%, #000 100%);
}

.main-title {
    font-family: 'Cinzel', serif;
    font-size: 3.2rem;
    text-align: center;
    background: linear-gradient(180deg, #FFFFFF 0%, #D4AF37 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 12px;
}

.terminal-label {
    font-family: 'Source Code Pro', monospace;
    color: #D4AF37;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    text-align: center;
}

.valuation-card {
    background: rgba(212,175,55,0.04);
    border: 2px solid rgba(212,175,55,0.4);
    padding: 50px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 0 50px rgba(212,175,55,0.15);
    margin-top: 30px;
}

header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# 3. LOAD PICKLES
# -----------------------------------
@st.cache_resource
def load_models():
    with open("d.pkl", "rb") as f:
        df = pickle.load(f)
    with open("pipelin.pkl", "rb") as f:
        pipeline = pickle.load(f)
    return df, pipeline

df, pipeline = load_models()

# -----------------------------------
# 4. HEADER
# -----------------------------------
st.markdown('<p class="terminal-label">// NEURAL VALUATION MODULE</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">PRICE PREDICTOR</h1>', unsafe_allow_html=True)
st.markdown("<hr style='border:0.5px solid rgba(212,175,55,0.15);'>", unsafe_allow_html=True)

# -----------------------------------
# 5. INPUT UI
# -----------------------------------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<p class='terminal-label'>Structure & Location</p>", unsafe_allow_html=True)
    property_type = st.selectbox("🏠 Property Type", df['property_type'].unique())
    sector = st.selectbox("📍 Sector", sorted(df['sector'].unique()))
    bedRoom = st.selectbox("🛏 Bedrooms", sorted(df['bedRoom'].unique()))
    bathroom = st.selectbox("🚿 Bathrooms", sorted(df['bathroom'].unique()))
    balcony = st.selectbox("🏖 Balcony", df['balcony'].unique())
    agePossession = st.selectbox("⌛ Property Age", df['agePossession'].unique())

with col2:
    st.markdown("<p class='terminal-label'>Dimensions & Amenities</p>", unsafe_allow_html=True)
    built_up_area = st.number_input("📐 Built-up Area (sq.ft.)", 100.0, 20000.0, 1200.0)
    servant_room = st.selectbox("🧹 Servant Room", [0.0, 1.0])
    store_room = st.selectbox("📦 Store Room", [0.0, 1.0])
    furnishing_type = st.selectbox("🪑 Furnishing Type", df['furnishing_type'].unique())
    luxury_category = st.selectbox("💎 Luxury Category", df['luxury_category'].unique())
    floor_category = st.selectbox("🏢 Floor Category", df['floor_category'].unique())

# -----------------------------------
# 6. PREDICTION
# -----------------------------------
if st.button("🔮 GENERATE VALUATION REPORT", use_container_width=True):

    input_df = pd.DataFrame([{
        'property_type': str(property_type),
        'sector': str(sector),
        'bedRoom': float(bedRoom),
        'bathroom': float(bathroom),
        'balcony': str(balcony),
        'agePossession': str(agePossession),
        'built_up_area': float(built_up_area),
        'servant room': float(servant_room),
        'store room': float(store_room),
        'furnishing_type': str(furnishing_type),
        'luxury_category': str(luxury_category),
        'floor_category': str(floor_category)
    }])

    # 🔒 Force categorical columns
    cat_cols = [
        'property_type','sector','balcony','agePossession',
        'furnishing_type','luxury_category','floor_category'
    ]
    input_df[cat_cols] = input_df[cat_cols].astype("object")

    try:
        prediction = pipeline.predict(input_df)
        price = prediction[0]

        st.markdown(f"""
        <div class="valuation-card">
            <p class="terminal-label">Valuation Successful</p>
            <h2 style="color:white;font-family:Outfit;font-weight:300;">ESTIMATED MARKET VALUE</h2>
            <h1 style="color:#D4AF37;font-family:Cinzel;font-size:4.5rem;">
                ₹ {price:.2f} Cr
            </h1>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Computation Error: {e}")

# -----------------------------------
# 7. DEBUG
# # -----------------------------------
# with st.expander("🔍 Debug"):
#     st.write(input_df)
#     st.write(input_df.dtypes)
