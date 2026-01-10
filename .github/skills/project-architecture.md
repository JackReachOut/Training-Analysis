# Skill: Project Architecture and Conventions

## Purpose
This skill provides Copilot and AI agents with a summary of the Training-Analysis project’s architecture, workflows, and best practices to improve the relevance and accuracy of AI-generated suggestions.

## Project Overview
- **Entrypoint:** `src/main.py` (CLI, launches Streamlit app, file discovery, CSV parsing)
- **Streamlit UI:** `src/app.py` (dashboard, run with `streamlit run src/app.py`)
- **CSV Parsing:** `load_training_plan_from_csv()` in `src/training_logic.py` parses CSVs into structured dataclasses (`TrainingPlan`, `Exercise`, `Set`). Parsing is positional and plan-type specific; plan names determine mapping logic.
- **Numbers Files:** Only archive listing is implemented (no IWA parsing yet).
- **Data Directory:** All input data is in `Trainingspläne/` (CSV and Numbers files).

## Developer Workflows
- Run CLI: `python src/main.py`
- Run Streamlit: `streamlit run src/app.py`
- Add/Update plans: Place new files in `Trainingspläne/`
- Testing: See `tests/`
- Dependencies: `requirements.txt`
- Virtualenv: `.venv/`

## Conventions
- All scripts expect to be run from the project root.
- Data is in `Trainingspläne/`.
- Separation of concerns: main.py (CLI), app.py (UI), training_logic.py (parsing), data_processing.py (utils).
- No external APIs.
- Keep code and data in their respective folders.

## UI/UX Guidelines
- Follow Material Design 3 (M3) for Streamlit UI.
- Use vibrant, contrasting color palettes.
- Ensure accessibility and adaptive components.

## How to Extend
- Add new plan types by extending `load_training_plan_from_csv()`.
- Add new analysis by expanding `src/data_processing.py` and UI in `src/app.py`.

---
This skill should be referenced by Copilot and AI agents to ensure all code and suggestions align with project standards and workflows.