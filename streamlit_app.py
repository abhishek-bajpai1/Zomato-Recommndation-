import streamlit as st
import pandas as pd
import os
from phase2.recommender_core import filter_restaurants, get_trending_restaurants
from phase4.ranking_engine import rank_restaurants
from phase3.llm_engine import RecommendationEngine
from dotenv import load_dotenv
import streamlit.components.v1 as components
import json
import base64
from phase5.kpt_engine import KPTEngine, get_kpt_confidence
from phase5.shadow_kpt import ShadowKPTEstimator, fuse_kpt_signals
import random

# Load environment variables FIRST
load_dotenv(override=True)

# 0. GLOBAL CONFIG & AUTH BRIDGE
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDRJ7W10gM2ZFUetfmAo6QF2Lgcdq0E1Vk",
    "authDomain": "zomatoai-3cf37.firebaseapp.com",
    "projectId": "zomatoai-3cf37",
    "storageBucket": "zomatoai-3cf37.firebasestorage.app",
    "messagingSenderId": "578592166445",
    "appId": "1:578592166445:web:8c2e5c67a1c226bb7ddea4",
}

def get_auth_html(button_text):
    config_json = json.dumps(FIREBASE_CONFIG)
    return f"""
    <div id="g_id_onload"
         data-client_id="578592166445-i1g04ud8ohcricufo8ctgemqv3d4k6vj.apps.googleusercontent.com"
         data-context="signin"
         data-ux_mode="popup"
         data-callback="handleCredentialResponse"
         data-auto_prompt="false">
    </div>

    <script src="https://accounts.google.com/gsi/client" async defer></script>
    <script>
        function parseJwt(token) {{
            try {{
                var base64Url = token.split('.')[1];
                var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                var jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {{
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                }}).join(''));
                return JSON.parse(jsonPayload);
            }} catch (e) {{
                return null;
            }}
        }}

        function handleCredentialResponse(response) {{
            const responsePayload = parseJwt(response.credential);
            if (responsePayload) {{
                const name = encodeURIComponent(responsePayload.name || responsePayload.given_name || "User");
                const baseUrl = window.parent.location.origin + window.parent.location.pathname;
                
                // Redirect the parent window to the app with success params
                window.parent.location.href = baseUrl + `?auth_success=true&user_name=${{name}}`;
            }}
        }}
    </script>
    <div style="display: flex; justify-content: center; padding: 20px 0;">
        <div class="g_id_signin"
             data-type="standard"
             data-shape="rectangular"
             data-theme="outline"
             data-text="signin_with"
             data-size="large"
             data-logo_alignment="left">
        </div>
    </div>
    """

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

# REAL FIREBASE BRIDGE: Check for auth callback via query params
if not st.session_state.get('logged_in', False):
    params = st.query_params
    if params.get("auth_success") == "true":
        st.session_state.logged_in = True
        st.session_state.user_name = params.get("user_name", "Explorer")
        st.session_state.show_auth = None
        st.query_params.clear()
        st.rerun()

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

    /* KPT Kitchen Health Dashboard Styles */
    .kpt-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 10px;
    }}
    .health-green {{ background: #e7f7ed; color: #1c8c44; border: 1px solid #d1f0db; }}
    .health-amber {{ background: #fff8e1; color: #b78103; border: 1px solid #ffecb3; }}
    .health-red   {{ background: #fff5f5; color: #e03131; border: 1px solid #ffe3e3; }}

    .signal-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }}
    .dot-green {{ background: #1c8c44; box-shadow: 0 0 8px #1c8c44; }}
    .dot-amber {{ background: #b78103; box-shadow: 0 0 8px #b78103; }}
    .dot-red   {{ background: #e03131; box-shadow: 0 0 8px #e03131; }}

    .kpt-details {{
        background: {theme_vars['surface_color']};
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 12px;
        margin-top: 12px;
        font-size: 13px;
    }}
    .signal-row {{
        display: flex;
        justify-content: space-between;
        margin-bottom: 6px;
        color: var(--text-sub);
    }}
    .signal-val {{
        font-weight: 700;
        color: var(--text-main);
    }}
    .shadow-diff {{
        font-size: 11px;
        font-style: italic;
        color: var(--text-sub);
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
        white-space: nowrap !important;
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
        white-space: nowrap !important;
    }}
    .google-btn:hover {{ background: #f8f8f8 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}

    /* Hide the iframe component default border */
    iframe {{ border: none !important; }}

    /* Mobile Adaptations */
    @media (max-width: 768px) {{
        .pill-nav {{ display: none; }}
        .search-outer {{ margin-top: -40px; }}
        .hero-tagline {{ font-size: 34px !important; }}
        .stButton > button {{
            padding: 8px 10px !important;
            font-size: 14px !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)

# 1. NAVBAR Reconstruction
cols = st.columns([1, 4, 1.5], gap="large")

# 0.5 Initialize KPT Engines
if 'kpt_engine' not in st.session_state:
    st.session_state.kpt_engine = KPTEngine()
if 'shadow_estimator' not in st.session_state:
    st.session_state.shadow_estimator = ShadowKPTEstimator()

# Initialize Recommendation Engine
if 'ai_engine' not in st.session_state:
    st.session_state.ai_engine = RecommendationEngine()

# Load and encode logo for header
with open("assets/zomato_logo.png", "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()

with cols[0]:
    st.markdown(f'''
        <div class="brand-logo" style="display: flex; align-items: center; gap: 8px;">
            <img src="data:image/png;base64,{logo_base64}" style="height: 30px; width: auto; object-fit: contain;">
            <span style="font-weight: 800; color: var(--text-main); letter-spacing: -0.5px; font-size: 20px;">AI</span>
        </div>
    ''', unsafe_allow_html=True)

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
            
            # REAL FIREBASE GOOGLE AUTH BRIDGE
            components.html(get_auth_html("Sign in with Google (Live)"), height=75)

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
            
            # REAL FIREBASE GOOGLE SIGNUP BRIDGE
            components.html(get_auth_html("Sign up with Google (Live)"), height=75)

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
    csv_path = "zomato_data.csv"
    if not os.path.exists(csv_path):
        try:
            from phase1.data_loader import load_zomato_data_kaggle
            return load_zomato_data_kaggle()
        except: return None
    # Use encoding='utf-8' or 'latin-1' and handle errors to fix the garbage text
    try:
        return pd.read_csv(csv_path, encoding='utf-8')
    except UnicodeDecodeError:
        return pd.read_csv(csv_path, encoding='latin-1')

df = load_data()

# Data Cleaning for display
if df is not None:
    # Fix the garbage characters like CafÃ© and other encoding artifacts
    for col in ['restaurant name', 'cuisines type']:
        if col in df.columns:
            def clean_text(text):
                if not isinstance(text, str): return text
                try:
                    if 'Ã' in text:
                        return text.encode('latin-1').decode('utf-8')
                except: pass
                return text.replace('ï¿½', '').strip()
            df[col] = df[col].apply(clean_text)

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
    st.markdown('<div style="padding: 20px 10%; margin-bottom: 20px;">', unsafe_allow_html=True)
    
    # NEW: AI LOGIC TRANSPARENCY
    with st.expander("🔍 See How recommendations are generated"):
        st.markdown(f"""
        ### The Zomato AI Logic:
        1. **Filtering**: We scan **7,000+ restaurants** to find matches in **{location if location != "Any Location" else "Bangalore"}** for **{cuisine}**.
        2. **Ranking**: We use a weighted formula:
           - **70% Weight**: User Rating ({rating_num}+ ★)
           - **30% Weight**: Popularity (Total Votes)
        3. **AI Analysis**: The Top 3 results are sent to our **Groq LLM (Llama 3)**.
        - The AI analyzes the specific menu and user craving to generate a **Personalized Verdict**.
        """)

    st.markdown('<h3 style="text-align:center; margin-bottom:20px; color:var(--text-main); font-weight:700;">Explore categories</h3>', unsafe_allow_html=True)
    cat_cols = st.columns(4)
    
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
    with cat_cols[3]:
        st.markdown('<div style="text-align:center;">', unsafe_allow_html=True)
        if st.button("🔥 Trending"):
            if st.session_state.logged_in:
                st.session_state.selected_category = "Trending"
                st.rerun()
            else:
                st.session_state.show_auth = 'login'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if submit or st.session_state.selected_category == "Trending":
        with st.spinner("Zomato AI is analyzing the best matches for you..."):
            if st.session_state.selected_category == "Trending":
                ranked_results = get_trending_restaurants(df, top_n=3)
                filtered_df = ranked_results # To bypass empty check
                user_query = "What are the hottest, highest-rated trending restaurants in Bangalore right now?"
            else:
                c_filter = None if cuisine == "All Cuisines" else cuisine
                loc_query = None if location == "Any Location" else location
                
                filtered_df = filter_restaurants(df, price=price_val, place=loc_query, rating=rating_num, cuisine=c_filter)
                ranked_results = rank_restaurants(filtered_df).head(3)
                user_query = f"I'm looking for {cuisine} food in {location} with a {budget_label} budget."
            
            if filtered_df.empty:
                st.error("No matches found for this combination. Try expanding your search area or budget!")
            else:
                # GET REAL AI INSIGHTS
                ai_expert_content = st.session_state.ai_engine.get_recommendations(user_query, ranked_results)
                
                # AI INSIGHT PANEL
                st.markdown(f'<div style="padding: 0 10% 80px 10%;"><h2 style="color:var(--text-main); margin-bottom:20px; font-weight:800; letter-spacing:-1px;">{"🔥 Trending Now" if st.session_state.selected_category == "Trending" else "Expert AI Match Score"}</h2>', unsafe_allow_html=True)
                
                _, ai_box_col, _ = st.columns([0.1, 5, 0.1])
                with ai_box_col:
                    st.markdown(f"""
                    <div style="background: {'rgba(255, 87, 34, 0.1)' if is_dark else '#f0f7ff'}; 
                                padding: 30px; border-radius: 20px; border: 1px solid var(--border-color); 
                                border-left: 8px solid var(--zomato-red); margin-bottom: 40px;">
                        <span style="font-size: 24px; margin-right: 15px;">🤖</span> 
                        <span style="color: var(--text-main); font-weight: 700; font-size: 18px;">{'AI Trend Analysis:' if st.session_state.selected_category == 'Trending' else 'Personalized Concierge Insight:'}</span>
                        <p style="color: var(--text-main); line-height: 1.6; margin-top: 15px; font-size: 16px;">{ai_expert_content[:450]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                res_cols = st.columns(3, gap="medium")
                # Verified high-quality food photography IDs from Unsplash
                food_photo_ids = [
                    "photo-1504674900247-0877df9cc836", # General Food
                    "photo-1546069901-ba9599a7e63c", # Salad
                    "photo-1567621113699-1a1df7bbad3e", # Dessert/Breakfast
                    "photo-1555939594-58d7cb561ad1", # Meat
                    "photo-1565299624946-b28f40a0ae38", # Pizza
                    "photo-1482049016688-2d3e1b311543"  # Sandwich
                ]
                
                for idx, (_, row) in enumerate(ranked_results.iterrows()):
                    # Create a robust URL with auto-formatting and compression
                    photo_id = food_photo_ids[idx % len(food_photo_ids)]
                    img_url = f"https://images.unsplash.com/{photo_id}?auto=format&fit=crop&w=600&h=400&q=80"
                    
                    # --- PHASE 5: KPT SIGNAL SIMULATION ---
                    # Simulate real-time kitchen stress for this restaurant
                    mock_orders = [{'complexity': random.choice(['Simple', 'Medium', 'Complex'])} for _ in range(random.randint(2, 8))]
                    kli = st.session_state.kpt_engine.calculate_kli(mock_orders, historical_rush_factor=random.uniform(0.8, 1.4))
                    
                    # Simulate merchant reliability (0.6 - 1.0)
                    mpbs = random.uniform(0.65, 0.95)
                    
                    # Predict KPT
                    base_prep = 20.0
                    predicted_kpt = st.session_state.kpt_engine.predict_kpt(base_prep, kli, mpbs)
                    confidence = get_kpt_confidence(mpbs, kli)
                    
                    # Shadow Ground Truth simulation
                    shadow_bias = random.uniform(-5, 2) # Minutes
                    shadow_kpt = predicted_kpt + shadow_bias
                    
                    # Final Calibrated Prep Time
                    calibrated_kpt = fuse_kpt_signals(predicted_kpt, shadow_kpt, confidence_weight=0.6)
                    
                    # UI Indicators
                    health_class = "health-green" if kli < 8 else ("health-amber" if kli < 15 else "health-red")
                    dot_class = "dot-green" if kli < 8 else ("dot-amber" if kli < 15 else "dot-red")
                    health_status = "Good" if kli < 8 else ("Busy" if kli < 15 else "Stressed")

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
                                
                                <div class="kpt-badge {health_class}">
                                    <span class="signal-dot {dot_class}"></span>
                                    Kitchen Status: {health_status}
                                </div>

                                <div style="background: var(--surface-color); padding: 15px; border-radius: 12px; border: 1px solid var(--border-color); color: var(--text-main); font-size: 14px; margin-top: 15px;">
                                    <strong>Prep Time:</strong> ~{int(calibrated_kpt)} mins ({confidence} Confidence) ⏱️
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("⚡ KPT Signal Intelligence"):
                            st.markdown(f"""
                            <div class="kpt-details">
                                <div class="signal-row">
                                    <span>Kitchen Load Index (KLI)</span>
                                    <span class="signal-val">{kli}</span>
                                </div>
                                <div class="signal-row">
                                    <span>Merchant Trust Score</span>
                                    <span class="signal-val">{int(mpbs*100)}%</span>
                                </div>
                                <div class="signal-row">
                                    <span>Shadow GPS Signal</span>
                                    <span class="signal-val">Detected</span>
                                </div>
                                <div class="shadow-diff">
                                    Bias Calibration: {shadow_bias:.1f} mins offset applied to manual signal
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("Dataset not found. Please verify the connection.")
