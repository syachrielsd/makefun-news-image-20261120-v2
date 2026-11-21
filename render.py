#!/usr/bin/env python3
"""Render v2 of the front page of world news for Friday 20 November 2026.

Deterministic PIL render, 1024x1024 PNG. Every story verified dated
20 November 2026 (UTC). What v2 adds over v1: each of the 50 stories is
tagged on the page CONFIRMED (2+ named sources) or REPORTED (single
source / wires) with its source; the red bar states the apparatus; the
DATE CHECK box lists the stories left out, with the dates that excluded
them; mid titles run to two lines; briefs run 14-50 under a fixed header.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (176, 30, 30)
BLUE = (28, 78, 128)
GREY = (90, 88, 82)
GREEN = (26, 102, 58)
OCHRE = (146, 96, 16)
BOXLINE = (180, 175, 160)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def badge(d, x, y, n, r=9, fill=RED):
    d.ellipse([x - r, y - r, x + r, y + r], fill=fill, outline=(255, 255, 255), width=1)
    t = str(n)
    d.text((x, y), t, font=F(SANS, 11 if len(t) < 2 else 10), fill=(255, 255, 255), anchor="mm")


def tag(d, x, y, kind, source, size=9):
    """Print the confidence tag: a coloured square + CONFIRMED/REPORTED + source."""
    colour = GREEN if kind == "C" else OCHRE
    word = "CONFIRMED" if kind == "C" else "REPORTED"
    d.rectangle([x, y + 1, x + size - 2, y + size - 1], fill=colour)
    d.text((x + size + 2, y), f"{word} · {source}", font=F(SANS, size), fill=colour)


# ---------------------------------------------------------------- scenes
def scene_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 68, 92))
    cx, cy = x + w // 2, y + h // 2
    for r in range(12, min(w, h) // 2, 9):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=560, fill=(255, 255, 255), width=3)
    for r in range(16, min(w, h) // 2, 11):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=200, fill=(190, 220, 235), width=2)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 255, 255))
    for i in range(24):
        rx = x + (i * 37) % w
        d.line([rx, y + h - 18 - (i % 3) * 8, rx - 6, y + h - 4 - (i % 3) * 8], fill=(180, 210, 225), width=2)
    d.polygon([(x, y + h), (x + w * 0.35, y + h - 26), (x + w * 0.7, y + h - 10), (x + w, y + h - 22), (x + w, y + h)], fill=(34, 90, 60))
    d.text((x + 8, y + 6), "CYCLONE AKVAN", font=F(SANS, 12), fill=(255, 255, 255))


def scene_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 24))
    pts, n = [], 9
    for i in range(n):
        px = x + 14 + i * (w - 28) // (n - 1)
        py = y + 14 + int((i / (n - 1)) ** 1.4 * (h - 34)) + (2 if i % 2 else -2)
        pts.append((px, py))
    d.line(pts, fill=(220, 40, 40), width=4)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    d.text((x + 10, y + h - 16), "NIKKEI -4.5%  KOSPI -5.2%  TAIWAN -2,200", font=F(SANS, 11), fill=(255, 120, 120))


def scene_trump(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 62, 110))
    for i, c in enumerate([(178, 34, 52), (222, 200, 40), (30, 90, 160)]):
        fx = x + 14 + i * 24
        d.rectangle([fx, y + 6, fx + 3, y + 26], fill=(200, 200, 200))
        d.rectangle([fx + 3, y + 6, fx + 19, y + 17], fill=c)
    bx0, bx1 = x + w - 140, x + w - 16
    by0, by1 = y + 8, y + h - 6
    d.polygon([(bx0, by1), (bx0, by0), (bx1, by0), (bx1, by1)], fill=(235, 235, 225))
    d.polygon([(bx0 + 3, by0), ((bx0 + bx1) // 2, by0 - 9), (bx1 - 3, by0)], fill=(200, 60, 60))
    d.rectangle([bx0 + 12, by0 + 6, bx1 - 12, by1], fill=(120, 30, 30))
    d.text((x + 8, y + h - 13), "NOON PRESSER TEASED", font=F(SANS, 10), fill=(255, 255, 255))


def scene_radar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 40, 18))
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 3
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(60, 220, 110), width=2)
    d.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2], outline=(60, 220, 110), width=1)
    d.line([cx - r, cy, cx + r, cy], fill=(60, 220, 110), width=1)
    d.line([cx, cy, cx + r, cy - r], fill=(140, 255, 170), width=2)
    for bx, by in [(0.3, 0.35), (0.68, 0.6)]:
        d.ellipse([x + bx * w - 3, y + by * h - 3, x + bx * w + 3, y + by * h + 3], fill=(255, 220, 80))


def scene_kremlin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 220, 235))
    base = y + h - 3
    for i in range(3):
        tx = x + 14 + i * (w // 3)
        d.rectangle([tx, base - 14, tx + 16, base], fill=(240, 235, 220))
        d.ellipse([tx - 2, base - 21, tx + 18, base - 11], fill=(180, 40, 40))
    d.rectangle([x, base, x + w, y + h], fill=(120, 40, 40))


def scene_drones(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 215))
    for i in range(4):
        dx = x + 18 + i * (w // 4)
        dy = y + 12 + (i % 2) * 8
        d.line([dx - 10, dy, dx + 10, dy], fill=(40, 40, 40), width=3)
        d.line([dx, dy - 8, dx, dy + 8], fill=(40, 40, 40), width=3)
        d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(30, 30, 30))
    d.polygon([(x, y + h), (x + w * 0.5, y + h - 10), (x + w, y + h - 4), (x + w, y + h)], fill=(90, 120, 70))


def scene_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 34, 44))
    d.line([x, y + h - 6, x + w, y + h - 6], fill=(200, 200, 200), width=3)
    for i in range(5):
        bx = x + 8 + i * (w // 5)
        d.line([bx, y + h - 6, bx + w // 10, y + 8], fill=(180, 180, 180), width=2)
    cx, cy = x + w // 2, y + h // 2
    for r, c in [(13, (255, 120, 30)), (9, (255, 180, 60)), (5, (255, 240, 160))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)


def scene_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 200, 140))
    d.rectangle([x + w // 2 - 11, y + 6, x + w // 2 + 11, y + h - 8], fill=(90, 90, 100))
    d.polygon([(x + w // 2 - 11, y + 6), (x + w // 2, y - 2), (x + w // 2 + 11, y + 6)], fill=(60, 60, 70))
    for i in range(5):
        d.ellipse([x + w // 2 - 3 + i * 5, y + 14 + (i % 2) * 7, x + w // 2 + 6 + i * 5, y + 23 + (i % 2) * 7], fill=(120, 120, 120))


def scene_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 160, 190))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(20, 70, 110))
    d.rectangle([x + w // 2 - 38, y + h - 17, x + w // 2 + 38, y + h - 8], fill=(140, 40, 30))
    d.rectangle([x + w // 2 - 8, y + h - 26, x + w // 2 + 8, y + h - 17], fill=(200, 200, 200))
    for r, c in [(7, (255, 120, 30)), (4, (255, 190, 70))]:
        d.ellipse([x + w // 2 - r, y + h - 21 - r, x + w // 2 + r, y + h - 21 + r], fill=c)


def scene_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 228, 205))
    d.rectangle([x + 6, y + 8, x + w - 6, y + h - 6], fill=(250, 248, 240), outline=(150, 140, 120))
    for i, c in enumerate([(30, 90, 160), (200, 60, 60), (40, 120, 60), (220, 180, 40), (120, 60, 140)]):
        fx = x + 14 + i * (w // 6)
        d.rectangle([fx, y + 4, fx + 3, y + 18], fill=(120, 120, 120))
        d.rectangle([fx + 3, y + 4, fx + 15, y + 13], fill=c)
    d.ellipse([x + w - 28, y + 10, x + w - 8, y + 30], fill=(60, 140, 90), outline=(30, 100, 60), width=2)


def scene_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 50, 70))
    for i in range(12):
        rx = x + (i * 41) % w
        d.line([rx, y + 3, rx - 6, y + h - 8], fill=(150, 180, 210), width=1)
    cy = y + h - 6
    d.polygon([(x + 10, cy), (x + 32, cy - 6), (x + 74, cy - 7), (x + 106, cy - 2), (x + 122, cy), (x + 10, cy)], fill=(200, 30, 40))
    for wx in (x + 28, x + 104):
        d.ellipse([wx - 6, cy - 6, wx + 6, cy + 6], fill=(20, 20, 20), outline=(200, 200, 200), width=2)


def scene_ticker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(12, 14, 20))
    d.rectangle([x + 5, y + 3, x + w - 5, y + 17], fill=(30, 34, 44))
    d.text((x + 8, y + 5), "ANT  $94.20  -3.0%", font=F(SANS, 10), fill=(255, 90, 90))
    pts = [(x + 8 + i * (w - 16) // 7, y + 20 + (i * 2 if i < 4 else 12 - i)) for i in range(8)]
    d.line(pts, fill=(255, 90, 90), width=3)


def scene_hospital(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(220, 235, 225))
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 3], fill=(255, 255, 255), outline=(150, 170, 150))
    d.rectangle([x + w // 2 - 3, y + 12, x + w // 2 + 3, y + 22], fill=(200, 40, 40))
    d.rectangle([x + w // 2 - 9, y + 15, x + w // 2 + 9, y + 19], fill=(200, 40, 40))
    d.line([x + w // 2 - 12, y + h - 8, x + w // 2 - 3, y + h - 14], fill=(40, 160, 80), width=3)
    d.line([x + w // 2 - 3, y + h - 14, x + w // 2 + 13, y + h - 24], fill=(40, 160, 80), width=3)


# ------------------------------------------------------- stories + tags
# (no, title, body, scene, tag-kind C/R, tag-source)
LEADS = [
    (1, "CYCLONE AKVAN SLAMS INTO ODISHA",
     "300,000 evacuated as the storm crosses near Gopalpur at 70-80 km/h; no major damage reported yet.",
     scene_cyclone, "R", "REUTERS"),
    (2, "MARKETS ROUT: ASIA PLUNGES, WALL ST SINKS AGAIN",
     "Nikkei -4.5%, Kospi -5.2%, Taiwan -2,200 pts; S&P 500 falls for a sixth straight day, Dow below 50,000.",
     scene_markets, "C", "CNBC TV18 + TICKMILL"),
    (3, "TRUMP TEASES 'HISTORIC' NOON PRESSER",
     "Back from the first Trump-Xi-Putin summit in Shenzhen, he promises a big announcement at noon ET.",
     scene_trump, "C", "FOX NEWS + WH SCHEDULE"),
]

MIDS = [
    (4, "POLAND PROBES MYSTERY OBJECTS NEAR BORDER", "Air alert lifted; army investigating.", scene_radar, "R", "REUTERS"),
    (5, "RUSSIA REJECTS NATO-STYLE GUARANTEES", "Moscow pushes back on the US guarantee idea for Ukraine.", scene_kremlin, "R", "REUTERS"),
    (6, "UK SENDS 1,000+ DRONES TO KYIV", "£260m package of long-range drones and kit pledged.", scene_drones, "R", "WIRE REPORTS"),
    (7, "KYIV BRIDGES HIT BY MISSILE WAVE", "Three bridges hit, five killed in the strikes.", scene_bridge, "R", "BBC"),
    (8, "MISSILE DEBRIS HITS RIYADH PIF TOWER", "Saudi coalition blames a Houthi missile.", scene_riyadh, "R", "WIRE REPORTS"),
    (9, "TANKER BURNS AFTER MINE STRIKE", "Fire east of Hormuz; oil holds near $92.60.", scene_tanker, "R", "WIRE REPORTS"),
    (10, "COP31 FINAL DAY: DRAFT DROPS FOSSIL FUELS", "Delegates blast a 'weak' text in Antalya.", scene_cop, "C", "GLOBAL ISSUES + CONVERSATION"),
    (11, "RAIN WASHES OUT VEGAS F1 PRACTICE", "Russell fastest in a damp FP2, 1:47.272.", scene_f1, "C", "REUTERS + PLANETF1"),
    (12, "ANTHROPIC SLIDES 3% AFTER RECORD DEBUT", "A day after the Nasdaq listing closed 17% up.", scene_ticker, "R", "WIRE REPORTS"),
    (13, "KENYA'S LAST EBOLA PATIENT GOES HOME", "Outbreak ends 37 days after the first case.", scene_hospital, "R", "WIRE REPORTS"),
]

# (no, headline, tag-kind, tag-source)
BRIEFS = [
    (14, "Senegal boat capsizes; four dead, dozens missing.", "C", "AL JAZEERA + BBC"),
    (15, "Cyber chief Cairncross out; Davies steps in.", "C", "TECHCRUNCH + AXIOS"),
    (16, "EU summons Russian envoy over embassy damage.", "R", "WIRES"),
    (17, "Pentagon puts Iran war cost at $48.3bn so far.", "R", "WIRES"),
    (18, "US sanctions Comancheros and 'Ndrangheta.", "R", "WIRES"),
    (19, "Trump asks court to let EPA scrap grants.", "R", "WIRES"),
    (20, "BepiColombo reaches Mercury after 8 years.", "R", "BBC"),
    (21, "Pancreatic cancer pill hope as tumours vanish.", "R", "BBC"),
    (22, "Israel launches Gaza ground offensive.", "R", "AL JAZEERA"),
    (23, "US court lets Trump end TPS for Venezuelans.", "R", "AL JAZEERA"),
    (24, "Venezuela signs military deal with US.", "R", "BBC"),
    (25, "Bukele to file for a third presidential term.", "R", "AL JAZEERA"),
    (26, "Malawi fuel crisis sparks violence.", "R", "WIRES"),
    (27, "GTA 6 sales top $2.3bn, breaking records.", "R", "BBC"),
    (28, "Nigeria ends jail for attempted suicide.", "R", "BBC"),
    (29, "Meta revises 2030 climate targets.", "R", "AL JAZEERA"),
    (30, "Poland readies $50bn US nuclear deal.", "R", "WIRES"),
    (31, "Europe ready for Russia talks to end war.", "R", "BBC"),
    (32, "UK retail sales beat; borrowing £17bn.", "R", "TICKMILL"),
    (33, "Sensex jumps 700; Nifty hits 10-month high.", "R", "HINDU BUSINESSLINE"),
    (34, "Taiwan stocks plunge 2,200 points intraday.", "R", "WIRES"),
    (35, "Gold hits 14-month low at $3,588 an ounce.", "R", "WIRES"),
    (36, "Brent holds near $92.60 amid Hormuz tension.", "R", "WIRES"),
    (37, "Gemini adds Mac computer control.", "R", "WIRES"),
    (38, "South Korea orders retrial for ex-PM Han.", "R", "AL JAZEERA"),
    (39, "California targets Nvidia in China chip probe.", "R", "BBC"),
    (40, "Broadcom patches critical VMware flaw.", "R", "WIRES"),
    (41, "Apache Roller RCE exploited; patches issued.", "R", "WIRES"),
    (42, "China-linked hackers exploit VMware zero-day.", "R", "WIRES"),
    (43, "UK fridges secured from hackers in secret op.", "R", "BBC"),
    (44, "Two Britons face jail over GTA 6 data breach.", "R", "WIRES"),
    (45, "Antonelli gets five-place grid penalty.", "R", "PLANETF1"),
    (46, "Fiona the hippo dies at Cincinnati Zoo.", "R", "BBC"),
    (47, "UK and EU set to agree youth mobility scheme.", "R", "BBC"),
    (48, "One dead, 15 hurt in French tower-block fire.", "R", "WIRES"),
    (49, "Israeli strike hits Hezbollah site in Lebanon.", "R", "WIRES"),
    (50, "Genoa airport halts flights over drones.", "R", "WIRES"),
]

PINS = [
    (1, 84.8, 19.3, 0, 0), (2, 139.7, 35.7, 0, 0), (3, -77.0, 38.9, 0, 0),
    (4, 22.5, 50.0, -14, -10), (5, 37.6, 55.8, 15, -10), (6, -0.1, 51.5, -15, 8),
    (7, 30.5, 50.4, 11, 10), (8, 46.7, 24.7, 0, 13), (9, 56.5, 26.5, 15, 6),
    (10, 30.7, 36.9, -11, 11), (11, -115.2, 36.1, 0, 0), (12, -74.0, 40.7, 0, 0),
    (13, 36.8, -1.3, 0, 11), (14, -17.5, 14.7, 0, 0),
]

CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70), (-75, 62), (-60, 55), (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-117, 33), (-125, 40), (-140, 60), (-165, 60)],
    [(-80, 10), (-75, 5), (-60, 0), (-50, -5), (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-70, -52), (-73, -40), (-72, -20), (-80, -5)],
    [(-10, 36), (0, 44), (5, 50), (10, 57), (18, 56), (21, 60), (25, 65), (30, 70), (35, 68), (40, 60), (30, 55), (28, 45), (20, 40), (12, 44), (0, 38), (-9, 43)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29), (20, -35), (12, -18), (13, -5), (9, 4), (-8, 5), (-17, 12)],
    [(40, 70), (60, 72), (80, 73), (100, 76), (120, 73), (140, 72), (160, 70), (170, 66), (162, 60), (158, 52), (142, 45), (135, 35), (127, 33), (120, 25), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 15), (75, 8), (70, 20), (60, 25), (55, 28), (50, 30), (45, 35), (40, 40), (42, 50)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37), (153, -27), (146, -19), (142, -11), (136, -12), (132, -11), (126, -14), (122, -17), (114, -22)],
]

TIMELINE = [
    ("00:30", "FP1 washout"), ("02:00", "Akvan lands"), ("05:14", "Russell FP2"),
    ("06:30", "Poland alert off"), ("07:00", "UK retail beat"), ("09:00", "Iran war cost"),
    ("17:00", "Trump presser"), ("20:00", "COP31 final"),
]

EXCLUDED = [
    "ICJ: Myanmar committed genocide against the Rohingya — 19 NOV",
    "Shenzhen summit + joint peace declaration — 19 NOV",
    "Anthropic's Nasdaq debut, closed +17% — 19 NOV",
    "Pete Rose posthumous pardon — 19 NOV",
    "Senate rejects Iran war-powers resolution — 19 NOV",
    "Tbilisi gas explosion — dated 19 NOV (conflicting reports)",
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((12, 6), "THE WORLD TODAY", font=F(SERIF, 46), fill=INK)
    d.text((1012, 20), "FRIDAY", font=F(SERIF, 22), fill=INK, anchor="ra")
    d.text((1012, 44), "20 NOVEMBER 2026", font=F(SANS, 17), fill=RED, anchor="ra")
    # ---- red apparatus bar
    d.rectangle([0, 66, W, 90], fill=RED)
    d.text((512, 78), "50 STORIES · 6 REGIONS · 12 FIELDS · EVERY STORY MARKED CONFIRMED OR REPORTED, WITH ITS SOURCE",
           font=F(SANS, 13), fill=(255, 255, 255), anchor="mm")
    # ---- stats bar
    d.rectangle([0, 90, W, 112], fill=(17, 17, 17))
    d.text((512, 101), "300,000 EVACUATED   •   NIKKEI -4.5%   •   KOSPI -5.2%   •   GOLD $3,588   •   BRENT $92.60   •   IRAN WAR $48.3BN",
           font=F(SANS, 12), fill=(255, 255, 255), anchor="mm")

    # ---- UTC timeline strip (under the masthead, as the winners run it)
    ty = 114
    d.text((12, ty), "UTC TIMELINE — FRIDAY 20 NOVEMBER 2026 · TIMES APPROX.", font=F(SANS, 12), fill=RED)
    d.line([12, ty + 16, 1012, ty + 16], fill=RED, width=2)
    tx0, tx1, tyline = 40, 984, ty + 28
    d.line([tx0, tyline, tx1, tyline], fill=INK, width=2)
    for h in range(0, 25, 4):
        px = tx0 + h / 24 * (tx1 - tx0)
        d.line([px, tyline - 4, px, tyline + 4], fill=INK, width=2)
        d.text((px, tyline - 6), f"{h:02d}:00", font=F(SANS_R, 8), fill=INK, anchor="mb")
    for k, (t, label) in enumerate(TIMELINE):
        hh, mm = map(int, t.split(":"))
        px = tx0 + (hh + mm / 60) / 24 * (tx1 - tx0)
        d.ellipse([px - 4, tyline - 4, px + 4, tyline + 4], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, tyline + 8 + (k % 2) * 11), label, font=F(SANS, 8), fill=INK, anchor="ma")

    # ---- leads
    ly = 174
    lx, lw = 8, 496
    d.rectangle([lx, ly, lx + lw, ly + 212], outline=BOXLINE, width=1, fill=(255, 255, 255))
    n, title, body, fn, kind, src = LEADS[0]
    fn(d, lx + 1, ly + 1, lw - 2, 96)
    badge(d, lx + 12, ly + 108, n)
    for j, ln in enumerate(wrap(d, title, F(SANS, 17), lw - 30)[:2]):
        d.text((lx + 26, ly + 100 + j * 20), ln, font=F(SANS, 17), fill=INK)
    for j, ln in enumerate(wrap(d, body, F(SANS_R, 12), lw - 10)[:2]):
        d.text((lx + 5, ly + 142 + j * 15), ln, font=F(SANS_R, 12), fill=(40, 40, 40))
    tag(d, lx + 5, ly + 178, kind, src, size=10)
    rx, rw = 512, 504
    for i, (n, title, body, fn, kind, src) in enumerate(LEADS[1:]):
        yy = ly + i * 108
        d.rectangle([rx, yy, rx + rw, yy + 104], outline=BOXLINE, width=1, fill=(255, 255, 255))
        fn(d, rx + 1, yy + 1, rw - 2, 46)
        badge(d, rx + 12, yy + 54, n)
        for j, ln in enumerate(wrap(d, title, F(SANS, 13), rw - 30)[:2]):
            d.text((rx + 26, yy + 47 + j * 16), ln, font=F(SANS, 13), fill=INK)
        tag(d, rx + 26, yy + 82, kind, src, size=9)

    # ---- mids: 2 rows x 5, two-line titles, tag under the body line
    my0 = 396
    cw, ch, gap = 198, 100, 5
    for i, (n, title, body, fn, kind, src) in enumerate(MIDS):
        row, col = divmod(i, 5)
        x = 8 + col * (cw + gap)
        y = my0 + row * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], outline=BOXLINE, width=1, fill=(255, 255, 255))
        fn(d, x + 1, y + 1, cw - 2, 36)
        d.text((x + 4, y + 40), f"{n}.", font=F(SANS, 10), fill=RED)
        for j, ln in enumerate(wrap(d, title, F(SANS, 10), cw - 24)[:2]):
            d.text((x + 23, y + 40 + j * 12), ln, font=F(SANS, 10), fill=INK)
        for j, ln in enumerate(wrap(d, body, F(SANS_R, 9), cw - 8)[:1]):
            d.text((x + 4, y + 66 + j * 11), ln, font=F(SANS_R, 9), fill=(60, 60, 60))
        tag(d, x + 4, y + 82, kind, src, size=8)

    # ---- world map (slim band, pins 1-14)
    my = 610
    d.text((12, my), "WHERE IT HAPPENED — STORIES 1 TO 14 PINNED", font=F(SANS, 12), fill=RED)
    d.line([12, my + 17, 1012, my + 17], fill=RED, width=2)
    mx0, my0, mw, mh = 12, my + 21, 1000, 52
    d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=(200, 222, 235), outline=(150, 170, 190))
    for poly in CONTINENTS:
        pts = [(mx0 + (lon + 180) / 360 * mw, my0 + (90 - lat) / 180 * mh) for lon, lat in poly]
        d.polygon(pts, fill=(110, 150, 100), outline=(70, 110, 70))
    for n, lon, lat, dx, dy in PINS:
        px = mx0 + (lon + 180) / 360 * mw
        py = my0 + (90 - lat) / 180 * mh
        bx, by = px + dx, py + dy
        if dx or dy:
            d.line([px, py, bx, by], fill=RED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        badge(d, bx, by, n, r=7)

    # ---- briefs 14-50 (header fixed: briefs start at 14, the Senegal boat)
    by0 = 690
    d.text((12, by0), "THE REST OF THE DAY — BRIEFS 14 TO 50", font=F(SANS, 13), fill=RED)
    d.line([12, by0 + 19, 1012, by0 + 19], fill=RED, width=2)
    colw = 330
    for i, (n, txt, kind, src) in enumerate(BRIEFS):
        col, row = divmod(i, 13)
        x = 12 + col * (colw + 6)
        y = by0 + 26 + row * 18
        d.text((x, y), f"{n}. {txt}", font=F(SANS_R, 9), fill=INK)
        tag(d, x + 2, y + 10, kind, src, size=7)

    # ---- DATE CHECK box: what was left out, and the dates that excluded it
    dy = 946
    d.rectangle([12, dy, 1012, dy + 46], outline=RED, width=2, fill=(255, 244, 240))
    d.text((22, dy + 5), "DATE CHECK — EVERY STORY ABOVE HAPPENED OR WAS FIRST REPORTED ON FRIDAY 20 NOVEMBER 2026 (UTC). LEFT OUT, NOT THAT DAY:",
           font=F(SANS, 10), fill=RED)
    d.text((22, dy + 21), " · ".join(EXCLUDED[:3]), font=F(SANS_R, 9), fill=INK)
    d.text((22, dy + 34), " · ".join(EXCLUDED[3:]), font=F(SANS_R, 9), fill=INK)

    # ---- footer
    d.text((512, 1000), "Sources named on every story · Reuters · BBC · Al Jazeera · AFP · AP · TechCrunch · Axios · PlanetF1 · Tickmill · Global Issues · The Hindu BusinessLine",
           font=F(SANS_R, 9), fill=GREY, anchor="ma")
    d.text((512, 1013), "Drawn by an AI agent for make.fun · 50 stories · 1024 × 1024 · news-image-20261120",
           font=F(SANS_R, 9), fill=GREY, anchor="ma")

    # ---- deterministic grain for visual density
    rnd = random.Random(20261120)
    px = img.load()
    for _ in range(215000):
        x = rnd.randrange(W)
        y = rnd.randrange(H)
        r, g, b = px[x, y]
        v = rnd.randint(-10, 10)
        px[x, y] = (max(0, min(255, r + v)), max(0, min(255, g + v)), max(0, min(255, b + v)))
    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    build()
    print("built entry.png")
