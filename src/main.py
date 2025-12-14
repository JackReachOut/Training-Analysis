

import os
import pandas as pd
import glob
import matplotlib.pyplot as plt

CSV_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Trainingsplanner/Trainingspläne'))

def find_csv_files(directory):
	return sorted(glob.glob(os.path.join(directory, '*.csv')))

def parse_workout_csv(file_path):
	# Read with ; as separator, no header
	df = pd.read_csv(file_path, sep=';', header=None, dtype=str)
	# The first row is week labels, rest is special structure
	weeks = [str(w).strip() for w in df.iloc[0, 1:].tolist()]
	data = []
	i = 1
	while i < len(df):
		row = df.iloc[i]
		first_cell = str(row[0]).strip() if pd.notna(row[0]) else ''
		# Skip section markers, empty, or nan rows
		if first_cell in ['-', '*', '', 'nan']:
			i += 1
			continue
		# Only treat as exercise if not KG/WD and not a time (e.g., '10 min.')
		if first_cell in ['KG', 'WD'] or 'min.' in first_cell:
			i += 1
			continue
		exercise = first_cell
		i += 1
		# Collect KG and WD rows for this exercise
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

def main():
	csv_files = find_csv_files(CSV_DIR)
	print(f"Found {len(csv_files)} CSV files:")
	for f in csv_files:
		print(f"  {os.path.basename(f)}")

	all_data = []
	for f in csv_files:
		workout_data = parse_workout_csv(f)
		all_data.append({'file': os.path.basename(f), 'data': workout_data})

	# Aggregate data per exercise
	exercise_dict = {}
	for entry in all_data:
		for ex in entry['data']:
			name = ex['exercise']
			weeks = ex['weeks']
			# Use first KG/WD row for each exercise (per file)
			kg_row = ex['kg'][0] if ex['kg'] else [None]*len(weeks)
			wd_row = ex['wd'][0] if ex['wd'] else [None]*len(weeks)
			if name not in exercise_dict:
				exercise_dict[name] = {'week': [], 'weight': [], 'sets': []}
			for w, k, d in zip(weeks, kg_row, wd_row):
				if w:
					# Only add if at least one of k or d is not None/empty
					k_val = float(k) if k and k.replace('.', '', 1).isdigit() else None
					d_val = int(d) if d and d.isdigit() else None
					if k_val is not None or d_val is not None:
						exercise_dict[name]['week'].append(w)
						exercise_dict[name]['weight'].append(k_val)
						exercise_dict[name]['sets'].append(d_val)

	# Plot progression for each exercise
	for name, vals in exercise_dict.items():
		if not vals['week']:
			continue
		fig, ax1 = plt.subplots()
		ax1.set_title(f"{name} - Weight and Sets Progression")
		ax1.set_xlabel("Week")
		ax1.set_ylabel("Weight (kg)", color='tab:blue')
		ax1.plot(vals['week'], vals['weight'], marker='o', color='tab:blue', label='Weight')
		ax1.tick_params(axis='y', labelcolor='tab:blue')
		ax2 = ax1.twinx()
		ax2.set_ylabel("Sets", color='tab:orange')
		ax2.plot(vals['week'], vals['sets'], marker='x', color='tab:orange', label='Sets')
		ax2.tick_params(axis='y', labelcolor='tab:orange')
		fig.tight_layout()
		plt.show()

if __name__ == '__main__':
	main()
