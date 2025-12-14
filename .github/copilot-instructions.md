

# Copilot Instructions for Training-Analysis

## Project Overview
This project analyzes Apple Numbers training plan files (`.numbers`) and CSVs from the `../Trainingspläne/` directory. The main logic is in `src/main.py`, which currently lists `.numbers` archive contents and demonstrates section parsing. The codebase is scaffolded for future expansion to real Numbers/IWA parsing and deeper analysis.

## Architecture & Data Flow
- **Entry Point:** `src/main.py` (see `main()`)
- **Input Data:** `.numbers` and `.csv` files in `../Trainingspläne/` (relative to project root)
- **Extraction:** Uses `zipfile` to inspect `.numbers` files (no IWA parsing yet)
- **Section Parsing:** `parse_sections_from_rows()` in `main.py` shows how workout sections are split by row markers (e.g., `-`, `*`)
- **Data Processing:** `src/data_processing.py` is present for future data transformation logic
- **Streamlit App:** `src/app.py` is intended for interactive UI (see below for details)

## Developer Workflows
- **Run CLI Analysis:**
  - `python src/main.py` (from project root)
  - Prints found `.numbers` files and their archive contents
- **Run Streamlit App:**
  - `streamlit run src/app.py` (from project root)
  - If `streamlit` is missing, install with `pip install streamlit`
- **Add/Update Training Plans:**
  - Place new `.numbers` or `.csv` files in `../Trainingspläne/` or its `numbers/` subfolder
- **Testing:**
  - Minimal: see `tests/test_placeholder.py` (expand as needed)
- **Dependencies:**
  - List in `requirements.txt` (add e.g. `pytest`, `streamlit` as needed)
- **Virtual Environment:**
  - Recommended: `python -m venv .venv && source .venv/bin/activate`
  - Install dependencies: `pip install -r requirements.txt`

## Project Conventions & Patterns
- **No real Numbers parsing yet:** Only archive listing is implemented; IWA parsing is a future task
- **Section parsing logic:** See `parse_sections_from_rows()` in `main.py` for how workout sections are identified
- **Relative paths:** All scripts expect to be run from the project root
- **Separation of concerns:**
  - `src/main.py`: CLI entry, file discovery, demo parsing
  - `src/app.py`: Streamlit UI (WIP)
  - `src/data_processing.py`: Data transformation (WIP)
- **No external APIs or integrations**
- **Keep code and data in their respective folders (`src/`, `tests/`, `../Trainingspläne/`)**

## Key Files & Directories
- `src/main.py`: Main CLI logic, parsing examples
- `src/app.py`: Streamlit app (run with `streamlit run src/app.py`)
- `src/data_processing.py`: Data processing utilities (expand as needed)
- `tests/test_placeholder.py`: Placeholder for tests
- `../Trainingspläne/`: Input `.numbers` and `.csv` files
- `requirements.txt`: Python dependencies

## Example: Adding a New Analysis
1. Add your `.numbers` or `.csv` file to `../Trainingspläne/`
2. Extend `extract_numbers_structure()` or add new parsing logic in `src/main.py` or `src/data_processing.py`
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
