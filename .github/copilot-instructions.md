

# Copilot Instructions for Training-Analysis

## Project Purpose & Architecture
This project analyzes Apple Numbers (`.numbers`) and CSV training plan files from `Trainingspläne/`. The main logic is in `src/main.py` and `src/training_logic.py`. The codebase is designed for extensible parsing and analysis, with a Streamlit dashboard for interactive exploration.

### Key Components
- **CLI Entrypoint:** `src/main.py` (launches Streamlit app)
- **Streamlit UI:** `src/app.py` (interactive dashboard, run with `streamlit run src/app.py`)
- **CSV Parsing:** `load_training_plan_from_csv()` in `src/training_logic.py` parses CSVs into structured dataclasses (`TrainingPlan`, `Exercise`, `Set`). Parsing is highly positional and plan-type specific.
- **Numbers Files:** Only archive listing is implemented; no IWA parsing yet.
- **Data Location:** All input data is in `Trainingspläne/` (CSV and Numbers files).

### Developer Workflows
- **Run Dashboard:** `python src/main.py` or `streamlit run src/app.py` (from project root)
- **Add/Update Training Plans:** Place new `.csv` or `.numbers` files in `Trainingspläne/`
- **Dependencies:** List in `requirements.txt` (install with `pip install -r requirements.txt`)
- **Virtual Environment:** Use `.venv` (`python -m venv .venv && source .venv/bin/activate`)
- **Testing:** Minimal; expand as needed in `tests/`

### Project Conventions & Patterns
- **Relative Paths:** All scripts expect to be run from the project root.
- **Separation of Concerns:** Keep code in `src/`, data in `Trainingspläne/`, and tests in `tests/`.
- **CSV Parsing:** See `load_training_plan_from_csv()` in `src/training_logic.py` for plan-specific mapping logic.
- **No external APIs or integrations.**

### Example: Adding a New Analysis
1. Add your `.csv` or `.numbers` file to `Trainingspläne/`
2. Extend `load_training_plan_from_csv()` or add new logic in `src/training_logic.py`
3. Add/expand tests in `tests/`

### UI/UX Guidelines (Streamlit)
When updating `src/app.py`, follow Material Design 3 (M3) principles:
- Use vibrant, contrasting color palettes for hierarchy ([M3 Color System](https://m3.material.io/styles/color/system/overview))
- Apply intuitive motion for transitions ([M3 Motion](https://m3.material.io/styles/motion/overview))
- Prefer adaptive, expressive components ([M3 Components](https://m3.material.io/components))
- Ensure accessibility: color contrast, focus states, keyboard navigation

For more, see [Material Design 3 guidelines](https://m3.material.io/).
