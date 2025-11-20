---
date: 2025-11-19T20:15:00-05:00
topic: button-golden-robust
status: research_complete
---

# RESEARCH — button-golden-robust

## Research Question
How can we keep Unity Cup flow responsive when the golden inspiration/showdown button is detected with low confidence, preventing GO clicks and inheritance confirmations?

## Summary (≤ 10 bullets)
- Unity classifier labels Inspiration/Kashimoto screens only when `button_golden` ≥ race_conf (default 0.8), so 0.3–0.5 detections never trigger those flows @core/perception/analyzers/screen.py#158-326.
- The same 0.8 `race_conf` gate is used for `race_race_day`, so Unity Cup Raceday is never recognized when YOLO outputs moderate confidence (0.55–0.75), leaving the agent in Unknown and blocking GO clicks @core/perception/analyzers/screen.py#263-276.
- AgentUnityCup retries GO by calling `find_best(..., conf_min=0.4)` once the screen is labeled, but never revisits `button_golden` when classification failed @core/actions/unity_cup/agent.py#284-304.
- Unknown-screen recovery clicks generic green/white buttons with a `threshold` parameter (0.55–0.65) yet does not bias toward the golden class, so the loop stalls if no other buttons appear @core/actions/unity_cup/agent.py#148-190.
- Global YOLO detection confidence defaults to 0.60; the classifier’s 0.80 cutoff is inconsistent and likely masks borderline detections instead of letting downstream logic decide @core/settings.py#143-147.
- No telemetry captures the suppressed `button_golden` detections, making it hard to know when shots were discarded.
- Inheritance/blessing popups share the same golden button but appear without `button_white`; the classifier requirement (`button_golden` AND `button_white`) for KashimotoTeam likely filters them out @core/perception/analyzers/screen.py#267-304.
- Find-best helper lacks progressive threshold fallback; once the initial low-conf search fails, the agent gives up @core/perception/extractors/state.py#39-50.
- Controller patience counter stops the loop entirely after prolonged unknown screens, turning a transient miss into a hard stop @core/actions/unity_cup/agent.py#148-190.

## Detailed Findings (by area)
### Area: Screen classification (Unity Cup)
- **Why relevant:** Determines whether the agent even reaches the click logic for GO/inheritance.
- **Files & anchors:**
  - `core/perception/analyzers/screen.py:158–326` — `classify_screen_unity_cup` gates “Inspiration” vs “KashimotoTeam” based on `button_golden` ≥ `race_conf` (default 0.80). Also requires `button_white` to distinguish Kashimoto screens.
  - `core/perception/analyzers/screen.py:263–276` — `race_race_day` also uses the same high `race_conf`; slower devices produce detections in the 0.6–0.7 range so the classifier never emits “Raceday”/“UnityCupRaceday,” preventing the race flow from running.
- **Cross-links:** Called directly by `AgentUnityCup.run`, so misclassification short-circuits training/event handling.

### Area: Unity Cup race-day progression
- **Why relevant:** Without a positive “Raceday” classification, the agent never calls `RaceFlow`, causing the reported “bot stuck” behavior.
- **Files & anchors:**
  - `core/perception/analyzers/screen.py:267–276` — requires both `race_race_day` and (for the Raceday branch) `lobby_tazuna` at ≥0.8 confidence.
  - `core/actions/unity_cup/agent.py:306–400` — race-day branch only executes after classifier returns `Raceday`; otherwise, unknown fallback keeps burning patience until the loop exits.
- **Cross-links:** The same low-confidence issues that hide golden buttons also hide `race_race_day`, so any mitigation (adaptive thresholds, multi-pass search) must cover both classes.

### Area: Unity agent loop & patience logic
- **Why relevant:** Shows how the bot behaves on each classified screen and what fallbacks exist.
- **Files & anchors:**
  - `core/actions/unity_cup/agent.py:128–400` — Main loop. Unknown handler simply spams general buttons and stops after `patience` iterations. Inspiration/Kashimoto sections call `find_best(..., conf_min=0.4)` once before clicking.
- **Cross-links:** Uses `self.waiter.click_when` for unknown fallback; depends on classification to enter the golden-button blocks.

### Area: Detection helpers
- **Why relevant:** `find_best` imposes another confidence floor and never relaxes it.
- **Files & anchors:**
  - `core/perception/extractors/state.py:39–50` — `find_best` filters detections by `conf_min` (0.40 hardcoded usage) and picks the max; no retries at lower thresholds.
- **Cross-links:** Called from Unity agent and other flows when clicking precise UI elements.

### Area: Global YOLO thresholds / settings
- **Why relevant:** Shows default detection floor vs. classifier expectations.
- **Files & anchors:**
  - `core/settings.py:143–147` — `YOLO_CONF` default 0.60. Classifier uses higher 0.80 requirement for golden button, so many detections never propagate.
- **Cross-links:** `AgentUnityCup` passes `self.conf = Settings.YOLO_CONF` to `yolo_engine.recognize`, so detections between 0.60 and 0.80 exist but are ignored later.

### Area: Inheritance/blessing popup state
- **Why relevant:** Bug report mentions inheritance blessing stuck; classification currently treats golden button + white button as KashimotoTeam, so inheritance (golden only) becomes “Unknown”.
- **Files & anchors:**
  - `core/perception/analyzers/screen.py:263–304` — If `button_golden` present without `button_white`, returns “Inspiration”; if both present, “KashimotoTeam”. No state dedicated to inheritance, so low-confidence detections keep it in “Unknown”.
- **Cross-links:** Without a specific inheritance branch, next-state logic never calls race flow or forced click.

## 360° Around Target(s)
- **Target file(s):** `core/perception/analyzers/screen.py`, `core/actions/unity_cup/agent.py`
- **Dependency graph (depth 2):**
  - `core/settings.py` — provides YOLO confidence defaults consumed by both classifier inputs and Unity agent capture.
  - `core/perception/extractors/state.py` — houses `find_best`, used by Unity agent when clicking detections.
  - `core/utils/waiter.py` (indirect) — `click_when` fallback invoked during unknown screen handling and general progression.

## Open Questions / Ambiguities
- Should `classify_screen_unity_cup` lower `race_conf` for `button_golden` specifically or implement a decay (e.g., after N unknown ticks) to catch marginal detections? Without this, we risk over-triggering on noise.
- Do inheritance blessing screens always lack `button_white`, and could we safely introduce a dedicated “InheritanceBlessing” screen label to drive more specific behavior?
- Would logging suppressed `button_golden` detections (e.g., when 0.3≤conf<0.8) improve retraining/threshold tuning, or should we add a runtime fallback (extra `find_best` scan with lower `conf_min`) before resorting to data collection?

## Suggested Next Step
- Draft `PLAN.md` covering: (1) classifier threshold adjustments or adaptive fallback, (2) Unity agent retry strategy (multi-threshold `find_best`, targeted waiter clicks) and logging, (3) tests/telemetry capturing low-confidence golden button scenarios before retraining YOLO.
