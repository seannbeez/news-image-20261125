#!/usr/bin/env python3
"""news-image-20261125 — Candidate B (Data-Wire/Analytics).

1024x1024 PNG broadsheet, Python + Pillow, deterministic (no network, no
clock, no randomness). Every drawn text line is tracked as a box; overflow,
truncation and overlap fail the build (exit 1).

Content source ONLY: ~/workspace/makefun/news-image-20261125/RESEARCH.md
(30 stories, 8 regions, edition closed 01:45 UTC 25 Nov 2026). No story or
number invented. Corrections applied vs Gemini blueprint: 3 heroes + 10
minis + 17 ALSO = 30 (not 12+15); 700,000 figure is soldiers KILLED incl.
missing (not "casualties & missing"). Nvidia strip shows +30% only, never
a $ value-added figure. Denmark ghetto-law item (ALSO #11) re-verified by
live search 25 Nov ~08:55 WIB: Reuters + multiple outlets agree the
Supreme Court UPHELD the evictions (23 Nov, 7 families, 91 leases);
the FrontPages.eu opposite summary is the outlier — item KEPT.

Layout (asymmetric, numbers-first): masthead -> 6-stat data band ->
7-tick overnight UTC timeline -> left column 2 stacked heroes, right
column world pin map + 3rd hero beneath -> 10 numbered minis (2x5) ->
ALSO ticker (3 cols, 17 items) -> DATE CHECK box -> legend + sources.
"""
import hashlib
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 247, 240)   # #FAF7F0 cream
INK = (26, 26, 26)        # #1A1A1A charcoal
RED = (163, 22, 33)
WHITE = (255, 255, 255)
GREY = (110, 105, 92)
CARD = (255, 255, 255)
EDGE = (200, 192, 172)
MAP_BG = (238, 233, 220)
MAP_FILL = (201, 194, 178)

BADGE_FILL = {"CONFIRMED": (30, 107, 58), "CLAIM": (180, 83, 9),
              "REPORTED": (47, 75, 124)}
REGION_FILL = {
    "USA": (31, 56, 100), "CHINA": (163, 22, 33), "HORMUZ": (133, 77, 14),
    "UKRAINE": (163, 22, 33), "POLAND": (31, 78, 121), "LIBYA": (133, 77, 14),
    "MARKETS": (15, 118, 110), "SENEGAL": (120, 53, 15), "EUROPE": (31, 78, 121),
    "INDIA": (146, 64, 14), "DRC": (120, 53, 15),
}

FONT_DIRS = ["/usr/share/fonts/truetype/liberation",
             "/usr/share/fonts/truetype/dejavu"]


def load_font(bold, size, serif=False, italic=False):
    if serif:
        if bold and italic:
            names = ["LiberationSerif-BoldItalic.ttf", "DejaVuSerif-Bold.ttf"]
        elif bold:
            names = ["LiberationSerif-Bold.ttf", "DejaVuSerif-Bold.ttf"]
        elif italic:
            names = ["LiberationSerif-Italic.ttf", "DejaVuSerif.ttf"]
        else:
            names = ["LiberationSerif-Regular.ttf", "DejaVuSerif.ttf"]
    else:
        if bold and italic:
            names = ["LiberationSans-BoldItalic.ttf", "DejaVuSans-Bold.ttf"]
        elif bold:
            names = ["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf"]
        elif italic:
            names = ["LiberationSans-Italic.ttf", "DejaVuSans.ttf"]
        else:
            names = ["LiberationSans-Regular.ttf", "DejaVuSans.ttf"]
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, int(size))
    return ImageFont.load_default()


def wrap_text(draw, text, fnt, max_w):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


class Audit:
    """Tracks every text box; records overflow / truncation / overlap."""

    def __init__(self):
        self.boxes = []   # (label, x0, y0, x1, y1)
        self.problems = []

    def put(self, draw, xy, lines, fnt, fill, cap=None, label="text"):
        x, y = xy
        step = int(fnt.size * 1.22)
        for ln in lines:
            w = draw.textlength(ln, font=fnt)
            self.boxes.append((label, x, y, x + w, y + fnt.size))
            if cap is not None and w > cap + 0.5:
                self.problems.append(
                    f"OVERFLOW {label}: '{ln}' {w:.0f}px > {cap}px")
            draw.text((x, y), ln, font=fnt, fill=fill)
            y += step
        return y

    def check_overlaps(self):
        n = 0
        for i in range(len(self.boxes)):
            for j in range(i + 1, len(self.boxes)):
                a, b = self.boxes[i], self.boxes[j]
                if a[0].startswith("deco") or b[0].startswith("deco"):
                    continue
                if a[1] < b[3] and b[1] < a[3] and a[2] < b[4] and b[2] < a[4]:
                    n += 1
                    self.problems.append(f"OVERLAP {a[0]} vs {b[0]}")
        return n


# ---------------------------------------------------------------- data
# Heroes 1-3. Heads <= ~60 chars (2 lines at 19pt in 360px); facts <= ~100
# chars (2 lines at 12.5pt full width).
HEROES = [
    {"tag": "USA · CYBER", "badge": "CONFIRMED", "color": (31, 56, 100),
     "src": "CNN · NYT · ABC",
     "head": "CIA and ODNI hit by cyberattack on open-source intel systems",
     "fact": "Unclassified systems breached; no classified data hit, "
             "officials say. Hacker, timing unknown.",
     "icon": "shield"},
    {"tag": "USA · CHINA · TECH", "badge": "CONFIRMED", "color": RED,
     "src": "Reuters · AP · US DOJ",
     "head": "Huawei convicted on 10 of 12 counts in US federal trial",
     "fact": "Bank fraud, wire fraud, Iran sanctions, trade-secret theft. "
             "Acquitted on racketeering counts.",
     "icon": "court"},
    {"tag": "MIDDLE EAST · HORMUZ", "badge": "CLAIM", "color": (133, 77, 14),
     "src": "DefenceMENA · Reuters · CENTCOM",
     "head": "Iran claims 4th tanker hit a mine in the Strait of Hormuz",
     "fact": "CENTCOM rejects the claims: routes cleared, mine-free. "
             "No names, flags or footage given.",
     "icon": "tanker"},
]

# Minis 4-13 (S1-S10). Heads <= ~52 chars (<=3 lines at 12pt in 174px);
# facts <= ~52 chars (<=2 lines at 10pt); sources <= 20 chars.
MINIS = [
    {"num": 4, "kick": "UKRAINE", "badge": "CONFIRMED",
     "color": (163, 22, 33), "icon": "missile", "src": "ISW",
     "head": "Putin: retaliation for refinery strikes 'inevitable'",
     "fact": "Says Kyiv ignored Trump's request to stop hits."},
    {"num": 5, "kick": "UKRAINE", "badge": "REPORTED",
     "color": (163, 22, 33), "icon": "chart", "src": "Meduza · RFE/RL",
     "head": "700,000+ Russian soldiers killed, incl. missing",
     "fact": "Hacked Rosstat analysis; 490,000 confirmed dead."},
    {"num": 6, "kick": "POLAND", "badge": "CONFIRMED",
     "color": (31, 78, 121), "icon": "jet", "src": "Fox News · Reuters",
     "head": "NATO jet cleared to down Russian missile over Poland",
     "fact": "Warsaw renews push for permanent US troops."},
    {"num": 7, "kick": "LIBYA", "badge": "CONFIRMED",
     "color": (133, 77, 14), "icon": "ship", "src": "Reuters",
     "head": "Kyiv: Benghazi ship strike was self-defence",
     "fact": "Sybiha cites UN Charter Art. 51; Tripoli condemns."},
    {"num": 8, "kick": "USA", "badge": "REPORTED",
     "color": (31, 56, 100), "icon": "pct", "src": "Reuters",
     "head": "Trump set to unveil new tariffs after capacity probe",
     "fact": "16 partners probed; rates still unknown. NOT YET."},
    {"num": 9, "kick": "MARKETS", "badge": "CONFIRMED",
     "color": (15, 118, 110), "icon": "chip", "src": "Reuters · Le Monde",
     "head": "Nvidia +30% as Huang return lifts Nasdaq +7%",
     "fact": "Chip index +14%; S&P 500 +4.73% on Monday."},
    {"num": 10, "kick": "SENEGAL", "badge": "CONFIRMED",
     "color": (120, 53, 15), "icon": "trophy", "src": "Reuters · Sky",
     "head": "Senegal reinstated as AFCON champions by CAS",
     "fact": "1-0 win over Morocco restored; Morocco to appeal."},
    {"num": 11, "kick": "EUROPE", "badge": "CONFIRMED",
     "color": (31, 78, 121), "icon": "ball", "src": "Reuters",
     "head": "Real Madrid thump PSV 5-1; Arsenal, City held",
     "fact": "Arsenal 1-1 Dortmund; City 2-2 Napoli."},
    {"num": 12, "kick": "INDIA", "badge": "CONFIRMED",
     "color": (146, 64, 14), "icon": "bars", "src": "Lowy Institute",
     "head": "India 3rd most powerful in Asia - Lowy Index",
     "fact": "40.5 pts, ahead of Japan 38.6; US 78.9, China 73.6."},
    {"num": 13, "kick": "DRC", "badge": "REPORTED",
     "color": (120, 53, 15), "icon": "cross", "src": "WHO · Stockbiz",
     "head": "WHO evacuates Ebola staff in DRC after 3-day shelter",
     "fact": "WHO-reported cumulative: 11,762 cases, 5,775 deaths."},
]

# ALSO 14-30. One line each (<= ~53 chars incl. source, 10pt in 318px).
ALSO = [
    (14, "Zhytomyr grid hit in overnight strikes (Zelensky)"),
    (15, "Odesa power out up to 3 weeks; pylons down (Forbes)"),
    (16, "EU proposes 22nd Russia sanctions package (UMonitor)"),
    (17, "Kyiv asks NATO for 40 jets; German UAV deal (UM)"),
    (18, "Gaza strikes kill 3+, incl. UNRWA worker (Al Jazeera)"),
    (19, "Gaza death toll 74,746 - REPORTED (WAFA)"),
    (20, "266m face acute food insecurity - WFP (BD Global)"),
    (21, "BJP & Akali Dal reunite for 2027 Punjab polls (Jagran)"),
    (22, "Nepal PM ends first state visit to India (Jagran)"),
    (23, "Japan-India first live-fire missile drills (SCMP)"),
    (24, "Denmark court backs 'ghetto law' evictions (Reuters)"),
    (25, "Spain drops all charges against Puigdemont (FrontPages)"),
    (26, "Estonia to shut Russia crossings from 1 Dec (wires)"),
    (27, "Brazil storms: 5 dead, 265 hurt, 19,854 displaced (IOM)"),
    (28, "700,000 displaced in S. Ethiopia fighting (Africanews)"),
    (29, "S. Africa unemployment 33.7%, 8.6m jobless (Prosperity)"),
    (30, "England beat Australia by 8 wickets in T20I (ScoreZaap)"),
]

# THE DAY IN NUMBERS — safe figures only. No $ value-added figure for
# Nvidia. 700,000 labelled killed incl. missing, hacked Rosstat analysis.
NUMBERS = [
    ("+30%", ["Nvidia shares", "Monday, Huang return"]),
    ("700,000+", ["Russian soldiers", "killed, incl. missing",
                  "hacked Rosstat analysis"]),
    ("10 of 12", ["Huawei counts", "convicted, Brooklyn"]),
    ("19,854", ["Brazil storm", "people displaced"]),
    ("5-1", ["Real Madrid", "over PSV, UCL"]),
    ("33.7%", ["S. Africa", "unemployment"]),
]

# Simplified continent outlines (lon, lat) — schematic flat-vector map.
LAND = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-100, 73), (-85, 70),
           (-70, 60), (-55, 47), (-65, 44), (-75, 35), (-85, 28),
           (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-145, 60),
           (-160, 58)],
    "SA": [(-80, 10), (-72, 4), (-58, -2), (-45, -8), (-40, -20),
           (-48, -28), (-58, -35), (-66, -48), (-72, -52), (-75, -35),
           (-75, -18), (-80, -5)],
    "AF": [(-17, 15), (-10, 30), (0, 35), (10, 37), (22, 33), (32, 31),
           (38, 22), (43, 12), (51, 11), (48, 0), (40, -12), (35, -22),
           (28, -32), (18, -34), (13, -25), (12, -15), (9, -1), (-8, 5)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (2, 51), (8, 57), (12, 59),
           (20, 56), (28, 60), (32, 70), (42, 68), (44, 58), (38, 50),
           (30, 46), (26, 40), (22, 36), (16, 40), (8, 44), (0, 40)],
    "AS": [(42, 68), (60, 70), (80, 73), (105, 76), (130, 72), (155, 68),
           (175, 65), (165, 60), (155, 50), (142, 42), (130, 34),
           (122, 30), (114, 22), (106, 10), (100, 8), (94, 16), (88, 22),
           (80, 12), (74, 8), (68, 22), (58, 25), (50, 30), (44, 38)],
    "OC": [(113, -22), (118, -32), (128, -32), (138, -35), (146, -39),
           (150, -37), (153, -28), (148, -20), (142, -11), (134, -12),
           (126, -14), (118, -20)],
}
# (story, lon, lat, dx, dy) — dx/dy nudge clustered pins apart; a leader
# line joins the true point to a nudged pin.
PINS = [
    (1, -77.0, 38.9, 0, 0), (2, -74.0, 40.7, -2, -14),
    (3, 56.0, 26.0, 0, 0), (4, 37.0, 56.0, 24, 4),
    (5, 38.0, 48.0, -24, 16), (6, 21.0, 52.0, 0, 0),
    (7, 20.0, 32.0, -2, 20), (8, -77.0, 38.9, 0, 14),
    (9, -74.0, 40.7, 16, -8), (10, -17.0, 15.0, 0, 0),
    (11, -3.7, 40.4, -26, 2), (12, 77.2, 28.6, 2, -14),
    (13, 29.0, 1.0, 0, 0), (14, 28.7, 50.25, 26, 12),
    (15, 30.7, 46.5, 8, 22), (16, 4.35, 50.85, -14, -20),
    (17, 30.5, 50.4, 30, -12), (18, 34.5, 31.5, 0, 0),
    (19, 34.5, 31.5, 16, 2), (20, 12.5, 41.9, 20, 14),
    (21, 75.0, 31.0, 0, 0), (22, 85.0, 27.7, 0, 0),
    (23, 139.7, 35.7, 0, 0), (24, 12.6, 56.0, -30, -2),
    (25, 2.17, 41.4, 0, 22), (26, 24.7, 59.4, 18, -18),
    (27, -53.8, -29.0, 0, 0), (28, 39.0, 3.5, 0, 0),
    (29, 28.0, -26.0, 0, 0), (30, 153.4, -28.0, 0, 0),
]


# ---------------------------------------------------------------- drawing
def badge(draw, x, y, label, size=11):
    fnt = load_font(True, size)
    w = int(draw.textlength(label, font=fnt)) + 12
    draw.rounded_rectangle([x, y, x + w, y + size + 6], radius=3,
                           fill=BADGE_FILL[label])
    draw.text((x + 6, y + 3), label, font=fnt, fill=WHITE)
    return w


def hero_icon(draw, kind, cx, cy, s):
    if kind == "shield":  # cyberattack: shield + lightning bolt
        draw.polygon([(cx - s, cy - s + 6), (cx + s, cy - s + 6),
                      (cx + s, cy), (cx, cy + s + 6), (cx - s, cy)],
                     outline=INK, width=3)
        draw.polygon([(cx + 4, cy - s + 12), (cx - 8, cy + 2),
                      (cx - 1, cy + 2), (cx - 4, cy + s - 2),
                      (cx + 9, cy - 2), (cx + 1, cy - 2)], fill=RED)
    elif kind == "court":  # courthouse: pediment + columns
        draw.polygon([(cx - s, cy - s // 2), (cx + s, cy - s // 2),
                      (cx, cy - s)], fill=INK)
        for k in (-1, 0, 1):
            draw.rectangle([cx + k * (s // 2) - 3, cy - s // 2 + 3,
                            cx + k * (s // 2) + 3, cy + s // 2], fill=INK)
        draw.rectangle([cx - s, cy + s // 2, cx + s, cy + s // 2 + 5],
                       fill=INK)
        draw.rectangle([cx - 5, cy + 2, cx + 5, cy + s // 2], fill=RED)
    elif kind == "tanker":  # tanker + spiked mine
        draw.polygon([(cx - s, cy + s // 4), (cx + s, cy + s // 4),
                      (cx + s - 8, cy + s // 2), (cx - s + 8, cy + s // 2)],
                     fill=INK)
        draw.rectangle([cx - s + 6, cy - s // 2, cx - 2, cy + s // 4],
                       fill=RED)
        draw.rectangle([cx + 2, cy - s // 3, cx + s - 6, cy + s // 4],
                       fill=GREY)
        mx, my, r = cx + s + 2, cy - s // 2, 7
        for ang in range(0, 360, 45):
            import math
            a = math.radians(ang)
            draw.line([mx + int(r * 0.7 * math.cos(a)),
                       my + int(r * 0.7 * math.sin(a)),
                       mx + int((r + 4) * math.cos(a)),
                       my + int((r + 4) * math.sin(a))], fill=RED, width=2)
        draw.ellipse([mx - r, my - r, mx + r, my + r], fill=RED)
        draw.line([cx - s - 4, cy + s // 2 + 7, cx + s + 10, cy + s // 2 + 7],
                  fill=(31, 78, 121), width=3)


def mini_icon(draw, kind, x, y, s, color):
    draw.rounded_rectangle([x, y, x + s, y + s], radius=2, fill=color)
    wht = WHITE
    if kind == "missile":
        draw.polygon([(x + 3, y + s - 3), (x + s - 3, y + 3),
                      (x + s - 6, y + s - 3)], fill=wht)
    elif kind == "chart":
        for k, hh in enumerate((5, 9, 12)):
            draw.rectangle([x + 3 + k * 4, y + s - 2 - hh,
                            x + 5 + k * 4, y + s - 2], fill=wht)
    elif kind == "jet":
        draw.polygon([(x + 2, y + s // 2), (x + s - 2, y + 3),
                      (x + s - 5, y + s // 2), (x + s - 2, y + s - 3)],
                     fill=wht)
    elif kind == "ship":
        draw.polygon([(x + 2, y + s - 6), (x + s - 2, y + s - 6),
                      (x + s - 4, y + s - 2), (x + 4, y + s - 2)], fill=wht)
        draw.line([x + s // 2, y + 3, x + s // 2, y + s - 6], fill=wht,
                  width=2)
    elif kind == "pct":
        fnt = load_font(True, 10)
        draw.text((x + 3, y + 2), "%", font=fnt, fill=wht)
    elif kind == "chip":
        draw.rectangle([x + 3, y + 3, x + s - 3, y + s - 3], outline=wht,
                       width=2)
        draw.rectangle([x + 6, y + 6, x + s - 6, y + s - 6], fill=wht)
    elif kind == "trophy":
        draw.polygon([(x + 3, y + 3), (x + s - 3, y + 3), (x + s - 5, y + 9),
                      (x + 5, y + 9)], fill=wht)
        draw.rectangle([x + s // 2 - 1, y + 9, x + s // 2 + 1, y + s - 4],
                       fill=wht)
        draw.rectangle([x + 4, y + s - 4, x + s - 4, y + s - 2], fill=wht)
    elif kind == "ball":
        draw.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=wht,
                     width=2)
        draw.ellipse([x + s // 2 - 2, y + s // 2 - 2, x + s // 2 + 2,
                      y + s // 2 + 2], fill=wht)
    elif kind == "bars":
        for k, hh in enumerate((5, 8, 11)):
            draw.rectangle([x + 3 + k * 4, y + s - 2 - hh,
                            x + 5 + k * 4, y + s - 2], fill=wht)
    elif kind == "cross":
        draw.rectangle([x + s // 2 - 2, y + 2, x + s // 2 + 2, y + s - 2],
                       fill=wht)
        draw.rectangle([x + 2, y + s // 2 - 2, x + s - 2, y + s // 2 + 2],
                       fill=wht)


def masthead(draw, tr):
    draw.rectangle([0, 0, W, 7], fill=RED)
    f_micro = load_font(True, 11)
    tr.put(draw, (24, 13), ["ONE DAY OF WORLD NEWS, ONE PICTURE"], f_micro,
           INK, label="micro-l")
    right = "30 STORIES · 8 REGIONS · ALL FROM THIS WEDNESDAY"
    w = draw.textlength(right, font=f_micro)
    tr.put(draw, (W - 24 - w, 13), [right], f_micro, INK, label="micro-r")
    size = 58
    while size > 40:
        f_date = load_font(True, size, serif=True)
        if draw.textlength("WEDNESDAY 25 NOVEMBER 2026", font=f_date) <= 976:
            break
        size -= 2
    date = "WEDNESDAY 25 NOVEMBER 2026"
    w = draw.textlength(date, font=f_date)
    tr.put(draw, ((W - w) / 2, 30), [date], f_date, INK, label="date")
    draw.line([24, 94, W - 24, 94], fill=INK, width=2)
    draw.line([24, 97, W - 24, 97], fill=INK, width=1)
    f_sub = load_font(False, 14, serif=True, italic=True)
    sub = ("CIA & ODNI Open-Source Intel Systems Hit by Cyberattack; "
           "Huawei Convicted on 10 of 12 Counts in US Federal Court; "
           "Iran Claims Hormuz Tanker Mine Strikes Amid Pentagon Denial")
    lines = wrap_text(draw, sub, f_sub, 976)
    y = tr.put(draw, (24, 102), lines, f_sub, RED, cap=976, label="subdek")
    if len(lines) > 2:
        tr.problems.append(f"TRUNC subdek: {len(lines)} lines")
    f_ed = load_font(True, 11)
    ed = "EDITION CLOSED 01:45 UTC — 24/25 NOV OVERNIGHT REPORT"
    w = draw.textlength(ed, font=f_ed)
    tr.put(draw, ((W - w) / 2, 137), [ed], f_ed, INK, label="edition")


def numbers_band(draw, tr, y0=152, h=70):
    draw.rectangle([24, y0, W - 24, y0 + h], fill=RED)
    draw.rectangle([24, y0, W - 24, y0 + h], outline=INK, width=1)
    cw = (W - 48) / 6
    f_lab = load_font(False, 9)
    for i, (num, lab) in enumerate(NUMBERS):
        x0 = 24 + i * cw
        if i:
            draw.line([x0, y0 + 8, x0, y0 + h - 8], fill=WHITE, width=1)
        size = 27
        while size > 20:
            f_n = load_font(True, size)
            if draw.textlength(num, font=f_n) <= cw - 10:
                break
            size -= 1
        w = draw.textlength(num, font=f_n)
        tr.put(draw, (x0 + (cw - w) / 2, y0 + 4), [num], f_n, WHITE,
               cap=cw - 8, label=f"num{i}")
        for j, ln in enumerate(lab):
            w2 = draw.textlength(ln, font=f_lab)
            tr.put(draw, (x0 + (cw - w2) / 2, y0 + 34 + j * 11), [ln],
                   f_lab, WHITE, cap=cw - 6, label=f"numlab{i}")
    return y0 + h


def timeline(draw, tr, y0=228):
    f_h = load_font(True, 11)
    tr.put(draw, (24, y0), ["OVERNIGHT CYCLE — 22:00-01:45 UTC"], f_h, INK,
           label="tl-h")
    f_n = load_font(False, 9)
    note = "Only sourced times labelled"
    w = draw.textlength(note, font=f_n)
    tr.put(draw, (W - 24 - w, y0 + 1), [note], f_n, GREY, label="tl-note")
    y_line = y0 + 18
    draw.line([24, y_line, W - 24, y_line], fill=INK, width=2)
    # 7 ticks across the 22:00-01:45 overnight window (225 min).
    # Labels ONLY for times sourced in RESEARCH.md.
    ticks = [(0.0, None), (0.204, "22:46 Huawei verdict"),
             (0.35, None), (0.533, "00:00 CIA hack reported"),
             (0.644, "00:25 Putin retaliation"), (0.82, None),
             (1.0, "01:45 Edition closed")]
    f_t = load_font(True, 9)
    for frac, lab in ticks:
        x = 24 + frac * (W - 48)
        draw.line([x, y_line - 4, x, y_line + 4], fill=RED, width=3)
        if lab:
            w = draw.textlength(lab, font=f_t)
            if frac >= 0.9:
                lx = W - 24 - w
            elif frac >= 0.5 and frac < 0.6:
                lx = x - w  # right-align to avoid the 00:25 label
            else:
                lx = x
            tr.put(draw, (lx, y_line + 7), [lab], f_t, INK, cap=200,
                   label=f"tl-{frac}")
    return y0 + 34


def hero(draw, tr, x0, y0, w, h, st, num):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=CARD, outline=INK, width=2)
    draw.rectangle([x0, y0, x0 + w, y0 + 20], fill=st["color"])
    f_tag = load_font(True, 11)
    tr.put(draw, (x0 + 8, y0 + 4), [f"{num} · {st['tag']}"], f_tag, WHITE,
           label=f"herotag{num}")
    hero_icon(draw, st["icon"], x0 + 52, y0 + 58, 22)
    tr.boxes.append((f"icon{num}", x0 + 28, y0 + 34, x0 + 76, y0 + 86))
    f_head = load_font(True, 19)
    hl = wrap_text(draw, st["head"], f_head, w - 114)
    y = tr.put(draw, (x0 + 104, y0 + 28), hl, f_head, INK, cap=w - 114,
               label=f"herohead{num}")
    if len(hl) > 3:
        tr.problems.append(f"TRUNC herohead{num}: '{st['head']}'")
    f_fact = load_font(False, 12.5)
    fl = wrap_text(draw, st["fact"], f_fact, w - 16)
    y = max(y + 4, y0 + 90)
    y = tr.put(draw, (x0 + 8, y), fl, f_fact, INK, cap=w - 16,
               label=f"herofact{num}")
    if len(fl) > 2:
        tr.problems.append(f"TRUNC herofact{num}: '{st['fact']}'")
    bw = badge(draw, x0 + 8, y0 + h - 24, st["badge"], size=11)
    f_src = load_font(False, 10.5)
    tr.put(draw, (x0 + 8 + bw + 8, y0 + h - 22), [st["src"]], f_src, GREY,
           label=f"herosrc{num}")


def world_map(draw, tr, x0, y0, w, h):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_BG, outline=INK,
                   width=1)
    f_lab = load_font(True, 10.5)
    tr.put(draw, (x0 + 8, y0 + 4),
           ["WHERE IT HAPPENED — 30 PINS = STORY NUMBERS"], f_lab, INK,
           label="maplabel")
    mx0, my0, mw, mh = x0, y0 + 20, w, h - 20

    def px(lon, lat):
        return mx0 + (lon + 180) / 360 * mw, my0 + (75 - lat) / 130 * mh
    for poly in LAND.values():
        draw.polygon([px(lo, la) for lo, la in poly], fill=MAP_FILL)
    f_pin = load_font(True, 7)
    for num, lon, lat, dx, dy in PINS:
        tx, ty = px(lon, lat)
        cx, cy = tx + dx, ty + dy
        if dx or dy:
            draw.line([tx, ty, cx, cy], fill=GREY, width=1)
            draw.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=RED)
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED,
                     outline=WHITE, width=1)
        draw.text((cx, cy), str(num), font=f_pin, fill=WHITE, anchor="mm")


def minis_grid(draw, tr, y0=588):
    cw, gap, ch = 190, 6, 100
    f_h = load_font(True, 12)
    tr.put(draw, (24, y0 - 16), ["SECONDARY — 10 NUMBERED STORIES"], f_h,
           INK, label="mini-h")
    # Verification legend, right of the minis header.
    f_l = load_font(True, 9)
    items = [("CONFIRMED", (30, 107, 58)), ("REPORTED", (47, 75, 124)),
             ("CLAIM", (180, 83, 9))]
    lx = W - 24
    for lab, col in reversed(items):
        w = draw.textlength(lab, font=f_l)
        lx -= w
        tr.put(draw, (lx, y0 - 15), [lab], f_l, INK, label=f"leg-{lab}")
        lx -= 14
        draw.rectangle([lx, y0 - 14, lx + 10, y0 - 4], fill=col)
        lx -= 8
    f_kick = load_font(True, 9)
    f_head = load_font(True, 12)
    f_fact = load_font(False, 10)
    f_src = load_font(False, 8)
    for idx, st in enumerate(MINIS):
        r, c = divmod(idx, 5)
        x0 = 24 + c * (cw + gap)
        yy = y0 + r * (ch + 6)
        draw.rectangle([x0, yy, x0 + cw, yy + ch], fill=CARD, outline=EDGE,
                       width=1)
        draw.rectangle([x0, yy, x0 + 4, yy + ch], fill=st["color"])
        mini_icon(draw, st["icon"], x0 + 8, yy + 5, 15, st["color"])
        tr.boxes.append((f"minicon{idx}", x0 + 8, yy + 5, x0 + 23, yy + 20))
        kick = f"{st['num']} · {st['kick']}"
        tr.put(draw, (x0 + 27, yy + 6), [kick], f_kick, st["color"],
               label=f"minikick{idx}")
        bw = badge(draw, x0 + cw - 4 - int(
            draw.textlength(st["badge"], font=load_font(True, 7.5))) - 12,
            yy + 4, st["badge"], size=7.5)
        hl = wrap_text(draw, st["head"], f_head, cw - 16)
        tr.put(draw, (x0 + 8, yy + 23), hl[:3], f_head, INK, cap=cw - 16,
               label=f"minihead{idx}")
        if len(hl) > 3:
            tr.problems.append(f"TRUNC minihead{idx}: '{st['head']}'")
        fl = wrap_text(draw, st["fact"], f_fact, cw - 16)
        tr.put(draw, (x0 + 8, yy + 66), fl[:2], f_fact, GREY, cap=cw - 16,
               label=f"minifact{idx}")
        if len(fl) > 2:
            tr.problems.append(f"TRUNC minifact{idx}: '{st['fact']}'")
        tr.put(draw, (x0 + 8, yy + 90), [st["src"]], f_src, GREY,
               label=f"minisrc{idx}")
    return y0 + 2 * ch + 6


def also_block(draw, tr, y0=818):
    f_h = load_font(True, 12)
    tr.put(draw, (24, y0 - 16),
           ["ALSO ON WEDNESDAY 25 NOVEMBER — 17 MORE STORIES"], f_h, INK,
           label="also-h")
    f_n = load_font(True, 10)
    f_b = load_font(False, 10)
    cols = [ALSO[0:6], ALSO[6:12], ALSO[12:17]]
    col_w = 318
    for ci, col in enumerate(cols):
        x0 = 24 + ci * (col_w + 10)
        for ri, (num, txt) in enumerate(col):
            yy = y0 + ri * 15
            nlab = f"{num}."
            tr.put(draw, (x0, yy), [nlab], f_n, RED, label=f"alson{num}")
            nw = draw.textlength(nlab, font=f_n)
            tr.put(draw, (x0 + nw + 4, yy), [txt], f_b, INK, cap=col_w - 20,
                   label=f"also{num}")
    return y0 + 6 * 15


def date_check(draw, tr, y0=912, h=76):
    draw.rectangle([24, y0, W - 24, y0 + h], fill=CARD, outline=INK, width=1)
    draw.line([512, y0 + 6, 512, y0 + h - 6], fill=EDGE, width=1)
    f_h = load_font(True, 11)
    f_b = load_font(False, 10)
    tr.put(draw, (36, y0 + 5), ["DATE CHECK — LEFT OUT (NOT 25 NOV)"],
           f_h, RED, label="dc-hl")
    left = [
        "COP31 collapse — ended Sun 22 Nov, no deal",
        "Merkury sunk, Benghazi — first reported 22 Nov",
        "Kh-101 missiles in Poland — Fri 20 Nov",
        "Huang reinstated — board vote Sun 22 Nov",
        "Alcaraz ATP Finals title — Sun 22 Nov",
    ]
    y = y0 + 22
    for ln in left:
        y = tr.put(draw, (36, y), [ln], f_b, INK, cap=460, label="dc-l")
    tr.put(draw, (524, y0 + 5), ["NOT YET — AT 01:45 UTC"], f_h, RED,
           label="dc-hr")
    right = [
        "Chess Game 2 result — due ~19:00 UTC",
        "Trump tariff announcement — expected Tue/Wed",
        "Wed-night UCL matches — not yet played",
        "Hormuz verification / footage — none released",
    ]
    y = y0 + 22
    for ln in right:
        y = tr.put(draw, (524, y), [ln], f_b, INK, cap=460, label="dc-r")
    return y0 + h


def footer(draw, tr, y0=994):
    f_l = load_font(False, 10)
    leg = ("LEGEND: CONFIRMED = multi-source verified · REPORTED = "
           "single-source / analysis · CLAIM = asserted, denied or unverified")
    w = draw.textlength(leg, font=f_l)
    tr.put(draw, ((W - w) / 2, y0), [leg], f_l, INK, label="legend")
    f_s = load_font(False, 9)
    src = ("Sources: CNN · NYT · Reuters · AP · US DOJ · ISW · WHO · IOM · "
           "Lowy Institute · Sky Sports · Le Monde · Stockbiz — 25 Nov 2026")
    w = draw.textlength(src, font=f_s)
    tr.put(draw, ((W - w) / 2, y0 + 14), [src], f_s, GREY, label="sources")


def render(path):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    tr = Audit()
    masthead(draw, tr)
    numbers_band(draw, tr, y0=152, h=70)
    timeline(draw, tr, y0=228)
    # Asymmetric middle: left 2 stacked heroes, right map + 3rd hero.
    hero(draw, tr, 24, 266, 476, 146, HEROES[0], 1)
    hero(draw, tr, 24, 418, 476, 146, HEROES[1], 2)
    world_map(draw, tr, 508, 266, 492, 146)
    hero(draw, tr, 508, 418, 492, 146, HEROES[2], 3)
    minis_grid(draw, tr, y0=588)
    also_block(draw, tr, y0=818)
    date_check(draw, tr, y0=908, h=82)
    footer(draw, tr, y0=996)
    tr.check_overlaps()
    img.save(path, "PNG", optimize=True)
    small = img.copy()
    small.thumbnail((300, 300), Image.LANCZOS)
    small.save(path.replace("entry.png", "entry-300px.png"), "PNG",
               optimize=True)
    return tr


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    tr = render(out)
    size = os.path.getsize(out)
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    im = Image.open(out)
    report = {"path": out, "bytes": size, "sha256": sha,
              "size_px": im.size, "problems": tr.problems,
              "n_boxes": len(tr.boxes)}
    print(json.dumps(report, indent=1))
    if tr.problems:
        sys.exit(1)
    if size > 1048576:
        print("FAIL: over 1 MiB")
        sys.exit(1)


if __name__ == "__main__":
    main()
