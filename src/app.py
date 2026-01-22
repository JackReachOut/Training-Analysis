# =============================
# Imports
# =============================
import os
import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
from bs4 import BeautifulSoup
from training_logic import load_training_plan_from_csv, generate_sample_csv


# =============================
# Streamlit Page Config & Title
# =============================
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




# =============================
# Paths & Directories
# =============================
csv_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Trainingspläne")




# =============================
# CSV Download & Upload Section
# =============================
st.sidebar.markdown("**CSV-Download & Upload:**")
example_download_path = os.path.join(csv_dir, "upload_beispiel_trainingsplan.csv")
if os.path.exists(example_download_path):
    with open(example_download_path, "rb") as f:
        example_download_data = f.read()
else:
    example_download_data = b""
st.sidebar.download_button(
    label="Beispiel-CSV herunterladen",
    data=example_download_data,
    file_name="beispiel_trainingsplan.csv",
    mime="text/csv"
)
uploaded_file = st.sidebar.file_uploader(
    "Eigene CSV hochladen:",
    type=["csv"],
    help="Lade eine Trainingsplan-CSV im passenden Format hoch. Die Datei wird nur im Browser verarbeitet und nicht gespeichert."
)

# --- Hinweis zu Datenspeicherung ---
st.sidebar.markdown("**Hinweis:**\n\nAlle Daten bleiben lokal im Browser und werden nicht gespeichert.")

# --- Plan-Auswahl: Beispiel oder Upload ---
plan_source = st.sidebar.radio(
    "Trainingsplan auswählen:",
    options=["Beispiel-Trainingsplan", "Eigene CSV hochladen"],
    index=0 if uploaded_file is None else 1
)


# =============================
# Load Training Plan Data
# =============================
df = None
if plan_source == "Beispiel-Trainingsplan":
    # Load example CSV from file
    example_csv_path = os.path.join(csv_dir, "Trainingsplan Beispiel.csv")
    if os.path.exists(example_csv_path):
        with open(example_csv_path, "r", encoding="utf-8") as f:
            plans = load_training_plan_from_csv(f)
    else:
        st.error("Beispiel-CSV 'Trainingsplan Beispiel.csv' nicht gefunden.")
        plans = []
elif plan_source == "Eigene CSV hochladen" and uploaded_file is not None:
    import io
    plans = load_training_plan_from_csv(uploaded_file)
else:
    plans = []


# =============================
# Flatten Training Plan Data for DataFrame
# =============================
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





    # =============================
    # Visualization Section
    # =============================
    col1, col2 = st.columns([2, 1])

    # --- Pie Chart: Sets per Exercise (Session) ---
    with col1:
        if not df.empty:
            repr_session = df["Session"].min()
            session_df = df[df["Session"] == repr_session]
            sets_per_ex = session_df.groupby("Exercise")["Set"].count().reset_index(name="Sets")
            fig_pie = px.pie(sets_per_ex, names="Exercise", values="Sets", title=f"Anzahl Sets pro Exercise (Session {repr_session})")
            st.plotly_chart(fig_pie, use_container_width=True)

    # --- Bar Chart: Avg. Sessions Until Weight Increase ---
    with col2:
        if not df.empty:
            unique_exercises = df["Exercise"].unique()
            bar_data = []
            for ex_name in unique_exercises:
                ex_df = df[df["Exercise"] == ex_name].sort_values(["Session", "Set"])
                session_weights = ex_df.groupby("Session")["Weight (kg)"].max().reset_index()
                session_weights = session_weights.sort_values("Session")
                prev_weight = None
                increase_sessions = []
                for idx, row in session_weights.iterrows():
                    if prev_weight is not None and row["Weight (kg)"] > prev_weight:
                        increase_sessions.append(row["Session"])
                    prev_weight = row["Weight (kg)"]
                if increase_sessions:
                    first_session = session_weights["Session"].iloc[0]
                    intervals = [increase_sessions[0] - first_session]
                    for i in range(1, len(increase_sessions)):
                        intervals.append(increase_sessions[i] - increase_sessions[i-1])
                    avg_sessions = sum(intervals) / len(intervals) if intervals else None
                else:
                    avg_sessions = None
                bar_data.append({"Exercise": ex_name, "Ø Sessions bis Erhöhung": avg_sessions})
            bar_df = pd.DataFrame(bar_data)
            if not bar_df.dropna().empty:
                max_sessions = bar_df["Ø Sessions bis Erhöhung"].max()
                upper_limit = max(1, int(max_sessions * 1.2))
            else:
                upper_limit = 1
            fig_bar = px.bar(bar_df, x="Exercise", y="Ø Sessions bis Erhöhung", range_y=[0, upper_limit], title="Ø Sessions bis Gewichtserhöhung pro Exercise")
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- Line/Bar Charts: Weight & Reps per Exercise ---
    st.markdown("---")
    st.subheader("Verlauf: Gewicht & Wiederholungen pro Übung über Sessions")
    col3, col4 = st.columns([1, 1])

    exercises = df["Exercise"].unique()
    st.markdown("**Wähle Übungen für die Diagramme:**")
    selected_exs = []
    for ex in exercises:
        if st.toggle(f"{ex}", value=(ex == exercises[0])):
            selected_exs.append(ex)

    # =============================
    # Muscle Group Visualizer & Editor
    # =============================
    if selected_exs:
        st.markdown("---")
        st.subheader("Muskelgruppen-Visualisierung & Zuordnung")
        html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "front_human_body.html")
        mapping_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "muscle_mappings", "exercise_to_muscle.json")
        # Load mappings
        if os.path.exists(mapping_path):
            with open(mapping_path, "r") as f:
                exercise_to_muscle = json.load(f)
        else:
            exercise_to_muscle = {}

        # Predefined muscle groups (from SVGs with data-position and id attributes)
        with open(html_path, "r") as f:
            full_html = f.read()
        soup = BeautifulSoup(full_html, "html.parser")
        svg_div = soup.find("div", class_="human-body")
        svg_elements = svg_div.find_all("svg") if svg_div else []
        predefined_groups = [svg.get("id") for svg in svg_elements if svg.get("id")]
        predefined_groups = sorted(predefined_groups)

        # Load back view SVG (same structure)
        back_html_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "back_human_body.html")
        with open(back_html_path, "r") as f:
            back_html = f.read()
        back_soup = BeautifulSoup(back_html, "html.parser")
        back_svg_div = back_soup.find("div", class_="human-body")
        back_svg_elements = back_svg_div.find_all("svg") if back_svg_div else []

        # Collect all highlight ids for selected exercises
        all_highlight_ids = set()
        for ex in selected_exs:
            current_groups = exercise_to_muscle.get(ex, [])
            selected_groups = st.multiselect(
                f"Wähle Muskelgruppen für '{ex}' (SVG-Regionen)",
                options=predefined_groups,
                default=[g for g in current_groups if g in predefined_groups],
                key=f"predef_{ex}"
            )
            if st.button(f"Speichere Muskelgruppen für '{ex}'", key=f"save_{ex}"):
                exercise_to_muscle[ex] = selected_groups
                with open(mapping_path, "w") as f:
                    json.dump(exercise_to_muscle, f, indent=2, ensure_ascii=False)
                st.success(f"Muskelgruppen für '{ex}' gespeichert.")
            # Add highlighted SVG ids for this exercise
            all_highlight_ids.update(selected_groups)
            st.markdown(f"#### {ex}")

        # Highlight the selected SVGs by adding a highlight class to their class attribute
        for svg in svg_elements:
            sid = svg.get("id")
            classes = svg.get("class", "")
            # BeautifulSoup may return a list for 'class' attribute
            if isinstance(classes, list):
                classes_str = " ".join(classes)
            else:
                classes_str = str(classes)
            if sid in all_highlight_ids:
                if "highlight" not in classes_str.split():
                    svg["class"] = (classes_str + " highlight").strip()
            else:
                if "highlight" in classes_str.split():
                    svg["class"] = " ".join([c for c in classes_str.split() if c != "highlight"])

        # Inject CSS for highlight class directly above SVGs
        highlight_css = """
        <style>
        .human-body svg {
            background: none;
            margin-bottom: 1.5rem;
            fill: #f3f4f6 !important;
            stroke: #bdbdbd !important;
            stroke-width: 1.2 !important;
            opacity: 1 !important;
            transition: fill 0.3s, stroke 0.3s, filter 0.3s;
            filter: none;
        }
        .human-body svg.highlight {
            fill: #ff0000 !important;
            stroke: #b71c1c !important;
            stroke-width: 2.5 !important;
            opacity: 0.95 !important;
            filter: drop-shadow(0 0 8px #ff000088);
            transition: fill 0.3s, stroke 0.3s, filter 0.3s;
        }
        .human-body svg.highlight:focus {
            outline: 2.5px solid #ffab00;
            outline-offset: 2px;
        }
        </style>
        """
        # Render the full SVG block
        svg_html = str(svg_div) if svg_div else ""
        st.markdown("<div style='width:100%;text-align:center;'>" + highlight_css + svg_html + "</div>", unsafe_allow_html=True)

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

        with col4:
            if selected_exs:
                reps_df = df[df["Exercise"].isin(selected_exs)]
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

        # --- Data Table in Expander ---
        with st.expander("Details als Tabelle anzeigen (optional)", expanded=False):
            st.caption("Hier siehst du alle Trainingsdaten als Tabelle. Für die meisten Nutzer sind die Diagramme oben ausreichend.")
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Bitte wähle einen Trainingsplan in der Sidebar aus.")
else:
    st.info("Keine Daten gefunden. Bitte lade eine passende CSV hoch oder nutze das Beispiel.")
