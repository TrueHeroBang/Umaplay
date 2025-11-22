---
status: plan_ready
---

# PLAN

## Objectives
- Reduce mis-selection of **scheduled races** when multiple G1 races or similar banners/names are present (e.g., "Asahi Hai Futurity Stakes" vs "Hanshin Juvenile Fillies").
- Use existing race datasets and banner templates to prefer the **intended planned race** while keeping behavior for unscheduled/generic race days unchanged.
- Make the behavior observable and debuggable via structured logs and, where useful, configuration toggles.

## Steps (general; not per-file)

### Step 1 — Define ambiguity groups and template metadata
**Goal:** Capture knowledge about races that are easily confused (name or banner wise) in a single, explicit configuration layer.

**Actions (high level):**
- Identify races that are known to be ambiguous (starting with Asahi vs Hanshin, plus any others that share banners/layouts or dates).
- Design a small data structure that can express **banner groups** or **synonym sets**, e.g., a mapping from canonical race name to a list of related race names whose templates should be considered together.
- Decide whether this lives alongside `assets/races/templates/index.json` (extended schema) or in a dedicated new JSON under `assets/races/`.
- Extend `RaceIndex` with helper(s) to expose:
  - All templates for a given canonical race.
  - Ambiguity/synonym groups for a planned race (if present), otherwise falling back to single-template behavior.
- Add minimal logging when ambiguity metadata is loaded so it is easy to confirm at runtime which group is being used.

**Affected files (expected):**
- `assets/races/templates/index.json` and/or a new race-ambiguity JSON under `assets/races/`.
- `core/utils/race_index.py` (helpers to read ambiguity groups and expose them).
- Optional: `docs/ai/features/race-synonimous-handling/RESEARCH.md` cross-check to keep terminology consistent (no structural change required).

**Quick validation:**
- Run a small Python snippet or unit test to fetch ambiguity data for known examples and assert that:
  - Canonicalization resolves both primary and secondary names.
  - `RaceIndex` returns the expected group members and template metadata.
- Verify logs indicate the ambiguity group being recognized at startup.

---

### Step 2 — Improve per-page scoring for scheduled races using ambiguity groups
**Goal:** Make `_pick_race_square` smarter on each page by considering all relevant templates for a planned race and enforcing a clearer winner.

**Actions (high level):**
- When `desired_race_name` is set, have `_pick_race_square` ask `RaceIndex` for:
  - The canonical planned race.
  - The full set of template candidates for that canonical name, including any ambiguity-group members.
- Pass the **entire candidate list** to `RaceBannerMatcher` for the ROI comparisons, rather than only the single desired race template.
- Define a decision rule for scheduled races, for example:
  - Accept a candidate only if the template score for the **intended race** is above a threshold and exceeds all other candidate templates by a margin.
  - If a different race’s template wins decisively (e.g., Hanshin template > Asahi template by margin), treat this as an ambiguous page and **do not lock in yet**.
- Keep the existing `MINIMUM_RACE_OCR_MATCH`/`OCR_DISCARD_MIN` logic but consider tightening thresholds for scheduled races to avoid early acceptance on weak signals.
- Preserve current behavior for non-scheduled races (no `desired_race_name`) so generic flows stay fast and unchanged.

**Affected files (expected):**
- `core/actions/race.py` (inside `_pick_race_square` scheduled-race path only).
- `core/perception/analyzers/matching/race_banner.py` (if additional helper APIs are useful, e.g., multi-name scoring utilities).

**Quick validation:**
- Enable verbose logging for a planned race day and confirm logs show:
  - The ambiguity group used for candidate templates.
  - Per-page scores for Asahi vs Hanshin (or similar) with clear winner logic.
- Simulate or replay captures where previously the wrong race was picked and verify that no click occurs until the right race clearly wins or ambiguity is resolved.

---

### Step 3 — Add optional full-list scan + global best selection for scheduled races
**Goal:** Provide a non-greedy, more robust path that scans across all visible pages before committing to a single race card, used only when needed.

**Actions (high level):**
- Introduce a mode or heuristic in `_pick_race_square` that, when `desired_race_name` is set and per-page confidence is **not high enough** or matches are ambiguous, switches into **full-scan** behavior:
  - During the existing scroll loop, instead of returning as soon as a good page-local candidate is found, accumulate a list of candidate descriptors per card (e.g., approximate y-range, OCR title, banner match scores, badge rank, and which template won per ambiguity group).
  - Track the globally best candidate across all pages according to a combined score that favors:
    - Correct template match.
    - Title OCR match.
    - Rank consistency and any known `order` constraints from `RaceIndex`.
- After scanning all pages, determine whether a **single global winner** exists that exceeds thresholds and margin constraints.
- Implement a second, targeted pass that restarts from the top of the race list and re-identifies the global-best card using fresh detections and ROI checks (to avoid stale coordinates), then clicks it.
- Ensure this global path is **only used for scheduled races** and guarded by a config flag or heuristic (e.g., only if ambiguity group exists or if no page ever produced a clearly confident winner).

**Affected files (expected):**
- `core/actions/race.py` (extend `_pick_race_square` with global candidate aggregation and a second-pass re-selection mechanism).
- Potentially `core/settings.py` (add one or more toggles, e.g., `RACE_SCHEDULED_FULL_SCAN_ENABLE`, thresholds/margins).

**Quick validation:**
- On a logged run with a planned race and multiple G1 options:
  - Confirm the scroll loop completes through all pages when ambiguity exists.
  - Check logs that show a global-best candidate summary and a final second-pass click consistent with that candidate.
  - Verify that for simple cases (only one obvious race) the fast per-page behavior is still taken and full-scan is skipped.

---

### Step 4 — Telemetry, configuration, and safety guards
**Goal:** Make the new logic observable, tunable, and safe to roll out gradually.

**Actions (high level):**
- Add structured logging around scheduled race selection that surfaces:
  - Whether ambiguity groups were active.
  - Whether full-scan mode was triggered vs short-circuit selection.
  - Final chosen race name, template scores, and OCR title snippet.
- Add configuration surfaces in `Settings` for:
  - Enabling/disabling ambiguity-group/template-based tie-breaking.
  - Enabling/disabling full-scan for scheduled races.
  - Thresholds/margins for template vs OCR scores.
- Ensure defaults preserve current behavior as closely as possible (e.g., new behavior off-by-default or tuned to mimic existing thresholds), to allow controlled testing.

**Affected files (expected):**
- `core/settings.py` (flags and thresholds).
- `core/actions/race.py` (wiring flags into behavior and logs).

**Quick validation:**
- Toggle new flags in a local config and confirm behavior differences via logs.
- Verify that disabling the feature returns selection to approximately current behavior.

---

### Step 5 — Tests, documentation updates, and clean-up
**Goal:** Lock in correctness with regression coverage and update docs so future work understands the design.

**Actions (high level):**
- Add unit-style tests (or deterministic harness scripts) that:
  - Feed synthetic OCR + banner crops into the scoring logic and assert the intended race wins over confusing alternatives.
  - Exercise the ambiguity group logic and global best selection logic with controlled scores.
- Add integration-style tests or replay harnesses (even semi-manual) that run through planned race days with recorded screenshots for Asahi vs Hanshin and similar cases.
- Update relevant documentation:
  - Extend `docs/ai/features/race-synonimous-handling/RESEARCH.md` only if behavior diverges from current research notes.
  - Optionally add short notes to `docs/ai/SYSTEM_OVERVIEW.md` or a dedicated feature doc if the behavior becomes central.
- Remove any dead code paths (e.g., unused `_resolve_template_path` helper) once new design fully replaces them, ensuring no regressions.

**Affected files (expected):**
- `tests/` or small harness scripts under `docs/ai/features/race-synonimous-handling/`.
- `core/actions/race.py`, `core/utils/race_index.py`, `core/perception/analyzers/matching/race_banner.py` (only if clean-ups are identified).
- `docs/ai/features/race-synonimous-handling/RESEARCH.md` (minor sync if needed).

**Quick validation:**
- Run targeted tests or scripts and confirm they pass on known-good and known-bad scenarios.
- Confirm logs for ambiguous scheduled races clearly show correct disambiguation behavior.

---

### Step 6 — Finalization
**Goal:** Stabilize, verify, and prepare for rollout.

**Actions (high level):**
- Run linters and any existing test suites relevant to races and lobby flows.
- Sanity-check a few full runs (URA / Unity Cup) with and without planned races to verify there are no regressions outside scheduled-race logic.
- Adjust thresholds/margins based on initial empirical feedback and lock them into config defaults.

**Quick validation:**
- All tests and lint checks pass.
- Manual or recorded runs show the bot picking the correct planned race in ambiguous cases and behaving as before on generic race days.

## Test Plan
- **Unit:**
  - Functions in `RaceIndex` that expose ambiguity groups and banner templates.
  - Scoring helper(s) in `RaceFlow` for combining OCR, badge rank, and template scores, including margin logic between candidate templates.
  - Any new utilities that identify and re-locate the global-best card in the second pass.
- **Integration/E2E:**
  - Full career segments covering planned Asahi vs Hanshin days, verifying that:
    - With ambiguity groups and full-scan disabled, behavior matches baseline.
    - With features enabled, the intended scheduled race is selected consistently.
  - Cases with no ambiguity (only one planned race) to ensure performance and correctness remain acceptable.
- **UX/Visual (if applicable):**
  - Optional: compare debug screenshots for selected race cards against expected banners to confirm visual match.

## Verification Checklist
- [ ] Lint and type checks pass locally.
- [ ] Planned race selection logs clearly identify which race was chosen and why.
- [ ] Ambiguity groups are loaded and used only for configured races.
- [ ] Full-scan mode (if enabled) triggers only for scheduled races and ambiguous/low-confidence situations.
- [ ] Non-scheduled race behavior remains consistent with previous releases.

## Rollback / Mitigation
- Disable the new behavior via `Settings` flags (e.g., turn off ambiguity-group and full-scan logic) to revert to the previous per-page greedy selector.
- If necessary, remove ambiguity-group configuration entries to fall back to single-template matching.
- As a last resort, revert the commit(s) touching `RaceFlow` and `RaceIndex`, keeping the template index data intact.

## Open Questions (if any)
- Which additional race pairs beyond Asahi vs Hanshin should be treated as ambiguity groups initially, and should this list be maintained in code or via external config?
- What runtime performance budget is acceptable for the full-scan + second-pass logic on slower machines or remote inference setups?
- Do we need UI/config-surface controls in the Web UI for tuning these thresholds, or is a config-file-only approach sufficient for now?
