# Recommendation and AI preview guide

The current recommendation layer is local and heuristic: it computes weighted feature scores, readiness, intensity adjustments, and template-based explanations. No external AI key is required.

## Flags and application boundaries

- `AI_PREVIEW_ENABLED=true`: mounts the preview router on the **web app**, `main:app`, at startup. That app loads `.env`.
- `AI_SCHEDULER_ENABLED=true`: enables ranking/readiness in `assemble_session`; errors fall back to the base selector. Export this variable before starting the **JSON app**, `src.interfaces.api:app`, which does not load `.env` itself.

## Endpoints

| App | Method | Path |
| --- | --- | --- |
| Web | GET | `/ai/preview` |
| Web | GET | `/api/ai/preview/recommendations` (optional `player_id`, `top_n`) |
| JSON | POST | `/plans/{player_id}` |
| JSON | POST | `/plans/{player_id}/override` |
| JSON | GET | `/api/ai/health` |

The health response hardcodes preview availability and is not a web-router readiness check. The web preview template has the same fresh-dependency compatibility caveat described in [README.md](README.md).

## Modules and data

- [src/ai](src/ai): features, ranker, progression, explanations, JSONL event storage.
- [src/nlp/assistant.py](src/nlp/assistant.py): local stub.
- JSON `PlanResponse.ai_notes`: indicates scheduler ranking status when populated.
- JSON API plan/override paths append events to `data/ai_logs.jsonl`; web plan routes do not use those logging calls.

Use synthetic player profiles and keep generated logs out of commits. See [the main README](README.md) for startup commands and the existing tests.
