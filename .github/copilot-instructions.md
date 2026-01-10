




# Copilot Instructions for Training-Analysis


## Project Overview & Architecture
This project analyzes Apple Numbers (`.numbers`) and CSV training plan files from `Trainingspläne/`, providing interactive analysis via a Streamlit dashboard. The architecture is designed for extensibility, with strict separation between data, parsing logic, and UI. All scripts expect to be run from the project root.


### Major Components
- **Entrypoint:** `src/main.py` (launches Streamlit UI; not a CLI parser)
- **Streamlit UI:** `src/app.py` (dashboard, run with `streamlit run src/app.py`)
- **CSV Parsing:** `load_training_plan_from_csv()` in `src/training_logic.py` parses CSVs into structured dataclasses (`TrainingPlan`, `Exercise`, `Set`). Parsing is highly positional and plan-type specific; plan names determine mapping logic. See code for block/row detection.
- **Numbers Files:** Only archive listing is implemented (no IWA parsing yet).
- **Data Directory:** All input data is in `Trainingspläne/` (CSV and Numbers files).


## Developer Workflows
- **Run Streamlit App:**
    - `python src/main.py` (preferred; launches Streamlit UI)
    - Or: `streamlit run src/app.py` (from project root)
    - If `streamlit` is missing, install with `pip install streamlit`
- **Add/Update Training Plans:**
    - Place new `.numbers` or `.csv` files in `Trainingspläne/` or its `numbers/` subfolder
- **Testing:**
    - No tests/ directory by default; add tests as needed
- **Dependencies:**
    - No `requirements.txt` by default; add and maintain as needed
- **Virtual Environment:**
    - Recommended: `python -m venv .venv && source .venv/bin/activate`
    - Install dependencies: `pip install -r requirements.txt`
- **Debugging:**
    - Use the VS Code debug task or run with `python -m debugpy --listen 5678 --wait-for-client src/main.py`


## Project Conventions & Patterns
- **Strict separation:**
    - `src/main.py`: Entrypoint, launches UI
    - `src/app.py`: Streamlit UI (all user interaction)
    - `src/training_logic.py`: CSV parsing logic (plan-specific, positional)
    - `src/data_processing.py`: Data processing utilities (expand as needed)
- **CSV Parsing:** Highly positional and plan-type specific. See `load_training_plan_from_csv()` in `src/training_logic.py` for block/row mapping logic. Each plan type may require custom mapping.
- **Relative Paths:** All scripts expect to be run from the project root. Data is in `Trainingspläne/` (not `src/`).
- **No external APIs or integrations.**
- **Keep code and data in their respective folders (`src/`, `Trainingspläne/`).**


## Example: Adding a New Plan Type or Analysis
1. Add your `.numbers` or `.csv` file to `Trainingspläne/`
2. Extend `load_training_plan_from_csv()` or add new parsing logic in `src/training_logic.py` (for new plan types, update block/row detection logic)
3. Add/expand tests (if a `tests/` directory exists)


## UI/UX Guidelines (Streamlit)
When updating `src/app.py`, follow Material Design 3 (M3) principles:
- Use vibrant, contrasting color palettes for hierarchy ([M3 Color System](https://m3.material.io/styles/color/system/overview))
- Apply intuitive motion for transitions ([M3 Motion](https://m3.material.io/styles/motion/overview))
- Prefer adaptive, expressive components ([M3 Components](https://m3.material.io/components))
- Ensure accessibility: color contrast, focus states, keyboard navigation

For more, see [Material Design 3 guidelines](https://m3.material.io/).
