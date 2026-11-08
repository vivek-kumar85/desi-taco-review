# The Desi Taco Co. review helper

The page customers open from the QR code on the counter at The Desi Taco Co., Salunkhe Vihar, Pune. Live at https://desi-taco.vercel.app (Vercel deploys every push to `main`).

Customers pick their own star rating and what they had, liked or would improve (each section also has an "Other" box to type in). The page drafts a short review from those choices only, the customer edits it, then copies it and opens Google's review form to paste it, add photos and post it themselves.

- Everything runs in the customer's browser. Nothing is sent or stored, apart from a list of recent drafts kept on the customer's own phone so it never shows the same one twice.
- Works on old and new phones, iPhones included: no flex `gap`, native control styling reset, 16px inputs (no iOS zoom), WebP logo with a PNG fallback, and a copy step that finishes inside the tap.
- Google review link: https://g.page/r/CQxIrJg7w7Q-EAE/review

## Files

| Path | What it is |
|---|---|
| `index.html`, `logo.webp`, `logo.png`, `favicon.png`, `apple-touch-icon.png` | What Vercel serves. Built, don't edit by hand. |
| `src/template.html` | The page: layout, styles and behaviour. |
| `src/gen.js` | The review writer (phrase banks, tone by stars, no repeats). |
| `src/logo_source.png` | The round logo, transparent background. |
| `src/build.py` | Rebuilds the served files from `src/`. |
| `tools/make_qr_card.py` | Makes the printable counter card and bag stickers (PDF). |

## Changing the page

```bash
python src/build.py
git add -A && git commit -m "Describe the change" && git push
```

## Printing the QR material

```bash
python tools/make_qr_card.py Desi_Taco_review_QR.pdf src/logo_source.png https://desi-taco.vercel.app/ https://g.page/r/CQxIrJg7w7Q-EAE/review
```

Page 1 is the A6 counter card (opens this page); page 2 is a sheet of 12 bag stickers (open Google's review form directly). Needs Python with Pillow, reportlab and PyMuPDF, and the Segoe UI fonts that come with Windows.
