## What You'll Add
- A small AI package for features + models
- A preview-only router and page to demo recommendations
- No changes to existing scheduling until you enable a flag

## Step-by-Step
1. Create AI package
   - src/ai/features.py
     - def player_features(player: PlayerProfile) -> dict
     - def drill_features(drill: Drill, position: Position) -> dict
   - src/ai/recommender.py
     - class Recommender:
       - def score(player_feats: dict, drill_feats: dict) -> float  (hybrid: rules + weights)
       - def rank(player, drills, context) -> list[tuple[Drill,float]]
   - src/ai/progression.py
     - def readiness(player_feats: dict) -> float (0–1 baseline)
   - src/ai/explain.py
     - def explain(drill: Drill, player_feats: dict, drill_feats: dict, score: float) -> str

2. Wire a preview API (separated)
   - src/interfaces/ai_preview.py (FastAPI Router)
     - GET /api/ai/preview/recommendations?player_id=... → {drills:[{id, name, score, readiness, why}]}
     - GET /ai/preview → TemplateResponse("ai_preview.html")
   - settings flag AI_PREVIEW_ENABLED; in web.py mount router only if enabled

3. Build preview UI
   - templates/ai_preview.html
     - Player picker (use _players from state)
     - Fetch /api/ai/preview/recommendations and render a table: Name, Score, Readiness, Why recommended

4. Keep current flow intact
   - Do not touch assemble_session yet; preview runs side-by-side

5. Prepare hybrid baseline (works day one)
   - Start with weights: score = w1*skill_gap + w2*recent_progress + w3*position_match + w4*(1/difficulty)
   - Tune weights manually; later learn them (LogisticRegression) from logged outcomes

6. Add light logging (optional)
   - src/ai/storage.py → append JSONL rows: {player_id, drill_id, features, score, readiness, chosen, outcome}
   - Use later to fit simple models (scikit-learn)

7. After preview approval (feature-flagged integration)
   - In src/planning/scheduler.py: if AI_SCHEDULER_ENABLED → call recommender.rank() and progression.readiness() before building SessionPlan
   - Else keep rule-based selection

## Contracts (Concrete)
- Recommendation response item:
  - { id: str, name: str, score: float, readiness: float, why: str }
- features.player: { age, skill_level_num, position_onehot, consistency, error_rate, delta_last_3 }
- features.drill: { difficulty, tags_onehot, intensity, position_match }

## Testing
- Unit tests for features and recommender scoring with fixed inputs
- Preview route e2e test: returns ranked list with explanations

## Files to Touch (Only when approved)
- New: src/ai/*.py, src/interfaces/ai_preview.py, templates/ai_preview.html
- Minimal: src/interfaces/web.py (conditional mount), src/config/settings.py (flag)

## Outcome
- You see AI ranking in /ai/preview without risking existing flows
- Once satisfied, flip a flag to use AI in real session generation