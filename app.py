import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. SETUP
# -----------------------------------------------------------------------------
st.set_page_config(page_title="VibeCheck 2026", page_icon="🍱", layout="wide")

# Initialize Session State for the To-Do List
if 'goals' not in st.session_state:
    st.session_state.goals = ["Survive the Holidays", "Deploy VibeCheck App"]

def add_goal():
    new_goal = st.session_state.new_goal_input
    if new_goal:
        st.session_state.goals.append(new_goal)
        st.session_state.new_goal_input = "" # Clear input

# -----------------------------------------------------------------------------
# 2. THE HIGH-CONTRAST CSS
# -----------------------------------------------------------------------------
def local_css(is_pro_mode):
    if is_pro_mode:
        bg_gradient = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        card_bg = "rgba(255, 255, 255, 0.95)"
        text_color = "#0f172a"
        accent_color = "#2563eb"
        shadow = "0 8px 32px 0 rgba(31, 38, 135, 0.1)"
    else:
        bg_gradient = "linear-gradient(120deg, #fccb90 0%, #d57eeb 100%)"
        card_bg = "rgba(255, 255, 255, 0.95)" 
        text_color = "#1f2937"
        accent_color = "#be185d"
        shadow = "0 8px 32px 0 rgba(219, 39, 119, 0.15)"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;700&display=swap');

        .stApp {{ background: {bg_gradient}; font-family: 'Space Grotesk', sans-serif; }}
        #MainMenu, footer, header {{visibility: hidden;}}
        
        /* CARD STYLING */
        [data-testid="stMetric"], div.stMarkdown, div[data-testid="stVerticalBlock"] > div {{
            border-radius: 24px;
        }}
        [data-testid="stMetric"], .stTextInput > div > div {{
            background: {card_bg};
            backdrop-filter: blur( 12px );
            box-shadow: {shadow};
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 24px;
        }}
        
        /* TEXT COLORS */
        h1, h2, h3, p, span, div, label {{
            font-family: 'Space Grotesk', sans-serif !important;
            color: {text_color} !important;
        }}
        [data-testid="stMetricValue"] {{
            font-size: 38px !important;
            font-weight: 800 !important;
            color: {accent_color} !important;
        }}
        
        /* CHECKBOX STYLING */
        .stCheckbox label span {{
            font-size: 18px;
        }}
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
    st.caption("Mode: " + ("Executive 💼" if is_pro else "Holiday 🎅"))

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
    st.title("📈 Executive Life-OS")
else:
    st.title("🎅 VibeCheck 2026")
    st.snow()

st.write("")

# --- ROW 1: PROGRESS ---
st.markdown(f"### 🗓️ 2025 Status: **{year_percent:.1f}% Complete**")
st.progress(year_percent / 100)
st.caption(f"Only {days_left} days remaining in this yearly cycle.")
st.write("")

# --- ROW 2: METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("☕ Caffeine (mg)" if is_pro else "🥛 Eggnog (L)", "2,450" if is_pro else "4.2", "+12%")
with col2:
    st.metric("🧠 Focus Score" if is_pro else "🌀 Chaos Level", "92/100" if is_pro else "Maximum", "Trending Up")
with col3:
    st.metric("📅 Year Used", f"{year_percent:.1f}%", f"{days_left} Days Left", delta_color="inverse")

st.write("")

# --- ROW 3: CHARTS ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("### ⏰ The Yearly Clock")
    df_year = pd.DataFrame({"Status": ["Passed", "Left"], "Val": [day_of_year, days_left]})
    fig_year = px.pie(df_year, values='Val', names='Status', hole=0.6, color_discrete_sequence=[accent, "#ffffff"])
    fig_year.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
    fig_year.update_traces(textinfo='percent+label', textfont_color=accent)
    st.plotly_chart(fig_year, use_container_width=True)

with c2:
    st.markdown("### 📊 12-Month Forecast")
    vals = [30, 40, 50, 45, 60, 70, 60, 65, 80, 85, 90, 95] if is_pro else [10, 90, 20, 100, 5, 50, 80, 10, 100, 20, 60, 99]
    fig_bar = px.bar(x=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], y=vals, color=vals, color_continuous_scale="Blues" if is_pro else "RdPu")
    fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", xaxis=dict(showgrid=False, title=None), yaxis=dict(showgrid=False, title=None), margin=dict(t=20, b=20, l=20, r=20))
    fig_bar.update_coloraxes(showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)

st.write("")

# --- NEW SECTION: RESOLUTIONS ---
st.markdown("### 📝 2026 Commitments")

# Input Area
c_input, c_btn = st.columns([4, 1])
with c_input:
    st.text_input("Add a new resolution...", key="new_goal_input", placeholder="e.g., Learn to fly a plane", on_change=add_goal)
with c_btn:
    st.write("") # Spacer
    st.write("") # Spacer
    if st.button("Add Task ➕"):
        add_goal()

# Display Checklist
st.write("Your Hit-List:")
for i, goal in enumerate(st.session_state.goals):
    st.checkbox(goal, key=f"goal_{i}")
