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
    # UPDATED STRUCTURE: Added "month" key
    st.session_state.goals = [
        {"task": "Survive the Holidays", "diff": 8, "label": "Essential 🎄", "done": False, "month": "December"},
        {"task": "Start Gym Arc", "diff": 6, "label": "Strategic ♟️", "done": False, "month": "January"}
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
        
        /* DELETE BUTTON */
        button[kind="secondary"] {{
            background-color: transparent !important; color: #ef4444 !important; border: 1px solid #ef4444 !important;
        }}
        button[kind="secondary"]:hover {{ background-color: #ef4444 !important; color: white !important; }}
        </style>
    """, unsafe_allow_html=True)
    return accent_color

# -----------------------------------------------------------------------------
# 4. LOGIC
# -----------------------------------------------------------------------------
def add_goal():
    task = st.session_state.get("new_goal_input", "")
    difficulty = st.session_state.get("difficulty_input", 5)
    month = st.session_state.get("month_input", "December") # GET MONTH
    is_pro = st.session_state.get("toggle_state", False)
    
    if task:
        if is_pro:
            label = "High Impact 🚀" if difficulty >= 8 else "Strategic ♟️" if difficulty >= 5 else "Quick Win ✅"
        else:
            label = "Delusional 🦄" if difficulty >= 9 else "Good Luck 💀" if difficulty >= 6 else "Baby Steps 🍼"
            
        st.session_state.goals.append({"task": task, "diff": difficulty, "label": label, "done": False, "month": month})
        st.session_state.new_goal_input = ""

def delete_goal(index):
    st.session_state.goals.pop(index)

def toggle_done(index):
    st.session_state.goals[index]["done"] = not st.session_state.goals[index]["done"]

def update_task_name(index, new_name):
    st.session_state.goals[index]["task"] = new_name

# -----------------------------------------------------------------------------
# 5. UI LAYOUT
# -----------------------------------------------------------------------------
col_header, col_toggle = st.columns([3, 1])
with col_toggle:
    st.write("")
    is_pro = st.toggle("✨ Pro Mode", value=False, key="toggle_state")

with col_header:
    if is_pro:
        st.title(f"📈 Executive Life-OS {current_year}")
    else:
        st.title(f"🎄 VibeCheck {current_year}")
        st.markdown('<div class="snow-container"><div class="snow-layer-1"></div><div class="snow-layer-2"></div></div>', unsafe_allow_html=True)

accent = local_css(is_pro)

# DASHBOARD
today = datetime.now()
day_of_year = today.timetuple().tm_yday
year_percent = (day_of_year / 365) * 100
days_left = 365 - day_of_year

st.markdown(f"### 🗓️ Annual Cycle: **{year_percent:.1f}% Complete**")
st.progress(year_percent / 100)
st.caption(f"{days_left} days remaining in {current_year}.")
st.write("")

# METRICS
c1, c2, c3 = st.columns(3)
c1.metric("☕ Caffeine" if is_pro else "🥛 Eggnog", "2,450 mg" if is_pro else "4.5 L", "+15%")
c2.metric("🧠 Focus" if is_pro else "🌀 Chaos", "94/100" if is_pro else "Max", "Peaking")
c3.metric("📅 Time Used", f"{year_percent:.1f}%", f"{days_left} Days Left", delta_color="inverse")

st.write("")

# CHARTS
c_left, c_right = st.columns(2)

with c_left:
    st.markdown("### 📊 Progress Parameter")
    total_goals = len(st.session_state.goals)
    completed_goals = sum(1 for g in st.session_state.goals if g["done"])
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = completed_goals,
        delta = {'reference': total_goals, 'relative': False, 'position': "top"},
        title = {'text': "Resolution Momentum", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [None, total_goals if total_goals > 0 else 1]},
            'bar': {'color': accent},
            'bgcolor': "rgba(255,255,255,0.4)",
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': total_goals}
        }
    ))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': '#0f172a'}, margin=dict(t=30, b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with c_right:
    st.markdown("### 🔮 Forecast")
    if is_pro:
        vals = [30, 45, 55, 60, 70, 80, 70, 80, 90, 95, 100, 100]
        y_label = "Productivity (%)"
    else:
        vals = [10, 90, 20, 100, 5, 50, 80, 10, 100, 50, 99, 10]
        y_label = "Chaos Level (%)"

    fig_bar = px.bar(x=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], y=vals, color=vals)
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
        xaxis=dict(showgrid=False, title="Month"), 
        yaxis=dict(showgrid=False, showticklabels=True, title=y_label), 
        margin=dict(t=10, b=0, l=0, r=0)
    )
    fig_bar.update_coloraxes(showscale=False)
    fig_bar.update_traces(hovertemplate=f'<b>Month:</b> %{{x}}<br><b>{y_label}:</b> %{{y}}<extra></extra>')
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# 6. MONTH-WISE RESOLUTION COURT
# -----------------------------------------------------------------------------
st.markdown("### ⚖️ The Resolution Court")

# Defined Timeline
timeline_months = ["December", "January", "February", "March", "April", "May", "June"]

# Input Section (Added Month Selector)
col_in, col_month, col_diff, col_btn = st.columns([3, 1.5, 1.5, 1])
with col_in:
    st.text_input("New Goal", placeholder="e.g. Learn AI", key="new_goal_input", label_visibility="collapsed")
with col_month:
    st.selectbox("Timeline", timeline_months, key="month_input", label_visibility="collapsed")
with col_diff:
    st.slider("Difficulty", 1, 10, 5, key="difficulty_input", label_visibility="collapsed")
with col_btn:
    st.button("Add ➕", on_click=add_goal)

st.write("")

# DISPLAY LOGIC: GROUP BY MONTH
for month in timeline_months:
    # Filter goals that belong to this month
    # We must use enumerate on the MAIN list to ensure indexes match for editing/deleting
    month_goals_indices = [i for i, g in enumerate(st.session_state.goals) if g.get('month', 'December') == month]
    
    if month_goals_indices:
        st.markdown(f"#### 🗓️ {month}")
        for i in month_goals_indices:
            goal = st.session_state.goals[i]
            with st.container():
                c_check, c_edit, c_label, c_del = st.columns([0.5, 3, 1.5, 0.5])
                
                with c_check:
                    st.checkbox("", value=goal["done"], key=f"check_{i}", on_change=toggle_done, args=(i,))
                
                with c_edit:
                    new_text = st.text_input("Task", value=goal['task'], key=f"edit_{i}", label_visibility="collapsed")
                    if new_text != goal['task']:
                        update_task_name(i, new_text)
                        
                with c_label:
                    st.caption(f"{goal['diff']}/10")
                    st.markdown(f"**{goal['label']}**")
                    
                with c_del:
                    st.button("🗑️", key=f"del_{i}", on_click=delete_goal, args=(i,), type="secondary")
                st.divider()
