
import streamlit as st
import os
import time
from training_logic import load_training_plan_from_csv, generate_sample_csv
import pandas as pd


import plotly.express as px
import json
# Import the new realistic SVG body renderer
from assets.realistic_body_svg import render_realistic_body_html

# --- Muscle Mapping Config ---
MAPPING_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "muscle_mappings")
MAPPING_FILE = os.path.join(MAPPING_DIR, "exercise_to_muscle.json")

MAJOR_MUSCLES = [
    "Chest", "Back", "Shoulders", "Biceps", "Triceps", "Legs", "Glutes", "Core"
]

def load_mapping():
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, "r") as f:
            return json.load(f)
    return {}

def save_mapping(mapping):
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=2)

def get_unique_exercises(df):
    return sorted(df["Exercise"].unique()) if not df.empty else []

# --- SVG Human Body (simplified, major muscle groups as IDs) ---
def get_body_svg(highlighted=None):
    highlighted = highlighted or []
    # Use a light neutral color for default (not black), visible on dark backgrounds
    color_map = {muscle: ("#FF5722" if muscle in highlighted else "#f5e6da") for muscle in MAJOR_MUSCLES}
    aria_labels = {
        "Chest": "Brust",
        "Back": "Rücken",
        "Shoulders": "Schultern",
        "Biceps": "Bizeps",
        "Triceps": "Trizeps",
        "Legs": "Beine",
        "Glutes": "Gesäß",
        "Core": "Rumpf/Bauch"
    }
    # Complex stylized SVG using ellipses, polygons, and paths for a human body
    svg = f'''
    <svg viewBox="0 0 200 500" width="100%" height="auto" aria-label="Muskeldiagramm" role="img" style="max-width:400px;display:block;margin:auto;">
        <desc>Interaktive Darstellung der wichtigsten Muskelgruppen</desc>
        <!-- Head -->
        <ellipse cx="100" cy="50" rx="22" ry="28" fill="#f5e6da" stroke="#bfae9e" stroke-width="2" />
        <!-- Shoulders -->
        <ellipse id="Shoulders" tabindex="0" aria-label="{aria_labels['Shoulders']}" cx="100" cy="95" rx="45" ry="18" fill="{color_map['Shoulders']}" stroke="#bfae9e" stroke-width="2" />
        <!-- Chest -->
        <ellipse id="Chest" tabindex="0" aria-label="{aria_labels['Chest']}" cx="100" cy="130" rx="32" ry="22" fill="{color_map['Chest']}" stroke="#bfae9e" stroke-width="2" />
        <!-- Back (behind chest, slightly offset) -->
        <ellipse id="Back" tabindex="0" aria-label="{aria_labels['Back']}" cx="100" cy="130" rx="38" ry="28" fill="{color_map['Back']}" fill-opacity="0.5" stroke="#bfae9e" stroke-width="2" />
        <!-- Core -->
        <ellipse id="Core" tabindex="0" aria-label="{aria_labels['Core']}" cx="100" cy="175" rx="25" ry="30" fill="{color_map['Core']}" stroke="#bfae9e" stroke-width="2" />
        <!-- Glutes -->
        <ellipse id="Glutes" tabindex="0" aria-label="{aria_labels['Glutes']}" cx="100" cy="220" rx="18" ry="14" fill="{color_map['Glutes']}" stroke="#bfae9e" stroke-width="2" />
        <!-- Left Biceps -->
        <ellipse id="Biceps" tabindex="0" aria-label="{aria_labels['Biceps']}" cx="55" cy="130" rx="10" ry="22" fill="{color_map['Biceps']}" stroke="#bfae9e" stroke-width="2" />
        <!-- Right Biceps -->
        <ellipse id="Biceps" tabindex="0" aria-label="{aria_labels['Biceps']}" cx="145" cy="130" rx="10" ry="22" fill="{color_map['Biceps']}" stroke="#bfae9e" stroke-width="2" />
        <!-- Left Triceps -->
        <ellipse id="Triceps" tabindex="0" aria-label="{aria_labels['Triceps']}" cx="45" cy="170" rx="8" ry="18" fill="{color_map['Triceps']}" stroke="#bfae9e" stroke-width="2" />
        <!-- Right Triceps -->
        <ellipse id="Triceps" tabindex="0" aria-label="{aria_labels['Triceps']}" cx="155" cy="170" rx="8" ry="18" fill="{color_map['Triceps']}" stroke="#bfae9e" stroke-width="2" />
        <!-- Left Leg -->
        <rect id="Legs" tabindex="0" aria-label="{aria_labels['Legs']}" x="80" y="235" width="15" height="80" rx="8" fill="{color_map['Legs']}" stroke="#bfae9e" stroke-width="2" />
        <!-- Right Leg -->
        <rect id="Legs" tabindex="0" aria-label="{aria_labels['Legs']}" x="105" y="235" width="15" height="80" rx="8" fill="{color_map['Legs']}" stroke="#bfae9e" stroke-width="2" />
        <!-- Outline (stylized) -->
        <path d="M100,22 Q80,50 80,95 Q80,250 87,320 Q90,350 100,480 Q110,350 113,320 Q120,250 120,95 Q120,50 100,22 Z" fill="none" stroke="#7a5c3a" stroke-width="2.5" />
    </svg>
    '''
    return svg

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


csv_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Trainingspläne")



# --- CSV Download & Upload ---
st.sidebar.markdown("**CSV-Download & Upload:**")

# Download Beispiel-CSV
st.sidebar.download_button(
    label="Beispiel-CSV herunterladen",
    data=generate_sample_csv(),
    file_name="beispiel_trainingsplan.csv",
    mime="text/csv"
)

# Upload CSV
uploaded_file = st.sidebar.file_uploader(
    "Eigene CSV hochladen:",
    type=["csv"],
    help="Lade eine Trainingsplan-CSV im passenden Format hoch."
)
if uploaded_file is not None:
    # Automatisch umbenennen mit Zeitstempel
    timestamp = int(time.time())
    safe_name = os.path.splitext(uploaded_file.name)[0]
    new_filename = f"upload_{safe_name}_{timestamp}.csv"
    save_path = os.path.join(csv_dir, new_filename)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Datei '{uploaded_file.name}' wurde als '{new_filename}' gespeichert.")

# --- CSV Auswahl & Anzeige ---
import re
def extract_leading_number(filename):
    match = re.match(r"(\d+)", filename)
    return int(match.group(1)) if match else -1

# Alle CSVs (inkl. Uploads) anzeigen, sortiert: erst nach führender Zahl, dann Uploads nach Zeitstempel
def sort_csvs(files):
    def sort_key(f):
        if f.startswith("upload_"):
            # Extrahiere Zeitstempel
            m = re.match(r"upload_.*_(\d+)\.csv", f)
            return (9999, -int(m.group(1)) if m else 0)
        else:
            return (-extract_leading_number(f), 0)
    return sorted(files, key=sort_key)

csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]
csv_files = sort_csvs(csv_files)


st.sidebar.markdown("**Verfügbare Trainingspläne:**")

# Prepare plan labels and mapping
plan_labels = [f.replace('.csv', '') for f in csv_files]
label_to_file = {label: f for label, f in zip(plan_labels, csv_files)}

# Use session_state to persist selected plan
if "selected_csv" not in st.session_state or st.session_state.selected_csv not in csv_files:
    st.session_state.selected_csv = csv_files[0] if csv_files else None

# --- Delete CSVs ---
if plan_labels:
    with st.sidebar.expander("Trainingsplan löschen", expanded=False):
        for label in plan_labels:
            file_to_delete = label_to_file[label]
            # Nicht löschen, wenn nur eine Datei übrig ist
            if len(plan_labels) > 1:
                delete_btn = st.button(f"Lösche '{label}'", key=f"delete_{label}")
                if delete_btn:
                    os.remove(os.path.join(csv_dir, file_to_delete))
                    st.success(f"'{label}' wurde gelöscht.")
                    # Nach dem Löschen Seite neu laden, damit Auswahl und Liste stimmen
                    st.rerun()

if plan_labels:
    # Fallback: if session_state.selected_csv is not in csv_files, pick first
    current_label = st.session_state.selected_csv.replace('.csv', '') if st.session_state.selected_csv and st.session_state.selected_csv.replace('.csv', '') in plan_labels else plan_labels[0]
    selected_label = st.sidebar.radio(
        "Trainingsplan auswählen:",
        options=plan_labels,
        index=plan_labels.index(current_label)
    )
    selected_csv = label_to_file[selected_label]
    st.session_state.selected_csv = selected_csv
else:
    selected_csv = None

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



        # ...existing code for all other graphs and tables...
        # --- Diagramm-Bereich ---
        col1, col2 = st.columns([2, 1])


        # --- Realistic HTML/CSS Human Body (major muscle groups as classes) ---


        def get_realistic_body_html(highlighted=None):
            highlighted = highlighted or []
            # Map major muscle groups to class names used in the HTML
            muscle_class_map = {
                "Chest": "chest",
                "Back": "back",
                "Shoulders": "shoulders",
                "Biceps": ["biceps-left", "biceps-right"],
                "Triceps": ["triceps-left", "triceps-right"],
                "Legs": ["leg-left", "leg-right"],
                "Glutes": "glutes",
                "Core": "core",
            }
            # Build highlight class set
            highlight_classes = set()
            for m in highlighted:
                if m in muscle_class_map:
                    val = muscle_class_map[m]
                    if isinstance(val, list):
                        highlight_classes.update(val)
                    else:
                        highlight_classes.add(val)

            # Material Design 3 highlight color
            highlight_color = "#FF5722"
            base_color = "#f5e6da"  # Light neutral for dark mode
            border_color = "#bfae9e"  # Mid-tone brown for contrast
            skin_color = "#f5e6da"

            # Inline CSS for realistic body
            style = f'''
<style>
.realistic-body-container {{
    width: 220px;
    margin: 0 auto;
    position: relative;
    aspect-ratio: 2/5;
    min-height: 400px;
}}
.realistic-body {{
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 380px;
}}
.body-part {{
    position: absolute;
    background: {base_color};
    border: 2px solid {border_color};
    transition: background 0.3s, box-shadow 0.3s;
    opacity: 0.95;
    box-shadow: 0 0 8px rgba(0,0,0,0.08); /* subtle shadow for contrast */
}}
.body-part.highlight {{
    background: {highlight_color};
    box-shadow: 0 0 0 4px #ffab91;
    opacity: 1.0;
}}
.head {{ left: 50%; top: 2%; width: 44px; height: 56px; background: {skin_color}; border-radius: 50%; transform: translate(-50%, 0); z-index: 2; }}
.shoulders {{ left: 50%; top: 13%; width: 120px; height: 36px; border-radius: 40px; transform: translate(-50%, 0); z-index: 2; }}
.chest {{ left: 50%; top: 21%; width: 80px; height: 44px; border-radius: 40px; transform: translate(-50%, 0); z-index: 2; }}
.back {{ left: 50%; top: 21%; width: 92px; height: 54px; border-radius: 40px; transform: translate(-50%, 0); opacity: 0.5; z-index: 1; }}
.core {{ left: 50%; top: 33%; width: 60px; height: 60px; border-radius: 40px; transform: translate(-50%, 0); z-index: 2; }}
.glutes {{ left: 50%; top: 48%; width: 36px; height: 28px; border-radius: 40px; transform: translate(-50%, 0); z-index: 2; }}
.biceps-left {{ left: 18%; top: 22%; width: 22px; height: 54px; border-radius: 40px; z-index: 2; }}
.biceps-right {{ left: 70%; top: 22%; width: 22px; height: 54px; border-radius: 40px; z-index: 2; }}
.triceps-left {{ left: 10%; top: 32%; width: 18px; height: 44px; border-radius: 40px; z-index: 2; }}
.triceps-right {{ left: 80%; top: 32%; width: 18px; height: 44px; border-radius: 40px; z-index: 2; }}
.leg-left {{ left: 38%; top: 56%; width: 22px; height: 110px; border-radius: 20px; z-index: 2; }}
.leg-right {{ left: 58%; top: 56%; width: 22px; height: 110px; border-radius: 20px; z-index: 2; }}
</style>
'''
            # HTML structure for the body
            html = f'''
            <div class="realistic-body-container">
              <div class="realistic-body">
                <div class="head body-part"></div>
                <div class="shoulders body-part{' highlight' if 'shoulders' in highlight_classes else ''}"></div>
                <div class="chest body-part{' highlight' if 'chest' in highlight_classes else ''}"></div>
                <div class="back body-part{' highlight' if 'back' in highlight_classes else ''}"></div>
                <div class="core body-part{' highlight' if 'core' in highlight_classes else ''}"></div>
                <div class="glutes body-part{' highlight' if 'glutes' in highlight_classes else ''}"></div>
                <div class="biceps-left body-part{' highlight' if 'biceps-left' in highlight_classes else ''}"></div>
                <div class="biceps-right body-part{' highlight' if 'biceps-right' in highlight_classes else ''}"></div>
                <div class="triceps-left body-part{' highlight' if 'triceps-left' in highlight_classes else ''}"></div>
                <div class="triceps-right body-part{' highlight' if 'triceps-right' in highlight_classes else ''}"></div>
                <div class="leg-left body-part{' highlight' if 'leg-left' in highlight_classes else ''}"></div>
                <div class="leg-right body-part{' highlight' if 'leg-right' in highlight_classes else ''}"></div>
              </div>
            </div>
            '''
            return style + html

        # Kreisdiagramm: Anzahl Exercises pro Session

        # Kreisdiagramm: Anzahl Exercises pro Session
        with col1:
            if not df.empty:
                repr_session = df["Session"].min()
                session_df = df[df["Session"] == repr_session]
                sets_per_ex = session_df.groupby("Exercise")["Set"].count().reset_index(name="Sets")
                fig_pie = px.pie(sets_per_ex, names="Exercise", values="Sets", title=f"Anzahl Sets pro Exercise (Session {repr_session})")
                st.plotly_chart(fig_pie, use_container_width=True)

        # Balkendiagramm: Ø Sessions bis Gewichtserhöhung
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

        # --- Neue Diagrammreihe: Gewichtsentwicklung & Reps pro Exercise ---
        st.markdown("---")
        st.subheader("Verlauf: Gewicht & Wiederholungen pro Übung über Sessions")
        col3, col4 = st.columns([1, 1])

        exercises = df["Exercise"].unique()
        st.markdown("**Wähle Übungen für die Diagramme:**")
        selected_exs = []
        for ex in exercises:
            if st.toggle(f"{ex}", value=(ex == exercises[0])):
                selected_exs.append(ex)

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

        # --- MUSCLE GROUP VISUALIZATION SECTION (moved below graphs) ---
        st.markdown("---")
        st.subheader("Muskelgruppen-Visualisierung für Übungen")
        st.markdown("Wähle eine Übung, um die trainierten Muskelgruppen am Körper hervorzuheben. Die Zuordnung kann unten bearbeitet werden.")

        # Load mapping
        mapping = load_mapping()
        unique_exs = get_unique_exercises(df)

        # Exercise selector for visualization
        selected_ex_vis = st.selectbox("Übung auswählen:", unique_exs, key="muscle_vis_ex_select")
        muscles_for_ex = mapping.get(selected_ex_vis, [])


        # Show SVG with highlighted muscles (existing)
        st.markdown(get_body_svg(muscles_for_ex), unsafe_allow_html=True)

        # Show Realistic HTML/CSS Human Body (new)
        import streamlit.components.v1 as components
        st.markdown("<br><b>Realistische Körperdarstellung (SVG):</b>", unsafe_allow_html=True)
        # Map major muscle groups to SVG classes for highlighting
        muscle_class_map = {
            "Chest": "chest",
            "Back": "back",
            "Shoulders": ["left-shoulder", "right-shoulder"],
            "Biceps": ["left-arm", "right-arm"],
            "Triceps": [],  # If you have triceps SVGs, add their classes here
            "Legs": ["left-leg", "right-leg"],
            "Glutes": "stomach",  # Or the correct SVG class for glutes
            "Core": "stomach",    # Or the correct SVG class for core
        }
        highlight_classes = set()
        for m in muscles_for_ex:
            val = muscle_class_map.get(m)
            if isinstance(val, list):
                highlight_classes.update(val)
            elif isinstance(val, str):
                highlight_classes.add(val)
        components.html(render_realistic_body_html(list(highlight_classes)), height=400)

        # --- Editable Mapping UI (in Expander, less prominent) ---
        with st.expander("Muskelgruppen-Zuordnung bearbeiten (optional)", expanded=False):
            st.caption("Hier kannst du die Zuordnung von Übungen zu Muskelgruppen anpassen. In der Regel ist dies nur einmal nötig.")
            with st.form("edit_muscle_mapping"):
                new_mapping = {}
                for ex in unique_exs:
                    sel = st.multiselect(f"{ex}", MAJOR_MUSCLES, default=mapping.get(ex, []), key=f"map_{ex}")
                    new_mapping[ex] = sel
                submitted = st.form_submit_button("Speichern")
                if submitted:
                    save_mapping(new_mapping)
                    st.success("Muskelgruppen-Zuordnung gespeichert. Änderungen werden nach Neuladen sichtbar.")

        st.markdown("---")

        # --- Data Table in Expander ---
        with st.expander("Details als Tabelle anzeigen (optional)", expanded=False):
            st.caption("Hier siehst du alle Trainingsdaten als Tabelle. Für die meisten Nutzer sind die Diagramme oben ausreichend.")
            st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No data found in this CSV.")
else:
    st.info("Bitte wähle einen Trainingsplan in der Sidebar aus.")
