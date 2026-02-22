import streamlit as st
import pandas as pd
import os
from phase2.recommender_core import filter_restaurants
from phase4.ranking_engine import rank_restaurants
from phase3.llm_engine import RecommendationEngine

# Set Page Config
st.set_page_config(page_title="Zomato AI Recommender", page_icon="🍴", layout="wide")

# Custom CSS for a Premium Zomato Look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background-color: #f8f8f8;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1200&q=80');
        background-size: cover;
        background-position: center;
        padding: 80px 40px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Result Cards */
    .res-card {
        background: white;
        padding: 0;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #eee;
        transition: transform 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .res-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px rgba(0,0,0,0.1);
    }
    
    .res-img-placeholder {
        height: 160px;
        background: #f0f0f0;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #ccc;
        font-size: 2rem;
    }
    
    .res-content {
        padding: 16px;
    }
    
    .res-name {
        color: #1c1c1c;
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    .res-meta {
        color: #696969;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }
    
    .res-rating {
        background: #24963f;
        color: white;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #eee;
    }
    
    .stButton>button {
        width: 100%;
        background-color: #EF4F5F !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button:hover {
        background-color: #d83a4a !important;
        box-shadow: 0 4px 12px rgba(239, 79, 95, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# App Hero Header
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Zomato <span style="font-weight: 300; opacity: 0.8;">AI</span></div>
    <div class="hero-subtitle">Discover the best food & drinks in Bangalore</div>
</div>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    if not os.path.exists("zomato_data.csv"):
        with st.spinner("Initializing Database..."):
            try:
                from phase1.data_loader import load_zomato_data_kaggle
                df = load_zomato_data_kaggle()
                if df is not None:
                    return df
            except Exception as e:
                st.error(f"Failed to auto-download dataset: {e}")
                return None
    
    if os.path.exists("zomato_data.csv"):
        return pd.read_csv("zomato_data.csv")
    return None

df = load_data()

if df is not None:
    # Sidebar Filters
    st.sidebar.markdown("<h2 style='color:#1c1c1c; margin-bottom: 20px;'>Preferences</h2>", unsafe_allow_html=True)
    
    locations = sorted(df['area'].unique().tolist())
    location = st.sidebar.selectbox("Select Location", ["Select Location"] + locations)
    
    cuisines = ['All Cuisines', 'North Indian', 'Chinese', 'South Indian', 'Fast Food', 'Biryani', 'Continental', 'Cafe', 'Italian', 'Bakery', 'Seafood', 'Mughlai', 'Pizza', 'Burger']
    cuisine = st.sidebar.selectbox("Choose Cuisine", cuisines)
    
    budget_map = {"Any Budget": None, "Budget (< 500)": "budget", "Mid-range (500-1500)": "mid", "Premium (> 1500)": "premium"}
    budget_label = st.sidebar.selectbox("Set Budget", list(budget_map.keys()))
    price = budget_map[budget_label]
    
    rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5, 0.1)

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    
    if st.sidebar.button("Show Recommendations"):
        if location == "Select Location":
            st.warning("📍 Please select a location to continue.")
        else:
            with st.spinner("Generating matches..."):
                cuisine_filter = None if cuisine == "All Cuisines" else cuisine
                filtered_df = filter_restaurants(df, price=price, place=location, rating=rating, cuisine=cuisine_filter)
                
                if filtered_df.empty:
                    st.error("No restaurants found matching your criteria. Try widening your search!")
                else:
                    ranked_df = rank_restaurants(filtered_df)
                    top_3 = ranked_df.head(3)
                    
                    # LLM Insight Section
                    engine = RecommendationEngine()
                    preferences_str = f"Location: {location}, Cuisine: {cuisine}, Budget: {budget_label}, Rating: {rating}+"
                    ai_insight = engine.get_recommendations(preferences_str, ranked_df)
                    
                    if ai_insight and not ai_insight.startswith("Error"):
                        st.markdown(f"""
                        <div style="background: white; padding: 24px; border-radius: 12px; margin-bottom: 30px; border-left: 5px solid #EF4F5F;">
                            <h4 style="margin: 0 0 10px 0; color: #EF4F5F;">✨ AI Expert Pick</h4>
                            <p style="color: #4f4f4f; font-style: italic; margin: 0;">{ai_insight}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"<h3 style='margin-bottom: 20px;'>Best matches in {location}</h3>", unsafe_allow_html=True)
                    
                    cols = st.columns(3)
                    for idx, (_, row) in enumerate(top_3.iterrows()):
                        with cols[idx]:
                            st.markdown(f"""
                                <div class="res-card">
                                    <div class="res-img-placeholder">🍽️</div>
                                    <div class="res-content">
                                        <div class="res-name">{row['restaurant name']}</div>
                                        <div class="res-meta">{row['cuisines type']}</div>
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                                            <span class="res-rating">{row['rate (out of 5)']} ★</span>
                                            <span style="font-size: 0.9rem; font-weight: 500;">₹{row['avg cost (two people)']} for 2</span>
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
else:
    st.error("Dataset not found! Please check your connection to Kaggle.")
