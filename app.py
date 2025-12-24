import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import random

# -----------------------------------------------------------------------------
# 1. SETUP & SESSION STATE
# -----------------------------------------------------------------------------
st.set_page_config(page_title="VibeCheck 2026", page_icon="🍱", layout="wide")

if 'goals' not in st.session_state:
    st.session_state.goals = [
        {"task": "Survive the Holidays", "diff": 8, "label": "Essential 🎄"},
        {"task": "Win Hackathon", "diff": 10, "label": "Legendary 🏆"}
    ]

# -----------------------------------------------------------------------------
# 2. THE SNOWBALL ENGINE (Custom CSS Generation)
# -----------------------------------------------------------------------------
# This generates random positions for tiny white dots (snowballs)
def generate_snow_css():
    def make_shadows(n):
        shadows = []
        for i in range(n):
            # Random X (0-100vw) and randomized Y start positions
            x = random.randint(1, 99)
            y = random.randint(-100, 0) # Start above screen
            shadows.append(f"{x}vw {y}vh 0 #fff")
        return ",".join(shadows)

    shadows_small = make_shadows(100) # 100 small balls
    shadows_medium = make_shadows(50)  # 50 medium balls

    return f"""
        /* SNOWBALL CONTAINER (invisible, just holds the layers) */
        .snow-container {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            pointer-events: none; z-index: 9999;
            overflow: hidden;
        }}

        /* THE FALLING ANIMATION */
        @keyframes snowfall {{
            to {{ transform: translateY(110vh); }}
        }}

        /* LAYER 1: Small Balls (Fast) */
        .snow-layer-1 {{
            width: 3px; height: 3px; background: transparent; border-radius: 50%;
            box-shadow: {shadows_small};
            animation: snowfall 15s linear infinite;
        }}
        
        /* LAYER 2: Medium Balls (Slower) */
        .snow-layer-2 {{
            width: 5px; height: 5px; background: transparent; border-radius: 50%;
            box-shadow: {shadows_medium};
            animation: snowfall
