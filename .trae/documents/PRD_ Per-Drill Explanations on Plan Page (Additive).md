## Goal

* Add a simple, per‑drill explanation line to the plan page, with no AI integration and no changes to existing scheduling logic.

## Scope (Additive Only)

* Show one short reason line under each drill row on plan.html: “Why: reason text”.

* Reasons are static, derived from drill attributes (category, level, intensity) or a fixed message.

## Data Source

* Template computes/display reasons using existing drill fields (category, level, intensity). No new DTOs or backend logic required.

## UI Changes

* In plan.html, beneath the intensity/duration, render a gray, small text line:

  * Example: “Why: Technical focus for current level; safe intensity.”

* Reuse existing styles (tag/tooltip/hint). No new CSS classes.

## Flags (Optional)

* EXPLAIN\_ENABLED (default false). When true, explanations render; otherwise page remains unchanged. If undesired, omit the flag and always render the line.

## Error/Fallback

* If a drill lacks expected fields, show a generic message: “Why: Balanced load for this session.”

## Testing

* Visual check: explanations appear; layout unaffected.

* Template test: ensures line renders once per drill when EXPLAIN\_ENABLED is true.

## Rollout

* Ship with EXPLAIN\_ENABLED=false; enable in preview. No impact to base scheduling or APIs.

