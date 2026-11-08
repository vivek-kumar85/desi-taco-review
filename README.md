# The Desi Taco Co. review helper

The page customers open from the QR code on the counter at The Desi Taco Co., Salunkhe Vihar, Pune. Live at https://desi-taco.vercel.app (Vercel deploys every push to `main`).

Customers tap what they had, liked or would improve (each section also has an "Other" box to type in). There's no star rating on this page: people give their stars once, on Google, and the review's tone follows their picks (only good things read happy, "could be better" picks read balanced). "Write my review" shows a short review written from those choices only; "Write another" swaps in a fresh one. Nothing is copied and Google doesn't open until they like it: "Copy & open Google" copies it and opens Google's review form in the same tap, and the 4-step picture guide right above that button shows what's left there: tap stars, tap the box, Paste, Post (and Add photos). (Google doesn't let any website fill in its review box or post for someone, so the paste is the one step left.)

- Everything runs in the customer's browser. Nothing is sent or stored, apart from a list of recent drafts kept on the customer's own phone so it never shows the same one twice.
- Works on old and new phones, iPhones included: no flex `gap`, native control styling reset, 16px inputs (no iOS zoom), WebP logo with a PNG fallback, and a copy step that finishes inside the tap.
- Google review link: https://g.page/r/CQxIrJg7w7Q-EAE/review

## Files

| Path | What it is |
|---|---|
| `index.html`, `logo.webp`, `logo.png`, `favicon.png`, `apple-touch-icon.png` | What Vercel serves. Built, don't edit by hand. |
| `src/template.html` | The page: layout, styles and behaviour. |
| `src/gen.js` | The review writer (phrase banks, tone from the picks, no repeats). |
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
