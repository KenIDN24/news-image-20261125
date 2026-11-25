#!/usr/bin/env python3
"""Draw the 25 November 2026 news front page (1024x1024)."""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

img = Image.new("RGB", (W, H), (247, 243, 236))
d = ImageDraw.Draw(img)

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def center_text(draw, y, text, fnt, fill, cx=W // 2):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")

# ---------- masthead ----------
d.rectangle([0, 0, W, 118], fill=(16, 32, 64))
center_text(d, 14, "THE WORLD IN ONE DAY", font(FS, 30), (212, 175, 55))
center_text(d, 48, "WEDNESDAY 25 NOVEMBER 2026", font(FB, 44), (255, 255, 255))
d.rectangle([0, 118, W, 124], fill=(178, 34, 34))
center_text(d, 130, "FOUR STORIES THAT DEFINED THE DAY", font(FB, 22), (90, 90, 90))

# ---------- panels ----------
PX, PY, PW, PH, GAP = 12, 164, 494, 416, 12

def panel(x, y, bg, tag, tagfill, head, body, art):
    d.rectangle([x, y, x + PW, y + PH], fill=bg, outline=(60, 60, 60), width=2)
    d.rectangle([x, y, x + PW, y + 58], fill=tagfill)
    d.text((x + 16, y + 14), tag, font=font(FB, 26), fill=(255, 255, 255))
    art(x, y)
    # headline below art band (art occupies y+58 .. y+210)
    hy = y + 218
    for ln in wrap(d, head, font(FB, 33), PW - 28):
        d.text((x + 14, hy), ln, font=font(FB, 33), fill=(20, 20, 20))
        hy += 40
    by = hy + 6
    for ln in wrap(d, body, font(FR, 24), PW - 28):
        d.text((x + 14, by), ln, font=font(FR, 24), fill=(70, 70, 70))
        by += 31

# --- art 1: sea strike ---
def art1(x, y):
    ay = y + 58
    d.rectangle([x, ay, x + PW, ay + 152], fill=(24, 68, 120))
    # sea
    d.rectangle([x, ay + 96, x + PW, ay + 152], fill=(10, 40, 80))
    # ship silhouette left
    d.polygon([(x + 40, ay + 96), (x + 200, ay + 96), (x + 180, ay + 78), (x + 60, ay + 78)], fill=(8, 24, 48))
    d.rectangle([x + 105, ay + 58, x + 115, ay + 78], fill=(8, 24, 48))
    # stricken ship right, listing
    d.polygon([(x + 300, ay + 96), (x + 450, ay + 96), (x + 430, ay + 84), (x + 320, ay + 84)], fill=(8, 24, 48))
    # explosion burst
    cx, cy = x + 380, ay + 55
    for r, col in [(46, (255, 140, 0)), (34, (255, 200, 40)), (20, (255, 240, 120))]:
        pts = []
        for i in range(12):
            a = math.pi * i / 6
            rr = r if i % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        d.polygon(pts, fill=col)
    # drone
    d.ellipse([x + 250, ay + 30, x + 262, ay + 42], fill=(230, 230, 230))
    d.line([x + 240, ay + 36, x + 272, ay + 36], fill=(230, 230, 230), width=3)
    d.line([x + 256, ay + 42, x + 330, ay + 50], fill=(200, 200, 200), width=2)

# --- art 2: Riyadh tower ---
def art2(x, y):
    ay = y + 58
    d.rectangle([x, ay, x + PW, ay + 152], fill=(58, 32, 64))
    # skyline
    for bx, bw, bh in [(0, 70, 60), (80, 55, 85), (145, 60, 45), (380, 65, 70), (455, 39, 50)]:
        d.rectangle([x + bx, ay + 152 - bh, x + bx + bw, ay + 152], fill=(30, 18, 36))
    # PIF tower (tall, centre)
    d.rectangle([x + 215, ay + 8, x + 275, ay + 152], fill=(90, 60, 95))
    d.polygon([(x + 215, ay + 8), (x + 275, ay + 8), (x + 245, ay - 6)], fill=(120, 85, 125))
    # windows
    for wy in range(ay + 20, ay + 145, 16):
        d.rectangle([x + 228, wy, x + 262, wy + 8], fill=(255, 210, 90))
    # smoke + flame at top
    d.ellipse([x + 285, ay + 2, x + 345, ay + 42], fill=(120, 120, 120))
    d.ellipse([x + 300, ay + 18, x + 340, ay + 48], fill=(90, 90, 90))
    for r, col in [(18, (255, 120, 0)), (11, (255, 200, 40))]:
        pts = []
        for i in range(10):
            a = math.pi * i / 5
            rr = r if i % 2 == 0 else r * 0.5
            pts.append((x + 292 + rr * math.cos(a), ay + 12 + rr * math.sin(a)))
        d.polygon(pts, fill=col)

# --- art 3: medal ---
def art3(x, y):
    ay = y + 58
    d.rectangle([x, ay, x + PW, ay + 152], fill=(24, 42, 60))
    # ribbon
    d.polygon([(x + 200, ay), (x + 294, ay), (x + 272, ay + 62), (x + 222, ay + 62)], fill=(178, 34, 34))
    d.polygon([(x + 222, ay + 62), (x + 272, ay + 62), (x + 247, ay + 84)], fill=(140, 24, 24))
    # medal disc
    cx, cy = x + 247, ay + 108
    d.ellipse([cx - 46, cy - 46, cx + 46, cy + 46], fill=(212, 175, 55))
    d.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], outline=(150, 115, 20), width=3)
    # star
    pts = []
    for i in range(10):
        a = -math.pi / 2 + math.pi * i / 5
        rr = 30 if i % 2 == 0 else 12
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=(255, 240, 180))

# --- art 4: courthouse / gavel ---
def art4(x, y):
    ay = y + 58
    d.rectangle([x, ay, x + PW, ay + 152], fill=(70, 62, 52))
    # courthouse pediment
    d.polygon([(x + 90, ay + 30), (x + 404, ay + 30), (x + 247, ay + 2)], fill=(210, 200, 180))
    # columns
    for cx in (130, 200, 270, 340):
        d.rectangle([x + cx, ay + 34, x + cx + 22, ay + 140], fill=(225, 218, 205))
    d.rectangle([x + 90, ay + 140, x + 404, ay + 152], fill=(190, 180, 160))
    # gavel over base
    d.rectangle([x + 218, ay + 96, x + 276, ay + 112], fill=(90, 55, 25))
    d.rectangle([x + 240, ay + 112, x + 254, ay + 140], fill=(120, 80, 40))
    d.rectangle([x + 210, ay + 140, x + 284, ay + 148], fill=(90, 55, 25))

panel(PX, PY, (255, 255, 255), "UKRAINE  •  WAR AT SEA", (16, 32, 64),
      "UKRAINE SINKS RUSSIAN WARSHIP",
      "Zelenskyy confirms strikes on Russian vessels off Libya and in the Gulf of Finland.",
      art1)
panel(PX + PW + GAP, PY, (255, 255, 255), "SAUDI ARABIA  •  RIYADH", (58, 32, 64),
      "HOUTHI DRONE HITS RIYADH TOWER",
      "Tallest tower in the capital struck for a second time in a week; 11 people wounded.",
      art2)
panel(PX, PY + PH + GAP, (255, 255, 255), "UNITED STATES  •  HONOUR", (24, 42, 60),
      "TRUMP AWARDS GIULIANI MEDAL OF FREEDOM",
      "Former New York mayor receives the nation's highest civilian honour.",
      art3)
panel(PX + PW + GAP, PY + PH + GAP, (255, 255, 255), "UNITED STATES  •  COURT", (70, 62, 52),
      "HUAWEI CONVICTED IN U.S. TRIAL",
      "Guilty over Iran business and trade-secret theft; cleared of racketeering.",
      art4)

# footer
d.rectangle([0, 1000, W, 1024], fill=(16, 32, 64))
center_text(d, 1003, "make.fun  •  WEDNESDAY 25 NOVEMBER 2026", font(FB, 18), (255, 255, 255))

img.save("/home/hatch/workspace/news-image-20261125/entry.png", optimize=True)
print("saved", img.size)
import os
print("bytes:", os.path.getsize("/home/hatch/workspace/news-image-20261125/entry.png"))
