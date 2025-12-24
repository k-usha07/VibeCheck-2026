import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. APP CONFIGURATION & SETUP
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="VibeCheck 2026",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. CSS STYLING (The "Pinterest/Bento" Look)
# -----------------------------------------------------------------------------
# This function injects custom CSS to make the boxes rounded and pretty
def local_css(is_pro_mode):
    # Colors change based on the toggle
    bg_color = "#F8FAFC" if is_pro_mode else "#FFF5F5"
    primary_color = "#1E3A8A" if is_pro_mode else "#FF4B4B"
    
    st.markdown(f"""
        <style>
        /* Main Background */
        .stApp {{
            background-color: {bg_color};
        }}
        
        /* The Bento Card Styling (Metrics) */
        [data-testid="stMetric"] {{
            background-color: white;
            border: 1px solid #e2e8f0;
            padding: 20px;
            border-radius: 20px; /* Rounded corners */
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
        }}
        
        /* Customize the Progress Bar Color */
        .stProgress > div > div > div > div {{
            background-color: {primary_color};
        }}
        
        /* Headers */
        h1, h2, h3 {{
            color: #1f2937;
            font-family: 'Inter', sans-serif;
        }}
        </style>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🎛️ Vibe Control")
    
    # The Main Toggle
    is_pro = st.toggle("Activate Executive Mode 💼", value=False)
    vibe_mode = "Pro" if is_pro else "Silly"
    
    st.divider()
    
    # User Input for the "Existential Clock"
    st.subheader("👤 User Data")
    age = st.slider("Your Age", min_value=1, max_value=85, value=22)
    life_expectancy = 80
    
    st.divider()
    st.caption(f"Current Mode: **{vibe_mode}**")
    st.caption("🚀 Built for Xmas Hackathon 2025")

# Apply the CSS based on the toggle state
local_css(is_pro)

# -----------------------------------------------------------------------------
# 4. DATA LOGIC & CALCULATIONS
# -----------------------------------------------------------------------------

# A. Existential Math
years_lived = age
years_remaining = life_expectancy - age
life_percent = (age / life_expectancy) * 100

# B. Year Progress Math (For 2025)
today = datetime.now()
day_of_year = today.timetuple().tm_yday
year_percent = (day_of_year / 365) * 100
days_left_in_year = 365 - day_of_year

# C. Color Palette for Charts
chart_color = "#1E3A8A" if is_pro else "#FF4B4B" # Blue for Pro, Red for Silly

# -----------------------------------------------------------------------------
# 5. UI LAYOUT (THE BENTO GRID)
# -----------------------------------------------------------------------------

# Title Section
if is_pro:
    st.title("📈 Executive Life-OS: 2026 Strategy")
else:
    st.title("🎄 VibeCheck 2026: The Holiday Edition")
    st.snow() # The fun animation

# --- TOP ROW: The "Time Remaining" Bar ---
st.markdown("### 🗓️ 2025 Lease Progress")
st.progress(year_percent / 100)
if is_pro:
    st.caption(f"Q4 Status: **{year_percent:.1f}% Complete**. {days_left_in_year} days remaining to close annual targets.")
else:
    st.caption(f"Warning! The year is **{year_percent:.1f}% gone**. Only {days_left_in_year} days left to cause chaos!")

st.write("") # Spacing

# --- MIDDLE ROW: Key Metrics (Bento Boxes) ---
col1, col2, col3 = st.columns(3)

with col1:
    # Logic: Toggle between Eggnog (Silly) and Caffeine (Pro)
    label = "☕ Caffeine Intake" if is_pro else "🥛 Eggnog Level"
    val = "2,400 mg" if is_pro else "4.5 Liters"
    delta = "+15% vs Avg" if is_pro else "Critical Levels"
    st.metric(label=label, value=val, delta=delta)

with col2:
    # Logic: Toggle between Focus (Pro) and Chaos (Silly)
    label = "🧠 Deep Work Score" if is_pro else "🌀 Chaos Probability"
    val = "87 / 100" if is_pro else "99.9%"
    delta = "High Efficiency" if is_pro else "Impending Doom"
    st.metric(label=label, value=val, delta=delta)

with col3:
    # Logic: The Life Percentage
    st.metric(label="⌛ Life Lease Used", value=f"{life_percent:.1f}%", delta=f"{years_remaining} Years Left", delta_color="inverse")

st.write("") # Spacing

# --- BOTTOM ROW: Visualizations (Plotly) ---
c_left, c_right = st.columns([1, 1])

with c_left:
    st.markdown("### 🧬 The Existential Clock")
    # Data for Pie Chart
    df_life = pd.DataFrame({
        "Status": ["Time Lived", "Time Remaining"],
        "Years": [years_lived, years_remaining]
    })
    
    # Plotly Donut Chart
    fig_life = px.pie(df_life, values='Years', names='Status', hole=0.6,
                      color_discrete_sequence=[chart_color, "#e2e8f0"])
    fig_life.update_layout(showlegend=False, margin=dict(t=20, b=0, l=0, r=0), height=300)
    st.plotly_chart(fig_life, use_container_width=True)

with c_right:
    st.markdown("### 📊 12-Month Forecast")
    
    # Mock Data for Heatmap/Bar
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # Pro mode = steady growth; Silly mode = random chaos spikes
    values = [30, 40, 45, 50, 55, 60, 55, 60, 70, 80, 90, 100] if is_pro else [10, 90, 20, 100, 5, 50, 80, 10, 100, 20, 60, 99]
    
    df_trend = pd.DataFrame({"Month": months, "Intensity": values})
    
    # Plotly Bar Chart
    fig_trend = px.bar(df_trend, x='Month', y='Intensity',
                       color='Intensity',
                       color_continuous_scale='Blues' if is_pro else 'Reds')
    fig_trend.update_layout(showlegend=False, margin=dict(t=20, b=0, l=0, r=0), height=300)
    st.plotly_chart(fig_trend, use_container_width=True)
