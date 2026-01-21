## Goal
- Provide a separated AI preview using only free, local libraries (no paid APIs), then integrate into the scheduler after approval.

## Free AI Stack
- ML: scikit-learn (LinearRegression/Ridge/LogisticRegression; StandardScaler/MinMaxScaler)
- Optional ranking helpers: scipy/numpy
- Optional NLP later: Hugging Face transformers with small open models, local-only (not required for MVP)

## Where AI Will Integrate (post-approval)
- Hook into assemble_session in [scheduler.py](file:///Users/advaith/Soccer%20Automation/src/planning/scheduler.py) to order drills and adjust intensities.
- Use PlayerProfile.performance_metrics in [models.py](file:///Users/advaith/Soccer%20Automation/src/domain/models.py) and Drill metadata in [registry.py](file:///Users/advaith/Soccer%20Automation/src/catalog/registry.py).

## Separated Preview (MVP)
- Router: src/interfaces/ai_preview.py → /ai/preview (HTML) and /api/ai/preview/recommendations (JSON).
- Template: templates/ai_preview.html showing ranked drills + “Why recommended”.
- Feature flag: AI_PREVIEW_ENABLED (default off) to mount preview.

## AI Modules
- src/ai/features.py: compute features (progression velocity, consistency, benchmark gaps).
- src/ai/recommender.py: hybrid scoring baseline combining rule signals with learned weights via LogisticRegression; safe default weights if no training data.
- src/ai/progression.py: readiness via Ridge regression; fallback heuristic if model not trained.
- src/ai/explain.py: generate human-readable explanations from top contributing features (no LLM needed).
- src/ai/storage.py: JSONL logs of preview interactions for future training (local files).

## Data Flow (Preview)
1. Select player (or demo).
2. Extract features for each candidate drill.
3. Rank with recommender; compute readiness.
4. Return ordered drills + explanations.
5. Render in ai_preview.html.

## Training (Free, Local)
- CLI command to train LogisticRegression/Ridge on JSONL logs.
- Store model weights as pickles under src/ai/models/.
- Reload weights at startup if available; otherwise use defaults.

## Non-Impact Guarantee
- No changes to current routes or scheduler until you confirm.
- Preview is additive and gated by the feature flag.

## Deliverables
- New src/ai/* modules
- New separated preview router and template
- Training CLI for local models

## Future Optional (still free)
- Add Hugging Face transformers locally for a coach natural-language preview.
- Add KMeans segmentation when enough data exists.