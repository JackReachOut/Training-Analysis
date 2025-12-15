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
    for col in range(1, num_cols):
        if pd.isna(df.iloc[8, col]) and pd.isna(df.iloc[13, col]) and pd.isna(df.iloc[18, col]):
            continue
        exercises = []
        if plan_name == "Krafttraining 1":
            ex1_name = str(df.iloc[6, 0])
            ex1_kg_row = 7
            ex1_dash_row = 10
            ex1_sets = df.iloc[ex1_kg_row:ex1_dash_row+1, 0].tolist().count('WD')
            ex1_set1_reps = int(df.iloc[8, col]) if pd.notna(df.iloc[8, col]) else 0
            ex1_set1_weight = parse_float(df.iloc[7, col])
            ex1_set2_reps = int(df.iloc[9, col]) if pd.notna(df.iloc[9, col]) else 0
            ex1_set2_weight = parse_float(df.iloc[7, col])
            ex1_sets_list = [Set(reps=ex1_set1_reps, weight=ex1_set1_weight), Set(reps=ex1_set2_reps, weight=ex1_set2_weight)]
            exercises.append(Exercise(name=ex1_name, sets=ex1_sets, set_list=ex1_sets_list))

            ex2_name = str(df.iloc[11, 0])
            ex2_kg_row = 12
            ex2_dash_row = 15
            ex2_sets = df.iloc[ex2_kg_row:ex2_dash_row+1, 0].tolist().count('WD')
            ex2_set1_reps = int(df.iloc[13, col]) if pd.notna(df.iloc[13, col]) else 0
            ex2_set1_weight = parse_float(df.iloc[12, col])
            ex2_set2_reps = int(df.iloc[14, col]) if pd.notna(df.iloc[14, col]) else 0
            ex2_set2_weight = parse_float(df.iloc[12, col])
            ex2_sets_list = [Set(reps=ex2_set1_reps, weight=ex2_set1_weight), Set(reps=ex2_set2_reps, weight=ex2_set2_weight)]
            exercises.append(Exercise(name=ex2_name, sets=ex2_sets, set_list=ex2_sets_list))

            ex3_name = str(df.iloc[16, 0])
            ex3_kg_row = 17
            ex3_dash_row = 20
            ex3_sets = df.iloc[ex3_kg_row:ex3_dash_row+1, 0].tolist().count('WD')
            ex3_set1_reps = int(df.iloc[18, col]) if pd.notna(df.iloc[18, col]) else 0
            ex3_set1_weight = parse_float(df.iloc[17, col])
            ex3_set2_reps = int(df.iloc[19, col]) if pd.notna(df.iloc[19, col]) else 0
            ex3_set2_weight = parse_float(df.iloc[17, col])
            ex3_sets_list = [Set(reps=ex3_set1_reps, weight=ex3_set1_weight), Set(reps=ex3_set2_reps, weight=ex3_set2_weight)]
            exercises.append(Exercise(name=ex3_name, sets=ex3_sets, set_list=ex3_sets_list))

            ex4_name = str(df.iloc[21, 0])
            ex4_kg_row = 22
            ex4_dash_row = 28
            ex4_sets = df.iloc[ex4_kg_row:ex4_dash_row+1, 0].tolist().count('WD')
            ex4_set1_reps = int(df.iloc[23, col]) if pd.notna(df.iloc[23, col]) else 0
            ex4_set1_weight = parse_float(df.iloc[22, col])
            ex4_set2_reps = int(df.iloc[24, col]) if pd.notna(df.iloc[24, col]) else 0
            ex4_set2_weight = parse_float(df.iloc[22, col])
            ex4_set3_reps = int(df.iloc[25, col]) if pd.notna(df.iloc[25, col]) else 0
            ex4_set3_weight = parse_float(df.iloc[22, col])
            ex4_set4_reps = int(df.iloc[26, col]) if pd.notna(df.iloc[26, col]) else 0
            ex4_set4_weight = parse_float(df.iloc[22, col])
            ex4_set5_reps = int(df.iloc[27, col]) if pd.notna(df.iloc[27, col]) else 0
            ex4_set5_weight = parse_float(df.iloc[22, col])
            ex4_sets_list = [Set(reps=ex4_set1_reps, weight=ex4_set1_weight), Set(reps=ex4_set2_reps, weight=ex4_set2_weight), Set(reps=ex4_set3_reps, weight=ex4_set3_weight), Set(reps=ex4_set4_reps, weight=ex4_set4_weight), Set(reps=ex4_set5_reps, weight=ex4_set5_weight)]
            exercises.append(Exercise(name=ex4_name, sets=ex4_sets, set_list=ex4_sets_list))

        elif plan_name in ["Krafttraining 2 ", "Krafttraining 3", "Krafttraining 4", "Krafttraining 5"]:
            ex1_name = str(df.iloc[6, 0])
            ex1_kg_row = 7
            ex1_dash_row = 11
            ex1_sets = df.iloc[ex1_kg_row:ex1_dash_row+1, 0].tolist().count('WD')
            ex1_set1_reps = int(df.iloc[8, col]) if pd.notna(df.iloc[8, col]) else 0
            ex1_set1_weight = parse_float(df.iloc[7, col])
            ex1_set2_reps = int(df.iloc[9, col]) if pd.notna(df.iloc[9, col]) else 0
            ex1_set2_weight = parse_float(df.iloc[7, col])
            ex1_set3_reps = int(df.iloc[10, col]) if pd.notna(df.iloc[10, col]) else 0
            ex1_set3_weight = parse_float(df.iloc[7, col])
            ex1_sets_list = [Set(reps=ex1_set1_reps, weight=ex1_set1_weight), Set(reps=ex1_set2_reps, weight=ex1_set2_weight), Set(reps=ex1_set3_reps, weight=ex1_set3_weight)]
            exercises.append(Exercise(name=ex1_name, sets=ex1_sets, set_list=ex1_sets_list))

            ex2_name = str(df.iloc[12, 0])
            ex2_kg_row = 13
            ex2_dash_row = 17
            ex2_sets = df.iloc[ex2_kg_row:ex2_dash_row+1, 0].tolist().count('WD')
            ex2_set1_reps = int(df.iloc[14, col]) if pd.notna(df.iloc[14, col]) else 0
            ex2_set1_weight = parse_float(df.iloc[12, col])
            ex2_set2_reps = int(df.iloc[15, col]) if pd.notna(df.iloc[15, col]) else 0
            ex2_set2_weight = parse_float(df.iloc[12, col])
            ex2_set3_reps = int(df.iloc[16, col]) if pd.notna(df.iloc[16, col]) else 0
            ex2_set3_weight = parse_float(df.iloc[12, col])
            ex2_sets_list = [Set(reps=ex2_set1_reps, weight=ex2_set1_weight), Set(reps=ex2_set2_reps, weight=ex2_set2_weight), Set(reps=ex2_set3_reps, weight=ex2_set3_weight)]
            exercises.append(Exercise(name=ex2_name, sets=ex2_sets, set_list=ex2_sets_list))

            ex3_name = str(df.iloc[18, 0])
            ex3_kg_row = 19
            ex3_dash_row = 23
            ex3_sets = df.iloc[ex3_kg_row:ex3_dash_row+1, 0].tolist().count('WD')
            ex3_set1_reps = int(df.iloc[20, col]) if pd.notna(df.iloc[20, col]) else 0
            ex3_set1_weight = parse_float(df.iloc[19, col])
            ex3_set2_reps = int(df.iloc[21, col]) if pd.notna(df.iloc[21, col]) else 0
            ex3_set2_weight = parse_float(df.iloc[19, col])
            ex3_set3_reps = int(df.iloc[22, col]) if pd.notna(df.iloc[22, col]) else 0
            ex3_set3_weight = parse_float(df.iloc[19, col])
            ex3_sets_list = [Set(reps=ex3_set1_reps, weight=ex3_set1_weight), Set(reps=ex3_set2_reps, weight=ex3_set2_weight), Set(reps=ex3_set3_reps, weight=ex3_set3_weight)]
            exercises.append(Exercise(name=ex3_name, sets=ex3_sets, set_list=ex3_sets_list))

            ex4_name = str(df.iloc[24, 0])
            ex4_kg_row = 25
            ex4_dash_row = 29
            ex4_sets = df.iloc[ex4_kg_row:ex4_dash_row+1, 0].tolist().count('WD')
            ex4_set1_reps = int(df.iloc[26, col]) if pd.notna(df.iloc[26, col]) else 0
            ex4_set1_weight = parse_float(df.iloc[25, col])
            ex4_set2_reps = int(df.iloc[27, col]) if pd.notna(df.iloc[27, col]) else 0
            ex4_set2_weight = parse_float(df.iloc[25, col])
            ex4_set3_reps = int(df.iloc[28, col]) if pd.notna(df.iloc[28, col]) else 0
            ex4_set3_weight = parse_float(df.iloc[25, col])
            ex4_sets_list = [Set(reps=ex4_set1_reps, weight=ex4_set1_weight), Set(reps=ex4_set2_reps, weight=ex4_set2_weight), Set(reps=ex4_set3_reps, weight=ex4_set3_weight)]
            exercises.append(Exercise(name=ex4_name, sets=ex4_sets, set_list=ex4_sets_list))

        elif plan_name == "Krafttraining 6":
            ex1_name = str(df.iloc[6, 0])
            ex1_kg_row = 7
            ex1_dash_row = 12
            ex1_sets = df.iloc[ex1_kg_row:ex1_dash_row+1, 0].tolist().count('WD')
            ex1_set1_reps = int(df.iloc[8, col]) if pd.notna(df.iloc[8, col]) else 0
            ex1_set1_weight = parse_float(df.iloc[7, col])
            ex1_set2_reps = int(df.iloc[9, col]) if pd.notna(df.iloc[9, col]) else 0
            ex1_set2_weight = parse_float(df.iloc[7, col])
            ex1_set3_reps = int(df.iloc[10, col]) if pd.notna(df.iloc[10, col]) else 0
            ex1_set3_weight = parse_float(df.iloc[7, col])
            ex1_set4_reps = int(df.iloc[11, col]) if pd.notna(df.iloc[11, col]) else 0
            ex1_set4_weight = parse_float(df.iloc[7, col])
            ex1_sets_list = [Set(reps=ex1_set1_reps, weight=ex1_set1_weight), Set(reps=ex1_set2_reps, weight=ex1_set2_weight), Set(reps=ex1_set3_reps, weight=ex1_set3_weight), Set(reps=ex1_set4_reps, weight=ex1_set4_weight)]
            exercises.append(Exercise(name=ex1_name, sets=ex1_sets, set_list=ex1_sets_list))

            ex2_name = str(df.iloc[13, 0])
            ex2_kg_row = 14
            ex2_dash_row = 19
            ex2_sets = df.iloc[ex2_kg_row:ex2_dash_row+1, 0].tolist().count('WD')
            ex2_set1_reps = int(df.iloc[15, col]) if pd.notna(df.iloc[15, col]) else 0
            ex2_set1_weight = parse_float(df.iloc[14, col])
            ex2_set2_reps = int(df.iloc[16, col]) if pd.notna(df.iloc[16, col]) else 0
            ex2_set2_weight = parse_float(df.iloc[14, col])
            ex2_set3_reps = int(df.iloc[17, col]) if pd.notna(df.iloc[17, col]) else 0
            ex2_set3_weight = parse_float(df.iloc[14, col])
            ex2_set4_reps = int(df.iloc[18, col]) if pd.notna(df.iloc[18, col]) else 0
            ex2_set4_weight = parse_float(df.iloc[14, col])
            ex2_sets_list = [Set(reps=ex2_set1_reps, weight=ex2_set1_weight), Set(reps=ex2_set2_reps, weight=ex2_set2_weight), Set(reps=ex2_set3_reps, weight=ex2_set3_weight), Set(reps=ex2_set4_reps, weight=ex2_set4_weight)]
            exercises.append(Exercise(name=ex2_name, sets=ex2_sets, set_list=ex2_sets_list))

            ex3_name = str(df.iloc[20, 0])
            ex3_kg_row = 21
            ex3_dash_row = 26
            ex3_sets = df.iloc[ex3_kg_row:ex3_dash_row+1, 0].tolist().count('WD')
            ex3_set1_reps = int(df.iloc[22, col]) if pd.notna(df.iloc[22, col]) else 0
            ex3_set1_weight = parse_float(df.iloc[21, col])
            ex3_set2_reps = int(df.iloc[23, col]) if pd.notna(df.iloc[23, col]) else 0
            ex3_set2_weight = parse_float(df.iloc[21, col])
            ex3_set3_reps = int(df.iloc[24, col]) if pd.notna(df.iloc[24, col]) else 0
            ex3_set3_weight = parse_float(df.iloc[21, col])
            ex3_set4_reps = int(df.iloc[25, col]) if pd.notna(df.iloc[25, col]) else 0
            ex3_set4_weight = parse_float(df.iloc[21, col])
            ex3_sets_list = [Set(reps=ex3_set1_reps, weight=ex3_set1_weight), Set(reps=ex3_set2_reps, weight=ex3_set2_weight), Set(reps=ex3_set3_reps, weight=ex3_set3_weight), Set(reps=ex3_set4_reps, weight=ex3_set4_weight)]
            exercises.append(Exercise(name=ex3_name, sets=ex3_sets, set_list=ex3_sets_list))

            ex4_name = str(df.iloc[27, 0])
            ex4_kg_row = 28
            ex4_dash_row = 33
            ex4_sets = df.iloc[ex4_kg_row:ex4_dash_row+1, 0].tolist().count('WD')
            ex4_set1_reps = int(df.iloc[29, col]) if pd.notna(df.iloc[29, col]) else 0
            ex4_set1_weight = parse_float(df.iloc[28, col])
            ex4_set2_reps = int(df.iloc[30, col]) if pd.notna(df.iloc[30, col]) else 0
            ex4_set2_weight = parse_float(df.iloc[28, col])
            ex4_set3_reps = int(df.iloc[31, col]) if pd.notna(df.iloc[31, col]) else 0
            ex4_set3_weight = parse_float(df.iloc[28, col])
            ex4_set4_reps = int(df.iloc[32, col]) if pd.notna(df.iloc[32, col]) else 0
            ex4_set4_weight = parse_float(df.iloc[28, col])
            ex4_set5_reps = int(df.iloc[33, col]) if pd.notna(df.iloc[33, col]) else 0
            ex4_set5_weight = parse_float(df.iloc[28, col])
            ex4_sets_list = [Set(reps=ex4_set1_reps, weight=ex4_set1_weight), Set(reps=ex4_set2_reps, weight=ex4_set2_weight), Set(reps=ex4_set3_reps, weight=ex4_set3_weight), Set(reps=ex4_set4_reps, weight=ex4_set4_weight), Set(reps=ex4_set5_reps, weight=ex4_set5_weight)]
            exercises.append(Exercise(name=ex4_name, sets=ex4_sets, set_list=ex4_sets_list))
        else:
            continue
        training_plans.append(TrainingPlan(name=plan_name, exercises=exercises))
        print(training_plans)
    return training_plans

def get_csv_path(directory, filename):
    search_pattern = os.path.join(directory, filename)
    matches = glob.glob(search_pattern)
    if matches:
        return matches[0]
    else:
        raise FileNotFoundError(f"No file named '{filename}' found in '{directory}'.")
