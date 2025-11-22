---
date: 2025-11-22T11:35:00-05:00
topic: race-synonimous-handling
status: research_complete
---

# RESEARCH — race-synonimous-handling

## Research Question
Improve robustness of **scheduled race selection** so that races with similar banners/names (e.g. *Asahi Hai Futurity Stakes* vs *Hanshin Juvenile Fillies*) are not confused, using the existing race datasets and banner template index.

## Summary (≤ 10 bullets)
- `RaceIndex` builds a canonical index over `datasets/in_game/races.json` and a banner template map from `assets/races/templates/index.json`.
- Planned/scheduled races come from `Lobby.plan_races` / scenario presets and are surfaced as `planned_race_name` + canonical key on Lobby state.
- `RaceFlow._pick_race_square` is the main selection routine; when `desired_race_name` is set it performs a **page-local greedy pick** as soon as any candidate score passes a threshold.
- OCR-based title matching (`clean_race_name` + `fuzzy_ratio`) is combined with badge rank and optional special handling for names containing `varies`.
- Banner template matching (`RaceBannerMatcher`) is already wired into `_pick_race_square` for desired races using `RaceIndex.banner_template(desired_race_name)` and the template index.
- Banner matching currently restricts to the desired race’s own template and is applied only to the **top few candidates on each page**, not globally.
- Ambiguity between similar G1 banners (e.g. Asahi vs Hanshin) is likely when both share structure, date, and similar card layouts; current logic may lock onto the first “good enough” square.
- For non-planned races the fallback still uses star count + badge rank only, with no template matching.
- There is room to implement a **non-greedy, full-list scan path** for planned races that aggregates candidate scores across scrolls and then revisits the best one, but this will require careful handling of scrolling and stale bounding boxes.

## Detailed Findings (by area)

### Area: Race datasets & indexing
- **Why relevant:** Defines how races are named, canonicalized, and associated with dates/templates; drives all planned-race logic.
- **Files & anchors:**
  - `core/utils/race_index.py:31–42` — `canonicalize_race_name()`; normalizes punctuation, accents, and non-word chars to build a lowercase key used across maps.
  - `core/utils/race_index.py:187–235` — `RaceIndex._ensure_loaded()`; loads `Settings.RACE_DATA_PATH` (JSON map of `race_name -> occurrences`), populates:
    - `_date_to_entries[date_key] -> [entry]`
    - `_name_to_dates[canonical_name] -> [date_key]`
    - `_name_to_entries[canonical_name] -> [entry]`
    - Each `entry` gets `display_title`, `rank`, `order`, `canonical_name`.
  - `core/utils/race_index.py:237–307` — core query helpers:
    - `by_date(key)` — races on a given career date.
    - `entry_for_name_on_date(race_name, key)` — single occurrence metadata (includes `display_title`, `rank`, `order`).
    - `expected_titles_for_race(race_name)` — list of `(display_title, rank)` across all dates; used when date_key is unknown.
  - `core/utils/race_index.py:309–376` — banner template loading from `assets/races/templates/index.json`.
    - Reads mapping `"Race Name" -> "web/public/race/...png"`.
    - Builds `_banner_templates[canonical_name] = { name, path, public_path, hash_hex, size }` using phash and image size.
    - `banner_template(name)` returns this metadata per canonical name; `all_banner_templates()` is used by the matcher.
- **Cross-links:**
  - `core/perception/analyzers/matching/race_banner.py` consumes `banner_template` / `all_banner_templates` for template matching.
  - `core/actions/race.py` asks `RaceIndex.entry_for_name_on_date` and `RaceIndex.expected_titles_for_race` when computing `expected_cards` for `desired_race_name`.

### Area: Planned / scheduled races
- **Why relevant:** Only planned races should use the more expensive and accurate matching logic; bug reports about specific G1 mis-selection are under this path.
- **Files & anchors:**
  - `core/actions/lobby.py:837–883` — `Lobby._plan_race_today()`:
    - Derives `key = date_key_from_dateinfo(self.state.date_info)`.
    - If `key in self.plan_races` and not in `_raced_keys_recent`, sets:
      - `state.planned_race_name = raw_name` (string from config/preset).
      - `state.planned_race_canonical = RaceIndex.canonicalize(raw_name)`.
      - `state.planned_race_tentative` from `plan_races_tentative[key]`.
    - Logs `[planned_race] plan_selected`.
  - `core/agent_scenario.py:197–216` — `_desired_race_today()`:
    - Re-builds `key` from `lobby.state.date_info`.
    - Reads from `plan = getattr(self.lobby, "plan_races", None) or self.plan_races`.
    - When a plan exists, canonicalizes `raw_race`, logs `[agent] Planned race for {key}: raw=... canon=...`, and sets
      `lobby.state.planned_race_canonical` / `planned_race_name` again.
    - Returns the raw string; callers treat this as `desired_race_name`.
  - `core/actions/ura/lobby.py:129–174` — checks `state.planned_race_name` in the lobby loop, and when guards pass, returns a `"TO_RACE"` transition; from there the flow enters RaceFlow.
- **Cross-links:**
  - `RaceFlow._pick_race_square()` is invoked with `desired_race_name` and (when available) `date_key`, so planned race metadata + templates feed into the low-level selector.

### Area: RaceFlow square selection & greedy behavior
- **Why relevant:** This is where the system decides which race square to click; mis-selection between similar G1s happens here.
- **Files & anchors:**
  - `core/actions/race.py:302–331` — `_pick_race_square(...)` signature and constants.
    - Supports `desired_race_name` and `date_key` plus priority knobs.
    - Key thresholds:
      - `MINIMUM_RACE_OCR_MATCH = 0.91`.
      - `OCR_DISCARD_MIN = 0.3` for rejecting OCR/template candidates.
      - `OCR_SCORE_WEIGHT = 0.2` blending OCR with template score.
  - `core/actions/race.py:331–349` — `clean_race_name()`; normalizes OCR title text by uppercasing, stripping directional words (RIGHT/LEFT/INNER/OUTER), correcting common OCR confusions (TURT→TURF, DIRF→DIRT), removing `/`, and dropping single-character tokens.
  - `core/actions/race.py:355–395` — expected card computation:
    - If `desired_race_name` is set:
      - With `date_key` → `RaceIndex.entry_for_name_on_date` to get `display_title`, `rank`, `order`.
      - Else → `RaceIndex.expected_titles_for_race` to aggregate `(display_title, rank)` pairs.
      - Fallback to `(desired_race_name, "UNK")` when dataset is missing.
  - `core/actions/race.py:396–432` — local template index helpers:
    - `_load_template_index()` reads `assets/races/templates/index.json` into a local dict, though in current code `_resolve_template_path()` is not used after definition. Effective banner matching is instead done via `RaceIndex.banner_template()` + `RaceBannerMatcher` (see below).
  - `core/actions/race.py:435–463` — top-level scroll loop & single-square fast path:
    - For each scroll `scroll_j` in `0..max_scrolls`:
      - Capture frame + YOLO detections; sort `race_square` by y.
      - Deduplicate `race_star` detections; load `race_badge`.
      - If **only one** square is visible on first page, immediately selects it (with optional `need_click` optimization) without OCR/template checks.
  - `core/actions/race.py:465–541` — per-page score computation for desired races:
    - For each square on the current page:
      - Counts stars inside square.
      - Identifies badge + its xyxy to define an OCR ROI to the right of the badge.
      - OCRs title text (`txt`), normalizes via `clean_race_name`.
      - For each `(expected_title, expected_rank)` in `expected_cards`:
        - Computes `s = fuzzy_ratio(txt, expected_title_n.upper())`.
        - If `"varies"` appears in the expected title, applies token-based matching override (to support cards where part of the title can change).
        - Penalizes mismatched badge rank by `-0.20` when badge OCR is known.
      - Tracks per-square `best_score_here` and updates page-local `page_scores` and the global `best_named`/`page_best`.
  - **Greedy step:** `core/actions/race.py:542–603`:
    - Once `page_scores` is populated, it is sorted descending.
    - **Per-page template matching:**
      - Fetches a single banner template candidate list: `[RaceIndex.banner_template(desired_race_name)]` (if any); this uses `assets/races/templates/index.json` via `RaceIndex._load_banner_templates`.
      - For up to the top 4 `page_scores` entries:
        - Defines a left-side ROI (badge-to-left) on the card.
        - OCRs this ROI and re-normalizes.
        - Computes a new OCR score vs `desired_race_name`.
        - Calls `self._banner_matcher.best_match(roi_img, candidates=[c["name"] for c in card_candidates])` to score banner similarity.
        - If both OCR and template score are low (`best_ocr < OCR_DISCARD_MIN` and `match_score < 0.5`), the candidate is hard-discarded by setting `adjusted_score = -1.0`.
        - Otherwise, blends `base_score`, OCR, and template scores into `adjusted_score`.
      - Resort `page_scores` by the adjusted score.
    - Finally chooses `top_sq, top_score = page_scores[0]` and, **if `top_score >= MINIMUM_RACE_OCR_MATCH`**, immediately returns that square for clicking.
    - This is the **page-local greedy pick**: it never compares candidates across different scroll pages.
  - `core/actions/race.py:619–680` — non-desired fallback path:
    - When `desired_race_name` is not set, falls back to star count + badge rank to pick best G1/other races, again greedily per scroll.
- **Cross-links:**
  - `core/perception/analyzers/matching/race_banner.py:45–127` implements the `RaceBannerMatcher` used by `_pick_race_square` for the per-page tie-breaker.
  - Template metadata from `RaceIndex.banner_template()` is ultimately derived from `assets/races/templates/index.json`, which is the special list you maintain for synonym/special-case banners.

### Area: Race banner matching implementation
- **Why relevant:** This is where template similarity is scored; understanding how candidates are picked informs why Asahi vs Hanshin may be confused.
- **Files & anchors:**
  - `core/perception/analyzers/matching/race_banner.py:45–74` — `RaceBannerMatcher` definition and caching.
  - `core/perception/analyzers/matching/race_banner.py:75–82` — `best_match()` returns the top result from the list returned by `match()`.
  - `core/perception/analyzers/matching/race_banner.py:83–127` — `match()`:
    - Prepares a region from the card image (no extra cropping for banners).
    - Fetches candidate template names: either provided explicitly or `RaceIndex.all_banner_templates().values()`.
    - Uses a fused metric combining TM, phash, and histogram similarity scores via `TemplateMatcherBase._match_region`.
    - Logs ambiguities when the top two scores differ by < 0.05.
  - `core/perception/analyzers/matching/race_banner.py:129–157` — `_resolve_template()`:
    - Given a `race_name`, canonicalizes it and retrieves the pre-loaded template metadata from `RaceIndex.banner_template()`.
    - Prepares a `TemplateEntry` (loads image, computes preprocessed forms) and memoizes it by canonical name.
- **Cross-links:**
  - In `_pick_race_square`, we only pass the **desired race’s own template** as candidate; we don’t consider rival templates like Hanshin Juvenile Fillies while evaluating Asahi Hai.
  - For non-desired (generic) selection there is currently **no** template-based re-ranking, only badge rank + stars.

## 360° Around Target(s)

- **Target file(s):**
  - `core/actions/race.py` — low-level race card selection and use of banner templates.
  - `core/utils/race_index.py` — dataset-backed index and banner template registry.
  - `core/perception/analyzers/matching/race_banner.py` — banner template matcher.
  - `core/actions/lobby.py` — planned race determination and guard logic.
  - `core/agent_scenario.py` — surfaces scheduled race name to RaceFlow via `_desired_race_today()`.

- **Dependency graph (depth 2):**
  - `datasets/in_game/races.json` → `core/utils/race_index.py` → `core/actions/lobby.py`, `core/agent_scenario.py`, `core/actions/race.py`.
  - `assets/races/templates/index.json` → `core/utils/race_index.py._load_banner_templates()` → `RaceIndex.banner_template()` / `all_banner_templates()` → `core/perception/analyzers/matching/race_banner.py` & indirectly `core/actions/race.py`.
  - `core/perception/analyzers/matching/base.py` (via `TemplateMatcherBase`) → provides fused TM/hash/hist behavior consumed by `RaceBannerMatcher`.
  - `core/settings.py` → provides `RACE_DATA_PATH`, `ROOT_DIR`, and flags that determine whether banner matching uses local vs remote matcher.
  - `core/actions/ura/lobby.py` / other scenario-specific lobbies → call into `RaceFlow` for actual race execution.

## Open Questions / Ambiguities

1. **Scope of full-list scan for scheduled races**  
   - *Question:* For planned races, should `_pick_race_square` **always** scan all scroll pages first (aggregating candidates) before deciding, or only when the first candidate’s score is below a stricter “scheduled” threshold?  
   - *Why it matters:* Full scans cost extra time and YOLO/OCR calls; a hybrid approach (fast path when match is extremely confident, fallback to full scan when ambiguous) might be a better UX/perf tradeoff.  
   - *Suggested resolution:* Introduce a `SCHEDULED_RACE_FULL_SCAN` mode or threshold, e.g. only fall back to full-list scan when top page-local candidate score is in a “gray band” (e.g. 0.91–0.96) or when `RaceBannerMatcher` reports ambiguous match.

2. **Design for revisiting the globally best card after scanning**  
   - *Question:* After scanning all pages, how should we **navigate back** to the best candidate card reliably?  
   - *Why it matters:* Current bounding boxes become stale as soon as we scroll; we can’t just click using coordinates captured earlier. A robust design is needed for non-greedy selection.  
   - *Suggested resolution:* Store summary metadata for the best candidate (e.g. expected `display_title`, a hash of the banner ROI, approximate badge rank). Then re-run a targeted search from the top: scroll from the first page again, using banner matching with a restricted candidate set (potentially multiple templates like Asahi + Hanshin) until we find the card whose template score matches the stored best. Only in this second pass do we click.

3. **Template candidate set for ambiguous pairs**  
   - *Question:* For problematic races like *Asahi Hai Futurity Stakes* vs *Hanshin Juvenile Fillies*, should we explicitly include **both** templates in the candidate list when evaluating cards for a scheduled Asahi race?  
   - *Why it matters:* Right now the banner matcher only compares against the desired race’s template. If Hanshin’s banner is visually closer to the observed card (or OCR is noisy), scores may drift. Including both templates allows us to assert that Asahi’s template should win by a margin; otherwise we might prefer falling back to OCR title + date constraints.  
   - *Suggested resolution:* Extend `assets/races/templates/index.json` or a parallel config to encode “template groups” or synonym sets (e.g. `["Asahi Hai Futurity Stakes", "Hanshin Juvenile Fillies"]`), and teach `_pick_race_square` to pass the entire group as `candidates` to `RaceBannerMatcher`. The final decision could then be: *only accept the scheduled race if its template beats others by a configurable margin; otherwise keep scanning or fall back to OCR-only logic*.

## Suggested Next Step

- Draft `PLAN.md` for `race-synonimous-handling` under the same feature folder with:
  - Concrete proposal for a **two-phase scheduled race picker**:
    1. Fast per-page greedy selection (current behavior) but guarded by stricter thresholds and banner-ambiguity checks.
    2. When ambiguous (or when a special race/synonym pair is configured), perform a full scroll scan accumulating candidates, then run a second targeted pass to click the globally best match.
  - Design for a small configuration layer mapping race names to **ambiguity groups** and/or to a specific multi-template candidate set.
  - Testing strategy:
    - Record debug captures around Asahi vs Hanshin dates and simulate `RaceFlow._pick_race_square` offline.
    - Regression tests that force conflicting templates and verify that scheduled race selection chooses the correct card, or intentionally declines when confidence is low.
