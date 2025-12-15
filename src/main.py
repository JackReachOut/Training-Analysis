import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List

#define model data (string nameoftrainingplan, model list exercise(string name, int sets, model list set(int reps, int weight)))
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

# Function to load a training plan from a CSV file
def load_training_plan_from_csv(csv_path: str) -> TrainingPlan:
	df = pd.read_csv(csv_path, header=None, delimiter=';')
	# Get training plan name from cell A2 (row 1, col 0)
	plan_name = str(df.iloc[1, 0])
	exercises = []

	if plan_name == "Krafttraining 1":
		# Exercise 1: name from A7, sets from count of 'WD' between 'KG' in A8 and '-' in A11
		ex1_name = str(df.iloc[6, 0])
		ex1_kg_row = 7  # A8
		ex1_dash_row = 10  # A11
		ex1_sets = df.iloc[ex1_kg_row:ex1_dash_row+1, 0].tolist().count('WD')
		ex1_set1_reps = int(df.iloc[8, 1]) if pd.notna(df.iloc[8, 1]) else 0  # B9
		ex1_set1_weight = float(df.iloc[7, 1]) if pd.notna(df.iloc[7, 1]) else 0  # B8
		ex1_set2_reps = int(df.iloc[9, 1]) if pd.notna(df.iloc[9, 1]) else 0  # B10
		ex1_set2_weight = float(df.iloc[7, 1]) if pd.notna(df.iloc[7, 1]) else 0  # B8
		ex1_sets_list = [Set(reps=ex1_set1_reps, weight=ex1_set1_weight), Set(reps=ex1_set2_reps, weight=ex1_set2_weight)]
		exercises.append(Exercise(name=ex1_name, sets=ex1_sets, set_list=ex1_sets_list))

		# Exercise 2: name from A12, sets from count of 'WD' between 'KG' in A13 and '-' in A16
		ex2_name = str(df.iloc[11, 0])
		ex2_kg_row = 12  # A13
		ex2_dash_row = 15  # A16
		ex2_sets = df.iloc[ex2_kg_row:ex2_dash_row+1, 0].tolist().count('WD')
		ex2_set1_reps = int(df.iloc[13, 1]) if pd.notna(df.iloc[13, 1]) else 0  # B14
		ex2_set1_weight = float(df.iloc[12, 1]) if pd.notna(df.iloc[12, 1]) else 0  # B13
		ex2_set2_reps = int(df.iloc[14, 1]) if pd.notna(df.iloc[14, 1]) else 0  # B15
		ex2_set2_weight = float(df.iloc[12, 1]) if pd.notna(df.iloc[12, 1]) else 0  # B13
		ex2_sets_list = [Set(reps=ex2_set1_reps, weight=ex2_set1_weight), Set(reps=ex2_set2_reps, weight=ex2_set2_weight)]
		exercises.append(Exercise(name=ex2_name, sets=ex2_sets, set_list=ex2_sets_list))

		# Exercise 3: name from A17, sets from count of 'WD' between 'KG' in A18 and '-' in A21
		ex3_name = str(df.iloc[16, 0])
		ex3_kg_row = 17  # A18
		ex3_dash_row = 20  # A21
		ex3_sets = df.iloc[ex3_kg_row:ex3_dash_row+1, 0].tolist().count('WD')
		ex3_set1_reps = int(df.iloc[18, 1]) if pd.notna(df.iloc[18, 1]) else 0  # B19
		ex3_set1_weight = float(df.iloc[17, 1]) if pd.notna(df.iloc[17, 1]) else 0  # B18
		ex3_set2_reps = int(df.iloc[19, 1]) if pd.notna(df.iloc[19, 1]) else 0  # B20
		ex3_set2_weight = float(df.iloc[17, 1]) if pd.notna(df.iloc[17, 1]) else 0  # B18
		ex3_sets_list = [Set(reps=ex3_set1_reps, weight=ex3_set1_weight), Set(reps=ex3_set2_reps, weight=ex3_set2_weight)]
		exercises.append(Exercise(name=ex3_name, sets=ex3_sets, set_list=ex3_sets_list))

		# Exercise 4: name from A22, sets from count of 'WD' between 'KG' in A23 and '*' in A29
		ex4_name = str(df.iloc[21, 0])
		ex4_kg_row = 22  # A23
		ex4_dash_row = 28  # A29
		ex4_sets = df.iloc[ex4_kg_row:ex4_dash_row+1, 0].tolist().count('WD')
		ex4_set1_reps = int(df.iloc[23, 1]) if pd.notna(df.iloc[23, 1]) else 0  # B24
		ex4_set1_weight = float(df.iloc[22, 1]) if pd.notna(df.iloc[22, 1]) else 0  # B23
		ex4_set2_reps = int(df.iloc[24, 1]) if pd.notna(df.iloc[24, 1]) else 0  # B25
		ex4_set2_weight = float(df.iloc[22, 1]) if pd.notna(df.iloc[22, 1]) else 0  # B23
		ex4_set3_reps = int(df.iloc[25, 1]) if pd.notna(df.iloc[25, 1]) else 0  # B26
		ex4_set3_weight = float(df.iloc[22, 1]) if pd.notna(df.iloc[22, 1]) else 0  # B23
		ex4_set4_reps = int(df.iloc[26, 1]) if pd.notna(df.iloc[26, 1]) else 0  # B27
		ex4_set4_weight = float(df.iloc[22, 1]) if pd.notna(df.iloc[22, 1]) else 0  # B23
		ex4_set5_reps = int(df.iloc[27, 1]) if pd.notna(df.iloc[27, 1]) else 0  # B28
		ex4_set5_weight = float(df.iloc[22, 1]) if pd.notna(df.iloc[22, 1]) else 0  # B23
		ex4_sets_list = [Set(reps=ex4_set1_reps, weight=ex4_set1_weight), Set(reps=ex4_set2_reps, weight=ex4_set2_weight), Set(reps=ex4_set3_reps, weight=ex4_set3_weight), Set(reps=ex4_set4_reps, weight=ex4_set4_weight), Set(reps=ex4_set5_reps, weight=ex4_set5_weight)]
		exercises.append(Exercise(name=ex4_name, sets=ex4_sets, set_list=ex4_sets_list))

	if plan_name == "Krafttraining 2 " or plan_name == "Krafttraining 3" or plan_name == "Krafttraining 4" or plan_name == "Krafttraining 5":
		# Exercise 1: name from A7, sets from count of 'WD' between 'KG' in A8 and '-' in A12
		ex1_name = str(df.iloc[6, 0])
		ex1_kg_row = 7  # A8
		ex1_dash_row = 11  # A12
		ex1_sets = df.iloc[ex1_kg_row:ex1_dash_row+1, 0].tolist().count('WD')
		ex1_set1_reps = int(df.iloc[8, 1]) if pd.notna(df.iloc[8, 1]) else 0  # B9
		ex1_set1_weight = float(df.iloc[7, 1]) if pd.notna(df.iloc[7, 1]) else 0  # B8
		ex1_set2_reps = int(df.iloc[9, 1]) if pd.notna(df.iloc[9, 1]) else 0  # B10
		ex1_set2_weight = float(df.iloc[7, 1]) if pd.notna(df.iloc[7, 1]) else 0  # B8
		ex1_set3_reps = int(df.iloc[10, 1]) if pd.notna(df.iloc[10, 1]) else 0  # B11
		ex1_set3_weight = float(df.iloc[7, 1]) if pd.notna(df.iloc[7, 1]) else 0  # B8
		ex1_sets_list = [Set(reps=ex1_set1_reps, weight=ex1_set1_weight), Set(reps=ex1_set2_reps, weight=ex1_set2_weight), Set(reps=ex1_set3_reps, weight=ex1_set3_weight)]
		exercises.append(Exercise(name=ex1_name, sets=ex1_sets, set_list=ex1_sets_list))

		# Exercise 2: name from A13, sets from count of 'WD' between 'KG' in A14 and '-' in A18
		ex2_name = str(df.iloc[12, 0])
		ex2_kg_row = 13  # A14
		ex2_dash_row = 17  # A18
		ex2_sets = df.iloc[ex2_kg_row:ex2_dash_row+1, 0].tolist().count('WD')
		ex2_set1_reps = int(df.iloc[14, 1]) if pd.notna(df.iloc[14, 1]) else 0  # B15
		ex2_set1_weight = float(df.iloc[12, 1]) if pd.notna(df.iloc[12, 1]) else 0  # B14
		ex2_set2_reps = int(df.iloc[15, 1]) if pd.notna(df.iloc[15, 1]) else 0  # B16
		ex2_set2_weight = float(df.iloc[12, 1]) if pd.notna(df.iloc[12, 1]) else 0  # B14
		ex2_set3_reps = int(df.iloc[16, 1]) if pd.notna(df.iloc[16, 1]) else 0  # B17
		ex2_set3_weight = float(df.iloc[12, 1]) if pd.notna(df.iloc[12, 1]) else 0  # B14
		ex2_sets_list = [Set(reps=ex2_set1_reps, weight=ex2_set1_weight), Set(reps=ex2_set2_reps, weight=ex2_set2_weight), Set(reps=ex2_set3_reps, weight=ex2_set3_weight)]
		exercises.append(Exercise(name=ex2_name, sets=ex2_sets, set_list=ex2_sets_list))

		# Exercise 3: name from A19, sets from count of 'WD' between 'KG' in A20 and '-' in A24
		ex3_name = str(df.iloc[18, 0])
		ex3_kg_row = 19  # A20
		ex3_dash_row = 23  # A24
		ex3_sets = df.iloc[ex3_kg_row:ex3_dash_row+1, 0].tolist().count('WD')
		ex3_set1_reps = int(df.iloc[20, 1]) if pd.notna(df.iloc[20, 1]) else 0  # B21
		ex3_set1_weight = float(df.iloc[19, 1]) if pd.notna(df.iloc[19, 1]) else 0  # B20
		ex3_set2_reps = int(df.iloc[21, 1]) if pd.notna(df.iloc[21, 1]) else 0  # B22
		ex3_set2_weight = float(df.iloc[19, 1]) if pd.notna(df.iloc[19, 1]) else 0  # B20
		ex3_set3_reps = int(df.iloc[22, 1]) if pd.notna(df.iloc[22, 1]) else 0  # B23
		ex3_set3_weight = float(df.iloc[19, 1]) if pd.notna(df.iloc[19, 1]) else 0  # B20
		ex3_sets_list = [Set(reps=ex3_set1_reps, weight=ex3_set1_weight), Set(reps=ex3_set2_reps, weight=ex3_set2_weight), Set(reps=ex3_set3_reps, weight=ex3_set3_weight)]
		exercises.append(Exercise(name=ex3_name, sets=ex3_sets, set_list=ex3_sets_list))

		# Exercise 4: name from A22, sets from count of 'WD' between 'KG' in A26 and '*' in A30
		ex4_name = str(df.iloc[24, 0])
		ex4_kg_row = 25  # A26
		ex4_dash_row = 29  # A30
		ex4_sets = df.iloc[ex4_kg_row:ex4_dash_row+1, 0].tolist().count('WD')
		ex4_set1_reps = int(df.iloc[26, 1]) if pd.notna(df.iloc[26, 1]) else 0  # B27
		ex4_set1_weight = float(df.iloc[25, 1]) if pd.notna(df.iloc[25, 1]) else 0  # B26
		ex4_set2_reps = int(df.iloc[27, 1]) if pd.notna(df.iloc[27, 1]) else 0  # B28
		ex4_set2_weight = float(df.iloc[25, 1]) if pd.notna(df.iloc[25, 1]) else 0  # B26
		ex4_set3_reps = int(df.iloc[28, 1]) if pd.notna(df.iloc[28, 1]) else 0  # B29
		ex4_set3_weight = float(df.iloc[25, 1]) if pd.notna(df.iloc[25, 1]) else 0  # B26
		ex4_sets_list = [Set(reps=ex4_set1_reps, weight=ex4_set1_weight), Set(reps=ex4_set2_reps, weight=ex4_set2_weight), Set(reps=ex4_set3_reps, weight=ex4_set3_weight)]
		exercises.append(Exercise(name=ex4_name, sets=ex4_sets, set_list=ex4_sets_list))

	if plan_name == "Krafttraining 6":
		# Exercise 1: name from A7, sets from count of 'WD' between 'KG' in A8 and '-' in A13
		ex1_name = str(df.iloc[6, 0])
		ex1_kg_row = 7  # A8
		ex1_dash_row = 12  # A13
		ex1_sets = df.iloc[ex1_kg_row:ex1_dash_row+1, 0].tolist().count('WD')
		ex1_set1_reps = int(df.iloc[8, 1]) if pd.notna(df.iloc[8, 1]) else 0  # B9
		ex1_set1_weight = float(df.iloc[7, 1]) if pd.notna(df.iloc[7, 1]) else 0  # B8
		ex1_set2_reps = int(df.iloc[9, 1]) if pd.notna(df.iloc[9, 1]) else 0  # B10
		ex1_set2_weight = float(df.iloc[7, 1]) if pd.notna(df.iloc[7, 1]) else 0  # B8
		ex1_set3_reps = int(df.iloc[10, 1]) if pd.notna(df.iloc[10, 1]) else 0  # B11
		ex1_set3_weight = float(df.iloc[7, 1]) if pd.notna(df.iloc[7, 1]) else 0  # B8
		ex1_set4_reps = int(df.iloc[11, 1]) if pd.notna(df.iloc[11, 1]) else 0  # B12
		ex1_set4_weight = float(df.iloc[7, 1]) if pd.notna(df.iloc[7, 1]) else 0  # B8
		ex1_sets_list = [Set(reps=ex1_set1_reps, weight=ex1_set1_weight), Set(reps=ex1_set2_reps, weight=ex1_set2_weight), Set(reps=ex1_set3_reps, weight=ex1_set3_weight), Set(reps=ex1_set4_reps, weight=ex1_set4_weight)]
		exercises.append(Exercise(name=ex1_name, sets=ex1_sets, set_list=ex1_sets_list))

		# Exercise 2: name from A14, sets from count of 'WD' between 'KG' in A15 and '-' in A20
		ex2_name = str(df.iloc[13, 0])
		ex2_kg_row = 14  # A15
		ex2_dash_row = 19  # A20
		ex2_sets = df.iloc[ex2_kg_row:ex2_dash_row+1, 0].tolist().count('WD')
		ex2_set1_reps = int(df.iloc[15, 1]) if pd.notna(df.iloc[15, 1]) else 0  # B16
		ex2_set1_weight = float(df.iloc[14, 1]) if pd.notna(df.iloc[14, 1]) else 0  # B15
		ex2_set2_reps = int(df.iloc[16, 1]) if pd.notna(df.iloc[16, 1]) else 0  # B17
		ex2_set2_weight = float(df.iloc[14, 1]) if pd.notna(df.iloc[14, 1]) else 0  # B15
		ex2_set3_reps = int(df.iloc[17, 1]) if pd.notna(df.iloc[17, 1]) else 0  # B18
		ex2_set3_weight = float(df.iloc[14, 1]) if pd.notna(df.iloc[14, 1]) else 0  # B15
		ex2_set4_reps = int(df.iloc[18, 1]) if pd.notna(df.iloc[18, 1]) else 0  # B19
		ex2_set4_weight = float(df.iloc[14, 1]) if pd.notna(df.iloc[14, 1]) else 0  # B15
		ex2_sets_list = [Set(reps=ex2_set1_reps, weight=ex2_set1_weight), Set(reps=ex2_set2_reps, weight=ex2_set2_weight), Set(reps=ex2_set3_reps, weight=ex2_set3_weight), Set(reps=ex2_set4_reps, weight=ex2_set4_weight)]
		exercises.append(Exercise(name=ex2_name, sets=ex2_sets, set_list=ex2_sets_list))

		# Exercise 3: name from A21, sets from count of 'WD' between 'KG' in A22 and '-' in A27
		ex3_name = str(df.iloc[20, 0])
		ex3_kg_row = 21  # A22
		ex3_dash_row = 26  # A27
		ex3_sets = df.iloc[ex3_kg_row:ex3_dash_row+1, 0].tolist().count('WD')
		ex3_set1_reps = int(df.iloc[22, 1]) if pd.notna(df.iloc[22, 1]) else 0  # B23
		ex3_set1_weight = float(df.iloc[21, 1]) if pd.notna(df.iloc[21, 1]) else 0  # B22
		ex3_set2_reps = int(df.iloc[23, 1]) if pd.notna(df.iloc[23, 1]) else 0  # B24
		ex3_set2_weight = float(df.iloc[21, 1]) if pd.notna(df.iloc[21, 1]) else 0  # B22
		ex3_set3_reps = int(df.iloc[24, 1]) if pd.notna(df.iloc[24, 1]) else 0  # B25
		ex3_set3_weight = float(df.iloc[21, 1]) if pd.notna(df.iloc[21, 1]) else 0  # B22
		ex3_set4_reps = int(df.iloc[25, 1]) if pd.notna(df.iloc[25, 1]) else 0  # B26
		ex3_set4_weight = float(df.iloc[21, 1]) if pd.notna(df.iloc[21, 1]) else 0  # B22
		ex3_sets_list = [Set(reps=ex3_set1_reps, weight=ex3_set1_weight), Set(reps=ex3_set2_reps, weight=ex3_set2_weight), Set(reps=ex3_set3_reps, weight=ex3_set3_weight), Set(reps=ex3_set4_reps, weight=ex3_set4_weight)]
		exercises.append(Exercise(name=ex3_name, sets=ex3_sets, set_list=ex3_sets_list))

		# Exercise 4: name from A28, sets from count of 'WD' between 'KG' in A29 and '*' in A34
		ex4_name = str(df.iloc[27, 0])
		ex4_kg_row = 28  # A29
		ex4_dash_row = 33  # A34
		ex4_sets = df.iloc[ex4_kg_row:ex4_dash_row+1, 0].tolist().count('WD')
		ex4_set1_reps = int(df.iloc[29, 1]) if pd.notna(df.iloc[29, 1]) else 0  # B30
		ex4_set1_weight = float(df.iloc[28, 1]) if pd.notna(df.iloc[28, 1]) else 0  # B29
		ex4_set2_reps = int(df.iloc[30, 1]) if pd.notna(df.iloc[30, 1]) else 0  # B31
		ex4_set2_weight = float(df.iloc[28, 1]) if pd.notna(df.iloc[28, 1]) else 0  # B29
		ex4_set3_reps = int(df.iloc[31, 1]) if pd.notna(df.iloc[31, 1]) else 0  # B32
		ex4_set3_weight = float(df.iloc[28, 1]) if pd.notna(df.iloc[28, 1]) else 0  # B29
		ex4_set4_reps = int(df.iloc[32, 1]) if pd.notna(df.iloc[32, 1]) else 0  # B33
		ex4_set4_weight = float(df.iloc[28, 1]) if pd.notna(df.iloc[28, 1]) else 0  # B29
		ex4_set5_reps = int(df.iloc[33, 1]) if pd.notna(df.iloc[33, 1]) else 0  # B34
		ex4_set5_weight = float(df.iloc[28, 1]) if pd.notna(df.iloc[28, 1]) else 0  # B29
		ex4_sets_list = [Set(reps=ex4_set1_reps, weight=ex4_set1_weight), Set(reps=ex4_set2_reps, weight=ex4_set2_weight), Set(reps=ex4_set3_reps, weight=ex4_set3_weight), Set(reps=ex4_set4_reps, weight=ex4_set4_weight), Set(reps=ex4_set5_reps, weight=ex4_set5_weight)]
		exercises.append(Exercise(name=ex4_name, sets=ex4_sets, set_list=ex4_sets_list))


	else:
		# Placeholder for other TrainingPlan types
		# TODO: Implement import logic for other plan types
		pass

	return TrainingPlan(name=plan_name, exercises=exercises)



# Clean function to get a specific CSV file from a directory
def get_csv_path(directory, filename):
	"""Return the full path to a specific CSV file in a directory."""
	search_pattern = os.path.join(directory, filename)
	matches = glob.glob(search_pattern)
	if matches:
		return matches[0]
	else:
		raise FileNotFoundError(f"No file named '{filename}' found in '{directory}'.")

# Instantiate model for 1.Trainingsplan Jan Persico.csv

if __name__ == "__main__":
	trainings_dir = os.path.abspath("Trainingspläne")
	# Find all .csv files in the directory
	csv_files = sorted([f for f in os.listdir(trainings_dir) if f.lower().endswith('.csv')])
	if not csv_files:
		print("No .csv files found in Trainingspläne directory.")
		exit(1)
	print("Available CSV files:")
	for idx, fname in enumerate(csv_files, 1):
		print(f"  {idx}: {fname}")
	while True:
		try:
			choice = int(input(f"Select a file to analyze (1-{len(csv_files)}): "))
			if 1 <= choice <= len(csv_files):
				selected_file = csv_files[choice - 1]
				break
			else:
				print("Invalid selection. Try again.")
		except ValueError:
			print("Please enter a valid number.")
	csv_path = get_csv_path(trainings_dir, selected_file)
	data = load_training_plan_from_csv(csv_path)
	print(data)

