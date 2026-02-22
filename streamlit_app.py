import streamlit as st
import pandas as pd
import os
from phase2.recommender_core import filter_restaurants
from phase4.ranking_engine import rank_restaurants
from phase3.llm_engine import RecommendationEngine

# Set Page Config
st.set_page_config(page_title="Zomato AI Recommender", page_icon="🍴", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Exact Next.js Replication
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    :root {
        --zomato-red: #EF4F5F;
    }

    /* Global Body Styling */
    .stApp {
        font-family: 'Outfit', sans-serif !important;
        background-color: #fff;
    }

    /* Hide Streamlit Header and Footer */
    header, footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Navbar Replication */
    .navbar-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 10%;
        background: white;
        position: sticky;
        top: 0;
        z-index: 1000;
        border-bottom: 1px solid #e8e8e8;
    }

    .nav-logo {
        height: 28px;
    }

    .nav-links {
        display: flex;
        gap: 30px;
        color: #696969;
        font-size: 18px;
        font-weight: 400;
    }

    /* Hero Section Replication */
    .hero-section {
        position: relative;
        height: 420px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        text-align: center;
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
    }

    .hero-logo {
        width: 300px;
        margin-bottom: 20px;
        filter: brightness(0) invert(1);
    }

    .hero-tagline {
        font-size: 36px;
        font-weight: 400;
        margin-bottom: 32px;
    }

    /* Floating Recommender Card */
    .recommender-card-wrapper {
        max-width: 1100px;
        margin: -40px auto 40px auto;
        padding: 0 20px;
        position: relative;
        z-index: 100;
    }

    .recommender-card {
        background: white;
        padding: 32px;
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        border: 1px solid #eee;
    }

    .card-title {
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--zomato-red);
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 24px;
    }

    /* Category Cards */
    .cat-container {
        display: flex;
        gap: 20px;
        padding: 40px 10%;
        margin-bottom: 40px;
    }

    .cat-card {
        flex: 1;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e8e8e8;
        background: white;
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .cat-card:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    .cat-img {
        height: 160px;
        background-size: cover;
        background-position: center;
    }

    .cat-content {
        padding: 12px 20px;
    }

    .cat-title {
        font-size: 20px;
        font-weight: 500;
        color: #1c1c1c;
    }

    .cat-subtitle {
        font-size: 14px;
        color: #4f4f4f;
        margin-top: 4px;
    }

    /* Recommendation Results */
    .res-container {
        padding: 0 10% 80px 10%;
    }

    .res-grid {
        display: flex;
        gap: 24px;
        flex-wrap: wrap;
    }

    .res-card {
        flex: 1 1 300px;
        border-radius: 16px;
        border: 1px solid #e8e8e8;
        overflow: hidden;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }

    .res-img {
        height: 200px;
        background-size: cover;
        background-position: center;
    }

    .res-content {
        padding: 20px;
    }

    .rating-badge {
        background: #24963f;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 14px;
        font-weight: 600;
    }

    .ai-insight {
        background: #fdf0f1;
        padding: 12px;
        border-radius: 8px;
        font-size: 14px;
        border-left: 3px solid var(--zomato-red);
        margin-top: 16px;
    }

    /* Streamlit Widget Overrides */
    .stSelectbox label, .stSlider label {
        font-size: 14px !important;
        color: #666 !important;
        margin-bottom: 8px !important;
    }
    
    .stButton > button {
        background-color: var(--zomato-red) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 16px !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #d83a4a !important;
        box-shadow: 0 4px 12px rgba(239, 79, 95, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. NAVBAR
st.markdown("""
<div class="navbar-container">
    <img src="https://b.zmtcdn.com/web_assets/b40b97e677bc7b2ca77c58c61db266fe1603954218.png" class="nav-logo">
    <div class="nav-links">
        <span>Log in</span>
        <span>Sign up</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. HERO
st.markdown("""
<div class="hero-section">
    <img src="https://b.zmtcdn.com/web_assets/8313a97515fcb0447d2e776b9730c1605039324.png" class="hero-logo">
    <h1 class="hero-tagline">Find the best restaurants, cafés and bars in Bangalore</h1>
</div>
""", unsafe_allow_html=True)

# 3. AI RECOMMENDER ENGINE (Floating Card)
@st.cache_data
def load_data():
    if not os.path.exists("zomato_data.csv"):
        try:
            from phase1.data_loader import load_zomato_data_kaggle
            return load_zomato_data_kaggle()
        except: return None
    return pd.read_csv("zomato_data.csv")

df = load_data()

st.markdown('<div class="recommender-card-wrapper"><div class="recommender-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">✨ AI Restaurant Recommender</div>', unsafe_allow_html=True)

if df is not None:
    # Form Layout using Streamlit Columns
    c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
    
    with c1:
        locations = sorted(df['area'].unique().tolist())
        location = st.selectbox("Location", ["Select Neighborhood"] + locations, label_visibility="visible")
    
    with c2:
        cuisines_list = ['All Cuisines', 'North Indian', 'Chinese', 'South Indian', 'Fast Food', 'Biryani', 'Continental', 'Cafe', 'Italian', 'Pizza']
        cuisine = st.selectbox("Cuisine Preference", cuisines_list)
        
    with c3:
        budget_map = {"Any Budget": None, "Budget (Under ₹500)": "budget", "Mid-range (₹500-₹1500)": "mid", "Premium (Above ₹1500)": "premium"}
        budget_label = st.selectbox("Budget", list(budget_map.keys()))
        price_val = budget_map[budget_label]
        
    with c4:
        # Min Rating dropdown like Next.js
        rating_val = st.selectbox("Min Rating", ["3.0+", "3.5+", "4.0+", "4.5+"], index=2)
        rating_num = float(rating_val.replace("+", ""))

    st.markdown("<br>", unsafe_allow_html=True)
    submit = st.button("Get AI Recommendations")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

    # 4. CATEGORY CARDS
    st.markdown("""
    <div class="cat-container">
        <div class="cat-card">
            <div class="cat-img" style="background-image: url('https://b.zmtcdn.com/webFrontend/e5b8785c257af2a7f354f1addaf37e4e1647364814.jpeg');"></div>
            <div class="cat-content">
                <div class="cat-title">Order Online</div>
                <div class="cat-subtitle">Stay home and order to your doorstep</div>
            </div>
        </div>
        <div class="cat-card">
            <div class="cat-img" style="background-image: url('https://b.zmtcdn.com/webFrontend/d026b357feb0d63c997549f6398da8cc1647364915.jpeg');"></div>
            <div class="cat-content">
                <div class="cat-title">Dining</div>
                <div class="cat-subtitle">View the city's favourite dining venues</div>
            </div>
        </div>
        <div class="cat-card">
            <div class="cat-img" style="background-image: url('https://b.zmtcdn.com/webFrontend/d9d80ef91cb552e3fdfadb3d4f4379761647365057.jpeg');"></div>
            <div class="cat-content">
                <div class="cat-title">Live Events</div>
                <div class="cat-subtitle">Discover India's best events & concerts</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. RECOMMENDATIONS RESULTS
    if submit:
        if location == "Select Neighborhood":
            st.warning("📍 Please select a neighborhood to get recommendations.")
        else:
            with st.spinner("Finding best matches for you..."):
                c_filter = None if cuisine == "All Cuisines" else cuisine
                filtered_df = filter_restaurants(df, price=price_val, place=location, rating=rating_num, cuisine=c_filter)
                
                if filtered_df.empty:
                    st.markdown(f"<div style='text-align:center; color:#666; padding:40px;'>No recommendations returned for {location}. Try relaxing filters.</div>", unsafe_allow_html=True)
                else:
                    ranked_results = rank_restaurants(filtered_df).head(3)
                    st.markdown(f"<div class='res-container'><h3>Top Picks for You in {location}</h3><div class='res-grid'>", unsafe_allow_html=True)
                    
                    # LLM Insight Engine
                    engine = RecommendationEngine()
                    preferences_str = f"{location}, {cuisine}, {budget_label}, {rating_val}"
                    ai_full_insight = engine.get_recommendations(preferences_str, ranked_results)
                    
                    cols = st.columns(3)
                    for idx, (_, row) in enumerate(ranked_results.iterrows()):
                        with cols[idx]:
                            # Render individual card
                            st.markdown(f"""
                            <div class="res-card">
                                <div class="res-img" style="background-image: url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=400&q=80&sig={idx}');"></div>
                                <div class="res-content">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                        <div style="font-size: 20px; font-weight: 600; color: #1c1c1c;">{row['restaurant name']}</div>
                                        <span class="rating-badge">{row['rate (out of 5)']} ★</span>
                                    </div>
                                    <div style="color: #4f4f4f; font-size: 14px; margin-bottom: 8px;">{row['cuisines type']}</div>
                                    <div style="color: #9c9c9c; font-size: 13px; margin-bottom: 16px;">{row['area']} • ₹{row['avg cost (two people)']} for two</div>
                                    <div class="ai-insight">
                                        <strong>AI Insight:</strong> Matches your {cuisine} preference in {location}.
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                    st.markdown("</div></div>", unsafe_allow_html=True)

else:
    st.markdown('<div class="recommender-card-wrapper"></div>', unsafe_allow_html=True)
    st.error("Dataset not found. Please refresh or check connection.")
