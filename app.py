import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# -----------------------------------------------------------------------------
# 1. SETUP & SESSION STATE
# -----------------------------------------------------------------------------
st.set_page_config(page_title="VibeCheck 2026", page_icon="🍱", layout="wide")

# Initialize Session State
if 'goals' not in st.session_state:
    st.session_state.goals = ["Survive the Holidays 🎄", "Deploy VibeCheck App 🚀"]

def add_goal():
    new_goal = st.session_state.new_goal_input
    if new_goal:
        st.session_state.goals.append(new_goal)
        st.session_state.new_goal_input = "" # Clear input
        st.toast("✨ Goal Added Successfully!", icon="🚀") # ANIMATED POP-UP

# -----------------------------------------------------------------------------
# 2. THE ANIMATED CSS ENGINE
# -----------------------------------------------------------------------------
def local_css(is_pro_mode):
    if is_pro_mode:
        bg_gradient = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        accent_color = "#2563eb"
        shadow_color = "rgba(31, 38, 135, 0.15)"
    else:
        bg_gradient = "linear-gradient(120deg, #fccb90 0%, #d57eeb 100%)"
        accent_color = "#be185d"
        shadow_color = "rgba(219, 39, 119, 0.2)"

    glass_bg = "rgba(255, 255, 255, 0.2)" 
    glass_border = "1px solid rgba(255, 255, 255, 0.3)"
    glass_blur = "blur( 20px )"
    text_color_primary = "#0f172a"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700;800&display=swap');

        /* 1. APP BACKGROUND */
        .stApp {{
            background: {bg_gradient};
            font-family: 'Space Grotesk', sans-serif;
        }}
        #MainMenu, footer, header {{visibility: hidden;}}

        /* 2. ENTRANCE ANIMATION (Slide Up) */
        @keyframes slideUp {{
            0% {{ opacity: 0; transform: translateY(20px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* 3. HOVER ANIMATION (Levitate) */
        .glass-card {{
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .glass-card:hover {{
            transform: translateY(-5px) scale(1.01);
            box-shadow: 0 15px 35px 0 {shadow_color} !important;
        }}

        /* 4. APPLYING ANIMATIONS TO STREAMLIT BOXES */
        [data-testid="stMetric"], 
        div.stMarkdown > div, 
        .stTextInput > div > div,
        .stCheckbox {{
            background: {glass_bg} !important;
            backdrop-filter: {glass_blur};
            -webkit-backdrop-filter: {glass_blur};
            border-radius: 24px !important;
            border: {glass_border};
            box-shadow: 0 8px 32px 0 {shadow_color};
            padding: 20px !important;
            animation: slideUp 0.8s ease-out forwards; /* Triggers the slide up */
        }}
        
        /* Remove extra padding inside columns */
        div[data-testid="stVerticalBlock"] > div > div.stMarkdown > div {{
             padding: 0px !important;
             background: transparent !important;
             box-shadow: none !important;
             border: none !important;
        }}

        /* TYPOGRAPHY */
        h1, h2, h3, p, span, div, label {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: {text_color_primary} !important;
        }}
        
        [data-testid="stMetricValue"] {{
            font-size: 42px !important;
            font-weight: 800 !important;
            color: {accent_color} !important;
        }}

        /* WIDGETS */
        .stProgress > div > div > div > div {{
            background-color: {accent_color};
            border-radius: 20px;
        }}
        .stButton > button {{
            background-color: {accent_color} !important;
            color: white !important;
            border-radius: 12px;
            border: none;
            padding: 10px 24px;
            transition: all 0.2s;
        }}
        .stButton > button:hover {{
            transform: scale(1.05);
        }}
        .stCheckbox label span {{ font-size: 18px; }}
        </style>
    """, unsafe_allow_html=True)
    return accent_color

# -----------------------------------------------------------------------------
# 3. SIDEBAR & LOGIC
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎛️ Vibe Controller")
    is_pro = st.toggle("✨ Activate Pro Mode", value=False)
    st.divider()
    mode_label = "Executive Strategy 💼" if is_pro else "Holiday Chaos 🎅"
    st.caption(f"Current Mode: **{mode_label}**")

accent = local_css(is_pro)

# Math
today = datetime.now()
day_of_year = today.timetuple().tm_yday
year_percent = (day_of_year / 365) * 100
days_left = 365 - day_of_year

# -----------------------------------------------------------------------------
# 4. UI LAYOUT
# -----------------------------------------------------------------------------

if is_pro:
    st.title("📈 Executive Life-OS: 2026 Outlook")
else:
    st.title("🎄 VibeCheck 2026")
    # Only snow on first load to not be annoying, or always if you prefer
    st.snow()

st.write("")

# --- ROW 1: PROGRESS ---
st.markdown(f"### 🗓️ 2025 Status: **{year_percent:.1f}% Complete**")
st.progress(year_percent / 100)
st.caption(f"Only {days_left} days remaining to close out this yearly cycle.")
st.write("")

# --- ROW 2: ANIMATED METRICS ---
# We use custom markdown wrapper to force the 'glass-card' class for hover effects
col1, col2, col3 = st.columns(3)

# Note: Streamlit metrics are hard to attach custom classes to directly without JS,
# so we rely on the global CSS hover effects defined in local_css logic for [data-testid="stMetric"]

with col1:
    st.metric("☕ Caffeine (mg)" if is_pro else "🥛 Eggnog (L)", "2,450" if is_pro else "4.5", "+15%")
with col2:
    st.metric("🧠 Focus Score" if is_pro else "🌀 Chaos Level", "94/100" if is_pro else "Maximum", "Peaking")
with col3:
    st.metric("📅 Year Used", f"{year_percent:.1f}%", f"{days_left} Days Left", delta_color="inverse")

st.write("")

# --- ROW 3: VISUALS ---
c1, c2 = st.columns(2)

with c1:
    st.markdown("### 🚀 Resolution Momentum")
    
    # Gauge Logic
    total_goals = len(st.session_state.goals)
    checked_goals = 0
    for i in range(total_goals):
        if st.session_state.get(f"goal_{i}", False):
            checked_goals += 1
    progress_val = (checked_goals / total_goals * 100) if total_goals > 0 else 0
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = progress_val,
        number = {'suffix': "%"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Completed: {checked_goals}/{total_goals}", 'font': {'size': 16}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 0, 'tickcolor': "rgba(0,0,0,0)"},
            'bar': {'color': accent},
            'bgcolor': "rgba(255,255,255,0.3)",
            'borderwidth': 0,
            'threshold': {'line': {'color': "white", 'width': 2}, 'thickness': 0.75, 'value': 100}
        }
    ))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': '#0f172a', 'family': 'Space Grotesk'}, margin=dict(t=40, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with c2:
    st.markdown("### 📊 12-Month Forecast")
    vals = [35, 45, 55, 60, 65, 75, 70, 75, 85, 90, 95, 100] if is_pro else [15, 85, 25, 95, 10, 60, 90, 15, 95, 30, 70, 99]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    fig_bar = px.bar(x=months, y=vals, color=vals, color_continuous_scale="Blues" if is_pro else "RdPu")
    
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", 
        plot_bgcolor="rgba(0,0,0,0)", 
        xaxis=dict(showgrid=False, title=None), 
        yaxis=dict(showgrid=False, title=None, showticklabels=False),
        margin=dict(t=20, b=0, l=0, r=0),
        hovermode="x unified"
    )
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_traces(hovertemplate='<b>Month:</b> %{x}<br><b>Intensity:</b> %{y}<extra></extra>')
    st.plotly_chart(fig_bar, use_container_width=True)

st.write("")

# --- ROW 4: CHECKLIST ---
st.markdown("### 📝 2026 Commitments Checklist")

c_input, c_btn = st.columns([4, 1])
with c_input:
    st.text_input("Add a new goal...", key="new_goal_input", placeholder="e.g., Ship that side project...", on_change=add_goal, label_visibility="collapsed")
with c_btn:
    st.button("Add ➕", on_click=add_goal, use_container_width=True)

with st.container():
    for i, goal in enumerate(st.session_state.goals):
        st.checkbox(goal, key=f"goal_{i}")
