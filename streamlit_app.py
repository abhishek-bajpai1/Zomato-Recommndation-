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
        background-color: #0d0d0d; /* Dark background for the main app */
    }

    /* Hide Streamlit Header and Footer */
    header, footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Clean Dark Header Replication */
    .header-wrapper {
        background-color: #0b0b0b;
        padding: 15px 5%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    .brand-logo {
        color: white;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .brand-logo span {
        color: #ff5722; /* Accent color */
    }

    .pill-nav {
        background-color: #f2f2f2;
        border-radius: 100px;
        padding: 10px 40px;
        display: flex;
        gap: 35px;
        align-items: center;
    }

    .nav-item {
        color: #2d3436;
        font-weight: 600;
        font-size: 15px;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 4px;
        cursor: pointer;
    }

    .nav-item:hover {
        color: #ff5722;
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 20px;
    }

    .icon-circle {
        width: 40px;
        height: 40px;
        background-color: #1e1e1e;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        cursor: pointer;
    }

    .profile-pic {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        border: 2px solid #2d3436;
        background-image: url('https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=100&q=80');
        background-size: cover;
    }

    /* Hero Section with Dark Theme */
    .hero-section {
        position: relative;
        height: 400px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        text-align: center;
        background: linear-gradient(rgba(13,13,13,0.7), rgba(13,13,13,0.7)), url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80') center/cover no-repeat;
    }

    .hero-tagline {
        font-size: 48px;
        font-weight: 700;
        margin-bottom: 20px;
        max-width: 800px;
    }

    /* Clean Search Bar (Rounded with Orange Border) */
    .search-container-wrapper {
        max-width: 900px;
        margin: -60px auto 40px auto;
        padding: 0 20px;
        position: relative;
        z-index: 100;
    }

    .search-box-pill {
        background: white;
        padding: 15px 30px;
        border-radius: 50px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        gap: 15px;
        border: 2px solid #ff5722; /* Orange border like in image */
    }

    /* Recommendation Results Dark Styling */
    .res-card {
        background: #1e1e1e;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 25px;
        border: 1px solid #333;
        transition: 0.3s;
        color: white;
    }

    .res-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.4);
    }

    .res-content {
        padding: 20px;
    }

    .rating-badge {
        background: #ff5722;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
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

# 1. CLEAN DARK HEADER
st.markdown("""
<div class="header-wrapper">
    <div class="brand-logo">ZOMATO<span>AI</span></div>
    <div class="pill-nav">
        <a class="nav-item">Home <span>↑</span></a>
        <a class="nav-item">Top Rated <span>↑</span></a>
        <a class="nav-item">Trending <span>↑</span></a>
        <a class="nav-item">Collections <span>↑</span></a>
        <a class="nav-item">Contact <span>↑</span></a>
    </div>
    <div class="header-right">
        <div class="icon-circle">🔍</div>
        <div class="profile-pic"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. DARK HERO
st.markdown("""
<div class="hero-section">
    <h1 class="hero-tagline">Discover the best food & drinks in Bangalore</h1>
</div>
""", unsafe_allow_html=True)

# 3. AI RECOMMENDER (Pill Search Bar)
@st.cache_data
def load_data():
    if not os.path.exists("zomato_data.csv"):
        try:
            from phase1.data_loader import load_zomato_data_kaggle
            return load_zomato_data_kaggle()
        except: return None
    return pd.read_csv("zomato_data.csv")

df = load_data()

st.markdown('<div class="search-container-wrapper"><div class="search-box-pill">', unsafe_allow_html=True)
st.markdown('<div style="color:#ff5722; font-size:20px;">🔍</div>', unsafe_allow_html=True)

if df is not None:
    # Use Streamlit columns for the actual interactive inputs inside the pill container
    c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
    
    with c1:
        locations = sorted(df['area'].unique().tolist())
        location = st.selectbox("Where?", ["Select Area"] + locations, label_visibility="collapsed")
    
    with c2:
        cuisines_list = ['All Cuisines', 'North Indian', 'Chinese', 'South Indian', 'Fast Food', 'Biryani', 'Cafe', 'Pizza']
        cuisine = st.selectbox("Cuisine?", cuisines_list, label_visibility="collapsed")
        
    with c3:
        budget_map = {"Any Budget": None, "Under ₹500": "budget", "₹500-₹1500": "mid", "Above ₹1500": "premium"}
        budget_label = st.selectbox("Budget?", list(budget_map.keys()), label_visibility="collapsed")
        price_val = budget_map[budget_label]
        
    with c4:
        rating_val = st.selectbox("Rating?", ["3.0+", "3.5+", "4.0+", "4.5+"], index=2, label_visibility="collapsed")
        rating_num = float(rating_val.replace("+", ""))

    st.markdown('</div>', unsafe_allow_html=True) # End search-box-pill
    
    st.markdown('<br>', unsafe_allow_html=True)
    submit = st.button("Search for AI Recommendations")
    st.markdown('</div>', unsafe_allow_html=True) # End search-container-wrapper

    # 4. CATEGORY TILES (Dark Mode Compatible)
    st.markdown("""
    <div style="padding: 40px 10%; display: flex; gap: 20px;">
        <div style="flex:1; background:#1e1e1e; padding:30px; border-radius:20px; border:1px solid #333; text-align:center;">
            <div style="font-size:40px; margin-bottom:10px;">🥘</div>
            <div style="color:white; font-size:20px; font-weight:600;">Full Meals</div>
        </div>
        <div style="flex:1; background:#1e1e1e; padding:30px; border-radius:20px; border:1px solid #333; text-align:center;">
            <div style="font-size:40px; margin-bottom:10px;">☕</div>
            <div style="color:white; font-size:20px; font-weight:600;">Cafes</div>
        </div>
        <div style="flex:1; background:#1e1e1e; padding:30px; border-radius:20px; border:1px solid #333; text-align:center;">
            <div style="font-size:40px; margin-bottom:10px;">🍸</div>
            <div style="color:white; font-size:20px; font-weight:600;">Nightlife</div>
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
