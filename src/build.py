"""Build the published review page from src/.

    python src/build.py

Writes, at the repo root (what Vercel serves):
  index.html            template.html with gen.js inlined
  logo.webp / logo.png  the round logo (WebP for new phones, PNG for old iPhones)
  favicon.png           browser tab icon
  apple-touch-icon.png  iPhone home-screen icon (logo on navy, no transparency)
"""
from pathlib import Path

from PIL import Image

SRC = Path(__file__).resolve().parent
OUT = SRC.parent
NAVY = (11, 18, 48, 255)


def build_images():
    logo = Image.open(SRC / "logo_source.png").convert("RGBA")
    web = logo.resize((312, 312), Image.LANCZOS)  # 2x the 156px display size
    web.save(OUT / "logo.webp", "WEBP", quality=80, method=6)
    web.save(OUT / "logo.png", "PNG", optimize=True)
    logo.resize((48, 48), Image.LANCZOS).save(OUT / "favicon.png", "PNG", optimize=True)
    # iOS fills transparency with black, so put the logo on the signboard navy
    icon = Image.new("RGBA", (180, 180), NAVY)
    mark = logo.resize((160, 160), Image.LANCZOS)
    icon.alpha_composite(mark, (10, 10))
    icon.convert("RGB").save(OUT / "apple-touch-icon.png", "PNG", optimize=True)


def build_page():
    html = (SRC / "template.html").read_text(encoding="utf-8")
    html = html.replace("{{GEN}}", (SRC / "gen.js").read_text(encoding="utf-8"))
    assert "{{" not in html, "a placeholder was left in the page"
    (OUT / "index.html").write_bytes(html.encode("utf-8"))  # LF line endings
    return len(html.encode("utf-8"))


if __name__ == "__main__":
    build_images()
    size = build_page()
    for name in ("index.html", "logo.webp", "logo.png", "favicon.png", "apple-touch-icon.png"):
        print(f"{name:22} {(OUT / name).stat().st_size:>7} bytes")
    print("page html", size, "bytes")
