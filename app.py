import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# -----------------------------------------------------------------------------
# 1. SETUP & SESSION STATE
# -----------------------------------------------------------------------------
st.set_page_config(page_title="VibeCheck", page_icon="🍱", layout="wide")

current_year = datetime.now().year

if 'goals' not in st.session_state:
    st.session_state.goals = [
        {"task": "Survive the Holidays", "diff": 8, "label": "Essential 🎄", "done": False},
        {"task": "Win Hackathon", "diff": 10, "label": "Legendary 🏆", "done": False}
    ]

# -----------------------------------------------------------------------------
# 2. ANIMATION ENGINE
# -----------------------------------------------------------------------------
def generate_animations(is_pro):
    if not is_pro:
        # SILLY MODE: Falling Snowballs
        def make_shadows(n):
            shadows = []
            for i in range(n):
                x = random.randint(1, 99)
                y = random.randint(-100, 0)
                shadows.append(f"{x}vw {y}vh 0 #fff")
            return ",".join(shadows)

        shadows_small = make_shadows(120)
        shadows_med = make_shadows(60)
        
        return f"""
        .snow-container {{ position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 9999; }}
        @keyframes snowfall {{ to {{ transform: translateY(110vh); }} }}
        .snow-layer-1 {{ width: 3px; height: 3px; background: transparent; border-radius: 50%; box-shadow: {shadows_small}; animation: snowfall 12s linear infinite; }}
        .snow-layer-2 {{ width: 5px; height: 5px; background: transparent; border-radius: 50%; box-shadow: {shadows_med}; animation: snowfall 20s linear infinite; }}
        """
    else:
        # PRO MODE: Tech Pulse
        return """
        @keyframes pulse-border {
            0% { border-color: rgba(255, 255, 255, 0.4); box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15); }
            50% { border-color: rgba(37, 99, 235, 0.5); box-shadow: 0 8px 32px 0 rgba(37, 99, 235, 0.2); }
            100% { border-color: rgba(255, 255, 255, 0.4); box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15); }
        }
        [data-testid="stMetric"], div.stMarkdown > div, .stTextInput > div > div {
            animation: slideUp 0.6s ease-out forwards, pulse-border 4s infinite ease-in-out !important;
        }
        """

# -----------------------------------------------------------------------------
# 3. CSS STYLING
# -----------------------------------------------------------------------------
def local_css(is_pro_mode):
    anim_css = generate_animations(is_pro_mode)
    
    if is_pro_mode:
        bg_gradient = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        accent_color = "#2563eb"
        glass_bg = "rgba(255, 255, 255, 0.6)"
        shadow_color = "rgba(31, 38, 135, 0.15)"
        text_color = "#0f172a"
    else:
        bg_gradient = "linear-gradient(120deg, #fccb90 0%, #d57eeb 100%)"
        accent_color = "#be185d"
        glass_bg = "rgba(255, 255, 255, 0.25)"
        shadow_color = "rgba(219, 39, 119, 0.2)"
        text_color = "#0f172a"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;800&display=swap');
        .stApp {{ background: {bg_gradient}; font-family: 'Space Grotesk', sans-serif; }}
        #MainMenu, footer, header {{visibility: hidden;}}

        {anim_css}

        @keyframes slideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        /* GLASS BOXES */
        [data-testid="stMetric"], div.stMarkdown > div, .stTextInput > div > div, .stSelectbox > div > div {{
            background: {glass_bg} !important; backdrop-filter: blur(20px);
            border-radius: 20px !important; border: 1px solid rgba(255, 255, 255, 0.4);
            box-shadow: 0 8px 32px 0 {shadow_color}; padding: 15px !important;
            animation: slideUp 0.6s ease-out forwards;
        }}
        
        div[data-testid="stVerticalBlock"] > div > div.stMarkdown > div {{ padding: 0 !important; border: none !important; box-shadow: none !important; background: transparent !important; }}
        
        /* TYPOGRAPHY */
        h1, h2, h3, p, label, div {{ color: {text_color} !important; font-family: 'Space Grotesk', sans-serif !important; }}
        [data-testid="stMetricValue"] {{ font-size: 36px !important; font-weight: 800; color: {accent_color} !important; }}
        
        /* WIDGETS */
        .stButton > button {{ background-color: {accent_color} !important; color: white !important; border-radius: 12px; border: none; padding: 10px 20px; width: 100%; }}
        
        /* DELETE BUTTON SPECIFIC STYLE */
        button[kind="secondary"] {{
            background-color: transparent !important;
            color: #ef4444 !important; /* Red text */
            border: 1px solid #ef4444 !important;
        }}
        button[kind="secondary"]:hover {{
            background-color: #ef4444 !important;
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    return accent_color

# -----------------------------------------------------------------------------
# 4. LOGIC
# -----------------------------------------------------------------------------
def add_goal():
    task =
