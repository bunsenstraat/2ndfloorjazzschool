#!/usr/bin/env python3
"""Render a whole campaign of posts and flyers in one go.

    python3 campaign.py campaigns/seizoen-2026-27.csv
    python3 campaign.py campaigns/seizoen-2026-27.csv walkin     # only rows whose name contains "walkin"

The CSV (comma or semicolon separated, so Excel/Numbers exports both work) has one row per poster:

    name        file name for this poster, e.g. "improviseren"
    template    ritme | gebroken-woord
    formats     optional: any of post, a4, share (default: all three)
    publish     ja = put the post and share image on the website, with its own share page
                (/delen/<name>/) for Facebook and WhatsApp; empty or nee = only export
    share_title title shown in the Facebook / WhatsApp preview of the share page
    share_text  description shown in that preview
    ...         every other column is a template option (t1, t2, w, side, info, bg, accent, size,
                bars, contact, page, qr, qrlabel); leave a cell empty to use the default.

Output: exports/<campaign>/<name>-post.png (1080x1080), <name>-a4.png, <name>-a4.pdf and
<name>-share.jpg (1200x630 preview: the poster plus the workshop essentials).
Published rows also go to ../assets/campaign/<campaign>/ with a manifest.json that build.py
turns into the share pages; run `python3 build.py .` in the site folder afterwards.
The QR code on each A4 flyer is tagged with the campaign and poster name, so visits from paper
can be told apart in the site statistics.
"""
import csv
import json
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
SIZES = {"post": (1080, 1080), "a4": (1240, 1754), "share": (1200, 630)}  # A4 PNG at 150 dpi; the PDF is true A4
SITE_DIR = HERE.parent / "assets" / "campaign"


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
    site = SITE_DIR / campaign
    manifest_path = site / "manifest.json"
    manifest = {e["name"]: e for e in json.loads(manifest_path.read_text())} if manifest_path.exists() else {}

    for row in read_rows(csv_path):
        name = (row.pop("name", "") or "").strip()
        template = (row.pop("template", "") or "").strip()
        formats = [f.strip() for f in (row.pop("formats", "") or "post,a4,share").split(",") if f.strip()]
        publish = (row.pop("publish", "") or "").strip().lower() in ("ja", "yes", "j", "y", "1", "x")
        share_title = (row.pop("share_title", "") or "").strip()
        share_text = (row.pop("share_text", "") or "").strip()
        if not name or name.startswith("#") or (only and only not in name):
            continue
        page = HERE / "templates" / f"{template}.html"
        if not page.exists():
            print(f"  skip {name}: unknown template '{template}'")
            continue
        options = {k.strip(): v.strip() for k, v in row.items() if k and v and v.strip()}
        if (publish or "share" in formats) and "post" not in formats:
            formats.insert(0, "post")  # the share image and the website need the square poster
        for fmt in formats:
            if fmt == "share":
                poster = (out / f"{name}-post.png").as_uri()
                share_page = HERE / "templates" / "share.html"
                render(chrome, f"{share_page.as_uri()}?{urlencode({'poster': poster})}",
                       "--window-size=1200,630", f"--screenshot={out / f'{name}-share.jpg'}")
                continue
            params = {**options, "format": "a4" if fmt == "a4" else "square", "export": "1",
                      "campaign": campaign, "name": name}
            url = f"{page.as_uri()}?{urlencode(params)}"
            w, h = SIZES[fmt]
            render(chrome, url, f"--window-size={w},{h}", f"--screenshot={out / f'{name}-{fmt}.png'}")
            if fmt == "a4":
                render(chrome, url, "--no-pdf-header-footer", f"--print-to-pdf={out / f'{name}-a4.pdf'}")
        if publish:
            site.mkdir(parents=True, exist_ok=True)
            post_url = f"{page.as_uri()}?{urlencode({**options, 'format': 'square', 'export': '1'})}"
            render(chrome, post_url, "--window-size=1080,1080", f"--screenshot={site / f'{name}.jpg'}")
            (site / f"{name}-share.jpg").write_bytes((out / f"{name}-share.jpg").read_bytes())
            manifest[name] = {"name": name, "campaign": campaign, "title": share_title, "text": share_text,
                              "post": f"/assets/campaign/{campaign}/{name}.jpg",
                              "share": f"/assets/campaign/{campaign}/{name}-share.jpg"}
        elif name in manifest:
            del manifest[name]  # unpublished again
        print(f"  {name}: {', '.join(formats)}{'  → website' if publish else ''}")
    if manifest or manifest_path.exists():
        site.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(list(manifest.values()), ensure_ascii=False, indent=2) + "\n")
    print(f"done → {out.relative_to(HERE)}/")


if __name__ == "__main__":
    main()
