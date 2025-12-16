
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


# Sortiere CSV-Dateien nach der führenden Zahl im Namen absteigend
import re
def extract_leading_number(filename):
    match = re.match(r"(\d+)", filename)
    return int(match.group(1)) if match else -1

csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]
csv_files.sort(key=extract_leading_number, reverse=True)

st.sidebar.markdown("**Verfügbare Trainingspläne:**")

# Use session_state to persist selected plan
if "selected_csv" not in st.session_state:
    st.session_state.selected_csv = csv_files[0] if csv_files else None

plan_labels = [f.replace('.csv', '') for f in csv_files]
selected_label = st.sidebar.radio(
    "Trainingsplan auswählen:",
    options=plan_labels,
    index=plan_labels.index(st.session_state.selected_csv.replace('.csv', '')) if st.session_state.selected_csv else 0
)
selected_csv = f"{selected_label}.csv"
st.session_state.selected_csv = selected_csv

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
                # Zeige die Exercises einer (repräsentativen) Session und summiere die Sets der Exercises
                # Jede Session ist gleich aufgebaut, daher reicht eine Session als Beispiel
                repr_session = df["Session"].min()  # z.B. die erste Session
                session_df = df[df["Session"] == repr_session]
                sets_per_ex = session_df.groupby("Exercise")["Set"].count().reset_index(name="Sets")
                fig_pie = px.pie(sets_per_ex, names="Exercise", values="Sets", title=f"Anzahl Sets pro Exercise (Session {repr_session})")
                st.plotly_chart(fig_pie, use_container_width=True)

        # Balkendiagramm: Jede Exercises hat einen Balken für die durchschnittliche Anzahl der Sessions, bis das Gewicht erhöht werden konnte
        with col2:
            if not df.empty:
                # Nur eindeutige Exercise-Namen
                unique_exercises = df["Exercise"].unique()
                bar_data = []
                for ex_name in unique_exercises:
                    ex_df = df[df["Exercise"] == ex_name].sort_values(["Session", "Set"])
                    session_weights = ex_df.groupby("Session")["Weight (kg)"].max().reset_index()
                    session_weights = session_weights.sort_values("Session")
                    # Finde die Sessions, in denen das Gewicht erhöht wurde
                    prev_weight = None
                    increase_sessions = []
                    for idx, row in session_weights.iterrows():
                        if prev_weight is not None and row["Weight (kg)"] > prev_weight:
                            increase_sessions.append(row["Session"])
                        prev_weight = row["Weight (kg)"]
                    # Wenn es keine Erhöhungen gibt, dann ist der Wert NaN
                    if increase_sessions:
                        # Sessions bis zur ersten Erhöhung: erste Erhöhungssession - erste Session
                        first_session = session_weights["Session"].iloc[0]
                        intervals = [increase_sessions[0] - first_session]
                        # Danach: Differenzen zwischen den Erhöhungssessions
                        for i in range(1, len(increase_sessions)):
                            intervals.append(increase_sessions[i] - increase_sessions[i-1])
                        avg_sessions = sum(intervals) / len(intervals) if intervals else None
                    else:
                        avg_sessions = None
                    bar_data.append({"Exercise": ex_name, "Ø Sessions bis Erhöhung": avg_sessions})
                bar_df = pd.DataFrame(bar_data)
                # Setze 1 als Minimum für die Y-Achse, falls alle Werte None sind, sonst max*1.2
                if not bar_df.dropna().empty:
                    max_sessions = bar_df["Ø Sessions bis Erhöhung"].max()
                    upper_limit = max(1, int(max_sessions * 1.2))
                else:
                    upper_limit = 1
                fig_bar = px.bar(bar_df, x="Exercise", y="Ø Sessions bis Erhöhung", range_y=[0, upper_limit], title="Ø Sessions bis Gewichtserhöhung pro Exercise")
                st.plotly_chart(fig_bar, use_container_width=True)


        # --- Neue Diagrammreihe: Gewichtsentwicklung & Reps pro Exercise ---
        st.markdown("---")
        st.subheader("Verlauf: Gewicht & Wiederholungen pro Übung über Sessions")
        col3, col4 = st.columns(2)

        # Auswahl für mehrere Exercises per Slide-Toggle (Checkboxes)
        exercises = df["Exercise"].unique()
        st.markdown("**Wähle Übungen für die Diagramme:**")
        selected_exs = []
        for ex in exercises:
            if st.toggle(f"{ex}", value=(ex == exercises[0])):
                selected_exs.append(ex)

        # Kurvendiagramm: Gewichtsentwicklung pro (mehrere) Exercise(s)
        with col3:
            if selected_exs:
                weight_df = df[df["Exercise"].isin(selected_exs)]
                fig_weight = px.line(
                    weight_df,
                    x="Session",
                    y="Weight (kg)",
                    color="Exercise",
                    markers=True,
                    title=f"Gewichtsentwicklung: {' & '.join(selected_exs)} über Sessions"
                )
                fig_weight.update_layout(
                    xaxis_title="Session",
                    yaxis_title="Gewicht (kg)"
                )
                st.plotly_chart(fig_weight, use_container_width=True)
            else:
                st.info("Keine Übung ausgewählt.")

        # Kurvendiagramm: Reps pro (mehrere) Exercise(s)
        with col4:
            if selected_exs:
                reps_df = df[df["Exercise"].isin(selected_exs)]
                # Group by Exercise and Session, then sum or average reps (choose average for more meaningful bar height)
                bar_reps = reps_df.groupby(["Exercise", "Session"])['Reps'].mean().reset_index()
                fig_reps_bar = px.bar(
                    bar_reps,
                    x="Session",
                    y="Reps",
                    color="Exercise",
                    barmode="group",
                    title=f"Wiederholungen (Balkendiagramm): {' & '.join(selected_exs)} über Sessions"
                )
                fig_reps_bar.update_layout(
                    xaxis_title="Session",
                    yaxis_title="Ø Wiederholungen"
                )
                st.plotly_chart(fig_reps_bar, use_container_width=True)
            else:
                st.info("Keine Übung ausgewählt.")




        # --- Tabelle darunter ---
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No data found in this CSV.")
else:
    st.info("Bitte wähle einen Trainingsplan in der Sidebar aus.")
