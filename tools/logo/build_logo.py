#!/usr/bin/env python3
"""The RBV-Studio logo, built by code: Fredoka (SIL Open Font License 1.1, `fonts/`) letters turned into outlines,
the counters of R and B lit lamp gold like windows at dusk, and the dot of the i the same gold.

    python3 tools/logo/build_logo.py tools/logo/fonts/Fredoka.ttf assets/brand

Writes the SVGs (mark, mark-square for places that round the corners themselves, wordmark, wordmark-on-dark) and,
with `resvg` (brew install resvg) and Pillow, the PNGs, the favicons and favicon.ico into assets/."""
import subprocess
import sys
from pathlib import Path

from fontTools.pens.areaPen import AreaPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

FONT, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

INK = "#1d1d1b"
TEAL = "#0f7781"
TILE_TOP, TILE_BOTTOM = "#16808b", "#0d5c65"
SNOW = "#f4f9fa"
LAMP_HI, LAMP = "#ffe3a1", "#f2b84b"

_cache = {}


def font(weight):
    if weight not in _cache:
        _cache[weight] = instantiateVariableFont(TTFont(FONT), {"wght": weight, "wdth": 100})
    return _cache[weight]


def contours(f, char):
    """The glyph's contours as recordings, its advance width."""
    name = f.getBestCmap()[ord(char)]
    glyph = f.getGlyphSet()[name]
    rec = RecordingPen()
    glyph.draw(rec)
    out, cur = [], []
    for op, args in rec.value:
        cur.append((op, args))
        if op in ("closePath", "endPath"):
            out.append(cur)
            cur = []
    return out, glyph.width


def replay(contour, pen):
    for op, args in contour:
        getattr(pen, op)(*args)


def area(contour):
    p = AreaPen()
    replay(contour, p)
    return p.value


def bounds(contour):
    p = BoundsPen(None)
    replay(contour, p)
    return p.bounds


def svg_path(contour_list, scale, x, y):
    """SVG path data for contours, scaled, flipped (font y up) and placed with the baseline at y."""
    pen = SVGPathPen(None, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
    t = TransformPen(pen, (scale, 0, 0, -scale, x, y))
    for c in contour_list:
        replay(c, t)
    return pen.getCommands()


def word(text, weight, size, x, y, fill, track=0.0, lit=True, dots=True):
    """Paths for a word: the letters in `fill`; with `lit`, the counters (holes) and the i's dot in lamp gold.
    Returns (svg, width)."""
    f = font(weight)
    upm = f["head"].unitsPerEm
    scale = size / upm
    parts, cx = [], x
    for ch in text:
        if ch == " ":
            cx += f["hmtx"]["space"][0] * scale + track * size
            continue
        cs, adv = contours(f, ch)
        if (lit or dots) and cs:
            big = max(cs, key=lambda c: abs(area(c)))
            sign = area(big) > 0
            holes = [c for c in cs if (area(c) > 0) != sign] if lit else []
            dot = []
            if dots and ch == "i":
                # the dot is the contour that sits highest
                dot = [max(cs, key=lambda c: bounds(c)[1])]
            body = [c for c in cs if c not in dot]
            # the gold goes under the letter: the font builds some letters (B) from overlapping pieces, so a hole
            # contour alone also covers parts of the letter; drawn underneath, only the real windows show
            if holes:
                parts.append(f'<path fill="url(#lamp)" d="{svg_path(holes, scale, cx, y)}"/>')
            parts.append(f'<path fill="{fill}" d="{svg_path(body, scale, cx, y)}"/>')
            if holes and ch == "B":
                # Fredoka's bold B has one counter, its middle bar only a notch from the right: close the bar from
                # the stem to the notch (font units) so the B shows two windows
                parts.append(
                    f'<rect fill="{fill}" x="{cx + 205 * scale:.2f}" y="{y - 432 * scale:.2f}" '
                    f'width="{140 * scale:.2f}" height="{151 * scale:.2f}"/>'
                )
            if dot:
                parts.append(f'<path fill="url(#lamp)" d="{svg_path(dot, scale, cx, y)}"/>')
        else:
            parts.append(f'<path fill="{fill}" d="{svg_path(cs, scale, cx, y)}"/>')
        cx += adv * scale + track * size
    return "\n  ".join(parts), cx - x - track * size


def defs(extra=""):
    return f"""<defs>
    <linearGradient id="lamp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{LAMP_HI}"/><stop offset="1" stop-color="{LAMP}"/></linearGradient>
    {extra}
  </defs>"""


def write(name, w, h, body, title):
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" role="img" aria-labelledby="t">
  <title id="t">{title}</title>
  {body}
</svg>
"""
    (OUT / name).write_text(svg)
    print("wrote", name, f"{w:.0f}x{h:.0f}")


# the mark: a tile holding RBV, its windows lit
S = 512
tile = f'<rect width="{S}" height="{S}" rx="{S * 0.23:.0f}" fill="url(#tile)"/>'
size = 214
_, lw = word("RBV", 700, size, 0, 0, SNOW, track=0.02)
x0 = (S - lw) / 2
cap = font(700)["OS/2"].sCapHeight * size / font(700)["head"].unitsPerEm
y0 = S / 2 + cap / 2
letters, _ = word("RBV", 700, size, x0, y0, SNOW, track=0.02)
tile_defs = f'<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{TILE_TOP}"/><stop offset="1" stop-color="{TILE_BOTTOM}"/></linearGradient>'
write("mark.svg", S, S, defs(tile_defs) + "\n  " + tile + "\n  " + letters, "RBV-Studio")
square = f'<rect width="{S}" height="{S}" fill="url(#tile)"/>'
write("mark-square.svg", S, S, defs(tile_defs) + "\n  " + square + "\n  " + letters, "RBV-Studio")

# the wordmark: RBV in ink with lit windows, Studio in teal with a lit dot, on one line
size = 120
rbv, w1 = word("RBV", 700, size, 0, 0, INK, track=0.02)
gap = size * 0.24
studio, w2 = word("Studio", 600, size, 0, 0, TEAL, track=0.01, lit=False)
f = font(700)
upm = f["head"].unitsPerEm
asc = f["OS/2"].sTypoAscender * size / upm
desc = -f["OS/2"].sTypoDescender * size / upm
pad = size * 0.06
H = asc * 0.86 + desc * 0.25 + pad * 2
base = pad + asc * 0.86
rbv, _ = word("RBV", 700, size, pad, base, INK, track=0.02)
studio, _ = word("Studio", 600, size, pad + w1 + gap, base, TEAL, track=0.01, lit=False)
W = pad * 2 + w1 + gap + w2
write("wordmark.svg", W, H, defs() + "\n  " + rbv + "\n  " + studio, "RBV-Studio")

# the wordmark for dark backgrounds
rbv_d, _ = word("RBV", 700, size, pad, base, SNOW, track=0.02)
studio_d, _ = word("Studio", 600, size, pad + w1 + gap, base, "#7fd3db", track=0.01, lit=False)
write("wordmark-on-dark.svg", W, H, defs() + "\n  " + rbv_d + "\n  " + studio_d, "RBV-Studio")



# PNG exports next to the SVGs' folder (assets/): favicons from the rounded mark, the Apple and Roblox icons from the
# square one (they round the corners themselves), the wordmark for the press kit
assets = OUT.parent


def png(svg, out, width, background=None):
    cmd = ["resvg", "-w", str(width)] + (["--background", background] if background else []) + [str(OUT / svg), str(out)]
    subprocess.run(cmd, check=True)
    print("rendered", out.relative_to(assets.parent) if assets.parent in out.parents else out)


for n in (16, 32, 48, 96, 192, 512):
    png("mark.svg", assets / f"favicon-{n}.png", n)
png("mark-square.svg", assets / "apple-touch-icon.png", 180)
png("mark-square.svg", OUT / "rbv-studio-icon-512.png", 512)
png("mark.svg", OUT / "rbv-studio-mark-1024.png", 1024)
png("wordmark.svg", OUT / "rbv-studio-wordmark.png", 1600)
png("wordmark-on-dark.svg", OUT / "rbv-studio-wordmark-on-dark.png", 1600)
try:
    from PIL import Image

    Image.open(assets / "favicon-48.png").save(assets / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("wrote favicon.ico")
except ImportError:
    print("Pillow missing: favicon.ico not written")
