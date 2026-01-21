# AI Integration Guide

## Flags
- AI_PREVIEW_ENABLED: enables /ai/preview routes
- AI_SCHEDULER_ENABLED: enables AI ranking/readiness in assemble_session

## Endpoints
- GET /ai/preview — preview UI
- GET /api/ai/preview/recommendations — JSON ranked drills with explanations
- POST /plans/{player_id} — returns PlanResponse with ai_notes
- POST /plans/{player_id}/override — applies overrides and logs event
- GET /api/ai/health — scheduler flag status and preview availability

## Data Fields
- PlanResponse.ai_notes: indicates AI scheduling status
- Logs: data/ai_logs.jsonl entries for plan generation and overrides

## Modules
- src/ai/* — features, recommender, progression, explain, storage
- src/nlp/assistant.py — local-only NLP stub

## Usage
1. Set flags in .env:
   - AI_PREVIEW_ENABLED=true
   - AI_SCHEDULER_ENABLED=false (enable later)
2. Preview at /ai/preview
3. Toggle scheduler flag when ready
