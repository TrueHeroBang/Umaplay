---
status: plan_ready
---

# PLAN

## Objectives
- Ensure Unity Cup flows progress even when `button_golden` or `race_race_day` detections arrive with mid confidence (≈0.4–0.7).
- Add adaptive fallbacks plus logging so future retraining knows when low-confidence clicks were required.
- Verify the bot advances through Inspiration/Kashimoto/inheritance and Unity Raceday without stalling on Unknown screens.

## Steps (general; not per-file)
### Step 1 — Relaxed detection & classification thresholds
**Goal:** Let screen classification surface borderline detections instead of hiding them.
**Actions (high level):**
- Introduce adaptive thresholds for `button_golden`/`race_race_day` in `classify_screen_unity_cup` (e.g., decay after N unknown loops or dedicated lower params).
- Ensure Settings exposes sane defaults and comments for the new thresholds.
- Keep false positives in check by requiring supporting detections (e.g., bounding-box sanity, optional tazuna presence) when using the relaxed path.
**Affected files (expected):**
- `core/perception/analyzers/screen.py`
- `core/settings.py`
**Quick validation:**
- Unit-style smoke: feed recorded detection lists (mid-confidence golden/race_day) into classifier and confirm it now returns Inspiration/Kashimoto/Raceday accordingly.

### Step 2 — Agent-side fallback clicks & telemetry
**Goal:** When classification still returns Unknown, proactively probe golden/race-day detections before giving up.
**Actions (high level):**
- In `AgentUnityCup`, add a secondary `find_best` call with progressively lower `conf_min` for `button_golden`/`race_race_day` when patience climbs.
- Add targeted `waiter.click_when` probes for GO/Next when a low-confidence race-day detection exists.
- Emit debug logs (and optional screenshot tags) whenever a fallback click fires so dataset curation knows when to harvest more samples.
**Affected files (expected):**
- `core/actions/unity_cup/agent.py`
- `core/utils/logger.py` (if new log helpers needed)
**Quick validation:**
- Run Unity Cup on recorded frames or live session with LOG=DEBUG; verify fallback logs show up and the agent proceeds past previously-stuck states.

### Step 3 — Instrumentation & guardrails
**Goal:** Avoid regressions by monitoring detection quality and keeping telemetry lightweight.
**Actions (high level):**
- Add counters/metrics (simple in-memory) for how often fallback tiers trigger.
- Persist debug captures when low-confidence clicks succeed (leveraging existing Waiter tags) for later dataset labeling.
- Gate the extra captures behind a setting flag to avoid disk spam in stable runs.
**Affected files (expected):**
- `core/actions/unity_cup/agent.py`
- `core/settings.py`
- `core/utils/waiter.py` (if extra tag plumbing needed)
**Quick validation:**
- Toggle the new debug flag on, run a short session, confirm counters/logs increment and captures land under `debug/unity_cup/...`.

### Step 4 — Tests & docs touch-up
**Goal:** Encode the new behavior and document the knobs.
**Actions (high level):**
- Add unit/regression tests for `classify_screen_unity_cup` covering relaxed thresholds and inheritance/raceday detection.
- Extend any existing Unity Cup scenario tests (or create focused ones) to cover agent fallback logic with mocked detections.
- Update README/SOP snippets if new settings are exposed to users.
**Affected files (expected):**
- `tests/core/...` (new or existing classifier/agent tests)
- `docs/ai/SOPs` or `README.md` if settings surface publicly
**Quick validation:**
- `pytest tests/core/...` passes; docs mention the new fallback knobs.

### Step 5 — Finalization
**Goal:** Stabilize and ensure the feature is production-ready.
**Actions (high level):**
- Run lint/type checks (ruff, mypy/pyright if applicable).
- Execute an end-to-end Unity Cup dry run to confirm the bot no longer stalls at Inspiration/inheritance or Raceday.
- Review logs/counters for abnormal spikes; adjust thresholds if needed.
**Quick validation:**
- All checks green; Unity Cup run reaches Raceday and GO click flows without manual intervention.

## Test Plan
- **Unit:**
  - Classifier tests covering golden-only, golden+white, and low-confidence race_race_day cases.
  - Agent fallback unit tests using mocked detections/patience counters.
- **Integration/E2E:**
  - Simulated Unity Cup flow on recorded screenshots to confirm progression through Inspiration → Raceday.
  - Live device smoke run verifying inheritance blessing and Unity Raceday no longer stall.
- **UX/Visual:**
  - None (backend logic only), but confirm debug captures look correct when enabled.

## Verification Checklist
- [ ] Lint and type checks pass locally
- [ ] Unity Cup flow reaches GO buttons with fallback logic disabled/enabled
- [ ] Debug logs show fallback events without flooding output
- [ ] No PII or excess captures stored when debug flag off
- [ ] Feature flags/threshold settings adjustable via config

## Rollback / Mitigation
- Disable new fallback via settings (revert thresholds to 0.8, turn off debug flag) or revert the plan’s commits; the previous behavior simply stops at Unknown instead of forcing clicks.

## Open Questions
- What exact patience threshold should trigger the relaxed classifier path vs. agent fallback? Need empirical data.
- Should low-confidence race-day handling also re-check Tazuna presence, or is race card alone enough? Confirm via captured frames.
- Do we need separate thresholds per device profile (scrcpy vs. Steam)? Might require config exposure later.
