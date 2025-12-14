
# --- Streamlit App: Read all data at startup, then display ---
import streamlit as st
import os
import sys
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(__file__))
from data_processing import find_csv_files, parse_workout_csv, aggregate_exercise_data

st.set_page_config(page_title="Training Analysis", page_icon="🏋️", layout="wide", initial_sidebar_state="expanded")

# --- Material Design 3 Color Palette ---
PRIMARY_COLOR = "#6750A4"
ON_PRIMARY = "#FFFFFF"
SECONDARY_COLOR = "#625B71"
SURFACE_COLOR = "#F5F5F7"
BACKGROUND_COLOR = "#FFFFFF"
ERROR_COLOR = "#B3261E"

# --- Custom CSS for Material 3 Look ---
st.markdown(f"""
    <style>
    html, body, [class*='css']  {{
        background-color: {BACKGROUND_COLOR};
        color: #1C1B1F;
        font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    }}
    .material-header {{
        background: linear-gradient(90deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%);
        color: {ON_PRIMARY};
        padding: 2rem 1.5rem 1rem 1.5rem;
        border-radius: 0 0 24px 24px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 16px rgba(103,80,164,0.08);
    }}
    .material-title {{
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 0.2em;
    }}
    .material-subtitle {{
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.92;
        margin-bottom: 0.5em;
    }}
    .material-section {{
        background: {SURFACE_COLOR};
        border-radius: 20px;
        box-shadow: 0 2px 8px rgba(98,91,113,0.06);
        padding: 2rem 1.5rem;
        margin-bottom: 2rem;
    }}
    .material-label {{
        font-size: 1.1rem;
        font-weight: 500;
        color: {PRIMARY_COLOR};
        margin-bottom: 0.5em;
        display: block;
    }}
    .stButton>button {{
        background: {PRIMARY_COLOR};
        color: {ON_PRIMARY};
        border-radius: 16px;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.6em 2em;
        border: none;
        box-shadow: 0 2px 8px rgba(103,80,164,0.10);
        transition: background 0.2s;
    }}
    .stButton>button:hover {{
        background: {SECONDARY_COLOR};
    }}
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown(
    f"""
    <div class="material-header">
        <div class="material-title">🏋️ Training Analysis</div>
        <div class="material-subtitle">
            Analyze Apple Numbers and CSV training plans with a modern, expressive UI.<br>
            <span style='font-size:1rem;opacity:0.8;'>Material Design 3 inspired</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Data Loading (all at startup) ---
CSV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Trainingsplanner/Trainingspläne'))
@st.cache_data
def load_data():
    csv_files = find_csv_files(CSV_DIR)
    all_data = []
    for f in csv_files:
        workout_data = parse_workout_csv(f)
        all_data.append({'file': os.path.basename(f), 'data': workout_data})
    return aggregate_exercise_data(all_data)

exercise_data = load_data()

# --- Main UI ---
st.title("Workout Plan Overview")
st.markdown("Select an exercise to see detailed progression.")

exercises = list(exercise_data.keys())
selected = st.selectbox("Choose exercise", exercises)

if selected:
    vals = exercise_data[selected]
    st.subheader(f"{selected} Progression")
    fig, ax1 = plt.subplots()
    ax1.set_title(f"{selected} - Weight and Sets Progression")
    ax1.set_xlabel("Week")
    ax1.set_ylabel("Weight (kg)", color='tab:blue')
    ax1.plot(vals['week'], vals['weight'], marker='o', color='tab:blue', label='Weight')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax2 = ax1.twinx()
    ax2.set_ylabel("Sets", color='tab:orange')
    ax2.plot(vals['week'], vals['sets'], marker='x', color='tab:orange', label='Sets')
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    fig.tight_layout()
    st.pyplot(fig)
    st.write("Raw Data:")
    st.dataframe({"Week": vals['week'], "Weight": vals['weight'], "Sets": vals['sets']})

st.markdown("---")
st.markdown("All exercises overview:")
cols = st.columns(2)
for idx, name in enumerate(exercises):
    vals = exercise_data[name]
    with cols[idx % 2]:
        st.markdown(f"**{name}**")
        fig, ax1 = plt.subplots(figsize=(4,2))
        ax1.plot(vals['week'], vals['weight'], marker='o', color='tab:blue', label='Weight')
        ax2 = ax1.twinx()
        ax2.plot(vals['week'], vals['sets'], marker='x', color='tab:orange', label='Sets')
        ax1.set_xticks([])
        ax1.set_yticks([])
        ax2.set_yticks([])
        st.pyplot(fig)
        st.caption("Click above to see details.")

# --- Footer ---
st.markdown(
    f"""
    <div style='text-align:center; color:#888; margin-top:2rem; font-size:0.95rem;'>
        &copy; 2025 Training Analysis &mdash; <a href="https://m3.material.io/" style="color:{PRIMARY_COLOR};text-decoration:none;">Material Design 3</a> inspired
    </div>
    """,
    unsafe_allow_html=True
)
