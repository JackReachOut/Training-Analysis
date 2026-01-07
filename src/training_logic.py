import io
import datetime
def generate_sample_csv():
    """
    Returns a sample CSV (as bytes) matching the expected structure for upload/download.
    """
    # Example: 2 exercises, 2 sessions, 2 sets each
    data = [
        ["", "Session 1", "Session 2"],
        ["Planname", "", ""],
        ["Kniebeuge", "", ""],
        ["60", "65", ""],
        ["WD", 8, 7],
        ["WD", 8, 7],
        ["Bankdrücken", "", ""],
        ["40", "42.5", ""],
        ["WD", 10, 9],
        ["WD", 10, 9],
    ]
    df = pd.DataFrame(data)
    output = io.StringIO()
    df.to_csv(output, sep=';', header=False, index=False)
    return output.getvalue().encode("utf-8")
import pandas as pd
import glob
import os
from dataclasses import dataclass, field
from typing import List

def parse_float(val):
    """
    Convert a value to float, handling both comma and period as decimal separator.
    Returns 0 if value is NaN or cannot be converted.
    """
    if pd.isna(val):
        return 0.0
    try:
        return float(str(val).replace(',', '.'))
    except Exception:
        return 0.0

@dataclass
class Set:
    reps: int
    weight: float

@dataclass
class Exercise:
    name: str
    sets: int
    set_list: List[Set] = field(default_factory=list)

@dataclass
class TrainingPlan:
    name: str
    exercises: List[Exercise] = field(default_factory=list)

def load_training_plan_from_csv(csv_path):
    df = pd.read_csv(csv_path, header=None, delimiter=';')
    training_plans = []
    num_cols = df.shape[1]
    plan_name = str(df.iloc[1, 0]) if pd.notna(df.iloc[1, 0]) else None

    # Dynamische Block-Erkennung: Suche alle Zeilen, in denen ein Übungsname steht (erste Spalte, nicht leer, nicht "WD", nicht Gewicht, nicht Zahl)
    exercise_blocks = []
    for idx in range(df.shape[0]):
        val = str(df.iloc[idx, 0])
        if val and val.strip() and val.strip() != 'WD' and not val.strip().replace('.', '', 1).isdigit() and not any(x in val.lower() for x in ['kg', 'wd', 'wiederholung', 'satz', 'pause']):
            # Prüfe, ob darunter ein Gewicht steht (nächste Zeile ist float oder Zahl)
            if idx+1 < df.shape[0]:
                kg_val = str(df.iloc[idx+1, 0])
                if kg_val and (kg_val.replace(',', '.').replace('-', '').replace(' ', '').replace('.', '', 1).isdigit() or 'kg' in kg_val.lower()):
                    exercise_blocks.append(idx)

    # Finde für jeden Block das Ende (nächster Block oder Dateiende)
    block_ranges = []
    for i, start in enumerate(exercise_blocks):
        end = exercise_blocks[i+1] if i+1 < len(exercise_blocks) else df.shape[0]
        block_ranges.append((start, end))

    for col in range(1, num_cols):
        # Überspringe leere Trainingstage
        if all(pd.isna(df.iloc[row, col]) for row in range(df.shape[0])):
            continue
        exercises = []
        for block_start, block_end in block_ranges:
            name = str(df.iloc[block_start, 0]).strip()
            kg_row = block_start + 1
            weight = parse_float(df.iloc[kg_row, col]) if kg_row < df.shape[0] else 0.0
            # Sätze: Zeilen im Block, die "WD" in Spalte 0 haben, enthalten die Wiederholungen in Spalte col
            sets = []
            for row in range(block_start+2, block_end):
                if str(df.iloc[row, 0]).strip() == 'WD':
                    reps = int(df.iloc[row, col]) if pd.notna(df.iloc[row, col]) else 0
                    sets.append(Set(reps=reps, weight=weight))
            if sets:
                exercises.append(Exercise(name=name, sets=len(sets), set_list=sets))
        if exercises:
            training_plans.append(TrainingPlan(name=plan_name, exercises=exercises))
    return training_plans

def get_csv_path(directory, filename):
    search_pattern = os.path.join(directory, filename)
    matches = glob.glob(search_pattern)
    if matches:
        return matches[0]
    else:
        raise FileNotFoundError(f"No file named '{filename}' found in '{directory}'.")
