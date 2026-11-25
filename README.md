# Wednesday 25 November 2026 — The World in One Day

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/seannbeez/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/seannbeez/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

A single 1024×1024 image summing up Wednesday 25 November 2026's world news,
built for the [news-image-20261125 bounty](https://make.fun/bounty/news-image-20261125)
on make.fun. The program is a one-file Node 22 copy: `main.ts` copies the
vendored `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`.

## The image

30 stories from 8 regions — 3 heroes + 10 numbered minis + 17 more — every
story with a sourced fact line and a CONFIRMED / REPORTED / CLAIM badge.

- **Heroes:** CIA & ODNI hit by cyberattack on unclassified intel systems;
  Huawei convicted on 10 of 12 counts in Brooklyn; Iran claims a 4th tanker
  hit a mine in the Strait of Hormuz (stamped CLAIM — CENTCOM rejects it).
- **6 giant numbers:** +30% · 700,000+ · 10 of 12 · 19,854 · 5–1 · 33.7%.
- **Also inside:** a 7-tick UTC timeline for the 22:00–01:45 overnight cycle
  (sourced times only, never fabricated), a world map with 30 numbered pins,
  a two-way DATE CHECK box (left-outs dated, never re-dated as Wednesday
  news, plus NOT YET items), and a verification legend. Edition closed
  01:45 UTC.
- **Flat vector art only**, cream paper, date in the largest type. Numbers
  are the safe figures: Nvidia +30% only (no dollar value-added figure);
  700,000+ is Russian soldiers killed *including missing* (hacked Rosstat
  analysis), labelled with the qualifier.

## How it was built

`build.py` renders the image with Pillow (deterministic — two builds are
byte-identical) and audits every text box for overflow, truncation and
overlap. `gate.py` runs the determinism check, a 300px LANCZOS downscale,
and the 300px legibility gate. Candidate B (this entry, data-wire layout)
beat Candidate A in a blind duel 92–78 at 300px and 95–82 full frame, then
beat the live Top 1 (wurk) 94–78 at 300px and 92–88 full frame — see
`H2H_ANALYSIS.md`. Full research, sources and date checks: `RESEARCH.md`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png (208,338 bytes, sha256
# cc3860c8ec9ffad107f01aca0a7806e18d917164618b6f0ce52aef180b807735)
```

## License

MIT — see `LICENSE`.
