
# Training-Analysis

## Project Overview
This project analyzes Apple Numbers training plan files (`.numbers`) and CSVs from the `Trainingspläne/` directory. The main logic is in `src/main.py`, which parses CSVs into structured models for further analysis. `.numbers` files are currently only listed (no IWA parsing yet). The codebase is scaffolded for future expansion to real Numbers parsing and deeper analysis.

## Architecture & Data Flow
- **Entry Point:** `src/main.py` (see `if __name__ == "__main__"`)
- **Input Data:** `.numbers` and `.csv` files in `Trainingspläne/` (relative to project root)
- **CSV Parsing:** `load_training_plan_from_csv()` in `src/main.py` parses CSVs into `TrainingPlan`, `Exercise`, and `Set` dataclasses. Parsing logic is highly positional and plan-type specific.
- **Numbers Files:** Only archive listing is implemented (see `extract_numbers_structure()` if present). No IWA parsing yet.
- **Data Processing:** `src/data_processing.py` is a placeholder for future transformation logic.
- **Streamlit App:** `src/app.py` is intended for interactive UI (WIP, see UI/UX below).

## Developer Workflows
- **Run CLI Analysis:**
	- `python src/main.py` (from project root)
	- Prompts user to select a CSV, parses it, and prints structured data
- **Run Streamlit App:**
	- `streamlit run src/app.py` (from project root)
	- If `streamlit` is missing, install with `pip install streamlit`
- **Add/Update Training Plans:**
	- Place new `.numbers` or `.csv` files in `Trainingspläne/` or its `numbers/` subfolder
- **Testing:**
	- Minimal: see `tests/test_placeholder.py` (expand as needed)
- **Dependencies:**
	- List in `requirements.txt` (add e.g. `pytest`, `streamlit` as needed)
- **Virtual Environment:**
	- Recommended: `python -m venv .venv && source .venv/bin/activate`
	- Install dependencies: `pip install -r requirements.txt`

## Project Conventions & Patterns
- **CSV Parsing:** Parsing is positional and plan-type specific. See `load_training_plan_from_csv()` in `src/main.py` for the mapping logic. Plan names (e.g., "Krafttraining 1") determine row/column mapping.
- **Relative Paths:** All scripts expect to be run from the project root. Data is in `Trainingspläne/` (not `src/`).
- **Separation of Concerns:**
	- `src/main.py`: CLI entry, file discovery, CSV parsing
	- `src/app.py`: Streamlit UI (WIP)
	- `src/data_processing.py`: Data processing utilities (expand as needed)
- **No external APIs or integrations**
- **Keep code and data in their respective folders (`src/`, `tests/`, `Trainingspläne/`)

## Key Files & Directories
- `src/main.py`: Main CLI logic, CSV parsing
- `src/app.py`: Streamlit app (run with `streamlit run src/app.py`)
- `src/data_processing.py`: Data processing utilities (expand as needed)
- `tests/test_placeholder.py`: Placeholder for tests
- `Trainingspläne/`: Input `.numbers` and `.csv` files
- `requirements.txt`: Python dependencies

## Example: Adding a New Analysis
1. Add your `.numbers` or `.csv` file to `Trainingspläne/`
2. Extend `load_training_plan_from_csv()` or add new parsing logic in `src/main.py` or `src/data_processing.py`
3. Add/expand tests in `tests/`

## UI/UX Guidelines: Material Design (M3)
When building or updating the Streamlit UI (`src/app.py`), follow Material Design 3 (M3) principles for a modern, accessible, and expressive user experience:

- **Color:** Use vibrant, contrasting color palettes to create visual hierarchy and highlight key actions ([M3 Color System](https://m3.material.io/styles/color/system/overview)).
- **Motion:** Apply intuitive, purposeful motion for transitions and feedback (e.g., loading, navigation) ([M3 Motion](https://m3.material.io/styles/motion/overview)).
- **Components:** Prefer adaptive, expressive components (buttons, toolbars, progress indicators) that respond to user interaction ([M3 Components](https://m3.material.io/components)).
- **Typography:** Use clear, flexible typography for readability and emphasis ([M3 Typography](https://m3.material.io/styles/typography/overview)).
- **Shape:** Incorporate contrasting shapes (rounded, cut, or decorative) to add personality and guide attention ([M3 Shape](https://m3.material.io/styles/shape/overview-principles)).
- **Accessibility:** Ensure sufficient color contrast, clear focus states, and keyboard navigation.
- **Consistency:** Maintain consistent spacing, alignment, and component usage across screens.

For more, see the official [Material Design 3 guidelines](https://m3.material.io/).
