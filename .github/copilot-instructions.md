

# Copilot Instructions for Training-Analysis

## Project Overview
This project analyzes Apple Numbers training plan files (`.numbers`) and CSVs from the `../Trainingspläne/` directory. The main logic is in `src/main.py`, which currently lists `.numbers` archive contents and demonstrates section parsing. The codebase is scaffolded for future expansion to real Numbers/IWA parsing and deeper analysis.

- **Streamlit App:** `src/app.py` is intended for interactive UI (see below for details)

- **Run CLI Analysis:**
  - `python src/main.py` (from project root)
- **Run Streamlit App:**
  - `streamlit run src/app.py` (from project root)
- **Add/Update Training Plans:**
- **Testing:**
- **Dependencies:**
- **Virtual Environment:**
  - Recommended: `python -m venv .venv && source .venv/bin/activate`
  - Install dependencies: `pip install -r requirements.txt`

- **Relative paths:** All scripts expect to be run from the project root
- **Separation of concerns:**
  - `src/main.py`: CLI entry, file discovery, demo parsing
- **No external APIs or integrations**
- **Keep code and data in their respective folders (`src/`, `tests/`, `../Trainingspläne/`)**
- `../Trainingspläne/`: Input `.numbers` and `.csv` files
- `requirements.txt`: Python dependencies

## Example: Adding a New Analysis
1. Add your `.numbers` or `.csv` file to `../Trainingspläne/`
2. Extend `extract_numbers_structure()` or add new parsing logic in `src/main.py` or `src/data_processing.py`
3. Add/expand tests in `tests/`


- **Shape:** Incorporate contrasting shapes (rounded, cut, or decorative) to add personality and guide attention ([M3 Shape](https://m3.material.io/styles/shape/overview-principles)).
- **Accessibility:** Ensure sufficient color contrast, clear focus states, and keyboard navigation.
- **Consistency:** Maintain consistent spacing, alignment, and component usage across screens.

For more, see the official [Material Design 3 guidelines](https://m3.material.io/).
