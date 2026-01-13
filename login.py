import streamlit as st
import time

# --- 1. SYSTEM ARCHITECTURE & CONFIG ---
st.set_page_config(
    page_title="GARMANDI | Institutional Real Estate OS",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THE ELITE DESIGN SYSTEM (CSS) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;900&family=Outfit:wght@100;300;400;700&display=swap');

    /* Global Atmosphere */
    [data-testid="stAppViewContainer"] {
        background-color: #020202;
        background-image: radial-gradient(circle at 2% 2%, #0a1a15 0%, #000 100%);
        color: #ffffff;
    }

    /* Branding & Typography */
    .garmandi-title {
        font-family: 'Cinzel', serif;
        font-size: 6.5rem;
        font-weight: 900;
        letter-spacing: 25px;
        text-align: center;
        background: linear-gradient(180deg, #FFFFFF 0%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 50px;
        margin-bottom: 0px;
    }

    .sub-heading {
        font-family: 'Outfit', sans-serif;
        text-align: center;
        color: #D4AF37;
        letter-spacing: 10px;
        font-size: 0.8rem;
        text-transform: uppercase;
        margin-bottom: 60px;
        opacity: 0.8;
    }

    /* 3D Module Cards */
    .module-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(212, 175, 55, 0.1);
        padding: 35px;
        border-radius: 4px;
        height: 420px;
        transition: 0.5s cubic-bezier(0.19, 1, 0.22, 1);
        backdrop-filter: blur(10px);
    }

    .module-card:hover {
        background: rgba(212, 175, 55, 0.08);
        border-color: #D4AF37;
        transform: translateY(-15px) perspective(1000px) rotateX(5deg);
        box-shadow: 0 25px 50px rgba(0,0,0,0.8);
    }

    .icon-box { font-size: 2.5rem; margin-bottom: 20px; }
    .feature-title { font-family: 'Cinzel', serif; color: #FFFFFF; font-size: 1.1rem; letter-spacing: 2px; margin-bottom: 15px; }
    .feature-desc { font-family: 'Outfit', sans-serif; color: rgba(255,255,255,0.6); font-size: 0.85rem; line-height: 1.7; }

    /* Buttons */
    .stButton>button {
        background: transparent;
        border: 1px solid rgba(212, 175, 55, 0.4);
        color: #D4AF37;
        font-family: 'Outfit', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 3px;
        border-radius: 0;
        width: 100%;
        margin-top: 20px;
        transition: 0.4s;
    }
    .stButton>button:hover { background: #D4AF37; color: black; border-color: #D4AF37; }

    /* Utility */
    header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. NAVIGATION ---
# Note: Ensure these files exist in your 'pages/' directory
pages = {
    "Dashboard": [st.Page("login.py", title="Executive Terminal", icon="💠", default=True)],
    "Intelligence": [
        st.Page("models/price_prediction.py", title="Valuation Engine"),
        st.Page("models/location.py", title="Locality IQ"),
        st.Page("models/Real Estate Recommender.py", title="Asset Matcher"),
        st.Page("models/Analysis.py", title="Market Pulse"),
        st.Page("models/MymaP.py", title="GIS Spatial"),
        st.Page("models/flora.py", title="Flora AI")
    ]
}
pg = st.navigation(pages)

if pg.title == "Executive Terminal":
    
    # --- HERO SECTION ---
    st.markdown('<h1 class="garmandi-title">GARMANDI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-heading">Neural Real Estate Intelligence v4.2</p>', unsafe_allow_html=True)

    # --- LIVE STATS BAR ---
    s1, s2, s3, s4 = st.columns(4)
    with s1: st.metric(label="Total Asset Liquidity", value="$1.4B", delta="12%")
    with s2: st.metric(label="Valuation Accuracy", value="99.1%", delta="0.4%")
    with s3: st.metric(label="Active Neural Nodes", value="1,024")
    with s4: st.metric(label="Market Sentiment", value="BULLISH", delta="High")

    st.markdown("<br><hr style='opacity:0.1;'><br>", unsafe_allow_html=True)

    # --- 6 FEATURES GRID (The Content) ---
    features = [
        {
            "name": "Valuation Engine", "icon": "💎", "path": "pages/price_prediction.py",
            "desc": "Proprietary neural networks crunching 15+ years of transaction data to predict future price appreciation with institutional precision."
        },
        {
            "name": "Locality Alpha", "icon": "🛰️", "path": "pages/location.py",
            "desc": "Beyond postcodes. We track gentrification, infrastructure pipeline, and social migration to find the next billion-dollar neighborhood."
        },
        {
            "name": "Asset Matcher", "icon": "🎯", "path": "pages/Real Estate Recommender.py",
            "desc": "Tailored acquisition logic. Align your capital deployment with assets that match your specific risk-profile and liquidity timelines."
        },
        {
            "name": "Market Pulse", "icon": "📈", "path": "pages/Analysis.py",
            "desc": "High-frequency data streams. Monitor supply-demand imbalances and absorption rates in the Mumbai & Tier-1 markets in real-time."
        },
        {
            "name": "Spatial Mapping", "icon": "🗺️", "path": "pages/MymaP.py",
            "desc": "Interactive 3D GIS environment. Visualize catchment areas, transit-oriented development impact, and satellite-verified land parcels."
        },
        {
            "name": "Flora AI Partner", "icon": "🎙️", "path": "pages/flora.py",
            "desc": "Our custom Large Language Model. A virtual investment partner capable of complex portfolio reasoning and instant market reports."
        }
    ]

    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            if idx < len(features):
                f = features[idx]
                with cols[j]:
                    st.markdown(f"""
                        <div class="module-card">
                            <div class="icon-box">{f['icon']}</div>
                            <div class="feature-title">{f['name'].upper()}</div>
                            <div class="feature-desc">{f['desc']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"INITIALIZE {f['name'].split()[0].upper()}", key=f['path']):
                        st.switch_page(f['path'])

    # --- ABOUT & ROBOT SECTION ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col_img, col_text = st.columns([1, 1.2])

    with col_img:
        st.markdown('<div style="padding:10px; border:1px solid #D4AF37; border-radius:20px;">', unsafe_allow_html=True)
        st.image("https://img.freepik.com/free-photo/view-futuristic-robot-working-office_23-2150841517.jpg", 
                 caption="FLORA CORE v4.2 - SECURE")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_text:
        st.markdown("""
            <h2 style='font-family:Cinzel; color:white; letter-spacing:3px;'>The Architect’s Vision</h2>
            <p style='font-family:Outfit; color:rgba(255,255,255,0.7); line-height:1.8;'>
                Garmandi isn't just a platform; it's a <b>Financial Terminal for Physical Assets</b>. 
                We believe that Real Estate investment has been opaque for too long. By merging 
                Satellite Intelligence with Neural Processing, we provide our clients the 
                'unfair advantage' needed in today's volatile markets.
                <br><br>
                Whether you are looking for institutional land parcels or high-yield residential 
                portfolios, Garmandi provides the <b>Alpha Signal</b> you've been missing.
            </p>
        """, unsafe_allow_html=True)
        if st.button("CONNECT TO NEURAL ADVISORY"):
            st.switch_page("pages/flora.py")

    # --- FOOTER ---
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align:center; padding:40px; background:rgba(212,175,55,0.03); border-top:1px solid rgba(212,175,55,0.2);">
            <p style="color:#D4AF37; font-family:Cinzel; letter-spacing:5px; font-size:0.8rem;">GARMANDI • GENEVA • MUMBAI • DUBAI</p>
            <p style="color:rgba(255,255,255,0.3); font-family:Outfit; font-size:0.7rem;">© 2026 GARMANDI QUANTITATIVE REAL ESTATE. ALL RIGHTS RESERVED.</p>
        </div>
    """, unsafe_allow_html=True)

else:
    pg.run()
