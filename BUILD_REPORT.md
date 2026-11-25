# BUILD REPORT — Candidate B (Data-Wire/Analytics) — news-image-20261125

- Built: Wed 25 Nov 2026 ~08:50–09:00 WIB, session started after competition
  open (2026-11-25T00:00:00Z). Account @seannbeez.
- Builder did NOT read or touch `cand-a/` (blind duel integrity).
- No submit, no `makefun record/submit/check`, no GitHub repo created.

## Deliverables

| File | Detail |
|---|---|
| `entry.png` | 1024×1024 PNG, **208,338 bytes** (limit 1,048,576), sha256 `cc3860c8ec9ffad107f01aca0a7806e18d917164618b6f0ce52aef180b807735` |
| `entry-300px.png` | 300×300 LANCZOS downscale, 102,815 bytes, sha256 `47cb558d2c85d7334ff6ec300fe6428aea4aa399ae8d430b3c7b62768c25c99f` |
| `build.py` | Deterministic Pillow renderer (no network/clock/randomness) |
| `gate.py` | Determinism + size + dimensions gate |
| `BUILD_REPORT.md` | This file |

## Gate result

- `python3 gate.py` → **GATE PASS**. Build exit 0, zero audit problems
  (174 tracked text boxes, no overflow/truncation/overlap), two runs
  byte-identical (sha256 match), 1024×1024, 208,338 B ≤ 1 MiB.

## 300px verdict — PASS (visually inspected)

- Date "WEDNESDAY 25 NOVEMBER 2026" is the largest readable element.
- All 6 numbers in the red data band readable: +30%, 700,000+, 10 of 12,
  19,854, 5–1, 33.7%.
- All 3 heroes identifiable (shield = CIA cyberattack, courthouse =
  Huawei trial, tanker + mine = Hormuz claim); red band, timeline and
  map structure read clearly at 300px.

## Layout (asymmetric, numbers-first)

Masthead (micro-bar + giant serif date + red italic sub-dek + edition
line) → 6-stat red data band directly below masthead → 7-tick overnight
UTC timeline → left column: Hero 1 (CIA/ODNI) stacked over Hero 2
(Huawei); right column: world pin map over Hero 3 (Hormuz CLAIM) →
10 numbered minis (2 rows × 5, icon + kicker + badge + source each) →
ALSO ticker (3 columns, 17 items) → DATE CHECK box → legend + sources.

## Story / region counts

- **30 stories, 8 regions**: 3 heroes + 10 minis + 17 ALSO.
  - Heroes: 1 CIA/ODNI cyberattack (CONFIRMED), 2 Huawei 10/12
    (CONFIRMED), 3 Hormuz tanker claim (CLAIM, "CENTCOM rejects" noted).
  - Minis 4–13: Putin retaliation, 700,000 Russian soldiers killed,
    Poland/NATO jet, Benghazi self-defence, Trump tariffs, Nvidia +30%,
    Senegal AFCON, Real Madrid 5–1, India Lowy Index, WHO Ebola DRC.
  - ALSO 14–30: Zhytomyr, Odesa, EU sanctions, Kyiv jets, Gaza strikes,
    Gaza toll 74,746 (REPORTED only), WFP 266m, BJP–Akali, Nepal PM,
    Japan–India drills, Denmark ghetto law, Puigdemont, Estonia border,
    Brazil storms, Ethiopia displacement, S. Africa 33.7%, England T20I.
  - Regions: North America, Europe, Middle East, Africa, East Asia,
    South Asia, Oceania, Latin America.
- World pin map: 30 numbered pins (1–30 = story numbers); clustered
  Europe/US pins fanned out with leader lines to keep numbers legible.
- Timeline: 7 ticks across 22:00–01:45 UTC overnight cycle; only sourced
  times labelled (22:46 Huawei verdict, 00:00 CIA hack reported, 00:25
  Putin retaliation, 01:45 edition closed); other ticks unlabeled.
- DATE CHECK: left-outs COP31 (22 Nov), Merkury (22 Nov), Kh-101 Poland
  (20 Nov), Huang reinstatement (22–23 Nov), Alcaraz (22 Nov); NOT YET:
  Chess Game 2, Trump tariffs, Wed-night UCL, Hormuz verification.
- Legend: CONFIRMED green / REPORTED blue / CLAIM amber (minis header
  + footer line).

## Numbers strip (safe figures only)

+30% Nvidia (no $ figure anywhere) · 700,000+ Russian soldiers killed,
incl. missing, hacked Rosstat analysis · 10 of 12 Huawei counts ·
19,854 Brazil storm displaced · 5–1 Real Madrid over PSV · 33.7%
South Africa unemployment. Gaza toll 74,746 is REPORTED only. Ebola
totals are WHO-reported cumulative only (11,762 cases, 5,775 deaths).

## Dropped / changed items

- **NONE dropped. All 30 stories present.**
- Denmark ghetto-law item (ALSO #11): sources in RESEARCH.md
  contradicted each other, so re-verified with one live search
  (25 Nov ~08:55 WIB). Reuters + CBS + multiple outlets agree: the
  Supreme Court **upheld** the evictions on Mon 23 Nov (7 families,
  91 leases, Nøjsomhed, Helsingør); the FrontPages.eu opposite summary
  is the outlier. Contradiction resolved → item **KEPT** as
  "Denmark court backs 'ghetto law' evictions (Reuters)". No verdict
  was drawn beyond the verified reporting.
- Corrections applied (audit findings, overriding Gemini blueprint):
  story split is 3 + 10 + 17 = 30 (Gemini wrote 12 + 15 — wrong);
  700,000 is soldiers **killed incl. missing**, not "casualties &
  missing"; Nvidia strip uses +30% only, never a $ value-added figure.
- Layout fixes during build: hero icons shrunk (s 26→22) after the
  audit flagged icon/fact overlap; DATE CHECK box enlarged (76→82px)
  after visual inspection showed the 5th left-out line clipped at the
  box edge; Europe pin cluster fanned out with leader lines and pin
  radius reduced (6→5px) after inspection showed a red blob.

## Fonts used

- Liberation Serif Bold (masthead date), Liberation Serif Italic
  (red sub-dek), Liberation Sans Bold/Regular (all other text).
  Fallback: DejaVu Serif/Sans. All local system fonts; no downloads.

## Content provenance

Every story, number and date comes from
`~/workspace/makefun/news-image-20261125/RESEARCH.md` only (edition
closed 01:45 UTC 25 Nov 2026), except the Denmark re-verification
above (live search, Reuters-corroborated). No story or number invented.
Flat vector art only (Pillow-drawn shapes/icons); no AI/painterly
images, no photos.

## MICRO-SURGERY — weekday fix (25 Nov 2026 ~09:50 WIB)

- **Why:** 25 November 2026 is a **Wednesday** (verified `date -d
  2026-11-25` = Wednesday; 24 Nov = Tuesday). The masthead wrongly
  said TUESDAY — a Criterion #1/#3 error caught by the champion duel.
- **Changed in `build.py` only (4 rendered strings, TUESDAY →
  WEDNESDAY):**
  - L376 micro-bar: "30 STORIES · 8 REGIONS · ALL FROM THIS TUESDAY"
    → "… ALL FROM THIS WEDNESDAY"
  - L382 fit-check measure line: "TUESDAY 25 NOVEMBER 2026" →
    "WEDNESDAY 25 NOVEMBER 2026"
  - L385 masthead date: "TUESDAY 25 NOVEMBER 2026" → "WEDNESDAY 25
    NOVEMBER 2026"
  - L568 ALSO header: "ALSO ON TUESDAY 25 NOVEMBER — 17 MORE STORIES"
    → "ALSO ON WEDNESDAY 25 NOVEMBER — 17 MORE STORIES"
- **Sweep:** case-insensitive grep for `tuesday`/`tue` found one more
  hit, L607 "Trump tariff announcement — expected Tue/Wed" (DATE CHECK
  box). Left unchanged on purpose: it is story text (a forward-looking
  expectation, not a claim that 25 Nov is Tuesday) and the task forbids
  changing story text; "expected Wed/Wed" would be nonsense. No other
  weekday reference remains in rendered strings.
- **Fit:** WEDNESDAY (2 chars longer) still fits at the full masthead
  size 58 — measured 928.7px ≤ 976px cap — so **no font-size reduction**
  was needed; no layout, colour, geometry, story, number or badge
  changed.
- **Re-verification:** `python3 build.py` exit 0, zero audit problems
  (174 boxes); `python3 gate.py` → **GATE PASS**; two runs
  byte-identical, sha256
  `cc3860c8ec9ffad107f01aca0a7806e18d917164618b6f0ce52aef180b807735`,
  1024×1024, 208,338 B ≤ 1 MiB. `entry-300px.png` re-rendered
  (LANCZOS, 300×300) and visually inspected: WEDNESDAY date is still
  the largest readable element, all 6 numbers in the red band readable,
  all 3 heroes identifiable.
- No submit, no `makefun record/submit/check`, no GitHub repo, no
  `cand-a/` touched. Deliverables table above updated to the new
  hashes/sizes.
