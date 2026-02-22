import streamlit as st
import pandas as pd
import os
from phase2.recommender_core import filter_restaurants
from phase4.ranking_engine import rank_restaurants
from phase3.llm_engine import RecommendationEngine

# Set Page Config
st.set_page_config(page_title="Zomato AI Recommender", page_icon="🍴", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for Full Zomato Replication
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background-color: #ffffff;
    }

    /* Navbar Replication */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 10%;
        background: white;
        position: sticky;
        top: 0;
        z-index: 999;
        border-bottom: 1px solid #f0f0f0;
    }

    .nav-search {
        display: flex;
        align-items: center;
        background: white;
        border: 1px solid #e8e8e8;
        border-radius: 8px;
        padding: 5px 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        width: 60%;
    }

    /* Hero Section Replication */
    .hero-bg {
        background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: white;
        text-align: center;
        margin-top: -50px;
    }

    .hero-logo {
        width: 300px;
        margin-bottom: 20px;
        filter: brightness(0) invert(1);
    }

    .hero-tagline {
        font-size: 2.2rem;
        font-weight: 500;
        margin-bottom: 30px;
    }

    /* Category Cards Replication */
    .category-container {
        display: flex;
        justify-content: center;
        gap: 20px;
        padding: 40px 10%;
    }

    .category-card {
        flex: 1;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #e8e8e8;
        transition: transform 0.2s;
        cursor: pointer;
    }

    .category-card:hover {
        transform: scale(1.03);
    }

    .category-img {
        height: 160px;
        background-size: cover;
        background-position: center;
    }

    .category-text {
        padding: 15px;
    }

    .category-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1c1c1c;
    }

    .category-desc {
        font-size: 0.9rem;
        color: #4f4f4f;
    }

    /* Results Header */
    .section-title {
        padding: 20px 10%;
        font-size: 1.8rem;
        font-weight: 600;
        color: #1c1c1c;
    }

    /* Recommendation Engine Section */
    .engine-section {
        background: #f8f8f8;
        padding: 60px 10%;
    }

    .recommender-card {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.05);
    }

    /* Result Card Styling */
    .res-card {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 25px;
        border: 1px solid #f0f0f0;
        transition: 0.3s;
    }

    .res-card:hover {
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    .res-info {
        padding: 15px;
    }

    .res-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .rating-badge {
        background: #24963f;
        color: white;
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
    }

    .btn-red {
        background-color: #EF4F5F !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100% !important;
        padding: 12px !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. Navbar Section
st.markdown("""
<div class="navbar">
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/bd/Zomato_Logo.png" style="height: 30px;">
    <div style="display: flex; gap: 30px; color: #696969; font-weight: 400;">
        <span>Add restaurant</span>
        <span>Log in</span>
        <span>Sign up</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Hero Section
st.markdown("""
<div class="hero-bg">
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/bd/Zomato_Logo.png" class="hero-logo">
    <div class="hero-tagline">Discover the best food & drinks in Bangalore</div>
</div>
""", unsafe_allow_html=True)

# 3. Category Sections
st.markdown("""
<div class="category-container">
    <div class="category-card">
        <div class="category-img" style="background-image: url('https://b.zmtcdn.com/webFrontend/e5b8785c257af2a7f354f1addaf37e4e1647364814.jpeg');"></div>
        <div class="category-text">
            <div class="category-title">Order Online</div>
            <div class="category-desc">Stay home and order to your doorstep</div>
        </div>
    </div>
    <div class="category-card">
        <div class="category-img" style="background-image: url('https://b.zmtcdn.com/webFrontend/d026b357feb0d63c997549f6398da8cc1647364915.jpeg');"></div>
        <div class="category-text">
            <div class="category-title">Dining</div>
            <div class="category-desc">View the city's favourite dining venues</div>
        </div>
    </div>
    <div class="category-card">
        <div class="category-img" style="background-image: url('https://b.zmtcdn.com/webFrontend/d9d80ef91cb552e3fdfadb3d4f4379761647365057.jpeg');"></div>
        <div class="category-text">
            <div class="category-title">Nightlife and Clubs</div>
            <div class="category-desc">Explore the city's top nightlife outlets</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Recommendation Engine Section
st.markdown("<div class='section-title'>AI Recommender</div>", unsafe_allow_html=True)

with st.container():
    st.markdown("<div style='padding: 0 10%; margin-bottom: 50px;'>", unsafe_allow_html=True)
    
    # Load Data
    @st.cache_data
    def load_data():
        if not os.path.exists("zomato_data.csv"):
            try:
                from phase1.data_loader import load_zomato_data_kaggle
                return load_zomato_data_kaggle()
            except:
                return None
        return pd.read_csv("zomato_data.csv")

    df = load_data()

    if df is not None:
        # Form Container
        st.markdown("<div class='recommender-card'>", unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            locations = sorted(df['area'].unique().tolist())
            location = st.selectbox("Where to?", ["Select Location"] + locations)
        
        with col2:
            cuisines_list = ['All Cuisines', 'North Indian', 'Chinese', 'South Indian', 'Fast Food', 'Biryani', 'Continental', 'Cafe', 'Italian', 'Pizza']
            cuisine = st.selectbox("What's on your mind?", cuisines_list)
            
        with col3:
            budget_map = {"Any Budget": None, "Budget (< 500)": "budget", "Mid-range (500-1500)": "mid", "Premium (> 1500)": "premium"}
            budget_label = st.selectbox("Budget", list(budget_map.keys()))
            price = budget_map[budget_label]
            
        with col4:
            rating = st.select_slider("Rating", options=[0.0, 3.0, 3.5, 4.0, 4.5, 5.0], value=3.5)

        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Explore Recommendations", key="rec_btn"):
            if location == "Select Location":
                st.warning("📍 Please select a neighborhood to explore.")
            else:
                with st.spinner("Finding highly-rated restaurants for you..."):
                    cuisine_filter = None if cuisine == "All Cuisines" else cuisine
                    filtered_df = filter_restaurants(df, price=price, place=location, rating=rating, cuisine=cuisine_filter)
                    
                    if filtered_df.empty:
                        st.error("We couldn't find matches for this combo. Try relaxing your filters!")
                    else:
                        ranked_df = rank_restaurants(filtered_df)
                        top_3 = ranked_df.head(3)
                        
                        # AI Insight
                        engine = RecommendationEngine()
                        ai_insight = engine.get_recommendations(f"{location}, {cuisine}, {budget_label}", ranked_df)
                        
                        if ai_insight and not ai_insight.startswith("Error"):
                            st.markdown(f"""
                            <div style="background: white; padding: 25px; border-radius: 12px; margin-top: 30px; border-left: 6px solid #EF4F5F; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                                <h4 style="margin: 0 0 10px 0; color: #EF4F5F; font-size: 1.1rem;">✨ AI Expert Pick</h4>
                                <p style="color: #4f4f4f; font-style: italic; font-size: 0.95rem;">{ai_insight}</p>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("<br><h4>Recommended for you</h4>", unsafe_allow_html=True)
                        
                        res_cols = st.columns(3)
                        for idx, (_, row) in enumerate(top_3.iterrows()):
                            with res_cols[idx]:
                                st.markdown(f"""
                                    <div class="res-card">
                                        <div style="height: 150px; background: #eee url('https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=400&q=80'); background-size: cover; background-position: center;"></div>
                                        <div class="res-info">
                                            <div class="res-top">
                                                <div style="font-weight: 600; font-size: 1.1rem; color: #1c1c1c;">{row['restaurant name']}</div>
                                                <div class="rating-badge">{row['rate (out of 5)']} ★</div>
                                            </div>
                                            <div style="color: #696969; font-size: 0.85rem; margin-top: 5px;">{row['cuisines type']}</div>
                                            <div style="display: flex; justify-content: space-between; margin-top: 15px; font-size: 0.9rem; color: #4f4f4f;">
                                                <span>₹{row['avg cost (two people)']} for two</span>
                                                <span style="color: #9c9c9c;">{row['area']}</span>
                                            </div>
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 5. Footer Replication
st.markdown("""
<div style="padding: 40px 10%; background: #f8f8f8; margin-top: 60px; border-top: 1px solid #e8e8e8;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/b/bd/Zomato_Logo.png" style="height: 30px;">
        <div style="display: flex; gap: 20px;">
            <div style="border: 1px solid #e8e8e8; padding: 5px 15px; border-radius: 5px; background: white;">India</div>
            <div style="border: 1px solid #e8e8e8; padding: 5px 15px; border-radius: 5px; background: white;">English</div>
        </div>
    </div>
    <div style="display: flex; gap: 100px; color: #696969; font-size: 0.85rem;">
        <div>
            <div style="font-weight: 600; color: #1c1c1c; margin-bottom: 15px; letter-spacing: 2px;">ABOUT ZOMATO</div>
            <p>Who We Are</p><p>Blog</p><p>Work With Us</p><p>Investor Relations</p>
        </div>
        <div>
            <div style="font-weight: 600; color: #1c1c1c; margin-bottom: 15px; letter-spacing: 2px;">ZOMAVERSE</div>
            <p>Zomato</p><p>Blinkit</p><p>Feeding India</p><p>Hypure</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
