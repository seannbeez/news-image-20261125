# H2H ANALYSIS — news-image-20261125 (blind duels, bin/gemini.py judge, gemini-3.6-flash)

All duels blind (neutral filenames, no candidate identity in the prompt).
Judge criteria: the bounty rubric in order (C1 one day's news + names that
day; C2 selection/breadth; C3 reads, nothing false; C4 faithful; C5 craft,
legible at 300px). Scores are the judge's Elo-style 0–100, not official
scores.

## Duel 1 — Candidate A vs Candidate B, 300px

- **Winner: B, 92–78.** "B arranges the 3 hero stories and world map in a
  balanced grid, far easier to identify at thumbnail size. A squeezes all
  three heroes into a narrow top row, compressed, less legible text. B
  maintains superior layout clarity and contrast with less visual clutter."

## Duel 2 — Candidate A vs Candidate B, full frame

- **Winner: B, 95–82.** "B features a cleaner visual hierarchy and superior
  graphic design grid. B's timeline strictly matches the 01:45 UTC edition
  window, whereas A includes events hours after edition close. B maps all
  30 story numbers cleanly onto the world map."

## Duel 3 — Candidate B vs live Top 1 (wurk, 97.8974%), 300px

- **Winner: B, 94–78.** "B features a massive, bold date header that
  dominates the top of the page. B includes a prominent, highly readable red
  6-number data strip. B's layout has superior graphic contrast and
  composition readability at thumbnail resolution."

## Duel 4 — Candidate B vs live Top 1 (wurk), full frame

- **Winner: B, 92–88.** "B features an exceptionally dense, well-structured
  visual architecture with 30 stories, clear verification badges, and key
  statistical callouts. B's vector typography and infographic layout provide
  superior legibility across all detailed story cards."

## Critical catch from Duel 4 (fixed before submit)

The champion-duel judge flagged a real error in OUR entry: the masthead
read "TUESDAY 25 NOVEMBER 2026" — but 25 Nov 2026 is a **Wednesday**
(verified: `date -d 2026-11-25` = Wednesday; 24 Nov = Tuesday). The error
came from the research file's inconsistent "ALSO ON TUESDAY" header and
was propagated through the coordinator brief into both candidates. The
wurk entry correctly says Wednesday.

**Micro-surgery (separate surgeon session, 4 strings in cand-b/build.py):**
masthead → "WEDNESDAY 25 NOVEMBER 2026"; micro-bar → "ALL FROM THIS
WEDNESDAY"; ALSO header → "ALSO ON WEDNESDAY 25 NOVEMBER". "Expected
Tue/Wed" in the DATE CHECK (tariff announcement, Tue 24 / Wed 25) was
deliberately left unchanged — it is story text, not a weekday claim.
Re-verified after the fix: gate PASS, two runs byte-identical, 300px PASS
(WEDNESDAY fits at full masthead size, 928.7px ≤ 976px cap), new sha256
cc3860c8ec9ffad107f01aca0a7806e18d917164618b6f0ce52aef180b807735.

## Why B won (summary)

- Numbers-first band directly under the masthead: the 6-stat strip reads at
  300px where A's equal-hero row compresses.
- Timeline honesty: only sourced times labelled, strictly inside the
  01:45 UTC edition window; A printed ticks at ~12:00–19:00 under a
  "22:00–01:45 overnight cycle" header — self-contradictory.
- Asymmetric hero layout (Hero 1 dominant left, map + Hero 3 right) gives
  the 300px thumbnail one big focal instead of three equal small ones.
- 30 real reported stories vs wurk's 21 (and vs #2's 50, of which 43 are
  FORECAST/SCHED calendar items — a C1/C4 weakness we do not share).

## Honest caveat

Local duels are a validity/quality gate, not a final-rank signal: the
news-image final is a 3-match lottery gated by opponent strength (last
final: dev 98.34% → final 56.96%, #5,218). B won every local duel
decisively, which is the most the local evidence can say.
