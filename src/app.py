
import streamlit as st
import os
from training_logic import load_training_plan_from_csv
import pandas as pd

st.set_page_config(
	page_title="Training Plans Dashboard",
	layout="wide",
	initial_sidebar_state="expanded",
)

st.title("🏋️ Training Plans Dashboard")
st.markdown("""
<style>
	.main { background-color: #f5f5f5; }
	.stDataFrame th, .stDataFrame td { font-size: 1.1em; }
</style>
""", unsafe_allow_html=True)

# List CSV files in Trainingspläne/
csv_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Trainingspläne")
csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]

selected_csv = st.sidebar.selectbox(
	"Select a training plan CSV:",
	csv_files,
	format_func=lambda x: x.replace('.csv', ''),
)

if selected_csv:
	csv_path = os.path.join(csv_dir, selected_csv)
	plans = load_training_plan_from_csv(csv_path)
	# Flatten for DataFrame
	rows = []
	for session_idx, plan in enumerate(plans, 1):
		for ex in plan.exercises:
			for idx, s in enumerate(ex.set_list, 1):
				rows.append({
					"Plan": plan.name,
					"Session": session_idx,  # Each plan is treated as a session (one instance of model exercises)
					"Exercise": ex.name,
					"Set": idx,
					"Reps": s.reps,
					"Weight (kg)": s.weight,
				})
	if rows:
		df = pd.DataFrame(rows)
		st.dataframe(df, use_container_width=True, hide_index=True)
	else:
		st.info("No data found in this CSV.")
else:
	st.info("Please select a CSV file from the sidebar.")
