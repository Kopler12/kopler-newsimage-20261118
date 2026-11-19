#!/usr/bin/env python3
"""Draw 'THE WORLD IN A DAY' — a newspaper front page for Wednesday
18 November 2026 — entirely with PIL shapes and type. Deterministic."""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (25, 25, 25)
RED = (179, 0, 27)
BLUE = (23, 63, 95)
GOLD = (185, 138, 28)
GREY = (110, 105, 95)
WHITE = (255, 255, 255)
SKY = (164, 192, 216)
SAND = (201, 178, 120)

FD = "/usr/share/fonts/truetype/dejavu"
SERIF = FD + "/DejaVuSerif-Bold.ttf"
SANSB = FD + "/DejaVuSans-Bold.ttf"
SANS = FD + "/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def letterspace(draw, cx, y, text, fnt, fill, tracking):
    """Draw text centred at cx with extra tracking between glyphs."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, maxw, leading):
    for line in wrap(draw, text, fnt, maxw):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_font(draw, text, path, size, maxw, minimum=18):
    """Shrink a headline font until the text fits on one line."""
    while size > minimum and draw.textlength(text, font=font(path, size)) > maxw:
        size -= 1
    return font(path, size)


def star(draw, cx, cy, r_out, r_in, fill, rot=-math.pi / 2):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = rot + i * math.pi / 5
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


def burst(draw, cx, cy, r):
    pts = []
    for i in range(16):
        rr = r if i % 2 == 0 else r * 0.42
        a = i * math.pi / 8
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    draw.polygon(pts, fill=RED)
    draw.ellipse([cx - r * 0.30, cy - r * 0.30, cx + r * 0.30, cy + r * 0.30],
                 fill=WHITE)


# ---------------------------------------------------------------- icons
def icon_bridge(draw, x, y, s):
    """Bridge with a broken, tilted middle span. Box is s x s."""
    ink, w = INK, max(3, s // 16)
    deck_y = y + s * 0.62
    for tx in (x + s * 0.14, x + s * 0.72):
        draw.rectangle([tx, y + s * 0.16, tx + s * 0.10, deck_y],
                       outline=ink, width=max(2, s // 26))
        draw.line([tx - s * 0.03, y + s * 0.16, tx + s * 0.13, y + s * 0.16],
                  fill=ink, width=w)
    draw.line([x + s * 0.03, deck_y, x + s * 0.40, deck_y], fill=ink, width=w)
    draw.line([x + s * 0.66, deck_y, x + s * 0.97, deck_y], fill=ink, width=w)
    # tilted broken span
    draw.line([x + s * 0.42, deck_y, x + s * 0.64, deck_y + s * 0.20],
              fill=RED, width=w)
    draw.line([x + s * 0.19, y + s * 0.20, x + s * 0.40, deck_y - s * 0.03],
              fill=ink, width=max(2, w - 1))
    draw.line([x + s * 0.77, y + s * 0.20, x + s * 0.68, deck_y - s * 0.03],
              fill=ink, width=max(2, w - 1))
    # water
    for i, wy in enumerate((0.80, 0.90)):
        draw.line([x + s * (0.05 + 0.06 * i), y + s * wy,
                   x + s * (0.42 + 0.06 * i), y + s * wy], fill=BLUE, width=2)
        draw.line([x + s * 0.58, y + s * wy, x + s * 0.95, y + s * wy],
                  fill=BLUE, width=2)


def icon_capitol(draw, x, y, s):
    ink, w = INK, max(3, s // 16)
    cx = x + s / 2
    draw.arc([cx - s * 0.30, y + s * 0.10, cx + s * 0.30, y + s * 0.70],
             start=180, end=360, fill=ink, width=w)
    draw.line([cx, y + s * 0.02, cx, y + s * 0.12], fill=ink, width=w)
    draw.ellipse([cx - s * 0.045, y - s * 0.01, cx + s * 0.045, y + s * 0.05],
                 fill=RED)
    draw.line([cx - s * 0.36, y + s * 0.42, cx + s * 0.36, y + s * 0.42],
              fill=ink, width=w)
    draw.rectangle([x + s * 0.14, y + s * 0.50, x + s * 0.86, y + s * 0.80],
                   outline=ink, width=w)
    for i in range(4):
        lx = x + s * (0.24 + 0.17 * i)
        draw.line([lx, y + s * 0.55, lx, y + s * 0.75], fill=ink, width=2)
    draw.line([x + s * 0.06, y + s * 0.86, x + s * 0.94, y + s * 0.86],
              fill=ink, width=w)


def icon_virus(draw, x, y, s):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.26
    for i in range(10):
        a = i * 2 * math.pi / 10 + 0.3
        x1, y1 = cx + r * 0.9 * math.cos(a), cy + r * 0.9 * math.sin(a)
        x2, y2 = cx + r * 1.45 * math.cos(a), cy + r * 1.45 * math.sin(a)
        draw.line([x1, y1, x2, y2], fill=INK, width=max(3, s // 18))
        draw.ellipse([x2 - s * 0.07, y2 - s * 0.07, x2 + s * 0.07, y2 + s * 0.07],
                     fill=RED)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)
    for dx, dy, rr in ((-0.35, -0.2, 0.16), (0.3, 0.25, 0.13), (0.05, -0.45, 0.10)):
        draw.ellipse([cx + r * dx - r * rr, cy + r * dy - r * rr,
                      cx + r * dx + r * rr, cy + r * dy + r * rr], fill=WHITE)


def icon_shield(draw, x, y, s):
    ink, w = INK, max(3, s // 16)
    pts = [(x + s * 0.50, y + s * 0.04), (x + s * 0.88, y + s * 0.14),
           (x + s * 0.88, y + s * 0.48), (x + s * 0.50, y + s * 0.96),
           (x + s * 0.12, y + s * 0.48), (x + s * 0.12, y + s * 0.14)]
    draw.polygon(pts, outline=ink, width=w)
    draw.line([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.22],
              fill=GOLD, width=w)
    crack = [(x + s * 0.52, y + s * 0.10), (x + s * 0.44, y + s * 0.32),
             (x + s * 0.58, y + s * 0.48), (x + s * 0.46, y + s * 0.66),
             (x + s * 0.54, y + s * 0.86)]
    draw.line(crack, fill=RED, width=w)


# ---------------------------------------------------------------- flags
def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 57))
    star(draw, x + w * 0.24, y + h * 0.30, w * 0.13, w * 0.052, (255, 222, 0))
    for i, (fx, fy) in enumerate(((0.46, 0.14), (0.52, 0.30),
                                  (0.52, 0.46), (0.46, 0.60))):
        star(draw, x + w * fx, y + h * fy, w * 0.055, w * 0.022, (255, 222, 0),
             rot=-math.pi / 2 + 0.4)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=3)


def flag_russia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 43, 30))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=3)


# ---------------------------------------------------------------- scene
def scene(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=BLUE)
    draw.rectangle([x, y, x + w, y + h * 0.34], fill=SKY)
    # coastline (right)
    draw.polygon([(x + w * 0.80, y + h), (x + w, y + h * 0.52),
                  (x + w, y + h)], fill=SAND)
    draw.line([(x + w * 0.80, y + h), (x + w, y + h * 0.52)], fill=INK, width=2)
    # sea dashes
    for i in range(5):
        sx = x + w * (0.05 + 0.11 * i)
        sy = y + h * (0.78 if i % 2 == 0 else 0.88)
        draw.line([sx, sy, sx + w * 0.06, sy], fill=WHITE, width=2)
    # tanker silhouette
    hx, hy = x + w * 0.10, y + h * 0.66
    hw, hh = w * 0.52, h * 0.20
    draw.polygon([(hx, hy), (hx + hw, hy), (hx + hw * 0.93, hy + hh),
                  (hx + hw * 0.06, hy + hh)], fill=INK)
    draw.rectangle([hx + hw * 0.06, hy - h * 0.13, hx + hw * 0.20, hy], fill=INK)
    for i, col in enumerate((GOLD, RED, GOLD)):
        cx0 = hx + hw * (0.28 + 0.20 * i)
        draw.rectangle([cx0, hy - h * 0.15, cx0 + hw * 0.17, hy - h * 0.01],
                       fill=col)
    # dashed drone arcs (quadratic beziers, sampled)
    def arc(p0, p1, p2):
        prev = None
        for i in range(25):
            t = i / 24
            px = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            py = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            if prev and i % 2 == 0:
                draw.line([prev, (px, py)], fill=WHITE, width=3)
            prev = (px, py)
    arc((x + w * 0.06, y + h * 0.08), (x + w * 0.34, y - h * 0.10),
        (x + w * 0.60, y + h * 0.30))
    arc((x + w * 0.16, y + h * 0.05), (x + w * 0.55, y - h * 0.06),
        (x + w * 0.86, y + h * 0.36))
    burst(draw, x + w * 0.60, y + h * 0.30, h * 0.22)
    burst(draw, x + w * 0.86, y + h * 0.36, h * 0.18)
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=3)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # side margin
    R = W - M                   # right edge
    CX = W // 2

    # --- kicker / masthead / rules
    letterspace(d, CX, 18, "ONE DAY · ONE IMAGE · THE WHOLE WORLD",
                font(SANSB, 24), RED, 3)
    f_mast = fit_font(d, "THE WORLD IN A DAY", SERIF, 84, R - M)
    tw = d.textlength("THE WORLD IN A DAY", font=f_mast)
    d.text((CX - tw / 2, 50), "THE WORLD IN A DAY", font=f_mast, fill=INK)
    d.line([M, 150, R, 150], fill=INK, width=4)
    d.line([M, 157, R, 157], fill=INK, width=1)

    # --- date band
    d.rectangle([M, 166, R, 224], fill=RED)
    f_date = font(SANSB, 44)
    dt = "WEDNESDAY · 18 NOVEMBER 2026"
    tw = d.textlength(dt, font=f_date)
    d.text((CX - tw / 2, 173), dt, font=f_date, fill=WHITE)

    # --- lead story (left)
    LX, LW = M, 612
    y = 238
    d.text((LX, y), "THE GULF — WAR", font=font(SANSB, 25), fill=RED)
    y += 34
    for line in ("IRAN STRIKES BACK", "AT U.S. BASES", "IN THE GULF"):
        f_head = fit_font(d, line, SERIF, 50, LW)
        d.text((LX, y), line, font=f_head, fill=INK)
        y += 57
    y += 2
    y = text_block(d, LX, y,
                   "Drones hit U.S. bases in Kuwait and Bahrain after a U.S. "
                   "strike on a missile site on Iran's Qeshm Island. "
                   "Washington says five Iranian tankers were sunk near Hormuz.",
                   font(SANS, 22), INK, LW, 29)
    y += 8
    scene(d, LX, y, LW, 66)
    y += 72
    cap = "THE STRAIT OF HORMUZ"
    f_cap = font(SANSB, 17)
    tw = d.textlength(cap, font=f_cap)
    d.text((LX + (LW - tw) / 2, y), cap, font=f_cap, fill=BLUE)
    lead_bottom = y + 22

    # --- right rail
    RX, RW = 672, R - 672
    d.line([660, 238, 660, lead_bottom], fill=INK, width=1)
    y = 238
    d.text((RX, y), "SHENZHEN — APEC SUMMIT", font=font(SANSB, 20), fill=RED)
    y += 30
    fw = (RW - 12) // 2
    flag_china(d, RX, y, fw, 58)
    flag_russia(d, RX + fw + 12, y, fw, 58)
    y += 68
    f_rhead = font(SERIF, 36)
    for line in wrap(d, "XI AND PUTIN CLOSE RANKS", f_rhead, RW):
        d.text((RX, y), line, font=f_rhead, fill=INK)
        y += 44
    y += 2
    text_block(d, RX, y,
               "China and Russia vow to resist protectionism, a day before "
               "a three-way summit with Trump. Quad leaders gather in Manila.",
               font(SANS, 22), INK, RW, 29)

    # --- grid of four cards
    gy = lead_bottom + 12
    d.line([M, gy - 8, R, gy - 8], fill=INK, width=2)
    cards = [
        ("UKRAINE", "KERCH BRIDGE HIT AGAIN",
         "A second Ukrainian strike in two days partly collapses the bridge to Crimea.",
         icon_bridge),
        ("UNITED STATES", "DEMOCRATS TAKE THE SENATE",
         "Peltola's win in Alaska seals a 56–44 majority.",
         icon_capitol),
        ("DR CONGO — HEALTH", "EBOLA PASSES 11,000 CASES",
         "Three in four infected children under five do not survive it.",
         icon_virus),
        ("UNITED STATES — HEALTH", "U.S. LOSES MEASLES-FREE STATUS",
         "Record cases — over 5,400 — end 26 years of elimination.",
         icon_shield),
    ]
    col_w = (R - M - 16) // 2
    row_h = 100
    for i, (label, head, body, icon) in enumerate(cards):
        cx0 = M + (col_w + 16) * (i % 2)
        cy0 = gy + (row_h + 8) * (i // 2)
        if i % 2 == 1:
            d.line([cx0 - 8, cy0, cx0 - 8, cy0 + row_h - 6], fill=(200, 192, 170), width=1)
        if i >= 2:
            d.line([cx0, cy0 - 5, cx0 + col_w, cy0 - 5], fill=(200, 192, 170), width=1)
        icon(d, cx0, cy0 + 10, 80)
        tx = cx0 + 92
        tw_ = col_w - 92
        d.text((tx, cy0), label, font=font(SANSB, 17), fill=RED)
        f_ch = fit_font(d, head, SERIF, 25, tw_, minimum=15)
        d.text((tx, cy0 + 22), head, font=f_ch, fill=INK)
        text_block(d, tx, cy0 + 54, body, font(SANS, 19), INK, tw_, 24)
    gy_end = gy + 2 * row_h + 8

    # --- also on Wednesday
    ay = gy_end + 10
    d.line([M, ay - 6, R, ay - 6], fill=INK, width=2)
    d.text((M, ay), "ALSO ON WEDNESDAY", font=font(SANSB, 18), fill=RED)
    ay += 24
    ay = text_block(d, M, ay,
                    "Gaza: UN warns 950,000 displaced face winter floods in tent "
                    "camps · Israel: Knesset elects Kahana speaker · COP31 talks "
                    "in Antalya enter decisive days",
                    font(SANS, 19), INK, R - M, 24)

    # --- footer
    d.line([M, 972, R, 972], fill=INK, width=1)
    foot = ("As reported on 18 November 2026 · Reuters · AP · AFP · UN · "
            "Drawn entirely by program — no photographs")
    f_foot = font(SANS, 17)
    tw = d.textlength(foot, font=f_foot)
    d.text((CX - tw / 2, 979), foot, font=f_foot, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "frontpage.png")
    img.save(out, optimize=True)
    print(out, os.path.getsize(out))


if __name__ == "__main__":
    main()
