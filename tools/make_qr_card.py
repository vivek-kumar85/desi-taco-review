"""Print-ready review QR material for The Desi Taco Co., in the logo's neon theme.

Page 1: A6 counter card (105 x 148 mm), navy like the signboard, logo on top.
Page 2: A4 sheet of 12 white stickers (60 x 60 mm) for takeaway bags.
Usage: python make_qr_card.py OUT.pdf LOGO.png [CARD_URL] [STICKER_URL]
The counter card can open the review helper page while the bag stickers go
straight to Google's review form. Also writes PNG previews of both pages.
"""
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4, A6
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.barcode import qrencoder

OUT = Path(sys.argv[1])
LOGO = sys.argv[2]
GOOGLE = "https://g.page/r/CQxIrJg7w7Q-EAE/review"
CARD_URL = sys.argv[3] if len(sys.argv) > 3 else GOOGLE
STICKER_URL = sys.argv[4] if len(sys.argv) > 4 else GOOGLE
CARD_SHORT = CARD_URL.split("://", 1)[-1].rstrip("/")
VIA_HELPER = CARD_URL != GOOGLE

NIGHT = HexColor("#0B1230")  # signboard navy
RED = HexColor("#E4292F")    # logo ring
YELLOW = HexColor("#FDF109") # "DESI" / "CO."
CYAN = HexColor("#0BB7E9")   # "TACO"
MUTED = HexColor("#B3BADF")
INK = HexColor("#0B1230")
CUT = HexColor("#C9CDD8")

pdfmetrics.registerFont(TTFont("UI", "C:/Windows/Fonts/segoeui.ttf"))
pdfmetrics.registerFont(TTFont("UIB", "C:/Windows/Fonts/segoeuib.ttf"))
pdfmetrics.registerFont(TTFont("UIX", "C:/Windows/Fonts/seguibl.ttf"))

_CODES = {}


def _code(url):
    if url not in _CODES:
        q = qrencoder.QRCode(None, qrencoder.QRErrorCorrectLevel.M)
        q.addData(url)
        q.make()
        _CODES[url] = q
    return _CODES[url]


def qr(c, x, y, size, url, border=4):
    """Draw the QR as one filled path of merged runs, so no seams show."""
    q = _code(url)
    n = q.getModuleCount()
    m = size / (n + 2 * border)
    c.setFillColor(INK)
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


def centred(c, text, font, size, y, cx, color):
    c.setFillColor(color)
    c.setFont(font, size)
    c.drawCentredString(cx, y, text)


def dashes(c, cx, y, text_w, color=RED):
    """The short red dashes either side of "CO." in the logo."""
    c.setFillColor(color)
    for sx in (cx - text_w / 2 - 6 * mm, cx + text_w / 2 + 2 * mm):
        c.roundRect(sx, y + 1.2 * mm, 4 * mm, 0.9 * mm, 0.45 * mm, stroke=0, fill=1)


def counter_card(c):
    W, H = A6
    cx = W / 2
    c.setFillColor(NIGHT)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    logo = 44 * mm
    c.drawImage(LOGO, cx - logo / 2, H - 4 * mm - logo, logo, logo, mask="auto")

    centred(c, "Loved the tacos?", "UIX", 21, 92 * mm, cx, white)
    centred(c, "Review us on Google in 30 seconds.", "UI", 10.5, 86 * mm, cx, MUTED)

    q = 46 * mm
    tile = q + 8 * mm
    ty = 81 * mm - tile
    c.setFillColor(white)
    c.setStrokeColor(RED)
    c.setLineWidth(1.8)
    c.roundRect(cx - tile / 2, ty, tile, tile, 4 * mm, stroke=1, fill=1)
    qr(c, cx - q / 2, ty + 4 * mm, q, CARD_URL)

    centred(c, "Point your phone camera here", "UIB", 9.5, ty - 5.5 * mm, cx, CYAN)
    tip = ("Tap what you had and we'll help you write it!" if VIA_HELPER
           else "Just tap the stars. A line about what you ate is a bonus!")
    centred(c, tip, "UI", 8, ty - 10 * mm, cx, MUTED)
    centred(c, CARD_SHORT, "UI", 6.5, ty - 14 * mm, cx, MUTED)

    thanks = "Shukriya!"
    centred(c, thanks, "UIX", 12, 5.5 * mm, cx, YELLOW)
    dashes(c, cx, 5.5 * mm, pdfmetrics.stringWidth(thanks, "UIX", 12))


def sticker_sheet(c):
    W, H = A4
    s = 60 * mm
    gap = 6 * mm
    cols, rows = 3, 4
    gw = cols * s + (cols - 1) * gap
    gh = rows * s + (rows - 1) * gap
    x0 = (W - gw) / 2
    y0 = (H - gh) / 2
    c.setFont("UI", 7)
    c.setFillColor(HexColor("#5A6080"))
    c.drawCentredString(W / 2, H - 10 * mm, "Takeaway bag stickers, 60 x 60 mm. Cut along the grey lines.")
    for r in range(rows):
        for k in range(cols):
            x = x0 + k * (s + gap)
            y = y0 + r * (s + gap)
            c.setStrokeColor(CUT)
            c.setLineWidth(0.4)
            c.setDash(2, 2)
            c.rect(x, y, s, s, stroke=1, fill=0)
            c.setDash()
            c.setStrokeColor(RED)
            c.setLineWidth(1.4)
            c.setFillColor(white)
            c.roundRect(x + 2 * mm, y + 2 * mm, s - 4 * mm, s - 4 * mm, 4 * mm, stroke=1, fill=1)
            cx = x + s / 2
            logo = 18 * mm
            ly = y + s - 3.2 * mm - logo
            # navy badge behind the neon logo, like the signboard
            c.setFillColor(NIGHT)
            c.circle(cx, ly + logo / 2, logo / 2, stroke=0, fill=1)
            c.drawImage(LOGO, cx - logo / 2, ly, logo, logo, mask="auto")
            centred(c, "Loved it? Review us!", "UIB", 8.5, y + s - 24.5 * mm, cx, INK)
            q = 31 * mm
            qr(c, cx - q / 2, y + 3.2 * mm, q, STICKER_URL)


c = canvas.Canvas(str(OUT), pagesize=A6)
c.setTitle("The Desi Taco Co. review QR")
counter_card(c)
c.showPage()
c.setPageSize(A4)
sticker_sheet(c)
c.showPage()
c.save()

import fitz  # PyMuPDF, for previews

doc = fitz.open(str(OUT))
for i, page in enumerate(doc):
    page.get_pixmap(dpi=110 if i else 170).save(str(OUT.with_name(f"{OUT.stem}_p{i + 1}.png")))
print("wrote", OUT)
print("  card    ->", CARD_URL, f"(QR version {_code(CARD_URL).getModuleCount()} modules)")
print("  sticker ->", STICKER_URL, f"(QR version {_code(STICKER_URL).getModuleCount()} modules)")
