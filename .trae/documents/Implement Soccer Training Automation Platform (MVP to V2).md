## Repository Setup
- Create a modular Python project under src/ with clear boundaries: domain, catalog, adaptive, planning, interfaces, storage, config, tests
- Target Python 3.11; enforce typing and strict validation
- Dependencies: pydantic, fastapi+uvicorn, sqlalchemy+alembic, typer, jsonlogic (or durable_rules), pytest, python-dotenv

## Core Domain Models
- PlayerProfile: id, name, age, position (enum), skill_level (enum), training_history[], performance_metrics, constraints (injury/availability)
- Drill: id, name, category (technical/tactical/physical), position_tags[], level, intensity, repetition_range, duration, equipment, space, prerequisites
- Assessment: id, player_id, date, metric_name, value, context
- SessionPlan: id, player_id/team_id, date, drills[], total_duration, notes, safety_flags
- DTOs via Pydantic with strict validation and custom validators (age ranges, enum bounds)

## Drill Catalog & Registry
- Author drills in YAML/JSON plus optional Python generators for parameterized drills
- Build a registry with query API: filter by position, skill level, constraints, equipment/space
- Add metadata for progression ladders and difficulty scaling

## Adaptive Engine (Rule-Based MVP)
- Feature extraction from PlayerProfile + recent Assessments (e.g., pass_accuracy, sprint_time)
- Rules evaluate eligibility and rank drills; jsonlogic for composable domain rules
- Difficulty tuner adjusts intensity, reps, and pacing per player growth curves
- Feedback module updates player state (skill_level/metrics) from outcomes

## Planning & Scheduling
- Assemble SessionPlan respecting time budget, safety constraints, and progression balance (technical/tactical/physical)
- Ensure rest spacing and avoid conflicting muscle groups; detect equipment/space conflicts
- Team planner composes per-player plans from a team template with overrides

## Coach Customization Tools
- Override generated drills (swap/add/remove), lock drills, set intensity caps
- Team-wide plan creation with per-player adjustments; export/import plans

## Interfaces
- CLI (Typer): import players, generate plans, record assessments, export reports
- API (FastAPI): endpoints for players, drills, session planning, assessments, coach overrides
- Use Pydantic DTOs for request/response, strict validation at boundaries

## Storage Layer
- SQLAlchemy models mirrored from domain; repositories for Player/Drill/Session/Assessment
- Start with SQLite; isolate via repository pattern to enable Postgres later
- Alembic migrations for schema evolution

## Observability & Config
- Structured logging (JSON) with correlation IDs; basic metrics (plans_generated, rule_hits)
- Config via env (.env) and settings module; avoid hardcoding secrets

## Testing Strategy
- Pytest unit tests for validation, rules, selection, and tuning
- Golden tests for representative players to validate plan outputs
- Property-based tests for rule engine safety invariants (e.g., age/intensity bounds)

## Performance & Scalability
- Cache drill catalog and precompute indexes; fast filters by tags/levels
- Keep selection O(n) over catalog with light ranking; near real-time generation
- Batch operations for team planning; async API where helpful

## Extensibility
- Strategy interface for adaptive selection (allow swapping rule-based with ML later)
- Plugin system for new drill families and constraints
- Clean DTOs to support future mobile/web clients and wearables

## Milestones
- M1 (MVP): domain models, catalog, rule-based generator, CLI, tests
- M2: FastAPI, storage+repos, coach overrides, migrations, integration tests
- M3: Adaptive feedback loop, metrics/logging, team planner
- M4: Performance tuning, export/reporting, preparatory hooks for ML

## Assumptions
- Fresh repo (no existing code); build from scratch following the PRD
- Rule-based adaptive logic is the initial core; ML is deferred