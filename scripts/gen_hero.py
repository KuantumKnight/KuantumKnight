"""
hero.svg — the cold open.

a letterboxed frame: a raymarched ascii spade turns slowly on the left while
the title card exposes on the right, one line at a time. the spade loops (it
is the only thing that moves after the first few seconds); everything else
fades in once and holds.
"""

import re

from lib import (INK, SILVER, SILVER_DIM, ASH, BLOOD, SERIF, MONO,
                 esc, font_css, film_defs, film_overlay, write_svg, profile, reveal)
from gen_ascii import frames, COLS, ROWS

W, H = 860, 360
BAR = 34                      # letterbox bar height
FS, LH, CW = 10, 11, 6.0      # ascii font size / line height / glyph width
TURN = 7.5                    # seconds per full rotation


def row(x0, y, line):
    """one ascii row. whitespace isn't reliable inside an <img> svg, so each
    run of glyphs gets its own x instead of leaning on leading spaces."""
    runs = "".join(
        f'<tspan x="{x0 + m.start() * CW:g}">{esc(m.group())}</tspan>'
        for m in re.finditer(r"\S+", line))
    return f'<text y="{y}">{runs}</text>'


def spade():
    fr = frames()
    n = len(fr)
    x0 = 44
    y0 = BAR + (H - 2 * BAR - ROWS * LH) // 2 + 8
    groups = []
    for k, rows in enumerate(fr):
        a, b = k / n, (k + 1) / n
        if k == 0:
            vals, times = "visible;hidden", f"0;{b:.4f}"
        elif k == n - 1:
            vals, times = "hidden;visible", f"0;{a:.4f}"
        else:
            vals, times = "hidden;visible;hidden", f"0;{a:.4f};{b:.4f}"
        text = "".join(row(x0, y0 + j * LH, r)
                       for j, r in enumerate(rows) if r.strip())
        groups.append(
            f'<g visibility="{"visible" if k == 0 else "hidden"}">'
            f'<animate attributeName="visibility" values="{vals}" keyTimes="{times}" '
            f'calcMode="discrete" dur="{TURN}s" repeatCount="indefinite"/>{text}</g>')
    return (f'<g font-family="{MONO}" font-size="{FS}" fill="{SILVER}" '
            f'opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="2.4s" begin="0.3s" fill="freeze"/>'
            + "".join(groups) + '</g>')


def build():
    me = profile()["identity"]
    X = 440
    title = [
        reveal(1.4, f'<text x="{X}" y="118" font-family="{MONO}" font-size="10" '
                    f'letter-spacing="4" fill="{ASH}">A KUANTUMKNIGHT PICTURE</text>'),
        reveal(2.1, f'<text x="{X-3}" y="186" font-family="{SERIF}" font-size="62" '
                    f'fill="{SILVER}">{esc(me["handle"])}</text>', dur=2.0),
        reveal(3.0, f'<text x="{X}" y="222" font-family="{SERIF}" font-style="italic" '
                    f'font-size="22" fill="{SILVER_DIM}">{esc(me["name"].lower())}</text>'),
        reveal(3.8, f'<rect x="{X}" y="246" width="6" height="6" fill="{BLOOD}"/>'
                    f'<text x="{X+16}" y="253" font-family="{MONO}" font-size="12" '
                    f'fill="{SILVER_DIM}">{esc(me["tagline"])}</text>'),
        reveal(4.4, f'<text x="{X+16}" y="273" font-family="{MONO}" font-size="11" '
                    f'fill="{ASH}">{esc(me["role"].lower())}</text>'),
    ]
    subs = reveal(0.6, f'<text x="{W/2}" y="{H-13}" text-anchor="middle" '
                       f'font-family="{MONO}" font-size="9" letter-spacing="3" '
                       f'fill="{ASH}">SC. 00 — COLD OPEN</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(me["handle"])} — a rotating ascii spade beside the title: {esc(me["tagline"])}">
  <defs>{film_defs(W, H, seed=3)}</defs>
  {font_css(serif=True, italic=True)}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  {spade()}
  {"".join(title)}
  {film_overlay(W, H, bars=BAR)}
  {subs}
</svg>
'''
    write_svg("assets/hero.svg", svg)


if __name__ == "__main__":
    build()
