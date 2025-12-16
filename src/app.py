

import streamlit as st
import os
from training_logic import load_training_plan_from_csv
import pandas as pd
import plotly.express as px

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

st.sidebar.markdown("**Verfügbare Trainingspläne:**")
selected_csv = None
for f in csv_files:
	label = f.replace('.csv', '')
	if st.sidebar.button(label, key=f"plan_{label}"):
		selected_csv = f

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
					"Session": session_idx,
					"Exercise": ex.name,
					"Set": idx,
					"Reps": s.reps,
					"Weight (kg)": s.weight,
				})
	if rows:
		df = pd.DataFrame(rows)

		# --- Diagramm-Bereich ---
		col1, col2 = st.columns(2)

		# Kreisdiagramm: Anzahl Exercises pro Session
		with col1:
			if not df.empty:
				pie_df = df.groupby(["Session", "Exercise"]).size().reset_index(name="Count")
				pie_counts = pie_df.groupby("Exercise").size().reset_index(name="Sessions")
				fig_pie = px.pie(pie_counts, names="Exercise", values="Sessions", title="Anzahl Exercises pro Session")
				st.plotly_chart(fig_pie, use_container_width=True)

		# Balkendiagramm: Für jede Exercise (einmalig) die Anzahl Sessions, in denen das Gewicht erhöht wurde
		with col2:
			if not df.empty:
				# Nur eindeutige Exercise-Namen
				unique_exercises = df["Exercise"].unique()
				bar_data = []
				for ex_name in unique_exercises:
					ex_df = df[df["Exercise"] == ex_name].sort_values(["Session", "Set"])
					# Zähle Sessions, in denen das Gewicht im Vergleich zur vorherigen Session erhöht wurde
					session_weights = ex_df.groupby("Session")["Weight (kg)"].max().reset_index()
					session_weights = session_weights.sort_values("Session")
					count_increases = 0
					prev_weight = None
					for _, row in session_weights.iterrows():
						if prev_weight is not None and row["Weight (kg)"] > prev_weight:
							count_increases += 1
						prev_weight = row["Weight (kg)"]
					bar_data.append({"Exercise": ex_name, "Sessions": count_increases})
				bar_df = pd.DataFrame(bar_data)
				fig_bar = px.bar(bar_df, x="Exercise", y="Sessions", range_y=[0, 10], title="Sessions bis Gewichtserhöhung pro Exercise")
				st.plotly_chart(fig_bar, use_container_width=True)

		# --- Tabelle darunter ---
		st.dataframe(df, use_container_width=True, hide_index=True)
	else:
		st.info("No data found in this CSV.")
else:
	st.info("Bitte wähle einen Trainingsplan in der Sidebar aus.")
