"""Paytm / Google Pay style QR standee for The Desi Taco Co. reviews.

Neon-signboard look from the logo: navy ground, glowing cyan frame, the round
logo, a big white QR tile with a "SCAN ME" tab and scan corners, three steps,
and neon taco / chilli doodles. One vector design, drawn on an A5 grid
(148 x 210 mm) and scaled for A4 (same proportions).

Writes, next to OUT_DIR:
  Desi_Taco_QR_Standee_A5_print.pdf  A5 + 3 mm bleed + crop marks (print shop)
  Desi_Taco_QR_Standee_A4_print.pdf  A4 + 3 mm bleed + crop marks
  Desi_Taco_QR_Standee.png            soft copy (A5 at 300 dpi, no bleed)

Usage: python make_standee.py OUT_DIR LOGO.png URL
"""
import math
import sys
from pathlib import Path

from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import qrencoder

OUT_DIR = Path(sys.argv[1])
LOGO = sys.argv[2]
URL = sys.argv[3]
SHORT = URL.split("://", 1)[-1].rstrip("/")
FONTS = Path(__file__).resolve().parent / "fonts"

NIGHT = HexColor("#0B1230")
NIGHT2 = HexColor("#131B47")
RED = HexColor("#E4292F")
YELLOW = HexColor("#FDF109")
CYAN = HexColor("#0BB7E9")
ORANGE = HexColor("#ED8B38")
GREEN = HexColor("#1CAD60")
MUTED = HexColor("#B3BADF")

pdfmetrics.registerFont(TTFont("B6", str(FONTS / "Baloo2-600.ttf")))
pdfmetrics.registerFont(TTFont("B8", str(FONTS / "Baloo2-800.ttf")))

W, H = 148 * mm, 210 * mm          # the A5 design grid
BLEED, SLUG = 3 * mm, 9 * mm       # bleed, and room for crop marks outside it


def qr(c, x, y, size, url, border=0):
    """QR as one filled path of merged runs (no hairline seams in print)."""
    q = qrencoder.QRCode(None, qrencoder.QRErrorCorrectLevel.M)
    q.addData(url)
    q.make()
    n = q.getModuleCount()
    m = size / (n + 2 * border)
    c.setFillColor(NIGHT)
    p = c.beginPath()
    for r in range(n):
        col = 0
        while col < n:
            if q.isDark(r, col):
                start = col
                while col < n and q.isDark(r, col):
                    col += 1
                top = y + size - (border + r) * m
                p.rect(x + (border + start) * m, top - m, (col - start) * m, m)
            else:
                col += 1
    c.drawPath(p, stroke=0, fill=1, fillMode=1)
    return n


def neon(c, draw, color, width):
    """Stroke a path a few times, wide and faint to thin and bright: a neon tube."""
    c.saveState()
    c.setStrokeColor(color)
    c.setLineCap(1)
    c.setLineJoin(1)
    for w, a in ((width * 5.5, 0.07), (width * 3.2, 0.14), (width * 1.8, 0.35), (width, 1.0)):
        c.setLineWidth(w)
        c.setStrokeAlpha(a)
        draw()
    c.restoreState()


def centred(c, text, font, size, y, color, cx=W / 2):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(cx, y, text)


def star(c, cx, cy, r, color):
    p = c.beginPath()
    for k in range(10):
        a = math.radians(90 + 36 * k)
        rad = r if k % 2 == 0 else r * 0.45
        x, y = cx + rad * math.cos(a), cy + rad * math.sin(a)
        p.moveTo(x, y) if k == 0 else p.lineTo(x, y)
    p.close()
    c.setFillColor(color)
    c.drawPath(p, stroke=0, fill=1)


def sparkle(c, cx, cy, r, color):
    """Four-point twinkle, like the ones around neon signs."""
    def draw():
        p = c.beginPath()
        p.moveTo(cx, cy + r)
        p.curveTo(cx + r * 0.12, cy + r * 0.12, cx + r * 0.12, cy + r * 0.12, cx + r, cy)
        p.curveTo(cx + r * 0.12, cy - r * 0.12, cx + r * 0.12, cy - r * 0.12, cx, cy - r)
        p.curveTo(cx - r * 0.12, cy - r * 0.12, cx - r * 0.12, cy - r * 0.12, cx - r, cy)
        p.curveTo(cx - r * 0.12, cy + r * 0.12, cx - r * 0.12, cy + r * 0.12, cx, cy + r)
        c.drawPath(p, stroke=1, fill=0)
    neon(c, draw, color, 0.45 * mm)


def taco(c, cx, cy, r, tilt):
    """Side-on taco: a U-shaped shell with a wavy lettuce line, as neon doodles."""
    c.saveState()
    c.translate(cx, cy)
    c.rotate(tilt)

    def shell():
        p = c.beginPath()
        p.arc(-r, -r, r, r, 180, 180)
        p.lineTo(-r, 0)
        c.drawPath(p, stroke=1, fill=0)

    def lettuce():
        p = c.beginPath()
        n = 6
        p.moveTo(-r, 0)
        for k in range(n):
            x0 = -r + 2 * r * k / n
            x1 = -r + 2 * r * (k + 1) / n
            p.curveTo(x0 + (x1 - x0) * 0.25, r * 0.28, x0 + (x1 - x0) * 0.75, r * 0.28, x1, 0)
        c.drawPath(p, stroke=1, fill=0)

    neon(c, shell, ORANGE, 0.55 * mm)
    neon(c, lettuce, GREEN, 0.5 * mm)
    c.setFillColor(RED)
    for dx in (-0.45, 0.05, 0.5):
        c.circle(dx * r, 0.12 * r, 0.09 * r, stroke=0, fill=1)
    c.restoreState()


def chilli(c, cx, cy, s, tilt):
    """Curved chilli with a green stem."""
    c.saveState()
    c.translate(cx, cy)
    c.rotate(tilt)

    def body():
        p = c.beginPath()
        p.moveTo(0, 0)
        p.curveTo(s * 0.55, s * 0.05, s * 0.95, -s * 0.25, s * 1.1, -s * 0.8)
        p.curveTo(s * 0.7, -s * 0.45, s * 0.35, -s * 0.28, 0, -s * 0.24)
        p.close()
        c.drawPath(p, stroke=1, fill=0)

    def stem():
        p = c.beginPath()
        p.moveTo(0, -s * 0.12)
        p.curveTo(-s * 0.15, -s * 0.1, -s * 0.22, s * 0.05, -s * 0.2, s * 0.2)
        c.drawPath(p, stroke=1, fill=0)

    neon(c, body, RED, 0.55 * mm)
    neon(c, stem, GREEN, 0.5 * mm)
    c.restoreState()


def glow(c, x, y, r, color, alpha):
    """Soft round glow made of stacked translucent circles."""
    c.saveState()
    c.setFillColor(color)
    steps = 14
    for k in range(steps):
        c.setFillAlpha(alpha / steps * 1.6)
        c.circle(x, y, r * (1 - k / steps), stroke=0, fill=1)
    c.restoreState()


def design(c):
    """The standee on the 148 x 210 mm grid, origin bottom-left of the trim."""
    cx = W / 2
    # ground (runs into the bleed) and the signboard glows
    c.setFillColor(NIGHT)
    c.rect(-BLEED, -BLEED, W + 2 * BLEED, H + 2 * BLEED, stroke=0, fill=1)
    glow(c, cx, 178 * mm, 70 * mm, CYAN, 0.22)
    glow(c, 132 * mm, 70 * mm, 60 * mm, RED, 0.14)
    glow(c, 14 * mm, 40 * mm, 50 * mm, ORANGE, 0.08)

    # neon frame
    inset = 5 * mm
    neon(c, lambda: c.roundRect(inset, inset, W - 2 * inset, H - 2 * inset, 9 * mm, stroke=1, fill=0), CYAN, 0.6 * mm)

    # logo with a dark disc behind so its own glow reads
    logo = 40 * mm
    ly = 159 * mm
    c.setFillColor(NIGHT)
    c.circle(cx, ly + logo / 2, logo / 2, stroke=0, fill=1)
    c.drawImage(LOGO, cx - logo / 2, ly, logo, logo, mask="auto")

    # neon doodles either side of the logo
    taco(c, 27 * mm, 186 * mm, 9 * mm, -12)
    chilli(c, 112 * mm, 190 * mm, 15 * mm, -18)
    sparkle(c, 30 * mm, 165 * mm, 3 * mm, YELLOW)
    sparkle(c, 121 * mm, 167 * mm, 2.4 * mm, CYAN)
    sparkle(c, 117 * mm, 199 * mm, 1.8 * mm, YELLOW)

    # five small stars: "review"
    for k in range(5):
        star(c, cx + (k - 2) * 6.2 * mm, 154.5 * mm, 2.3 * mm, YELLOW)

    # headline with "tacos?" in yellow
    size = 31
    a, b = "Loved the ", "tacos?"
    wa, wb = pdfmetrics.stringWidth(a, "B8", size), pdfmetrics.stringWidth(b, "B8", size)
    x0 = cx - (wa + wb) / 2
    c.setFont("B8", size)
    c.setFillColor(white)
    c.drawString(x0, 140 * mm, a)
    c.setFillColor(YELLOW)
    c.drawString(x0 + wa, 140 * mm, b)
    centred(c, "Scan & review us on Google", "B6", 14.5, 131 * mm, CYAN)

    # the QR tile: white, red neon edge, scan corners, SCAN ME tab
    tile = 74 * mm
    tx, ty = cx - tile / 2, 48 * mm
    neon(c, lambda: c.roundRect(tx, ty, tile, tile, 6 * mm, stroke=1, fill=0), RED, 0.7 * mm)
    c.setFillColor(white)
    c.roundRect(tx, ty, tile, tile, 6 * mm, stroke=0, fill=1)
    # 56 mm code: at least 4 modules of white on the sides and bottom (scanner
    # quiet zone), a little more on top where the SCAN ME tab sits
    code = 56 * mm
    modules = qr(c, cx - code / 2, ty + 7.8 * mm, code, URL)
    # camera-style corner brackets just outside the tile
    g, L = 3.2 * mm, 9 * mm
    def corners():
        for (x, y, sx, sy) in ((tx - g, ty - g, 1, 1), (tx + tile + g, ty - g, -1, 1),
                               (tx - g, ty + tile + g, 1, -1), (tx + tile + g, ty + tile + g, -1, -1)):
            p = c.beginPath()
            p.moveTo(x, y + sy * L)
            p.lineTo(x, y)
            p.lineTo(x + sx * L, y)
            c.drawPath(p, stroke=1, fill=0)
    neon(c, corners, YELLOW, 0.8 * mm)
    # SCAN ME tab across the top edge
    tab_w, tab_h = 33 * mm, 8.6 * mm
    c.setFillColor(YELLOW)
    c.roundRect(cx - tab_w / 2, ty + tile - tab_h / 2, tab_w, tab_h, tab_h / 2, stroke=0, fill=1)
    centred(c, "SCAN ME", "B8", 13, ty + tile - 1.6 * mm, NIGHT)
    centred(c, SHORT, "B6", 7.6, ty - 6.6 * mm, MUTED)

    # three steps
    steps = [("Scan", "the QR"), ("Tap what", "you had"), ("Paste & post", "on Google")]
    for k, (l1, l2) in enumerate(steps):
        sx = cx + (k - 1) * 44 * mm
        c.setFillColor(YELLOW)
        c.circle(sx, 33.5 * mm, 4.2 * mm, stroke=0, fill=1)
        centred(c, str(k + 1), "B8", 13, 31.4 * mm, NIGHT, sx)
        centred(c, l1, "B6", 10, 24.5 * mm, white, sx)
        centred(c, l2, "B6", 10, 20.6 * mm, white, sx)
        if k < 2:  # little arrows between steps
            ax = sx + 22 * mm
            def arrow(ax=ax):
                p = c.beginPath()
                p.moveTo(ax - 3 * mm, 33.5 * mm)
                p.lineTo(ax + 3 * mm, 33.5 * mm)
                p.moveTo(ax + 1 * mm, 35.3 * mm)
                p.lineTo(ax + 3 * mm, 33.5 * mm)
                p.lineTo(ax + 1 * mm, 31.7 * mm)
                c.drawPath(p, stroke=1, fill=0)
            neon(c, arrow, CYAN, 0.45 * mm)

    # thanks
    thanks = "Shukriya!"
    tw = pdfmetrics.stringWidth(thanks, "B8", 17)
    centred(c, thanks, "B8", 17, 11.6 * mm, YELLOW)
    c.setFillColor(RED)
    for dx in (-tw / 2 - 8 * mm, tw / 2 + 3 * mm):
        c.roundRect(cx + dx, 13.2 * mm, 5 * mm, 1.1 * mm, 0.55 * mm, stroke=0, fill=1)
    centred(c, "The Desi Taco Co.  ·  Salunkhe Vihar, Pune", "B6", 8, 7.6 * mm, MUTED)
    return modules


def crop_marks(c, w, h, off):
    """Thin marks at each trim corner, in the slug, clear of the bleed."""
    c.saveState()
    c.setStrokeColor(black)
    c.setLineWidth(0.25)
    gap, length = BLEED + 1 * mm, 6 * mm
    for x, y, sx, sy in ((off, off, -1, -1), (off + w, off, 1, -1), (off, off + h, -1, 1), (off + w, off + h, 1, 1)):
        c.line(x + sx * gap, y, x + sx * (gap + length), y)
        c.line(x, y + sy * gap, x, y + sy * (gap + length))
    c.restoreState()


def print_pdf(path, trim_w, trim_h, label):
    """Exact trim size; the A5 design is scaled evenly to the trim height and
    centred (A4 is a hair wider in proportion; the navy ground fills it)."""
    w, h = trim_w, trim_h
    scale = h / H
    off = BLEED + SLUG
    c = canvas.Canvas(str(path), pagesize=(w + 2 * off, h + 2 * off), initialFontName="B6")
    c.setTitle(f"The Desi Taco Co. review QR standee ({label})")
    c.saveState()
    c.translate(off + (w - W * scale) / 2, off)
    c.scale(scale, scale)
    modules = design(c)
    c.restoreState()
    # white slug so the marks are visible on screen too
    c.setFillColor(white)
    for (x, y, ww, hh) in ((0, 0, w + 2 * off, SLUG), (0, h + off + BLEED, w + 2 * off, SLUG),
                           (0, 0, SLUG, h + 2 * off), (w + off + BLEED, 0, SLUG, h + 2 * off)):
        c.rect(x, y, ww, hh, stroke=0, fill=1)
    crop_marks(c, w, h, off)
    c.setFillColor(HexColor("#666666"))
    c.setFont("B6", 6)
    c.drawString(off, 3 * mm, f"Desi Taco review standee, {label} ({w / mm:.0f} x {h / mm:.0f} mm). 3 mm bleed; trim at the corner marks.")
    c.showPage()
    c.save()
    return modules


def soft_copy(path_pdf):
    c = canvas.Canvas(str(path_pdf), pagesize=(W, H), initialFontName="B6")
    design(c)
    c.showPage()
    c.save()


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    m = print_pdf(OUT_DIR / "Desi_Taco_QR_Standee_A5_print.pdf", 148 * mm, 210 * mm, "A5")
    print_pdf(OUT_DIR / "Desi_Taco_QR_Standee_A4_print.pdf", 210 * mm, 297 * mm, "A4")
    tmp = OUT_DIR / "_soft.pdf"
    soft_copy(tmp)
    import pymupdf
    pymupdf.open(str(tmp))[0].get_pixmap(dpi=300).save(str(OUT_DIR / "Desi_Taco_QR_Standee.png"))
    tmp.unlink()
    print("QR:", URL, f"({m} modules)")
    for f in sorted(OUT_DIR.glob("Desi_Taco_QR_Standee*")):
        print(f.name, f.stat().st_size // 1024, "KB")
