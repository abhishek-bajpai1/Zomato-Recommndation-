import streamlit as st
import pandas as pd
import os
from phase2.recommender_core import filter_restaurants
from phase4.ranking_engine import rank_restaurants
from phase3.llm_engine import RecommendationEngine

# Set Page Config
st.set_page_config(page_title="Zomato AI", page_icon="🍴", layout="wide", initial_sidebar_state="collapsed")

# 1. THEME MANAGEMENT
with st.sidebar:
    st.title("Settings")
    theme_choice = st.radio("UI Theme", ["Premium Dark", "Sleek Light"], index=0)
    st.divider()
    st.markdown("### About Zomato AI")
    st.info("Powering your cravings with real-time AI expert insights.")

is_dark = theme_choice == "Premium Dark"

# Initialize Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'show_auth' not in st.session_state:
    st.session_state.show_auth = None

# Custom CSS with Dynamic Variables
theme_vars = {
    "bg_color": "#0d0d0d" if is_dark else "#ffffff",
    "surface_color": "#1a1a1a" if is_dark else "#f8f8f8",
    "text_main": "#ffffff" if is_dark else "#1c1c1c",
    "text_sub": "#aaaaaa" if is_dark else "#696969",
    "border_color": "#333333" if is_dark else "#e8e8e8",
    "card_bg": "#1a1a1a" if is_dark else "#ffffff",
    "shadow": "0 10px 40px rgba(0,0,0,0.5)" if is_dark else "0 4px 20px rgba(0,0,0,0.08)",
    "nav_bg": "rgba(255,255,255,0.05)" if is_dark else "rgba(255,255,255,0.95)",
    "nav_text": "#ffffff" if is_dark else "#1c1c1c"
}

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
    
    :root {{
        --zomato-red: #EF4F5F;
        --accent-orange: #ff5722;
        --bg-color: {theme_vars['bg_color']};
        --surface-color: {theme_vars['surface_color']};
        --text-main: {theme_vars['text_main']};
        --text-sub: {theme_vars['text_sub']};
        --border-color: {theme_vars['border_color']};
        --card-bg: {theme_vars['card_bg']};
        --shadow: {theme_vars['shadow']};
    }}

    /* Global styling */
    .stApp {{
        font-family: 'Outfit', sans-serif !important;
        background-color: var(--bg-color);
        color: var(--text-main);
    }}

    /* Layout cleanup */
    header, footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    .block-container {{padding-top: 0rem !important; padding-bottom: 5rem !important;}}

    /* Navbar Reconstruction */
    .brand-logo {{
        color: var(--text-main);
        font-size: 26px;
        font-weight: 800;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    .brand-logo span {{ color: var(--zomato-red); }}

    .pill-nav {{
        background: {theme_vars['nav_bg']};
        backdrop-filter: blur(10px);
        border-radius: 100px;
        padding: 8px 30px;
        display: flex;
        gap: 25px;
        align-items: center;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
    }}

    .nav-item {{
        color: {theme_vars['nav_text']};
        font-weight: 600;
        font-size: 14px;
        text-decoration: none;
        cursor: pointer;
        opacity: 0.8;
    }}
    .nav-item:hover {{ opacity: 1; color: var(--zomato-red); }}

    /* Hero Refinement */
    .hero-section {{
        height: 380px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        text-align: center;
        background: linear-gradient(rgba(0,0,0,{'0.6' if is_dark else '0.3'}), rgba(0,0,0,{'0.8' if is_dark else '0.5'})), 
                    url('https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&w=1200&q=80') center/cover;
        margin-bottom: 20px;
    }}

    .hero-tagline {{
        font-size: clamp(32px, 5vw, 56px);
        font-weight: 800;
        letter-spacing: -1.5px;
        margin-bottom: 10px;
    }}

    /* Search Container Styling */
    .search-outer {{
        max-width: 1000px;
        margin: -70px auto 40px auto;
        padding: 0 20px;
        position: relative;
        z-index: 100;
    }}

    .search-pill-bg {{
        background: var(--card_bg);
        padding: 20px 30px;
        border-radius: 24px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
    }}

    /* Result Card Reconstruction */
    .res-card {{
        background: var(--card-bg);
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 25px;
        border: 1px solid var(--border-color);
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}
    .res-card:hover {{ 
        transform: translateY(-8px) scale(1.02); 
        box-shadow: var(--shadow);
    }}

    .rating-badge {{
        background: #24963F;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 14px;
    }}

    /* Auth Overlay as Elegant Card */
    .auth-card {{
        background: var(--card-bg);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid var(--border-color);
        max-width: 450px;
        margin: 50px auto;
        box-shadow: var(--shadow);
    }}

    /* Streamlit Overrides */
    .stSelectbox div[data-baseweb="select"] {{
        background-color: var(--surface-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        color: var(--text-main) !important;
    }}
    
    .stButton > button {{
        background: var(--zomato-red) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100%;
        transition: 0.3s !important;
    }}
    .stButton > button:hover {{ transform: scale(1.02); opacity: 0.9; }}

    /* Google Sign-in Button Style */
    .google-btn {{
        background: white !important;
        color: #757575 !important;
        border: 1px solid #ddd !important;
        border-radius: 12px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        width: 100%;
        cursor: pointer;
        transition: 0.2s;
        margin-top: 15px;
    }}
    .google-btn:hover {{ background: #f8f8f8 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}

    /* Mobile Adaptations */
    @media (max-width: 768px) {{
        .pill-nav {{ display: none; }}
        .search-outer {{ margin-top: -40px; }}
        .hero-tagline {{ font-size: 34px !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)

# 1. NAVBAR Reconstruction
cols = st.columns([1, 4, 1.5], gap="large")

# Initialize Recommendation Engine
if 'ai_engine' not in st.session_state:
    st.session_state.ai_engine = RecommendationEngine()

with cols[0]:
    st.markdown('<div class="brand-logo">ZOMATO<span>AI</span></div>', unsafe_allow_html=True)

with cols[1]:
    st.markdown("""
    <div style="display: flex; justify-content: center;">
        <div class="pill-nav">
            <span class="nav-item">Home</span>
            <span class="nav-item">Dining</span>
            <span class="nav-item">Nightlife</span>
            <span class="nav-item">Trending</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    if not st.session_state.logged_in:
        auth_row = st.columns(2)
        with auth_row[0]:
            if st.button("Log in", key="login_btn"):
                st.session_state.show_auth = 'login'
        with auth_row[1]:
            if st.button("Sign up", key="signup_btn"):
                st.session_state.show_auth = 'signup'
    else:
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; justify-content:flex-end;">
            <span style="color:var(--text-main); font-weight:600;">{st.session_state.user_name}</span>
            <div style="width:36px; height:36px; border-radius:50%; background:var(--zomato-red);"></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()

# 2. AUTH MODAL (Centered Card)
if st.session_state.show_auth:
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="color:var(--text-main); margin-bottom:30px; text-align:center; font-weight:800;">{"Welcome Back" if st.session_state.show_auth == "login" else "Create AI Account"}</h2>', unsafe_allow_html=True)
        
        email = st.text_input("Work Email", placeholder="email@example.com")
        password = st.text_input("Access Key", type="password", placeholder="••••••••")
        
        if st.session_state.show_auth == 'login':
            if st.button("Authenticate Now"):
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.user_name = email.split('@')[0].capitalize()
                    st.session_state.show_auth = None
                    st.success("Access Granted!")
                    st.rerun()
            
            st.markdown('<div style="text-align:center; margin-top:20px; color:var(--text-sub); font-size:14px;">— OR —</div>', unsafe_allow_html=True)
            if st.button("Sign in with Google", key="google_login"):
                st.session_state.logged_in = True
                st.session_state.user_name = "Google User"
                st.session_state.show_auth = None
                st.success("Signed in with Google")
                st.rerun()
        else:
            name = st.text_input("Full Identity", placeholder="Your Name")
            if st.button("Initialize Account"):
                if email and password and name:
                    st.session_state.logged_in = True
                    st.session_state.user_name = name
                    st.session_state.show_auth = None
                    st.success("Profile Activated!")
                    st.rerun()
            
            st.markdown('<div style="text-align:center; margin-top:20px; color:var(--text-sub); font-size:14px;">— OR —</div>', unsafe_allow_html=True)
            if st.button("Sign up with Google", key="google_signup"):
                st.session_state.logged_in = True
                st.session_state.user_name = "Google Explorer"
                st.session_state.show_auth = None
                st.success("Account created via Google")
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Nevermind, take me back", key="close_auth"):
            st.session_state.show_auth = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# 3. HERO SECTION
st.markdown(f"""
    <div class="hero-section">
        <h1 class="hero-tagline">Find the best food in Bangalore</h1>
        <p style="font-size: 18px; opacity: 0.9; color: white;">Powered by Zomato AI – Expert Recommendations in Seconds</p>
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
        if st.session_state.logged_in:
            submit = st.button("Generate Expert Recommendations ✨", use_container_width=True)
        else:
            st.button("Log in to Unlock AI Recommendations 🔒", disabled=True, use_container_width=True)
            st.markdown('<p style="color:var(--zomato-red); font-size:12px; text-align:center; margin-top:5px;">Join for free to access our AI food expert</p>', unsafe_allow_html=True)
            submit = False
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
            if st.session_state.logged_in:
                st.session_state.selected_category = "Meals"
                st.rerun()
            else:
                st.session_state.show_auth = 'login'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cat_cols[1]:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("☕ Cafes"):
            if st.session_state.logged_in:
                st.session_state.selected_category = "Cafes"
                st.rerun()
            else:
                st.session_state.show_auth = 'login'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with cat_cols[2]:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🥂 Nightlife"):
            if st.session_state.logged_in:
                st.session_state.selected_category = "Nightlife"
                st.rerun()
            else:
                st.session_state.show_auth = 'login'
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
                
                # AI INSIGHT PANEL
                st.markdown(f'<div style="padding: 0 10% 80px 10%;"><h2 style="color:var(--text-main); margin-bottom:20px; font-weight:800; letter-spacing:-1px;">Expert AI Match Score</h2>', unsafe_allow_html=True)
                
                _, ai_box_col, _ = st.columns([0.1, 5, 0.1])
                with ai_box_col:
                    st.markdown(f"""
                    <div style="background: {'rgba(255, 87, 34, 0.1)' if is_dark else '#f0f7ff'}; 
                                padding: 30px; border-radius: 20px; border: 1px solid var(--border-color); 
                                border-left: 8px solid var(--zomato-red); margin-bottom: 40px;">
                        <span style="font-size: 24px; margin-right: 15px;">🤖</span> 
                        <span style="color: var(--text-main); font-weight: 700; font-size: 18px;">Personalized Concierge Insight:</span>
                        <p style="color: var(--text-main); line-height: 1.6; margin-top: 15px; font-size: 16px;">{ai_expert_content[:450]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                res_cols = st.columns(3, gap="medium")
                food_images = [
                    "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=600&h=400&fit=crop",
                    "https://images.unsplash.com/photo-1476224483470-401aa1988d78?w=600&h=400&fit=crop"
                ]
                
                for idx, (_, row) in enumerate(ranked_results.iterrows()):
                    img_url = food_images[idx % len(food_images)]
                    with res_cols[idx]:
                        st.markdown(f"""
                        <div class="res-card">
                            <img src="{img_url}" style="width: 100%; height: 200px; object-fit: cover;">
                            <div style="padding: 24px;">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
                                    <div style="color: var(--text-main); font-size: 20px; font-weight: 700;">{row['restaurant name']}</div>
                                    <span class="rating-badge">{row['rate (out of 5)']} ★</span>
                                </div>
                                <div style="color: var(--text-sub); font-size: 14px; margin-bottom: 8px;">{row['cuisines type']}</div>
                                <div style="color: var(--text-sub); font-size: 13px; margin-bottom: 20px;">{row['area']} • ₹{row['avg cost (two people)']} for two</div>
                                <div style="background: var(--surface-color); padding: 15px; border-radius: 12px; border: 1px solid var(--border-color); color: var(--text-main); font-size: 14px;">
                                    <strong>AI Insight:</strong> A premium match based on your preferences.
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("Dataset not found. Please verify the connection.")
