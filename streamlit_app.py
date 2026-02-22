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

# Custom CSS for Professional Light UI & Mobile Responsiveness
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    :root {
        --zomato-red: #EF4F5F;
        --accent-orange: #ff5722;
        --bg-color: #ffffff;
        --surface-color: #f8f8f8;
        --text-main: #1c1c1c;
        --text-sub: #696969;
        --border-color: #e8e8e8;
        --shadow-sm: 0 2px 8px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 20px rgba(0,0,0,0.08);
        --shadow-lg: 0 10px 40px rgba(0,0,0,0.12);
    }

    /* Global Body Styling */
    .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: var(--bg-color);
        color: var(--text-main);
    }

    /* Hide Streamlit Header and Footer */
    header, footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Navigation Styling */
    .brand-logo {
        color: var(--text-main);
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 4px;
        cursor: pointer;
    }

    .brand-logo span {
        color: var(--zomato-red);
    }

    .pill-nav {
        background-color: white;
        border-radius: 100px;
        padding: 6px 24px;
        display: flex;
        gap: 20px;
        align-items: center;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-sm);
    }

    .nav-item {
        color: var(--text-sub);
        font-weight: 500;
        font-size: 14px;
        text-decoration: none;
        cursor: pointer;
        transition: all 0.2s;
    }

    .nav-item:hover {
        color: var(--zomato-red);
    }

    /* Hero Section */
    .hero-section {
        height: 320px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        text-align: center;
        background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80') center/cover;
        margin-bottom: 20px;
    }

    .hero-tagline {
        font-size: clamp(28px, 5vw, 48px);
        font-weight: 800;
        margin-bottom: 10px;
        padding: 0 20px;
        letter-spacing: -1px;
    }

    /* Search Container */
    .search-outer {
        max-width: 1000px;
        margin: -60px auto 40px auto;
        padding: 0 20px;
        position: relative;
        z-index: 100;
    }

    .search-pill-bg {
        background: white;
        padding: 12px 24px;
        border-radius: 20px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow-lg);
    }

    /* Result Cards */
    .res-card {
        background: white;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 25px;
        border: 1px solid var(--border-color);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-sm);
    }
    .res-card:hover { 
        transform: translateY(-8px); 
        box-shadow: var(--shadow-md);
    }

    .rating-badge {
        background: #24963F; /* Zomato Green for ratings */
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-weight: 700;
        font-size: 14px;
    }

    /* Streamlit UI Overrides */
    .stSelectbox div[data-baseweb="select"] {
        border: 1px solid transparent !important;
        background-color: #f3f3f3 !important;
        border-radius: 12px !important;
        transition: 0.2s;
    }
    .stSelectbox div[data-baseweb="select"]:hover {
        border-color: #ddd !important;
    }
    
    div[data-testid="stExpander"] {
        border: none !important;
        background: var(--surface-color) !important;
        border-radius: 16px !important;
    }

    .stButton > button {
        background-color: var(--zomato-red) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(239, 79, 95, 0.2) !important;
        width: 100%;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 15px rgba(239, 79, 95, 0.3) !important;
    }

    /* MOBILE RESPONSIVENESS */
    @media (max-width: 768px) {
        .pill-nav {
            display: none; /* Hide desktop nav on mobile */
        }
        .hero-section {
            height: 260px;
        }
        .search-outer {
            margin-top: -40px;
        }
        .search-pill-bg {
            padding: 15px;
        }
        .brand-logo {
            font-size: 20px;
        }
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 10px;
        }
    }
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
            st.markdown('<div style="margin-top:-4px">', unsafe_allow_html=True)
            if st.button("Sign up", key="signup_btn"):
                st.session_state.show_auth = 'signup'
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="header-right" style="display:flex; align-items:center; gap:10px; justify-content:flex-end;">
            <span style="color: var(--text-main); font-weight: 600; font-size:14px;">Hi, {st.session_state.user_name}</span>
            <div style="width:32px; height:32px; border-radius:50%; background:#eee; border:1px solid #ddd;"></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()

# 2. AUTH MODAL (Inline)
if st.session_state.show_auth:
    with st.container():
        st.markdown(f'<div class="auth-overlay" style="background:white; border:1px solid #ddd; padding:40px; border-radius:20px; box-shadow:var(--shadow-lg); max-width:400px; margin:20px auto;">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="color:var(--text-main); margin-bottom:20px; font-weight:700;">{"Log in" if st.session_state.show_auth == "login" else "Create Account"}</h2>', unsafe_allow_html=True)
        
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
    st.markdown('<div style="padding: 20px 10%; margin-bottom: 40px;">', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align:center; margin-bottom:20px; color:var(--text-main); font-weight:700;">Explore categories</h3>', unsafe_allow_html=True)
    cat_cols = st.columns(3)
    
    with cat_cols[0]:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🍱 Full Meals"):
            st.session_state.selected_category = "Meals"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cat_cols[1]:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("☕ Cafes"):
            st.session_state.selected_category = "Cafes"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cat_cols[2]:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🥂 Nightlife"):
            st.session_state.selected_category = "Nightlife"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
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
                
                st.markdown(f'<div style="padding: 0 10% 80px 10%;"><h2 style="color:var(--text-main); margin-bottom:10px; font-weight:800; letter-spacing:-1px;">Top AI Picks</h2>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background: #E8F3FF; padding: 20px; border-radius: 16px; border-left: 5px solid #2D7FF9; margin-bottom: 30px;">
                    <span style="font-size: 20px;">🤖</span> <span style="color: #1a1a1a; font-weight: 600;">AI Summary:</span> 
                    <span style="color: #333; line-height: 1.5;">{ai_expert_content[:350]}...</span>
                </div>
                """, unsafe_allow_html=True)
                
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
                        <div class="res-card">
                            <img src="{img_url}" style="width: 100%; height: 180px; object-fit: cover;">
                            <div style="padding: 20px;">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <div style="color: var(--text-main); font-size: 18px; font-weight: 700;">{row['restaurant name']}</div>
                                    <span class="rating-badge">{row['rate (out of 5)']} ★</span>
                                </div>
                                <div style="color: var(--text-sub); font-size: 13px; margin-bottom: 4px;">{row['cuisines type']}</div>
                                <div style="color: #888; font-size: 12px; margin-bottom: 15px;">{row['area']} • ₹{row['avg cost (two people)']} for two</div>
                                <div style="background: #F8F8F8; padding: 12px; border-radius: 12px; border: 1px solid #eee; color: #444; font-size: 12px; line-height: 1.5;">
                                    <strong>AI Verdict:</strong> {indiv_insight[:140]}...
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("Dataset not found. Please verify the connection.")
