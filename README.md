# Soccer Training Automation

A FastAPI-based web app that helps coaches generate structured, time-bounded soccer training sessions from a curated drill catalog. It includes a clean Jinja-powered UI, JSON APIs, and an optional, fully separated AI preview for ranked drill recommendations and readiness explanations.

## Features
- Create and manage player profiles (position, level, basic performance metrics)
- Browse a drill catalog and filter by position/level
- Generate session plans with intensity and duration targets
- Apply simple overrides (e.g., intensity caps) after plan generation
- Per-drill “Why” explanation line (additive UI, no AI required)
- Optional AI preview (flag-gated) that demos ranked drills and readiness

## Tech Stack
- Backend: Python, FastAPI, Jinja2 templates
- Frontend: Tailwind (CDN) + custom CSS
- Runtime: uvicorn (development)
- Data: in-memory state for simplicity; optional JSONL logging

## Getting Started
```bash
# Clone your repo
git clone https://github.com/Advaith-1506/Soccer-Training-Plan-Generator.git
cd Soccer-Training-Plan-Generator

# Or use existing local folder
cd "/Users/advaith/Soccer Automation"

# Create virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate  # on macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the web app
python3 -m uvicorn main:app --reload --port 8000
```

Open http://127.0.0.1:8000/ to view the homepage shell. Static assets are served from `/static`. The plan page template is in `templates/plan.html`.

## Project Structure
- `main.py` — application entry (loads FastAPI app)
- `src/interfaces/web.py` — web routes, template rendering, static mount
- `src/interfaces/api.py` — JSON API for players, drills, plans
- `src/interfaces/state.py` — in-memory state and registry wiring
- `src/domain/models.py` — PlayerProfile, Drill, SessionPlan
- `src/catalog/registry.py` — drill registry and filtering
- `src/planning/scheduler.py` — session assembly logic
- `templates/` — Jinja templates (including `plan.html`, `ai_preview.html`)
- `static/` — CSS and assets (see `style.css`)
- `src/ai/` — optional AI modules (preview only; separated)
- `AI_README.md` — AI integration guide and flags
- `tests/` — basic tests for planner behavior

## API Endpoints (Highlights)
- `POST /players` — create a player
- `GET /players` — list players
- `GET /drills` — list drills
- `POST /plans/{player_id}` — generate a plan for a player
- `POST /plans/{player_id}/override` — apply overrides (e.g., intensity cap)
- `GET /api/ai/health` — AI preview/scheduler status (diagnostic)

## Configuration Flags
- `AI_PREVIEW_ENABLED` — enables the AI preview routes (`/ai/preview`)
- `AI_SCHEDULER_ENABLED` — integrates AI ranking into plan assembly (off by default to keep base behavior stable)

Set flags in a `.env` file:
```env
AI_PREVIEW_ENABLED=true
AI_SCHEDULER_ENABLED=false
```

## AI Preview (Optional)
- Preview UI: `/ai/preview`
- Separate router and template; does not affect base planning when flags are off
- See `AI_README.md` for details on modules and usage

## Development
- Run tests:
```bash
pytest -q
```
- Common tasks live under `src/interfaces/cli.py` (e.g., training logs stub)

## Notes
- This app favors simplicity and local development. No database is required; state is in memory.
- The AI preview is intentionally separated and gated to avoid impacting core flows.

