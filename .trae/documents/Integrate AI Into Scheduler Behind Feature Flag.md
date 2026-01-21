## Overview

* Add a feature-flagged AI scheduling hook with robust fallbacks, logging, and tests.

* Define a roadmap for a local-only coach NLP interface using free models.

## 1) Feature-Flagged AI Scheduling Hook

### Integration Point

* Modify assemble\_session in [scheduler.py](file:///Users/advaith/Soccer%20Automation/src/planning/scheduler.py) to optionally:

  * Fetch candidates from registry

  * Call src.ai.recommender.rank and src.ai.progression.readiness\_score

  * Adjust intensities, order drills, attach explanations

### Toggle Mechanism

* New env flag: AI\_SCHEDULER\_ENABLED (default false)

* Loaded via dotenv in [web.py](file:///Users/advaith/Soccer%20Automation/src/interfaces/web.py) and passed to planning

* Runtime toggle detection; no restart required for off→on if env reloaded

### Error Handling & Fallbacks

* Try/except around AI steps; on error:

  * Log error event (type, trace, player\_id)

  * Fallback to existing rule-based ordering in [selectors.py](file:///Users/advaith/Soccer%20Automation/src/adaptive/selectors.py)

  * Continue plan generation with safe defaults

### Logging

* Log per-plan metrics in src.ai.storage:

  * player\_id, readiness, top feature contributions, drill scores, final order, duration

  * timing metrics (ms for ranking/readiness)

  * flag status, success/failure reason

### UI

* Show “AI Insight” on [plan.html](file:///Users/advaith/Soccer%20Automation/templates/plan.html) under each drill

* Badge indicating AI scheduling active

### Tests

* Unit: rank ordering, readiness thresholds, intensity adjust

* Integration: assemble\_session with flag on/off, error path falls back

* Performance: simple timing asserts (upper bounds) in CI (skippable locally)

## 2) Coach NLP Interface Roadmap

### Architecture

* Local-only Hugging Face model (small distilled encoder+decoder) for intent classification + prompt-to-plan suggestions

* Service module src/nlp/assistant.py providing:

  * parse\_intent(text): returns structured request (age group, focus, level)

  * generate\_suggestions(intent, registry): returns drill list + rationale

* Modular interface to swap models (configurable model path/tokenizer)

### Offline Execution

* Use transformers with on-disk model weights; no external calls

* Provide CPU-only baseline and measure latency targets (<300ms parse, <800ms suggestion best-effort)

### Free Tier Requirements

* Use open-source, license-compatible models (e.g., DistilBERT + small seq2seq)

* No paid API keys; optional quantized weights for speed

### Benchmarks

* Collect timing via simple decorators

* Log latency and token counts; persist in JSONL for monitoring

### Tests (NLP)

* Unit: intent parsing on canned prompts

* Integration: suggestion generation returns valid drills with explanations

* Deterministic fallbacks if model missing (rules-based)

## Shared Requirements

* Follow code style/architecture; reuse existing modules (state, registry)

* Backward compatible defaults: flags off by default

* Document flags, endpoints, data fields in a README section

* Monitoring/Alerting:

  * Structured logs with levels via config/logging

  * Add a health endpoint /api/ai/health reporting flag status, last error, avg latency

  * Simple alerts: log warnings when error rate or latency exceeds thresholds (ready for future hook to email/Slack)

## Deliverables

* AI scheduler hook behind AI\_SCHEDULER\_ENABLED with fallbacks + logging

* “AI Insight” UI and DTO updates

* NLP assistant module design + stubbed local path loader

* Tests (unit/integration/perf) and docs

* Health/monitor logging and threshold warnings

