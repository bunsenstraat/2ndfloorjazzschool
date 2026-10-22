#!/usr/bin/env python3
"""Render a whole campaign of posts and flyers in one go.

    python3 campaign.py campaigns/seizoen-2026-27.csv
    python3 campaign.py campaigns/seizoen-2026-27.csv walkin     # only rows whose name contains "walkin"

The CSV (comma or semicolon separated, so Excel/Numbers exports both work) has one row per poster:

    name        file name for this poster, e.g. "improviseren"
    template    ritme | gebroken-woord
    formats     optional: any of post, a4 (default: both)
    ...         every other column is a template option (t1, t2, w, side, info, bg, accent, size,
                bars, contact, page, qr, qrlabel); leave a cell empty to use the default.

Output: exports/<campaign>/<name>-post.png (1080x1080), <name>-a4.png and <name>-a4.pdf.
The QR code on each A4 flyer is tagged with the campaign and poster name, so visits from paper
can be told apart in the site statistics.
"""
import csv
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode

HERE = Path(__file__).resolve().parent
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "chromium", "chromium-browser",
]
SIZES = {"post": (1080, 1080), "a4": (1240, 1754)}  # A4 PNG at 150 dpi; the PDF is true A4


def find_chrome():
    for c in CHROME_CANDIDATES:
        if os.path.isabs(c) and os.path.exists(c):
            return c
        if not os.path.isabs(c) and subprocess.run(["which", c], capture_output=True).returncode == 0:
            return c
    sys.exit("Google Chrome not found; it is used to render the templates.")


def read_rows(path):
    text = path.read_text(encoding="utf-8-sig")
    dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=",;")
    return list(csv.DictReader(text.splitlines(), dialect=dialect))


def render(chrome, url, *args):
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--virtual-time-budget=4000", "--force-device-scale-factor=1", *args, url],
                   check=True, capture_output=True)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    csv_path = Path(sys.argv[1]).resolve()
    only = sys.argv[2] if len(sys.argv) > 2 else None
    campaign = csv_path.stem
    out = HERE / "exports" / campaign
    out.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome()

    for row in read_rows(csv_path):
        name = (row.pop("name", "") or "").strip()
        template = (row.pop("template", "") or "").strip()
        formats = [f.strip() for f in (row.pop("formats", "") or "post,a4").split(",") if f.strip()]
        if not name or name.startswith("#") or (only and only not in name):
            continue
        page = HERE / "templates" / f"{template}.html"
        if not page.exists():
            print(f"  skip {name}: unknown template '{template}'")
            continue
        options = {k.strip(): v.strip() for k, v in row.items() if k and v and v.strip()}
        for fmt in formats:
            params = {**options, "format": "a4" if fmt == "a4" else "square", "export": "1",
                      "campaign": campaign, "name": name}
            url = f"{page.as_uri()}?{urlencode(params)}"
            w, h = SIZES[fmt]
            render(chrome, url, f"--window-size={w},{h}", f"--screenshot={out / f'{name}-{fmt}.png'}")
            if fmt == "a4":
                render(chrome, url, "--no-pdf-header-footer", f"--print-to-pdf={out / f'{name}-a4.pdf'}")
        print(f"  {name}: {', '.join(formats)}")
    print(f"done → {out.relative_to(HERE)}/")


if __name__ == "__main__":
    main()
