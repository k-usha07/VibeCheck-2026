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

# Initialize Session State
if 'goals' not in st.session_state:
    # Structure: [Task Name, Difficulty Score, Judgment Label]
    st.session_state.goals = [
        {"task": "Survive the Holidays", "diff": 8, "label": "Essential 🎄"},
        {"task": "Win Hackathon", "diff": 10, "label": "Legendary 🏆"}
    ]

# -----------------------------------------------------------------------------
# 2. LOGIC: THE "JUDGMENT ENGINE"
# -----------------------------------------------------------------------------
def add_goal():
    task = st.session_state.new_goal_input
    difficulty = st.session_state.difficulty_input
    is_pro = st.session_state.toggle_state # Get current mode
    
    if task:
        # JUDGMENT LOGIC ⚖️
        if is_pro:
            # Professional Judging
            if difficulty >= 8: label = "High Impact 🚀"
            elif difficulty >= 5: label = "Strategic ♟️"
            else: label = "Quick Win ✅"
        else:
            # Silly Judging
            if difficulty >= 9: label = "Delusional 🦄"
            elif difficulty >= 6: label = "Good Luck 💀"
            else: label = "Baby Steps 🍼"
            
        # Add to list
        st.session_state.goals.append({"task": task, "diff": difficulty, "label": label})
        st.session_state.new_goal_input = "" # Clear input
        st.toast(f"Goal Judged: {label}", icon="⚖️")

# -----------------------------------------------------------------------------
# 3. CSS STYLING (Glassmorphism + Animations)
# -----------------------------------------------------------------------------
def local_css(is_pro_mode):
    if is_pro_mode:
        bg_gradient = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        accent_color = "#2563eb" # Blue
        shadow_color = "rgba(31, 38, 135, 0.15)"
    else:
        bg_gradient = "linear-gradient(120deg, #fccb90 0%, #d57eeb 100%)"
        accent_color = "#be185d" # Pink
        shadow_color = "rgba(219, 39, 119, 0.2)"

    glass_bg = "rgba(255, 255, 255, 0.25)" 
    glass_border = "1px solid rgba(255, 255, 255, 0.4)"
    glass_blur = "blur( 20px )"
    text_color = "#0f172a"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;800&display=swap');

        .stApp {{ background: {bg_gradient}; font-family: 'Space Grotesk', sans-serif; }}
        #MainMenu, footer, header {{visibility: hidden;}}

        /* ANIMATIONS */
        @keyframes slideUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        /* BOX STYLING */
        [data-testid="stMetric"], div.stMarkdown > div, .stTextInput > div > div, .stSelectbox > div > div {{
            background: {glass_bg} !important;
            backdrop-filter: {glass_blur};
            border-radius: 20px !important;
            border: {glass_border};
            box-shadow: 0 8px 32px 0 {shadow_color};
            padding: 15px !important;
            animation: slideUp 0.6s ease-out forwards;
        }}
        
        /* REMOVE PADDING FIX */
        div[data-testid="stVerticalBlock"] > div > div.stMarkdown > div {{ padding: 0px !important; border: none !important; box-shadow: none !important; background: transparent !important; }}

        /* TEXT & WIDGETS */
        h1, h2, h3, p, label, div {{ color: {text_color} !important; font-family: 'Space Grotesk', sans-serif !important; }}
        [data-testid="stMetricValue"] {{ font-size: 36px !important; font-weight: 800; color: {accent_color} !important; }}
        
        /* TOGGLE SWITCH SIZE */
        .stToggle label {{ font-size: 20px; font-weight: bold; }}
        
        /* BUTTON STYLING */
        .stButton > button {{
            background-color: {accent_color} !important;
            color: white !important;
            border-radius: 12px;
            border: none;
            padding: 10px 20px;
            width: 100%;
        }}
        </style>
    """, unsafe_allow_html=True)
    return accent_color

# -----------------------------------------------------------------------------
# 4. TOP CONTROL BAR (Moved Toggle Here!)
# -----------------------------------------------------------------------------
# We use columns to put the title on the Left and the Toggle on the Right
col_header, col_toggle = st.columns([3, 1])

with col_toggle:
    st.write("") # Spacing to align with title
    # KEY FIX: Toggle is now main stage, not sidebar
    is_pro = st.toggle("✨ Pro Mode", value=False, key="toggle_state")

with col_header:
    if is_pro:
        st.title("📈 Executive Life-OS")
    else:
        st.title("🎄 VibeCheck 2026")

# Apply CSS immediately after toggle
accent = local_css(is_pro)

# -----------------------------------------------------------------------------
# 5. MAIN DASHBOARD
# -----------------------------------------------------------------------------
today = datetime.now()
day_of_year = today.timetuple().tm_yday
year_percent = (day_of_year / 365) * 100
days_left = 365 - day_of_year

# PROGRESS BAR
st.markdown(f"### 🗓️ 2025 Status: **{year_percent:.1f}% Complete**")
st.progress(year_percent / 100)
st.caption(f"Only {days_left} days remaining.")
st.write("")

# METRICS ROW
c1, c2, c3 = st.columns(3)
c1.metric("☕ Caffeine" if is_pro else "🥛 Eggnog", "2,450 mg" if is_pro else "4.5 L", "+15%")
c2.metric("🧠 Focus" if is_pro else "🌀 Chaos", "94/100" if is_pro else "Max", "Peaking")
c3.metric("📅 Year Used", f"{year_percent:.1f}%", f"{days_left} Days Left", delta_color="inverse")

st.write("")

# CHARTS ROW
c_left, c_right = st.columns(2)

with c_left:
    st.markdown("### 🚀 Resolution Momentum")
    total = len(st.session_state.goals)
    # Mock calculation for completed tasks (just 50% for visual demo)
    completed = int(total * 0.4) 
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = completed,
        title = {'text': f"Active Goals: {total}", 'font': {'size': 20}},
        gauge = {'axis': {'range': [None, total+5]}, 'bar': {'color': accent}, 'bgcolor': "rgba(255,255,255,0.4)"}
    ))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': '#0f172a'}, margin=dict(t=30, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with c_right:
    st.markdown("### 📊 12-Month Forecast")
    vals = [30, 40, 50, 60, 70, 80, 70, 80, 90, 95, 100, 100] if is_pro else [10, 90, 20, 100, 5, 50, 80, 10, 100, 50, 99, 10]
    fig_bar = px.bar(x=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], y=vals, color=vals)
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False), yaxis=dict(showgrid=False, showticklabels=False), margin=dict(t=10, b=0, l=0, r=0))
    fig_bar.update_coloraxes(showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------------------------------------------------------
# 6. NEW FEATURE: RESOLUTION JUDGE ⚖️
# -----------------------------------------------------------------------------
st.divider()
st.markdown("### ⚖️ The Resolution Court")

# Input Columns
col_in, col_diff, col_btn = st.columns([3, 2, 1])

with col_in:
    st.text_input("Goal Name", placeholder="e.g. Become President", key="new_goal_input", label_visibility="collapsed")

with col_diff:
    # THE JUDGING PARAMETER
    st.slider("Difficulty Level", 1, 10, 5, key="difficulty_input", help="1=Easy, 10=Impossible")

with col_btn:
    st.button("Judge & Add 🔨", on_click=add_goal)

# Display List
st.write("")
for i, goal in enumerate(st.session_state.goals):
    # Each Card shows the Label (Result of Judgment)
    with st.container():
        c_check, c_text, c_label = st.columns([1, 4, 2])
        with c_check:
            st.checkbox("", key=f"check_{i}")
        with c_text:
            st.markdown(f"**{goal['task']}**")
        with c_label:
            st.caption(f"Rated: {goal['diff']}/10")
            st.markdown(f"**{goal['label']}**")
        st.divider()
