---
status: plan_ready
---

# PLAN

## Objectives
- Respect the "Try again on failed goal" toggle so alarm clocks are only consumed when explicitly allowed.
- Provide clear logs and UI cues confirming whether a loss was detected, which button was clicked, and why retries occurred or were skipped.
- Avoid race-after hangs by reliably transitioning from failed goal screens back to lobby or normal post-race flows.

## Steps (general; not per-file)
### Step 1 — Instrument loss detection and retry decisions
**Goal:** Understand when the bot believes a loss occurred and why it attempts retries.  
**Actions (high level):**
- Add structured logging around the segments that detect loss indicators (e.g., "TRY AGAIN" button sightings, OCR snippets, mood/rank cues).
- Record whether OCR text matched, whether the button candidate was rejected due to forbidden texts, and what UI state followed.
- Surface counters/metrics (in-memory) for detected losses vs wins to quickly validate future fixes.
**Affected files (expected):**
- `core/actions/race.py`
- `core/utils/waiter.py`
**Quick validation:**
- Run a failed-race scenario and confirm logs explicitly show loss detection inputs and retry decisions without consuming the clock when disabled.

### Step 2 — Harden retry gating and UI flow
**Goal:** Enforce the setting, eliminate false positives, and prevent hangs between retry states.
**Actions (high level):**
- Refactor the retry branch so it first confirms `Settings.TRY_AGAIN_ON_FAILED_GOAL` before entering any click loops.
- Differentiate buttons by both text and spatial context (e.g., relative position, popup presence) so "NEXT" can’t be mistaken for "TRY AGAIN".
- After clicking retry, handle the alarm-clock confirmation / intermediate screens before recursing to `lobby()`.
- When the toggle is off, ensure the flow skips straight to the "Next" / results handling logic without waiting on retry UI.
**Affected files (expected):**
- `core/actions/race.py`
- `core/utils/waiter.py`
**Quick validation:**
- In a controlled failed race with the toggle off, verify no retry clicks occur and the flow proceeds to "Next".
- With toggle on, confirm a retry happens only once and the lobby resumes without hanging on the alarm-clock overlay.

### Step 3 — Improve user-facing controls and clarity
**Goal:** Make it obvious what the toggle does and ensure settings persist reliably.
**Actions (high level):**
- Update UI copy/tooltip to explain that enabling the toggle consumes an alarm clock to rerun the failed goal race immediately; disabling means continue without retries.
- Double-check config plumbing so `tryAgainOnFailedGoal` persists through presets and defaults safely (no silent re-enables).
- Consider exposing a runtime log line when the toggle is read so diagnostics can confirm its value.
**Affected files (expected):**
- `web/src/components/general/GeneralForm.tsx`
- `core/settings.py`
- `prefs/config.json` sample if needed
**Quick validation:**
- Flip the toggle in the UI, save, restart the bot, and confirm logs show the persisted value.

### Step 4 — Testing & regression coverage
**Goal:** Ensure future changes don’t regress retry logic.
**Actions (high level):**
- Add unit-style tests around helper functions (e.g., button disambiguation, loss-detection logic) with mocked detections.
- Add integration or scenario tests (if feasible) simulating failed-goal frames to assert behavior with the toggle on/off.
- Update debug documentation or SOPs if new troubleshooting steps exist.
**Affected files (expected):**
- `tests/core/actions/test_race_retry.py` (new) or equivalent
- Existing test helpers/mocks
**Quick validation:**
- Run targeted pytest suite and ensure new tests pass; confirm CI remains green.

### Step 5 — Finalization
**Goal:** Stabilize, verify, and close out.
**Actions (high level):**
- Run linting/formatting and type checks.
- Reverify both toggle states manually (or via replay) to ensure no hangs and correct logging.
- Remove any temporary diagnostics left from earlier steps.
**Quick validation:**
- All checks green; manual scenario confirms expected behavior.

## Test Plan
- **Unit:** Validate button disambiguation helpers and loss-detection decisions with mocked detections/OCR outputs for TRY AGAIN vs NEXT vs RACE.
- **Integration/E2E:** Run a failed goal race in both toggle states to ensure retries happen only when enabled and that the flow exits cleanly to lobby/results.
- **UX/Visual:** Confirm UI toggle labels/tooltips render correctly and reflect current config values after reload.

## Verification Checklist
- [ ] Lint and type checks pass locally
- [ ] RaceDay flow respects retry toggle across multiple failed-goal scenarios
- [ ] Logs clearly state when retries occur or are skipped, with no ambiguous green-button clicks
- [ ] No sensitive data added to logs; feature flag behaves as expected

## Rollback / Mitigation
- Disable the feature by setting `tryAgainOnFailedGoal` to false in config, or revert the plan’s commits. Since changes are isolated to retry logic, a simple config toggle or code rollback restores previous behavior.

## Open Questions (if any)
- Can we capture a deterministic signal (beyond button text) that the race was lost, such as a loss banner or alarm-clock icon, to reduce reliance on text OCR?
- Should retries be limited to specific goal types (e.g., fans/maiden) or all failed races when enabled?
- Do Daily Race / Nav flows need similar retry gating, or is this confined to main training runs?
