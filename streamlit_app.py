import streamlit as st
import pandas as pd
import os
from phase2.recommender_core import filter_restaurants
from phase4.ranking_engine import rank_restaurants
from phase3.llm_engine import RecommendationEngine

# Set Page Config
st.set_page_config(page_title="Zomato AI Recommender", page_icon="🍴", layout="wide")

# Custom CSS for Zomato Theme
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #CB202D;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #b11b27;
        color: white;
    }
    .restaurant-card {
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border: 1px solid #f0f0f0;
    }
    .title {
        color: #CB202D;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# App Header
st.image("https://upload.wikimedia.org/wikipedia/commons/b/bd/Zomato_Logo.png", width=150)
st.title("AI Recommendation Engine")
st.markdown("Find the best places to eat in Bangalore based on your mood and taste.")

# Load Data
@st.cache_data
def load_data():
    if not os.path.exists("zomato_data.csv"):
        with st.spinner("Downloading dataset from Kaggle... Please wait."):
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
    st.sidebar.header("Your Preferences")
    
    locations = sorted(df['area'].unique().tolist())
    location = st.sidebar.selectbox("Location", ["Select Location"] + locations)
    
    cuisines = ['All Cuisines', 'North Indian', 'Chinese', 'South Indian', 'Fast Food', 'Biryani', 'Continental', 'Cafe', 'Italian', 'Bakery', 'Seafood', 'Mughlai', 'Pizza', 'Burger']
    cuisine = st.sidebar.selectbox("Cuisine", cuisines)
    
    budget_map = {"Any": None, "Budget (< 500)": "budget", "Mid-range (500-1500)": "mid", "Premium (> 1500)": "premium"}
    budget_label = st.sidebar.selectbox("Budget", list(budget_map.keys()))
    price = budget_map[budget_label]
    
    rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5, 0.1)

    if st.sidebar.button("Get AI Recommendations"):
        if location == "Select Location":
            st.error("Please select a location first!")
        else:
            with st.spinner("Finding the best matches for you..."):
                # Filtering logic
                cuisine_filter = None if cuisine == "All Cuisines" else cuisine
                filtered_df = filter_restaurants(df, price=price, place=location, rating=rating, cuisine=cuisine_filter)
                
                if filtered_df.empty:
                    st.warning("No restaurants found matching your criteria. Try relaxing your filters!")
                else:
                    # Ranking logic
                    ranked_df = rank_restaurants(filtered_df)
                    top_3 = ranked_df.head(3)
                    
                    st.subheader(f"Top 3 Recommendations in {location}")
                    
                    # LLM Insight
                    engine = RecommendationEngine()
                    preferences_str = f"Location: {location}, Cuisine: {cuisine}, Budget: {budget_label}, Rating: {rating}+"
                    ai_insight = engine.get_recommendations(preferences_str, ranked_df)
                    
                    if ai_insight and not ai_insight.startswith("Error"):
                        st.info(f"✨ **AI Insight:**\n\n{ai_insight}")
                    else:
                        st.info("Showing top matches from our dataset...")

                    cols = st.columns(3)
                    for idx, (_, row) in enumerate(top_3.iterrows()):
                        with cols[idx]:
                            st.markdown(f"""
                                <div class="restaurant-card">
                                    <h3 class="title">{row['restaurant name']}</h3>
                                    <p>⭐ <b>{row['rate (out of 5)']}/5</b> ({row['num of ratings']} votes)</p>
                                    <p>🥘 {row['cuisines type']}</p>
                                    <p>💰 Avg Cost: ₹{row['avg cost (two people)']}</p>
                                    <p>📍 {row['local address']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
else:
    st.error("Dataset not found! Please run the data ingestion phase first to generate `zomato_data.csv`.")
    st.info("Try running: `python phase1/data_loader.py` in your terminal.")
