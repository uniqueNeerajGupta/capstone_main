import streamlit as st
import pickle
import pandas as pd

# -----------------------------------
# 1. PAGE CONFIG & GARMANDI THEME
# -----------------------------------
st.set_page_config(page_title="GARMANDI | Recommender", page_icon="🏘️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Source+Code+Pro:wght@400&family=Outfit:wght@300;600&display=swap');

[data-testid="stAppViewContainer"] {
    background: #020202;
    background-image: radial-gradient(circle at 2% 2%, #0a1a15 0%, #000 100%);
}

.main-title {
    font-family: 'Cinzel', serif; 
    font-size: 3rem; 
    text-align: center;
    background: linear-gradient(180deg, #FFFFFF 0%, #D4AF37 100%);
    -webkit-background-clip: text; 
    -webkit-text-fill-color: transparent;
    letter-spacing: 10px; 
    margin-bottom: 5px;
}

.asset-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(212, 175, 55, 0.2);
    border-left: 4px solid #D4AF37;
    padding: 20px; 
    border-radius: 8px;
    margin-bottom: 15px; 
    transition: 0.3s;
}
.asset-card:hover {
    background: rgba(212, 175, 55, 0.08);
    transform: translateX(10px);
}

.terminal-label {
    font-family: 'Source Code Pro', monospace; 
    color: #D4AF37; 
    font-size: 0.75rem; 
    letter-spacing: 2px;
}

header, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# 2. LOAD RECOMMENDER DATA
# -----------------------------------
@st.cache_resource
def load_recommender_data():
    try:
        with open("recommender_data.pkl", "rb") as file:
            return pickle.load(file)
    except Exception as e:
        st.error(f"Engine Offline: {e}")
        return None

data = load_recommender_data()

if data:
    cosine_sim1 = data["cosine_sim1"]
    cosine_sim2 = data["cosine_sim2"]
    cosine_sim3 = data["cosine_sim3"]
    location_df_normalized = data["location_df_normalized"]

    # -----------------------------------
    # 3. RECOMMENDATION LOGIC
    # -----------------------------------
    def recommend_properties_with_scores(property_name, top_n=10):
        cosine_sim_matrix = 30 * cosine_sim1 + 20 * cosine_sim2 + 8 * cosine_sim3
        idx = location_df_normalized.index.get_loc(property_name)
        sim_scores = list(enumerate(cosine_sim_matrix[idx]))
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
        top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
        top_properties = location_df_normalized.index[top_indices].tolist()

        return pd.DataFrame({
            'PropertyName': top_properties,
            'SimilarityScore': [round(score, 3) for score in top_scores]
        })

    # -----------------------------------
    # 4. HEADER & INPUTS
    # -----------------------------------
    st.markdown('<p class="terminal-label" style="text-align:center;">// CONTENT-BASED FILTERING UNIT</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">ASSET MATCH</h1>', unsafe_allow_html=True)
    st.markdown("<hr style='border: 0.5px solid rgba(212,175,55,0.1);'>", unsafe_allow_html=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        property_name = st.selectbox(
            "🏠 SELECT REFERENCE PROPERTY:",
            location_df_normalized.index.tolist()
        )
    with c2:
        top_n = st.select_slider("🔢 MATCH COUNT", options=range(3, 16), value=5)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔎 ANALYZE SIMILAR ASSETS", use_container_width=True):
        recommendations = recommend_properties_with_scores(property_name, top_n)

        st.markdown(f"### 🎯 Identification Complete: {top_n} Matches for {property_name}")
        
        # -----------------------------------
        # 5. DISPLAY AS ELITE TILES
        # -----------------------------------
        for i, row in recommendations.iterrows():
            match_pct = min(100, int((row['SimilarityScore'] / 58) * 100))
            st.markdown(
                f"""
                <div class="asset-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h4 style="color:white; margin:0; font-family:Outfit;">{row['PropertyName']}</h4>
                        <span style="color:#D4AF37; font-family:Source Code Pro;">{match_pct}% MATCH</span>
                    </div>
                    <div style="width: 100%; background: rgba(255,255,255,0.05); height: 4px; margin-top: 10px; border-radius: 2px;">
                        <div style="width: {match_pct}%; background: #D4AF37; height: 100%; border-radius: 2px;"></div>
                    </div>
                    <p style="color:gray; font-size:12px; margin-top: 8px;">Institutional Similarity Score: {row['SimilarityScore']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------
# 6. FOOTER
# -----------------------------------
st.markdown("<br><hr style='opacity:0.1;'><p style='text-align:center; color:rgba(212,175,55,0.2); font-size:0.7rem;'>GARMANDI RECOMMENDATION UNIT © 2026</p>", unsafe_allow_html=True)
