# The Desi Taco Co. review helper

The page customers open from the QR code on the counter at The Desi Taco Co., Salunkhe Vihar, Pune. Live at https://desitaco.arthproductionhouse.com on Cloudflare's free plan (a Worker that serves the page's files, plus a D1 database). The old address, https://desi-taco.vercel.app, forwards there, so QR codes printed earlier keep working.

Customers tap what they had, liked or would improve (each section also has an "Other" box to type in). There's no star rating on this page: people give their stars once, on Google, and the review's tone follows their picks (only good things read happy, "could be better" picks read balanced). "Write my review" shows a short review written from those choices only; "Write another" swaps in a fresh one. Nothing is copied and Google doesn't open until they like it: "Copy & open Google" copies it and opens Google's review form in the same tap, and the 4-step picture guide right above that button shows what's left there: tap stars, tap the box, Paste, Post (and Add photos). (Google doesn't let any website fill in its review box or post for someone, so the paste is the one step left.)

- The review writer (`src/gen.js`) runs in the customer's browser: hand-written phrase banks mixed at random. No AI service, no API key, no cost per review.
- Every review is unique for everyone. Before showing a review, the phone sends a fingerprint of it (a SHA-256 code of its words, never the text itself) to `/api/claim`; `worker/index.js` hands each fingerprint out only once (table `seen` in D1). Reviews that differ only in punctuation or emoji count as the same. If the check can't be reached, the page still works, and the phone's own list of its last 300 drafts keeps it from repeating itself.
- Free for the long run: Cloudflare's free plan allows 100,000 checks a day, and the page's files are free and unlimited.
- Cloudflare's own Web Analytics counter is switched on for the domain, so it adds its cookie-free page-view beacon.
- Works on old and new phones, iPhones included: no flex `gap`, native control styling reset, 16px inputs (no iOS zoom), WebP logo with a PNG fallback, and a copy step that finishes inside the tap.
- Google review link: https://g.page/r/CQxIrJg7w7Q-EAE/review

## Files

| Path | What it is |
|---|---|
| `public/` | What Cloudflare serves: `index.html`, logos and icons. Built by `src/build.py`; don't edit by hand. |
| `worker/index.js` | The only server code: the unique-review check at `/api/claim`. |
| `schema.sql` | The D1 table it uses (`seen`: fingerprint and time). |
| `wrangler.jsonc` | Cloudflare settings: the address, the files, the database. |
| `vercel.json` | Forwards the old desi-taco.vercel.app address to the new one. |
| `src/template.html` | The page: layout, styles and behaviour. |
| `src/gen.js` | The review writer (phrase banks, tone from the picks, no repeats). |
| `src/logo_source.png` | The round logo, transparent background. |
| `src/build.py` | Rebuilds `public/` from `src/`. |
| `tools/make_qr_card.py` | Makes the printable counter card and bag stickers (PDF). |

## Changing the page

```bash
python src/build.py
npx wrangler@4.152.0 deploy
git add -A && git commit -m "Describe the change" && git push
```

`wrangler deploy` needs a one-time `npx wrangler@4.152.0 login` on the computer, with the Cloudflare account that holds arthproductionhouse.com. To create the database table on a fresh account: `npx wrangler@4.152.0 d1 execute desi-taco-reviews --remote --file schema.sql`.

## Printing the QR material

```bash
python tools/make_qr_card.py Desi_Taco_review_QR.pdf src/logo_source.png https://desitaco.arthproductionhouse.com/ https://g.page/r/CQxIrJg7w7Q-EAE/review
```

Page 1 is the A6 counter card (opens this page); page 2 is a sheet of 12 bag stickers (open Google's review form directly). Needs Python with Pillow, reportlab and PyMuPDF, and the Segoe UI fonts that come with Windows.
