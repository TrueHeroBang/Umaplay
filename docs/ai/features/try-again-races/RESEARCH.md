---
date: 2025-11-19T20:20:00-05:00
topic: try-again-races
status: research_complete
---

# RESEARCH — try-again-races

## Research Question
Why does the "Try again on failed goal" toggle still cause automatic retries and hangs after a failed race, and what touchpoints must change to make the behavior reliable?

## Summary (≤ 10 bullets)
- RaceFlow unconditionally hunts for green buttons after every race and only conditionally short-circuits when `Settings.TRY_AGAIN_ON_FAILED_GOAL` is true, so disabled users still hit the reactive retry loop and conflicting Next-button clicks.@core/actions/race.py#600-825
- The current retry logic just spam-clicks green buttons with text filters and no extra logging, making it impossible to tell whether the bot actually saw a loss or misread a button like "NEXT" as "TRY AGAIN".@core/actions/race.py#763-825
- `Settings.TRY_AGAIN_ON_FAILED_GOAL` defaults to true and is only flipped via the general config payload, so stale configs or missing migrations may silently re-enable the feature.@core/settings.py#201-288
- Web toggle is surfaced in `GeneralForm` but lacks warning text describing what UI cues gate retries, leaving users unsure about its scope (goal races only vs any loss).@web/src/components/general/GeneralForm.tsx#290-300
- There is no instrumentation around the loss-detection path (no OCR of result banners, no mood/rank parsing) to confirm whether a loss happened before attempting retries.@core/actions/race.py#761-825
- The Waiter API clicks green buttons by class first, then optional OCR text matches; with `allow_greedy_click=False`, OCR must succeed, otherwise nothing happens and the flow hangs on the lobby screen.@core/utils/waiter.py#1-400
- Retry recursion (`self.lobby()`) assumes the lobby state will reappear within 5s, but after using an alarm clock, the UI shows an interstitial (clock confirmation) that lacks detection hooks, leading to loops.@core/actions/race.py#781-785
- Logs from the reported session show the flow looping on `race_after` waits, indicating the bot never recognized the post-failure UI, corroborating the suspicion that retry detection fails silently.@core/actions/race.py#786-824
- No tests cover failed-goal flows, so the feature has never been validated end-to-end; the comment even states it "never tested".@core/actions/race.py#763-825

## Detailed Findings (by area)
### Area: RaceFlow retry handling
- **Why relevant:** Contains the loss-detection branch, recursive retry call, and post-race button clicks that currently misbehave.
- **Files & anchors:**
  - `core/actions/race.py:600-825` — lobby interaction, skip loop, loss detection, retry recursion, "Next" handling.
- **Cross-links:** Relies on `Waiter.click_when` to discriminate between green buttons and uses `Settings.TRY_AGAIN_ON_FAILED_GOAL` for gating.

### Area: Settings plumbing
- **Why relevant:** Determines default retry behavior and how config toggles propagate, influencing whether the feature is even disabled for users.
- **Files & anchors:**
  - `core/settings.py:201-288` — default `TRY_AGAIN_ON_FAILED_GOAL` and config loading.
- **Cross-links:** Config is edited through the web UI and persisted under `prefs/config.json`.

### Area: Web UI toggle
- **Why relevant:** User-facing control for the feature; unclear labeling may cause misconfiguration or misinterpretation.
- **Files & anchors:**
  - `web/src/components/general/GeneralForm.tsx:290-300` — switch wiring and label.
- **Cross-links:** Changes propagate to `configStore` → `Settings.apply_config()`.

### Area: Waiter button discrimination
- **Why relevant:** `click_when` heuristics decide whether a detected green button is "TRY AGAIN" vs "NEXT" or "RACE". Misclassification explains discord comment about confusing buttons.
- **Files & anchors:**
  - `core/utils/waiter.py` (button search helpers) — not yet instrumented for per-text disambiguation logs.
- **Cross-links:** Called throughout RaceFlow skip/next logic.

## 360° Around Target(s)
- **Target file(s):** `core/actions/race.py`, `core/settings.py`, `web/src/components/general/GeneralForm.tsx`, `core/utils/waiter.py`
- **Dependency graph (depth 2):**
  - `core/actions/race.py` → `core/utils/waiter.py`, `core/controllers/base.py`, `core/utils/logger.py`.
  - `core/settings.py` → `prefs/config.json` schema (via `Settings.apply_config()`), consumed by `main.py` and flows.
  - `web/src/components/general/GeneralForm.tsx` → `web/src/store/configStore.ts`, `web/src/models/config.schema.ts`.
  - `core/utils/waiter.py` → YOLO detector outputs (`dets` from `core/perception/`), `core/utils/logger.py`.

## Open Questions / Ambiguities
1. Does the bot currently detect race failures via explicit UI text (e.g., "Failed Goal") or merely assume a loss if "TRY AGAIN" appears? Need to confirm OCR pipeline coverage to avoid false positives.
2. How should the bot behave when the user disables retries but the game still offers an alarm clock? Should it click "View Results" automatically or wait for manual intervention?
3. Do other flows (Daily Races, Nav modes) share the same retry flag, and should changes here affect them, or is the scope limited to goal races inside training runs?

## Suggested Next Step
- Draft `PLAN.md` enumerating: (1) detection improvements for loss vs win screens, (2) logging/instrumentation additions around `try_again` decisions, (3) Waiter text/position disambiguation, (4) config/UI updates, and (5) regression tests covering both enabled and disabled states.
