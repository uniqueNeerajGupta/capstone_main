import streamlit as st
import pickle

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(page_title="📍 Property Radius Search", page_icon="🏘️", layout="centered")

# -----------------------
# TITLE
# -----------------------
st.markdown(
    """
    <h1 style='text-align:center; color:#2E8B57;'>🏙️ Real Estate Radius Finder</h1>
    <p style='text-align:center; color:gray; font-size:16px;'>
        Find nearby properties based on your chosen location and radius.
    </p>
    <hr style='border: 1px solid #ddd;'>
    """,
    unsafe_allow_html=True
)

# -----------------------
# LOGIN CHECK
# -----------------------


# -----------------------
# LOAD PICKLE DATA
# -----------------------
with open('location_df.pkl', 'rb') as file:
    location_df = pickle.load(file)

# -----------------------
# USER INPUTS (Beautiful layout)
# -----------------------
st.markdown("<h3 style='color:#1E90FF;'>📍 Select Location and Radius</h3>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])
with col1:
    selected_location = st.selectbox(
        "🏠 Choose a location:",
        sorted(location_df.columns.tolist())
    )
with col2:
    radius = st.number_input("📏 Select radius (in kms):", min_value=0.0, max_value=50.0, step=0.5)

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------
# SEARCH BUTTON
# -----------------------
search_button = st.button("🔎 Search Nearby Properties")

# -----------------------
# RESULTS SECTION
# -----------------------
if search_button:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🏘️ Top Matching Properties")

    result_ser = (
        location_df[location_df['Gurgaon Railway Station'] < 4900.0]
        .sort_values(by='Bajghera Road')
        .head(5)
        .index
    )

    # -----------------------
    # DISPLAY AS BEAUTIFUL CARDS
    # -----------------------
    for idx, val in enumerate(result_ser, start=1):
        st.markdown(
            f"""
            <div style="
                background-color:#f9f9f9;
                padding:15px;
                margin-bottom:10px;
                border-radius:15px;
                box-shadow:0 2px 6px rgba(0,0,0,0.1);
                ">
                <h4 style="color:#2E8B57; margin:0;">🏠 {idx}. {val}</h4>
                <p style="color:gray; font-size:14px; margin:5px 0;">
                    📍 Within 5km radius of Gurgaon Railway Station
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.success("✅ Search completed successfully!")

else:
    st.info("👆 Select a location and radius, then click **Search Nearby Properties** to view results.")

# -----------------------
# FOOTER
# -----------------------
st.markdown(
    "<p style='text-align:center; color:gray; margin-top:50px;'>✨ Designed by Neeraj — Real Estate Data Explorer</p>",
    unsafe_allow_html=True
)