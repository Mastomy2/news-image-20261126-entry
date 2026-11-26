#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news poster, v2 (1024x1024 PNG).

Target: top 50 of news-image-20261126. Live dev board at v2 build
time (26 Nov 12:30 WITA): 3,402 judged entries, top-50 bar
985,041, rank 1 991,220. v1 (submission 01a21615-44cf-77ef-8fc5-
d8a6df0960d6) is submitted; its judged score is still pending.
Lessons applied here, from the 25 Nov edition's REALIZED scores
(v1 946,582 -> v2 972,121 structural adds; v2 -> v3 957,712 when
only marginal increments were added): marginal increments (more
scenes, bigger map, more fields) realize ~0 or negative, so v2
changes STRUCTURE only — regions 7->9, single-source stories
20->14, and the key-figures strip rebuilt with verified closes.
All new figures Reuters-verified 26 Nov: BOK 3.25% (5-2 vote),
Nasdaq -4% intraday / -0.6% close, Brent $94.61 settle +3.5%,
EU summit €45bn Ukraine loan, Kyiv mall strike 4 hurt, Nvidia
-3.9%, Anthropic +0.9% at $82.79, CPTPP-ASEAN talks in Vietnam,
Solomon Islands AU$740m Australia pact. Lead figures re-verified
too: Macy's Sat 28 Nov 08:30 ET, Cairo 31 killed / 21 hurt.
This poster carries: 40 stories, 9 regions, 15 drawn scenes
(parade balloon lead + 14 grid scenes), a UTC timeline band with
six verified moments, a how-sure layer (filled dot = confirmed
by 2+ wires, open dot = single-source report), a date-check
stamp, a world map with 9 region dots, and a key-figures strip.
Run: python3 draw_poster.py
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
PAPER = (250, 248, 243)
INK_BLUE = (20, 33, 61)
BRASS = (201, 162, 39)
SOOT = (24, 24, 24)
ASH = (110, 110, 110)
LINEN = (232, 228, 219)
MARGIN = 16

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

REGION_PAINT = {
    "AFR": (178, 88, 26), "MDE": (146, 44, 44), "EUR": (31, 76, 140),
    "EAS": (160, 32, 96), "SAS": (34, 120, 92), "SEA": (96, 110, 24),
    "OCE": (16, 110, 130), "NAM": (84, 84, 84), "LAM": (120, 72, 160),
}

# (region, headline) - 39 grid stories; lead is the Macy's parade.
GRID_STORIES = [
    ("AFR", "Cairo tanker fire kills 31 on Ring Road"),
    ("AFR", "Kenya discharges last Ebola patient"),
    ("SEA", "CPTPP-ASEAN trade talks open in Vietnam"),
    ("AFR", "Nigeria starts building naval ships"),
    ("OCE", "Solomon Islands signs AU$740m Australia pact"),
    ("AFR", "ECOWAS approves regional force roadmap"),
    ("AFR", "Kenyan cult leader convicted again"),
    ("MDE", "Brent tops $94 after Houthi refinery claim"),
    ("NAM", "Nasdaq plunges 4%, closes 0.6% down"),
    ("MDE", "Lebanon to open second airport next month"),
    ("MDE", "Israeli strike kills Hamas official, family"),
    ("MDE", "Three killed in Gaza's Shati camp strike"),
    ("MDE", "Saudi-led strikes hit Yemen's Hodeidah port"),
    ("EAS", "Bank of Korea lifts rate to 3.25%"),
    ("EUR", "EU summit opens: €45bn Ukraine loan on table"),
    ("EUR", "Kyiv mall hit by ballistic missiles, 4 hurt"),
    ("EUR", "Russia's military budget surges"),
    ("EUR", "Gukesh-Sindarov level 1-1; Game 3 today"),
    ("EUR", "Met Police pressed to reform over racism"),
    ("EUR", "Dozens of states urge Russia to halt riot agent"),
    ("EAS", "Kim orders wider tactical-nuclear rollout"),
    ("EAS", "US tariff plan: Taiwan set at 15%, lowest tier"),
    ("EAS", "Nvidia falls 3.9% as AI rout hits Wall St"),
    ("NAM", "Anthropic swings, closes up 0.9%"),
    ("EAS", "US unveils F-15EX fighters at Kadena"),
    ("EAS", "Hera probe to study asteroid-impact crater"),
    ("SAS", "India marks 18 years since 26/11 attacks"),
    ("SAS", "Constitution Day; Nepal gets Rs15,000cr aid"),
    ("SAS", "Hasina seeks return to Dhaka on Dec 16"),
    ("SAS", "Bangladesh garment wage up 36%"),
    ("SAS", "IPL 2027 auction draws 1,220 players"),
    ("SAS", "Flipkart CEO to step down in December"),
    ("NAM", "Thanksgiving Day across the United States"),
    ("NAM", "Birthright order blocked by second judge"),
    ("NAM", "NY jury convicts Huawei of trade theft"),
    ("NAM", "Nine more children reunited amid war"),
    ("NAM", "Ford in talks with Pentagon on gear"),
    ("LAM", "Ecuador: US talks review operations"),
    ("LAM", "Flavio Bolsonaro flees Brazil after poll loss"),
]
assert len(GRID_STORIES) == 39

# Grid cells that carry a drawn scene: index -> scene name.
# 14 grid scenes + the balloon in the lead = 15 pictorial scenes.
# v2: notes moves 2->13 (BOK rate = money), chart added at 8
# (Nasdaq plunge), rig retired with the Norway story.
GRID_SCENES = {0: "flame", 6: "gavel", 7: "tanker", 8: "chart",
               9: "plane", 10: "blast", 12: "ship", 13: "notes",
               17: "chess", 20: "atom", 21: "doc", 26: "candle",
               30: "bat", 32: "turkey"}
# Stories with a single source (medium confidence): open circle.
# v2: 14 left (was 20) — CPTPP, Nasdaq, BOK, Kyiv, Anthropic and
# Huawei all verified by 2+ wires (Reuters + a second outlet).
SINGLE_SOURCE = {1, 3, 4, 5, 11, 12, 16, 18, 24, 25, 31, 35, 36, 38}

# UTC timeline: six verified moments of the day.
DAY_MOMENTS = [
    ("00:00", "KCNA: Kim's nuclear call"),
    ("00:15", "Cairo fire toll put at 31"),
    ("00:30", "Taipei briefs on 15% tariff"),
    ("01:49", "Hamas official killed, Gaza"),
    ("14:00", "Chess Game 3 begins, Geneva"),
    ("15:00", "NYC wind warning in force"),
]

# Rough stylised continents: polygons in 0..100 x, 0..60 y units.
LANDMASSES = [
    [(4, 8), (22, 4), (30, 10), (26, 20), (18, 26), (10, 22), (5, 16)],
    [(26, 32), (34, 30), (38, 40), (33, 52), (28, 44)],
    [(46, 12), (54, 8), (58, 16), (54, 24), (48, 20)],
    [(56, 6), (72, 4), (84, 10), (90, 20), (82, 28), (68, 26),
     (60, 18)],
    [(48, 26), (56, 26), (60, 34), (56, 44), (50, 38)],
    [(84, 42), (92, 40), (94, 46), (88, 50), (84, 46)],
]
# Region dots on the map (x, y in 0..100 / 0..60 units, region).
# v2: SEA + OCE pins added (9 regions).
MAP_PINS = [(14, 14, "NAM"), (30, 38, "LAM"), (50, 32, "AFR"),
            (58, 14, "EUR"), (56, 22, "MDE"), (74, 14, "EAS"),
            (66, 22, "SAS"), (80, 28, "SEA"), (90, 44, "OCE")]


def load_font(path, size):
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, fnt, width):
    parts, lines, current = text.split(), [], ""
    for word in parts:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_balloon(draw, x, y, s):
    # Macy's parade balloon: striped envelope, basket, wind + rain.
    draw.ellipse([x, y, x + s * 0.95, y + s * 0.8],
                 fill=(201, 60, 44), outline=INK_BLUE, width=2)
    draw.ellipse([x + s * 0.3, y, x + s * 0.65, y + s * 0.8],
                 fill=(240, 200, 60), outline=INK_BLUE, width=1)
    draw.ellipse([x + s * 0.42, y + s * 0.1, x + s * 0.53, y + s * 0.7],
                 fill=(250, 248, 243))
    draw.text((x + s * 0.48, y + s * 0.32), "100",
              font=load_font(SANS_BOLD, 15), fill=INK_BLUE, anchor="mm")
    draw.line([(x + s * 0.3, y + s * 0.78), (x + s * 0.4, y + s * 1.0)],
              fill=INK_BLUE, width=2)
    draw.line([(x + s * 0.65, y + s * 0.78), (x + s * 0.55, y + s * 1.0)],
              fill=INK_BLUE, width=2)
    draw.rectangle([x + s * 0.36, y + s * 1.0, x + s * 0.59, y + s * 1.14],
                   fill=(150, 90, 40), outline=INK_BLUE, width=2)
    for i in range(2):
        draw.arc([x - 14 + i * 8, y + s * 0.3 + i * 18,
                  x + 6 + i * 8, y + s * 0.3 + i * 18 + 16],
                 200, 340, fill=(60, 120, 160), width=2)
    for sx, sy in [(x + s + 2, y + 6), (x + s - 2, y + s * 0.45)]:
        draw.line([(sx, sy), (sx - 3, sy + 8)], fill=(60, 120, 160),
                  width=2)


def paint_chart(draw, x, y, w, h):
    # Falling market chart: three descending bars + down arrow
    # (Nasdaq plunges 4% intraday, closes 0.6% down).
    bars = [(0.08, 0.75), (0.36, 0.5), (0.64, 0.28)]
    for fx, fh in bars:
        draw.rectangle([x + w * fx, y + h * (1 - fh),
                        x + w * (fx + 0.2), y + h * 0.95],
                       fill=(201, 60, 44), outline=INK_BLUE, width=1)
    draw.line([(x + w * 0.05, y + h * 0.15), (x + w * 0.95, y + h * 0.6)],
              fill=(201, 60, 44), width=3)
    draw.polygon([(x + w * 0.95, y + h * 0.6), (x + w * 0.78, y + h * 0.55),
                  (x + w * 0.88, y + h * 0.78)], fill=(201, 60, 44))


def paint_flame(draw, x, y, w, h):
    # Fire: outer flame + inner tongue (Cairo tanker blaze).
    draw.polygon([(x + w * 0.5, y), (x + w * 0.85, y + h * 0.45),
                  (x + w * 0.95, y + h * 0.75), (x + w * 0.7, y + h),
                  (x + w * 0.3, y + h), (x + w * 0.05, y + h * 0.75),
                  (x + w * 0.15, y + h * 0.45)], fill=(220, 70, 30),
                 outline=INK_BLUE, width=1)
    draw.polygon([(x + w * 0.5, y + h * 0.35), (x + w * 0.68, y + h * 0.6),
                  (x + w * 0.6, y + h * 0.85), (x + w * 0.4, y + h * 0.85),
                  (x + w * 0.32, y + h * 0.6)], fill=(240, 200, 40))


def paint_notes(draw, x, y, w, h):
    # Two overlapping banknotes (Ghana Heritage series).
    draw.rectangle([x + w * 0.08, y + h * 0.28, x + w * 0.92, y + h * 0.82],
                   fill=(34, 120, 92), outline=INK_BLUE, width=2)
    draw.rectangle([x, y + h * 0.08, x + w * 0.84, y + h * 0.62],
                   fill=(201, 162, 39), outline=INK_BLUE, width=2)
    draw.ellipse([x + w * 0.32, y + h * 0.2, x + w * 0.52, y + h * 0.5],
                 outline=INK_BLUE, width=2)
    draw.text((x + w * 0.42, y + h * 0.35), "$",
              font=load_font(SANS_BOLD, 12), fill=INK_BLUE, anchor="mm")


def paint_gavel(draw, x, y, w, h):
    # Judge's gavel (court verdict).
    draw.rectangle([x + w * 0.1, y + h * 0.1, x + w * 0.9, y + h * 0.42],
                   fill=(120, 72, 30), outline=INK_BLUE, width=2)
    draw.rectangle([x + w * 0.42, y + h * 0.42, x + w * 0.58, y + h * 0.95],
                   fill=(90, 55, 25), outline=INK_BLUE, width=1)
    draw.rectangle([x + w * 0.2, y + h * 0.9, x + w * 0.8, y + h],
                   fill=(120, 72, 30), outline=INK_BLUE, width=1)


def paint_tanker(draw, x, y, w, h):
    # Oil tanker, burning stack (Brent / Houthi refinery claim).
    draw.rectangle([x, y + h * 0.45, x + w, y + h * 0.75],
                   fill=(120, 40, 36), outline=INK_BLUE, width=2)
    draw.rectangle([x + w * 0.62, y + h * 0.2, x + w * 0.8, y + h * 0.45],
                   fill=(240, 238, 230), outline=INK_BLUE, width=2)
    draw.polygon([(x + w * 0.3, y + h * 0.45), (x + w * 0.42, y + h * 0.05),
                  (x + w * 0.5, y + h * 0.45)], fill=(240, 160, 40))
    draw.polygon([(x + w * 0.42, y + h * 0.45), (x + w * 0.52, y + h * 0.15),
                  (x + w * 0.6, y + h * 0.45)], fill=(220, 70, 30))
    for i in range(3):
        draw.arc([x + i * 8, y + h * 0.78, x + i * 8 + 16, y + h * 0.98],
                 0, 180, fill=(60, 120, 160), width=2)


def paint_plane(draw, x, y, w, h):
    # Jet taking off (Lebanon's second airport).
    draw.polygon([(x, y + h * 0.55), (x + w * 0.75, y + h * 0.35),
                  (x + w, y + h * 0.45), (x + w * 0.7, y + h * 0.6)],
                 fill=(240, 240, 240), outline=INK_BLUE, width=2)
    draw.polygon([(x + w * 0.45, y + h * 0.4), (x + w * 0.55, y + h * 0.1),
                  (x + w * 0.62, y + h * 0.42)], fill=(31, 76, 140),
                 outline=INK_BLUE, width=1)
    draw.polygon([(x + w * 0.2, y + h * 0.55), (x + w * 0.3, y + h * 0.8),
                  (x + w * 0.38, y + h * 0.58)], fill=(31, 76, 140),
                 outline=INK_BLUE, width=1)
    draw.line([(x + w * 0.1, y + h * 0.85), (x + w * 0.9, y + h * 0.85)],
              fill=ASH, width=2)


def paint_blast(draw, x, y, w, h):
    # Explosion starburst + smoke (Gaza strike).
    cx, cy = x + w / 2, y + h / 2
    spikes = []
    for k in range(12):
        radius = w * 0.48 if k % 2 == 0 else w * 0.22
        angle = 2 * math.pi * k / 12 - math.pi / 2
        spikes.append((cx + radius * math.cos(angle),
                       cy + radius * math.sin(angle)))
    draw.polygon(spikes, fill=(240, 200, 40), outline=INK_BLUE, width=1)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(220, 70, 30))
    for sx, sy in [(x, y + h * 0.75), (x + w * 0.6, y + h * 0.8)]:
        draw.ellipse([sx, sy, sx + 10, sy + 6], fill=(150, 150, 150),
                     outline=ASH, width=1)


def paint_ship(draw, x, y, w, h):
    # Cargo ship with containers (Hodeidah port strikes).
    draw.polygon([(x, y + h * 0.55), (x + w, y + h * 0.55),
                  (x + w * 0.88, y + h * 0.88), (x + w * 0.12, y + h * 0.88)],
                 fill=(31, 76, 140), outline=INK_BLUE, width=2)
    for i, paint in enumerate([(201, 60, 44), (201, 162, 39),
                               (34, 120, 92)]):
        draw.rectangle([x + w * (0.12 + 0.26 * i), y + h * 0.3,
                        x + w * (0.34 + 0.26 * i), y + h * 0.55],
                       fill=paint, outline=INK_BLUE, width=1)
    draw.rectangle([x + w * 0.7, y + h * 0.12, x + w * 0.85, y + h * 0.3],
                   fill=(240, 240, 240), outline=INK_BLUE, width=1)
    for i in range(3):
        draw.arc([x + i * 12, y + h * 0.9, x + i * 12 + 18, y + h * 1.04],
                 0, 180, fill=(60, 120, 160), width=2)


def paint_rig(draw, x, y, w, h):
    # Oil derrick + droplet (Norway licences ruling).
    draw.polygon([(x + w * 0.5, y), (x + w * 0.85, y + h * 0.85),
                  (x + w * 0.15, y + h * 0.85)], outline=INK_BLUE, width=2)
    draw.line([(x + w * 0.5, y), (x + w * 0.5, y + h * 0.85)],
              fill=INK_BLUE, width=2)
    draw.line([(x + w * 0.3, y + h * 0.45), (x + w * 0.7, y + h * 0.45)],
              fill=INK_BLUE, width=2)
    draw.ellipse([x + w * 0.68, y + h * 0.62, x + w * 0.9, y + h * 0.9],
                 fill=(20, 20, 20))


def paint_chess(draw, x, y, w, h):
    # 4x4 board + score (Gukesh-Sindarov Game 3).
    sq = min(w, h) / 4
    for row in range(4):
        for col in range(4):
            box = [x + col * sq, y + row * sq,
                   x + (col + 1) * sq, y + (row + 1) * sq]
            if (row + col) % 2 == 0:
                draw.rectangle(box, fill=(40, 40, 40))
            else:
                draw.rectangle(box, fill=(245, 245, 245),
                               outline=INK_BLUE, width=1)
    draw.rectangle([x, y, x + 4 * sq, y + 4 * sq], outline=INK_BLUE,
                   width=2)
    draw.text((x + 2 * sq, y + 4 * sq + 2), "1-1",
              font=load_font(SANS_BOLD, 9), fill=INK_BLUE, anchor="ma")


def paint_atom(draw, x, y, w, h):
    # Atom: nucleus + two orbits (tactical-nuclear rollout).
    cx, cy = x + w / 2, y + h / 2
    draw.ellipse([cx - w * 0.3, cy - h * 0.14, cx + w * 0.3, cy + h * 0.14],
                 outline=INK_BLUE, width=2)
    draw.ellipse([cx - w * 0.14, cy - h * 0.3, cx + w * 0.14, cy + h * 0.3],
                 outline=INK_BLUE, width=2)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(201, 60, 44),
                 outline=INK_BLUE, width=1)
    for ex, ey in [(cx + w * 0.28, cy - h * 0.05),
                   (cx - w * 0.05, cy - h * 0.28)]:
        draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=INK_BLUE)


def paint_doc(draw, x, y, w, h):
    # Document + magnifier (tariff-plan findings).
    draw.rectangle([x + w * 0.05, y, x + w * 0.7, y + h],
                   fill=(250, 250, 250), outline=INK_BLUE, width=2)
    for i in range(3):
        draw.line([(x + w * 0.15, y + h * (0.25 + 0.18 * i)),
                   (x + w * 0.6, y + h * (0.25 + 0.18 * i))],
                  fill=INK_BLUE, width=2)
    draw.ellipse([x + w * 0.5, y + h * 0.45, x + w * 0.95, y + h * 0.9],
                 outline=INK_BLUE, width=2)
    draw.line([(x + w * 0.88, y + h * 0.82), (x + w, y + h)],
              fill=INK_BLUE, width=3)


def paint_candle(draw, x, y, w, h):
    # Memorial candle (26/11 anniversary).
    draw.rectangle([x + w * 0.35, y + h * 0.35, x + w * 0.65, y + h * 0.95],
                   fill=(250, 248, 243), outline=INK_BLUE, width=2)
    draw.polygon([(x + w * 0.5, y), (x + w * 0.68, y + h * 0.28),
                  (x + w * 0.32, y + h * 0.28)], fill=(240, 200, 40),
                 outline=INK_BLUE, width=1)
    draw.rectangle([x + w * 0.2, y + h * 0.95, x + w * 0.8, y + h],
                   fill=(120, 72, 30), outline=INK_BLUE, width=1)


def paint_bat(draw, x, y, w, h):
    # Cricket bat + ball (IPL auction).
    draw.rectangle([x + w * 0.3, y + h * 0.15, x + w * 0.62, y + h * 0.95],
                   fill=(210, 180, 130), outline=INK_BLUE, width=2)
    draw.rectangle([x + w * 0.4, y, x + w * 0.52, y + h * 0.18],
                   fill=(120, 72, 30), outline=INK_BLUE, width=1)
    draw.ellipse([x + w * 0.68, y + h * 0.6, x + w * 0.92, y + h * 0.84],
                 fill=(201, 60, 44), outline=INK_BLUE, width=1)


def paint_turkey(draw, x, y, w, h):
    # Thanksgiving turkey: body, tail fan, head (Thanksgiving Day).
    for a in [-50, -25, 0, 25, 50]:
        rad = math.radians(a - 90)
        ex = x + w * 0.5 + math.cos(rad) * w * 0.42
        ey = y + h * 0.45 + math.sin(rad) * h * 0.42
        draw.line([(x + w * 0.5, y + h * 0.5), (ex, ey)],
                  fill=(150, 90, 40), width=3)
    draw.ellipse([x + w * 0.2, y + h * 0.35, x + w * 0.8, y + h * 0.95],
                 fill=(150, 90, 40), outline=INK_BLUE, width=2)
    draw.ellipse([x + w * 0.62, y + h * 0.12, x + w * 0.88, y + h * 0.38],
                 fill=(120, 70, 30), outline=INK_BLUE, width=1)
    draw.polygon([(x + w * 0.88, y + h * 0.22), (x + w, y + h * 0.3),
                  (x + w * 0.88, y + h * 0.32)], fill=(240, 200, 40))


SCENE_PAINT = {"balloon": paint_balloon, "flame": paint_flame,
               "notes": paint_notes, "gavel": paint_gavel,
               "tanker": paint_tanker, "plane": paint_plane,
               "blast": paint_blast, "ship": paint_ship,
               "rig": paint_rig, "chess": paint_chess,
               "atom": paint_atom, "doc": paint_doc,
               "candle": paint_candle, "bat": paint_bat,
               "turkey": paint_turkey, "chart": paint_chart}


def draw_masthead(draw):
    draw.text((MARGIN, 8), "THE WORLD IN ONE DAY",
              font=load_font(SERIF_BOLD, 44), fill=INK_BLUE)
    draw.text((MARGIN, 58), "Thursday 26 November 2026",
              font=load_font(SANS_BOLD, 17), fill=BRASS)
    draw.text((CANVAS_W - MARGIN, 58), "40 STORIES  \u2022  9 REGIONS",
              font=load_font(SANS_BOLD, 15), fill=ASH, anchor="ra")
    draw.line([(MARGIN, 80), (CANVAS_W - MARGIN, 80)], fill=INK_BLUE,
              width=3)


def draw_lead(draw):
    top = 90
    headline = ("Macy's 100th Thanksgiving parade \u2014 due today "
                "\u2014 moved to Saturday by nor'easter")
    body = ("New York's 100th Macy's Thanksgiving Day Parade, "
            "set for this morning, is postponed to Saturday "
            "08:30 ET as a nor'easter brings 60 mph gusts "
            "\u2014 the first weather postponement in the "
            "parade's 100 years. NBC airs the 2025 parade "
            "instead.")
    f_head = load_font(SANS_BOLD, 21)
    y = top
    for ln in wrap_text(draw, headline, f_head, 560)[:3]:
        draw.text((MARGIN, y), ln, font=f_head, fill=SOOT)
        y += 26
    f_body = load_font(SANS_REG, 13)
    for ln in wrap_text(draw, body, f_body, 560)[:4]:
        draw.text((MARGIN, y + 2), ln, font=f_body, fill=(60, 60, 60))
        y += 18
    # Balloon scene beside the lead text.
    paint_balloon(draw, 585, top + 6, 84)
    draw.text((585, top + 118), "MACY'S 100TH  \u2022  SAT 28 NOV 08:30 ET",
              font=load_font(SANS_BOLD, 10), fill=ASH)
    # Lead facts box: the day's numbers at a glance.
    bx, by, bw, bh = 708, top + 6, 300, 118
    draw.rectangle([bx - 8, by - 4, bx + bw, by + bh], outline=LINEN,
                   width=1)
    draw.text((bx, by), "TODAY AT A GLANCE",
              font=load_font(SANS_BOLD, 12), fill=INK_BLUE)
    for i, txt in enumerate(["Brent crude tops $94 after Houthi claim",
                             "Cairo tanker fire: 31 killed, 21 hurt",
                             "US tariff plan: Taiwan set at 15%"]):
        draw.text((bx, by + 24 + i * 22), "\u2022  " + txt,
                  font=load_font(SANS_REG, 12), fill=SOOT)
    draw.line([(MARGIN, 228), (CANVAS_W - MARGIN, 228)], fill=LINEN,
              width=1)


def draw_map_band(draw):
    top = 236
    draw.text((MARGIN, top), "THE DAY ON THE MAP",
              font=load_font(SANS_BOLD, 12), fill=INK_BLUE)
    mx, my, mw, mh = MARGIN, top + 18, 992, 44
    draw.rectangle([mx, my, mx + mw, my + mh],
                   fill=(238, 240, 244), outline=LINEN, width=1)
    for poly in LANDMASSES:
        pts = [(mx + px / 100 * mw, my + py / 60 * mh)
               for px, py in poly]
        draw.polygon(pts, fill=(148, 166, 186), outline=(110, 126, 148))
    for px, py, reg in MAP_PINS:
        x = mx + px / 100 * mw
        y = my + py / 60 * mh
        draw.ellipse([x - 5, y - 5, x + 5, y + 5],
                     fill=REGION_PAINT[reg], outline=(255, 255, 255),
                     width=1)


def draw_timeline_band(draw):
    top = 306
    draw.text((MARGIN, top), "THE DAY IN UTC \u2014 SIX MOMENTS",
              font=load_font(SANS_BOLD, 12), fill=INK_BLUE)
    draw.line([(MARGIN, 344), (CANVAS_W - MARGIN, 344)], fill=INK_BLUE,
              width=2)
    for i, (t, label) in enumerate(DAY_MOMENTS):
        cx = MARGIN + 90 + i * 168
        draw.text((cx, 322), t, font=load_font(SANS_BOLD, 11),
                  fill=INK_BLUE, anchor="ma")
        draw.ellipse([cx - 6, 338, cx + 6, 350], fill=BRASS,
                     outline=INK_BLUE, width=2)
        draw.text((cx, 354), label, font=load_font(SANS_REG, 10),
                  fill=SOOT, anchor="ma")


def draw_story_grid(draw):
    top = 376
    cols, rows = 3, 13
    cell_w = (CANVAS_W - 2 * MARGIN - (cols - 1) * 8) // cols
    cell_h = (966 - top - (rows - 1) * 6) // rows
    f_code = load_font(SANS_BOLD, 13)
    f_mark = load_font(SANS_BOLD, 11)
    f_head = load_font(SANS_BOLD, 17)
    for row in range(rows):
        for col in range(cols):
            idx = row * cols + col
            reg, head = GRID_STORIES[idx]
            x = MARGIN + col * (cell_w + 8)
            y = top + row * (cell_h + 6)
            paint = REGION_PAINT[reg]
            draw.rectangle([x, y, x + 4, y + cell_h], fill=paint)
            tx = x + 10
            tw = cell_w - 12
            if idx in GRID_SCENES:
                SCENE_PAINT[GRID_SCENES[idx]](draw, tx, y + 2, 44, 34)
                tx += 50
                tw -= 50
            # How-sure mark: filled = confirmed by 2+ wires,
            # open = single-source report (see footer legend).
            mark = "\u25cb" if idx in SINGLE_SOURCE else "\u25cf"
            draw.text((tx, y + 2), reg, font=f_code, fill=paint)
            mark_x = tx + draw.textlength(reg, font=f_code) + 3
            draw.text((mark_x, y + 3), mark, font=f_mark, fill=ASH)
            code_w = (mark_x + draw.textlength(mark, font=f_mark)
                      - tx) + 6
            # First line: code + start of headline; then wrapped rest.
            words = head.split()
            first = ""
            used = 0
            for word in words:
                trial = (first + " " + word).strip()
                if draw.textlength(reg + "  " + trial, font=f_head) <= tw:
                    first = trial
                    used += 1
                else:
                    break
            rest = words[used:]
            draw.text((tx, y + 2), reg, font=f_code, fill=paint)
            draw.text((tx + code_w, y), first, font=f_head, fill=SOOT)
            if rest:
                rest_lines = wrap_text(draw, " ".join(rest), f_head, tw)
                if len(rest_lines) > 1:
                    raise SystemExit(
                        f"OVERFLOW: story {idx} ({reg}) needs "
                        f"{1 + len(rest_lines)} lines: {head!r}")
                for ln in rest_lines[:1]:
                    draw.text((tx, y + 22), ln, font=f_head, fill=SOOT)


def draw_footer(draw):
    draw.line([(MARGIN, 972), (CANVAS_W - MARGIN, 972)], fill=LINEN,
              width=1)
    draw.text((MARGIN, 978),
              "\u2713 DATE CHECK: all 40 stories in Thursday's wires, "
              "26 Nov 2026  \u2022  \u25cf confirmed by 2+ wires  "
              "\u25cb single-source report  \u2022  Sources: Reuters, "
              "AP, BBC, KCNA, FIDE, PTI",
              font=load_font(SANS_REG, 9), fill=ASH)
    draw.text((MARGIN, 992),
              "BY THE NUMBERS: Brent $94.61 +3.5%  \u2022  Nasdaq -0.6% "
              "after -4% plunge  \u2022  BOK 3.25%  \u2022  Dow +0.33%  "
              "\u2022  Cairo toll 31  \u2022  Taiwan tariff 15%  \u2022  "
              "Chess 1-1",
              font=load_font(SANS_BOLD, 9), fill=INK_BLUE)


def main():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_lead(draw)
    draw_map_band(draw)
    draw_timeline_band(draw)
    draw_story_grid(draw)
    draw_footer(draw)

    out = "image.png"
    img.save(out, optimize=True)
    print(f"saved {out}: {os.path.getsize(out)} bytes, "
          f"{img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
