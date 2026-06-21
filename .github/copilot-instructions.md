




# Copilot Instructions for Training-Analysis

These instructions are always-on project guidance for GitHub Copilot.
Keep outputs practical, repository-specific, and easy to verify.

## Project Summary
- This repository is a Python + Streamlit training analysis app.
- It analyzes CSV training plans from `Trainingspläne/` and visualizes progress.
- Apple Numbers (`.numbers`) support is limited; CSV is the implemented path.

## Architecture
- `src/main.py` is the entrypoint and launches Streamlit (`src/app.py`).
- `src/app.py` contains dashboard/UI logic and visualizations.
- `src/training_logic.py` contains parsing dataclasses and CSV parsing logic.
- `muscle_mappings/exercise_to_muscle.json` stores exercise-to-muscle mappings.
- `assets/` contains human body HTML/CSS assets used by the UI.
- Input data files live in `Trainingspläne/`.

## Run And Validate
- Always run commands from the repository root.
- Preferred app run command: `python src/main.py`.
- Alternative run command: `streamlit run src/app.py`.
- Use the workspace virtual environment when available (`.venv`).
- If adding dependencies, install in the active venv and update dependency documentation/files in the repo.
- After code changes, run the most relevant validation you can (app start, targeted checks, or tests if present).

## Coding Conventions
- Keep a clear separation of concerns:
  - Parsing/domain logic in `src/training_logic.py`.
  - Presentation and interaction logic in `src/app.py`.
  - Startup orchestration in `src/main.py`.
- Preserve existing public dataclasses and parser behavior unless the task explicitly requires a change.
- For CSV parser updates, treat parsing as positional and block-based; maintain compatibility with current CSV layout assumptions.
- Use explicit, readable Python over clever one-liners.
- Avoid introducing new frameworks or large dependencies unless justified by the task.

## Data And File Handling
- Keep training plan source files under `Trainingspläne/`.
- Do not hardcode absolute machine-specific paths.
- Prefer UTF-8 text handling and robust numeric parsing for CSV values.

## UI Guidance
- Keep Streamlit changes accessible and readable.
- Preserve German user-facing copy unless a task asks for language changes.
- For UI enhancements, follow Material Design 3 principles (color hierarchy, accessible contrast, clear interaction feedback).

## Change Discipline
- Make minimal, targeted edits.
- Do not refactor unrelated areas in the same change.
- If behavior changes, include a short note in code comments or PR description explaining why.

## When Instructions Seem Incomplete
- Prefer these repository instructions first.
- If details are missing, inspect nearby code and README before making assumptions.
