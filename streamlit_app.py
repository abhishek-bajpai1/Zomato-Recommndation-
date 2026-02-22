import streamlit as st
import pandas as pd
import os
from phase2.recommender_core import filter_restaurants
from phase4.ranking_engine import rank_restaurants
from phase3.llm_engine import RecommendationEngine

# Set Page Config
st.set_page_config(page_title="Zomato AI", page_icon="🍴", layout="wide", initial_sidebar_state="collapsed")

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'show_auth' not in st.session_state:
    st.session_state.show_auth = None # 'login' or 'signup'

# Custom CSS for Professional Dark UI
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    :root {
        --zomato-red: #EF4F5F;
        --accent-orange: #ff5722;
    }

    /* Global Body Styling */
    .stApp {
        font-family: 'Outfit', sans-serif !important;
        background-color: #0d0d0d;
    }

    /* Hide Streamlit Header and Footer */
    header, footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Clean Dark Header */
    .header-wrapper {
        background-color: #0d0d0d;
        padding: 20px 5%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 1000;
        border-bottom: 1px solid #1a1a1a;
    }

    .brand-logo {
        color: white;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 6px;
        cursor: pointer;
    }

    .brand-logo span {
        color: var(--accent-orange);
    }

    .pill-nav {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 100px;
        padding: 8px 30px;
        display: flex;
        gap: 25px;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .nav-item {
        color: #1c1c1c;
        font-weight: 600;
        font-size: 14px;
        text-decoration: none;
        cursor: pointer;
        transition: color 0.2s;
    }

    .nav-item:hover {
        color: var(--accent-orange);
    }

    .header-right {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .auth-btn {
        background: transparent;
        border: 1px solid #333;
        color: #ddd;
        padding: 8px 18px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }

    .auth-btn:hover {
        background: #1e1e1e;
        border-color: #555;
        color: white;
    }

    .profile-trigger {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        border: 2px solid var(--accent-orange);
        background: url('https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=100&q=80') center/cover;
        cursor: pointer;
    }

    /* Hero Section */
    .hero-section {
        height: 380px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        text-align: center;
        background: linear-gradient(rgba(13,13,13,0.6), rgba(13,13,13,0.8)), url('https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&w=1200&q=80') center/cover;
    }

    .hero-tagline {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }

    /* Search Container */
    .search-outer {
        max-width: 1000px;
        margin: -50px auto 40px auto;
        padding: 0 20px;
        position: relative;
        z-index: 100;
    }

    .search-pill-bg {
        background: white;
        padding: 10px 20px;
        border-radius: 60px;
        border: 2px solid var(--accent-orange);
        box-shadow: 0 15px 45px rgba(0,0,0,0.4);
    }

    /* Authenticate Overlay */
    .auth-overlay {
        background: rgba(0,0,0,0.8);
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #333;
        max-width: 400px;
        margin: 20px auto;
        text-align: center;
    }

    /* Result Cards */
    .res-card {
        background: #1a1a1a;
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 25px;
        border: 1px solid #222;
        transition: transform 0.3s;
    }
    .res-card:hover { transform: translateY(-5px); }

    .rating-badge {
        background: #ff5722;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
    }

    /* Streamlit Overrides */
    .stSelectbox div[data-baseweb="select"] {
        border: none !important;
        background-color: transparent !important;
    }
    .stSelectbox svg { color: #666 !important; }

    .stButton > button {
        background: var(--zomato-red) !important;
        color: white !important;
        border-radius: 10px !important;
        height: 50px !important;
        font-weight: 700 !important;
        border: none !important;
        transition: 0.3s !important;
    }
    .stButton > button:hover { opacity: 0.9; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# 1. NAVBAR
cols = st.columns([1, 4, 1.5])

# Initialize Recommendation Engine
if 'ai_engine' not in st.session_state:
    st.session_state.ai_engine = RecommendationEngine()

with cols[0]:
    if st.button("ZOMATO AI", key="logo_home"):
        # Reset state but keep login
        st.session_state.pop('selected_category', None)
        st.rerun()

with cols[1]:
    st.markdown("""
    <div style="display: flex; justify-content: center;">
        <div class="pill-nav">
            <span class="nav-item">Home</span>
            <span class="nav-item">Dining</span>
            <span class="nav-item">Nightlife</span>
            <span class="nav-item">Trending</span>
            <span class="nav-item">Contact</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    if not st.session_state.logged_in:
        auth_cols = st.columns(2)
        with auth_cols[0]:
            if st.button("Log in", key="login_btn"):
                st.session_state.show_auth = 'login'
        with auth_cols[1]:
            if st.button("Sign up", key="signup_btn"):
                st.session_state.show_auth = 'signup'
    else:
        st.markdown(f"""
        <div class="header-right">
            <span style="color: white; font-weight: 500;">Hi, {st.session_state.user_name}</span>
            <div class="profile-trigger"></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()

# 2. AUTH MODAL (Inline)
if st.session_state.show_auth:
    with st.container():
        st.markdown(f'<div class="auth-overlay">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="color:white; margin-bottom:20px;">{"Log in" if st.session_state.show_auth == "login" else "Create Account"}</h2>', unsafe_allow_html=True)
        
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        if st.session_state.show_auth == 'login':
            if st.button("Confirm Login"):
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.user_name = email.split('@')[0].capitalize()
                    st.session_state.show_auth = None
                    st.success("Welcome back!")
                    st.rerun()
        else:
            name = st.text_input("Full Name", placeholder="Your Name")
            if st.button("Create Account"):
                if email and password and name:
                    st.session_state.logged_in = True
                    st.session_state.user_name = name
                    st.session_state.show_auth = None
                    st.success("Account created!")
                    st.rerun()
        
        if st.button("Close"):
            st.session_state.show_auth = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 3. HERO
st.markdown("""
<div class="hero-section">
    <h1 class="hero-tagline">Discover the best food & drinks in Bangalore</h1>
    <p style="color: #ccc; font-size: 18px;">Powered by Zomato AI – Expert Recommendations in Seconds</p>
</div>
""", unsafe_allow_html=True)

# 4. SEARCH PILL
@st.cache_data
def load_data():
    if not os.path.exists("zomato_data.csv"):
        try:
            from phase1.data_loader import load_zomato_data_kaggle
            return load_zomato_data_kaggle()
        except: return None
    return pd.read_csv("zomato_data.csv")

df = load_data()

# Category Selection Logic
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

st.markdown('<div class="search-outer"><div class="search-pill-bg">', unsafe_allow_html=True)
if df is not None:
    s_cols = st.columns([0.2, 1.5, 1, 1, 0.8])
    with s_cols[0]:
        st.markdown('<div style="color:#ff5722; font-size:24px; padding-top:5px;">🔍</div>', unsafe_allow_html=True)
    
    with s_cols[1]:
        # Intelligent Location Discovery
        locations = sorted(df['area'].unique().tolist())
        location = st.selectbox("Area", ["Any Location"] + locations, index=0, label_visibility="collapsed")
    
    with s_cols[2]:
        # Dynamic Cuisine Discovery
        all_cuisines = set()
        df['cuisines type'].dropna().apply(lambda x: [all_cuisines.add(c.strip()) for c in x.split(',')])
        sorted_cuisines = sorted(list(all_cuisines))
        
        # Override if category selected
        default_cuisine_idx = 0
        if st.session_state.selected_category == "Cafes":
            if "Cafe" in sorted_cuisines: default_cuisine_idx = sorted_cuisines.index("Cafe") + 1
        
        cuisine = st.selectbox("Cuisine", ["All Cuisines"] + sorted_cuisines, index=default_cuisine_idx, label_visibility="collapsed")
    
    with s_cols[3]:
        budget_map = {"Any Budget": None, "Under ₹500": "budget", "₹500-₹1500": "mid", "Above ₹1500": "premium"}
        budget_label = st.selectbox("Budget", list(budget_map.keys()), label_visibility="collapsed")
        price_val = budget_map[budget_label]
    
    with s_cols[4]:
        rating_val = st.selectbox("Rating", ["3.0+", "3.5+", "4.0+", "4.5+"], index=2, label_visibility="collapsed")
        rating_num = float(rating_val.replace("+", ""))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)
    btn_cols = st.columns([4, 1])
    with btn_cols[0]:
        submit = st.button("Generate Expert Recommendations ✨", use_container_width=True)
    with btn_cols[1]:
        if st.button("Reset 🔄", use_container_width=True):
            st.session_state.selected_category = None
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # 5. INTERACTIVE CATEGORY TILES
    st.markdown('<div style="padding: 20px 10%; display: flex; gap: 20px;">', unsafe_allow_html=True)
    cat_cols = st.columns(3)
    
    with cat_cols[0]:
        if st.button("🍱 Full Meals"):
            st.session_state.selected_category = "Meals"
            st.rerun()
    with cat_cols[1]:
        if st.button("☕ Cafes"):
            st.session_state.selected_category = "Cafes"
            st.rerun()
    with cat_cols[2]:
        if st.button("🥂 Nightlife"):
            st.session_state.selected_category = "Nightlife"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        with st.spinner("Zomato AI is analyzing the best matches for you..."):
            c_filter = None if cuisine == "All Cuisines" else cuisine
            loc_query = None if location == "Any Location" else location
            
            filtered_df = filter_restaurants(df, price=price_val, place=loc_query, rating=rating_num, cuisine=c_filter)
            
            if filtered_df.empty:
                st.error("No matches found for this combination. Try expanding your search area or budget!")
            else:
                ranked_results = rank_restaurants(filtered_df).head(3)
                
                # GET REAL AI INSIGHTS
                user_query = f"I'm looking for {cuisine} food in {location} with a {budget_label} budget."
                ai_expert_content = st.session_state.ai_engine.get_recommendations(user_query, ranked_results)
                
                st.markdown(f'<div style="padding: 0 10% 80px 10%;"><h2 style="color:white; margin-bottom:10px;">Top AI Picks</h2>', unsafe_allow_html=True)
                st.info(f"🤖 **AI Expert Summary:** {ai_expert_content[:300]}...")
                
                res_cols = st.columns(3)
                food_images = [
                    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1476224483470-401aa1988d78?w=600&h=400&fit=crop"
                ]
                
                for idx, (_, row) in enumerate(ranked_results.iterrows()):
                    img_url = food_images[idx % len(food_images)]
                    with res_cols[idx]:
                        # Specific AI Insight for this restaurant
                        restaurant_context = f"Why is {row['restaurant name']} a good choice?"
                        indiv_insight = st.session_state.ai_engine.get_recommendations(restaurant_context, pd.DataFrame([row]))
                        
                        st.markdown(f"""
                        <div class="res-card" style="height: 100%;">
                            <img src="{img_url}" style="width: 100%; height: 200px; object-fit: cover;">
                            <div style="padding: 20px;">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                                    <div style="color: white; font-size: 18px; font-weight: 700;">{row['restaurant name']}</div>
                                    <span class="rating-badge">{row['rate (out of 5)']} ★</span>
                                </div>
                                <div style="color: #aaa; font-size: 13px; margin-bottom: 8px;">{row['cuisines type']}</div>
                                <div style="color: #666; font-size: 12px; margin-bottom: 15px;">{row['area']} • ₹{row['avg cost (two people)']} for two</div>
                                <div style="background: rgba(255, 87, 34, 0.05); padding: 12px; border-radius: 12px; border-left: 3px solid #ff5722; color: #ddd; font-size: 13px; line-height: 1.4;">
                                    <strong>AI Verdict:</strong> {indiv_insight[:150]}...
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("Dataset not found. Please verify the connection.")
