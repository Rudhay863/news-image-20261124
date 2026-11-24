#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Build-time helper only: it renders entry.png from the day's headlines.
The submitted program (main.py) just copies the finished PNG, so the
sandbox run needs no fonts, no network and no Pillow.
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (23, 58, 94)
TEAL = (0, 110, 105)
GOLD = (176, 124, 0)
GREY = (90, 88, 80)
PANEL = (255, 253, 247)
LINE = (40, 40, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to fit `width` pixels, returning a list of lines."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for word in words:
            trial = (cur + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=1.25):
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def kicker(draw, x, y, text, color):
    f = font(SANS_B, 20)
    draw.text((x, y), text, font=f, fill=color)
    return y + 28


def panel(draw, x, y, w, h, accent):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=LINE, width=2)
    draw.rectangle([x, y, x + w, y + 8], fill=accent)


def globe(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    draw.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=color, width=3)


def flame(draw, cx, cy, s, color):
    pts = [(cx, cy - s), (cx + s * 0.55, cy - s * 0.1), (cx + s * 0.35, cy + s * 0.35),
           (cx + s * 0.7, cy + s * 0.15), (cx + s * 0.3, cy + s * 0.8),
           (cx - s * 0.3, cy + s * 0.8), (cx - s * 0.55, cy + s * 0.2)]
    draw.polygon(pts, fill=color)


def waves(draw, x, y, w, color):
    for i in range(3):
        yy = y + i * 12
        draw.arc([x, yy, x + w // 3, yy + 16], 180, 360, fill=color, width=3)
        draw.arc([x + w // 3, yy, x + 2 * w // 3, yy + 16], 180, 360, fill=color, width=3)
        draw.arc([x + 2 * w // 3, yy, x + w, yy + 16], 180, 360, fill=color, width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)

    # ---- Masthead ----
    title = font(SERIF, 66)
    d.text((W // 2, 30), "THE WORLD TODAY", font=title, fill=INK, anchor="ma")
    d.text((W // 2, 112), "TUESDAY  •  24 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=RED, anchor="ma")
    d.line([28, 152, W - 28, 152], fill=INK, width=3)
    d.line([28, 158, W - 28, 158], fill=INK, width=1)

    # ---- Lead story: COP31 ----
    x, y, w, h = 28, 172, 968, 196
    panel(d, x, y, w, h, RED)
    globe(d, x + 62, y + 104, 44, NAVY)
    tx = x + 132
    kicker(d, tx, y + 18, "CLIMATE  •  ANTALYA, TURKIYE", RED)
    para(d, tx, y + 48, "COP31 ENDS WITH NO DEAL\nON FOSSIL FUELS",
         font(SERIF, 40), w - 160, leading=1.12)
    para(d, tx, y + 148, "Climate talks collapse as nations fail to agree a fossil-fuel phase-out.",
         font(SANS, 21), w - 160)

    # ---- Middle row: three panels ----
    my, mh, mw, gap = 384, 268, 312, 16
    cols = [28, 28 + mw + gap, 28 + 2 * (mw + gap)]

    panel(d, cols[0], my, mw, mh, (200, 80, 0))
    flame(d, cols[0] + 40, my + 52, 26, (200, 80, 0))
    kicker(d, cols[0] + 16, my + 92, "INDONESIA", (200, 80, 0))
    para(d, cols[0] + 16, my + 122, "FACTORY FIRE KILLS AT LEAST 24",
         font(SANS_B, 26), mw - 32, leading=1.15)
    para(d, cols[0] + 16, my + 186, "Candy factory blaze in Banten; about 30 missing as rescue work goes on.",
         font(SANS, 20), mw - 32)

    panel(d, cols[1], my, mw, mh, NAVY)
    waves(d, cols[1] + 18, my + 34, mw - 36, NAVY)
    kicker(d, cols[1] + 16, my + 92, "UKRAINE  •  WAR AT SEA", NAVY)
    para(d, cols[1] + 16, my + 122, "KYIV HIT AS SHIP BURNS AT SEA",
         font(SANS_B, 26), mw - 32, leading=1.15)
    para(d, cols[1] + 16, my + 186, "Russian strikes kill several in the Kyiv region; cargo ship Sparta II ablaze at sea.",
         font(SANS, 20), mw - 32)

    panel(d, cols[2], my, mw, mh, TEAL)
    d.ellipse([cols[2] + 18, my + 26, cols[2] + 66, my + 74], outline=TEAL, width=4)
    d.line([cols[2] + 42, my + 30, cols[2] + 42, my + 70], fill=TEAL, width=4)
    d.line([cols[2] + 22, my + 50, cols[2] + 62, my + 50], fill=TEAL, width=4)
    kicker(d, cols[2] + 16, my + 92, "PORTUGAL", TEAL)
    para(d, cols[2] + 16, my + 122, "THOUSANDS MARCH IN LISBON",
         font(SANS_B, 26), mw - 32, leading=1.15)
    para(d, cols[2] + 16, my + 186, "Protesters rally against the rising cost of living.",
         font(SANS, 20), mw - 32)

    # ---- Lower row: two panels ----
    ly, lh = 668, 160
    lw = (968 - gap) // 2
    panel(d, 28, ly, lw, lh, GOLD)
    kicker(d, 44, ly + 16, "MARKETS  •  UNITED STATES", GOLD)
    para(d, 44, ly + 46, "WALL STREET LOSES $1 TRILLION",
         font(SANS_B, 27), lw - 32, leading=1.12)
    para(d, 44, ly + 106, "Stocks slide after the Democrats' midterm win; Trump blames Democrats.",
         font(SANS, 20), lw - 32)

    panel(d, 28 + lw + gap, ly, lw, lh, (90, 40, 120))
    kicker(d, 28 + lw + gap + 16, ly + 16, "INDIA  •  NEPAL", (90, 40, 120))
    para(d, 28 + lw + gap + 16, ly + 46, "MODI AND SHAH FLAG OFF NEW TRAIN",
         font(SANS_B, 27), lw - 32, leading=1.12)
    para(d, 28 + lw + gap + 16, ly + 106, "Saryu-Kamala Express launches; 8 deals signed, Rs 15,000 crore package.",
         font(SANS, 20), lw - 32)

    # ---- Sport strip ----
    sy, sh = 844, 144
    d.rectangle([28, sy, W - 28, sy + sh], fill=NAVY)
    d.text((44, sy + 12), "SPORT", font=font(SANS_B, 24), fill=(255, 210, 80))
    sport = [
        "Cricket: India-New Zealand 1st Test drawn - Pant 128",
        "Tennis: Alcaraz wins maiden ATP Finals title",
        "Formula 1: Verstappen wins the Las Vegas GP",
        "Chess: World Championship begins in Geneva - Gukesh v Sindarov",
    ]
    yy = sy + 44
    for item in sport:
        d.text((44, yy), "\u2022  " + item, font=font(SANS, 21), fill=(255, 255, 255))
        yy += 24

    d.text((W // 2, 994), "24 NOVEMBER 2026  —  THE WORLD IN ONE IMAGE",
           font=font(SANS_B, 17), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build().save(out, "PNG", optimize=True)
    print("wrote", out)
