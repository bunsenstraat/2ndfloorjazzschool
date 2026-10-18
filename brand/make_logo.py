"""Generate the 2nd Floor Jazz School logo as outlined SVGs (no font needed to display them).

Logo: "2nd floor jazz school" in Archivo Black Extra Condensed (wdth 62, wght 900),
tight tracking, with "jazz" in the accent colour.

Run with a Python that has fontTools, brotli and uharfbuzz installed:
    python make_logo.py
"""
import io
import os

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "logo")
os.makedirs(OUT, exist_ok=True)

INK, PAPER, ORANGE, YELLOW = "#141317", "#efe6d2", "#de6b1f", "#e6b532"
TRACKING = -0.035  # em, as in the sketches
WORDSPACE = 0.07  # em of extra space between words, so "floor" and "jazz" don't merge

# --- static instance of the variable font -------------------------------------------
vf = TTFont(os.path.join(HERE, "fonts", "archivo-normal-100-900.woff2"))
font = instantiateVariableFont(vf, {"wdth": 62, "wght": 900})
font.flavor = None
buf = io.BytesIO()
font.save(buf)
blob = hb.Blob(buf.getvalue())
hbfont = hb.Font(hb.Face(blob))
glyphset = font.getGlyphSet()
UPEM = font["head"].unitsPerEm
ASC = 0.72 * UPEM  # cap/x-height zone used for vertical placement


def shape(text):
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": False})
    names = [font.getGlyphName(i.codepoint) for i in buf.glyph_infos]
    return list(zip(names, [p.x_advance for p in buf.glyph_positions]))


def line(segments, size):
    """segments: [(text, colour)]. Returns (svg_paths, width, (ymin, ymax)) at `size` px."""
    s = size / UPEM
    x = 0.0
    out, ymin, ymax = [], 0, 0
    for text, colour in segments:
        d_parts = []
        for name, adv in shape(text):
            pen = SVGPathPen(glyphset)
            # flip y (font units are y-up), scale to px
            glyphset[name].draw(TransformPen(pen, (s, 0, 0, -s, x, 0)))
            if pen.getCommands():
                d_parts.append(pen.getCommands())
            bp = BoundsPen(glyphset)
            glyphset[name].draw(bp)
            if bp.bounds:
                ymin = min(ymin, -bp.bounds[3] * s)
                ymax = max(ymax, -bp.bounds[1] * s)
            x += adv * s + TRACKING * size
            if name == "space":
                x += WORDSPACE * size
        if d_parts:
            out.append((" ".join(d_parts), colour))
    return out, x - TRACKING * size, (ymin, ymax)


def svg(lines, pad, bg=None, square=None, radius=0, align="left", title="2nd Floor Jazz School"):
    """lines: list of (paths, width, (ymin, ymax)) stacked with a small gap."""
    gap = 0.06
    heights = [l[2][1] - l[2][0] for l in lines]
    widths = [l[1] for l in lines]
    content_w = max(widths)
    content_h = sum(heights) + gap * heights[0] * (len(lines) - 1)
    W = content_w + 2 * pad
    H = content_h + 2 * pad
    ox = oy = 0
    if square:
        W = H = square
        ox = (square - content_w) / 2 - pad
        oy = (square - content_h) / 2 - pad
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.1f} {H:.1f}" width="{W:.0f}" height="{H:.0f}" role="img" aria-label="{title}">',
             f"<title>{title}</title>"]
    if bg:
        parts.append(f'<rect width="{W:.1f}" height="{H:.1f}" rx="{radius}" fill="{bg}"/>')
    y = pad + oy
    for (paths, w, (ymin, ymax)), h in zip(lines, heights):
        dx = pad + ox + ((content_w - w) / 2 if align == "center" else 0)
        base = y - ymin
        parts.append(f'<g transform="translate({dx:.2f} {base:.2f})">')
        for d, c in paths:
            parts.append(f'<path fill="{c}" d="{d}"/>')
        parts.append("</g>")
        y += h + gap * heights[0]
    parts.append("</svg>")
    return "\n".join(parts)


def save(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content + "\n")
    print("wrote", name)


def horiz(base, accent, size=100):
    return line([("2nd floor ", base), ("jazz", accent), (" school", base)], size)


# horizontal logo
save("logo.svg", svg([horiz(INK, ORANGE)], pad=4))
save("logo-inverse.svg", svg([horiz(PAPER, YELLOW)], pad=4))
save("logo-ink.svg", svg([horiz(INK, INK)], pad=4))            # one-colour, e.g. stamps / print
save("logo-white.svg", svg([horiz("#ffffff", "#ffffff")], pad=4))

# stacked logo (profile pictures, square spaces)
st1 = line([("2nd floor", INK)], 100)
st2 = line([("jazz", ORANGE), (" school", INK)], 100)
save("logo-stacked.svg", svg([st1, st2], pad=4))
st1i = line([("2nd floor", PAPER)], 100)
st2i = line([("jazz", YELLOW), (" school", PAPER)], 100)
save("logo-stacked-inverse.svg", svg([st1i, st2i], pad=4))

# profile picture (square, safe inside a circle crop)
p1 = line([("2nd floor", INK)], 215)
p2 = line([("jazz", ORANGE), (" school", INK)], 215)
save("profile.svg", svg([p1, p2], pad=0, bg=PAPER, square=1080, align="left"))
p1i = line([("2nd floor", PAPER)], 215)
p2i = line([("jazz", YELLOW), (" school", PAPER)], 215)
save("profile-dark.svg", svg([p1i, p2i], pad=0, bg=INK, square=1080, align="left"))

# app icon / favicon: "2nd" on orange
ic = line([("2nd", PAPER)], 300)
save("icon.svg", svg([ic], pad=0, bg=ORANGE, square=512, radius=96, align="center"))
