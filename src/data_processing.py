import os
import pandas as pd

def find_csv_files(directory):
    import glob
    return sorted(glob.glob(os.path.join(directory, '*.csv')))

def parse_workout_csv(file_path):
    df = pd.read_csv(file_path, sep=';', header=None, dtype=str)
    weeks = [str(w).strip() for w in df.iloc[0, 1:].tolist()]
    data = []
    i = 1
    while i < len(df):
        row = df.iloc[i]
        first_cell = str(row[0]).strip() if pd.notna(row[0]) else ''
        if first_cell in ['-', '*', '', 'nan']:
            i += 1
            continue
        if first_cell in ['KG', 'WD'] or 'min.' in first_cell:
            i += 1
            continue
        exercise = first_cell
        i += 1
        kg, wd = [], []
        while i < len(df):
            subrow = df.iloc[i]
            subcell = str(subrow[0]).strip() if pd.notna(subrow[0]) else ''
            if subcell == 'KG':
                kg.append([str(x).strip() for x in subrow[1:].tolist()])
                i += 1
            elif subcell == 'WD':
                wd.append([str(x).strip() for x in subrow[1:].tolist()])
                i += 1
            else:
                break
        data.append({
            'exercise': exercise,
            'kg': kg,
            'wd': wd,
            'weeks': weeks
        })
    return data

def aggregate_exercise_data(all_data):
    exercise_dict = {}
    for entry in all_data:
        for ex in entry['data']:
            name = ex['exercise']
            weeks = ex['weeks']
            kg_row = ex['kg'][0] if ex['kg'] else [None]*len(weeks)
            wd_row = ex['wd'][0] if ex['wd'] else [None]*len(weeks)
            if name not in exercise_dict:
                exercise_dict[name] = {'week': [], 'weight': [], 'sets': []}
            for w, k, d in zip(weeks, kg_row, wd_row):
                if w:
                    k_val = float(k) if k and k.replace('.', '', 1).isdigit() else None
                    d_val = int(d) if d and d.isdigit() else None
                    if k_val is not None or d_val is not None:
                        exercise_dict[name]['week'].append(w)
                        exercise_dict[name]['weight'].append(k_val)
                        exercise_dict[name]['sets'].append(d_val)
    return exercise_dict
