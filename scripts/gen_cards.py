"""
card_*.svg — one case file per featured project.

a thin letterboxed still: a large dim serif numeral, the name, a one-line
brief, a sentence of detail, and the stack set as plain text. the right half
carries the project's engraved poster as a 1-bit dither (keyed by project id
in scripts/poster_images.py), fading into the ink behind the text. copy comes from profile.json. each card is wrapped in a link in the
README, so the whole frame is clickable.
"""

import math

from lib import (INK, SILVER, SILVER_DIM, ASH, BLOOD, SERIF, MONO, esc,
                 font_css, film_defs, film_overlay, write_svg, collect, profile,
                 reveal)
from poster_images import POSTERS

W, H = 860, 220
BAR = 10
TX = 190                     # text column


def wrap(text, n=62, maxlines=2):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + len(w) + 1 > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return lines[:maxlines]


# -------------------------------------------------------- backdrop ----

PX = 430                     # poster occupies the right half


def backdrop(key):
    """the dithered poster, tinted silver, fading in from the text side."""
    w, h, b64 = POSTERS[key]
    cx, cy = PX + w / 2, H / 2
    return f'''<defs>
    <filter id="tint" color-interpolation-filters="sRGB">
      <feColorMatrix values="0 0 0 0 0.847  0 0 0 0 0.835  0 0 0 0 0.808  0.3 0.3 0.3 0 0"/>
    </filter>
    <linearGradient id="fadeg" x1="{PX + 100}" x2="{PX + 300}" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/>
    </linearGradient>
    <mask id="fade" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect width="{W}" height="{H}" fill="url(#fadeg)"/>
    </mask>
  </defs>
  <g mask="url(#fade)" opacity="0">
    <animate attributeName="opacity" from="0" to="0.62" dur="2.4s" begin="0.2s" fill="freeze"/>
    <g transform="translate({cx} {cy})"><g>
      <animateTransform attributeName="transform" type="scale"
        values="1.04;1" dur="6s" begin="0.2s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.6 0.3 1"/>
      <image x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" filter="url(#tint)"
             style="image-rendering:pixelated" href="data:image/png;base64,{b64}"/>
    </g></g>
  </g>'''


def _star(cx, cy, r):
    pts = []
    for k in range(10):
        rad = r if k % 2 == 0 else r * 0.42
        a = math.pi / 2 + k * math.pi / 5
        pts.append(f"{cx + rad * math.cos(a):.1f},{cy - rad * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"


def star_count(x, stars):
    """a red star and the star count, counting up once beside the name.
    the last frame is visible by default so a renderer that ignores
    animation still shows the real number."""
    n, t0, dur = 12, 1.0, 1.4
    frames = []
    for k in range(1, n + 1):
        on = t0 + dur * (k - 1) / n
        off = t0 + dur * k / n
        last = k == n
        anim = (f'<set attributeName="visibility" to="hidden" begin="0s"/>'
                f'<set attributeName="visibility" to="visible" begin="{on:.3f}s"/>')
        if not last:
            anim += f'<set attributeName="visibility" to="hidden" begin="{off:.3f}s"/>'
        frames.append(
            f'<text x="{x + 16}" y="94" font-family="{SERIF}" font-size="28" fill="{SILVER}" '
            f'visibility="{"visible" if last else "hidden"}">{anim}{round(stars * k / n)}</text>')
    digits = len(str(stars))
    return (f'<path d="{_star(x + 5, 84, 6)}" fill="{BLOOD}"/>'
            + "".join(frames)
            + f'<text x="{x + 20 + digits * 14}" y="94" font-family="{MONO}" font-size="10" '
              f'letter-spacing="1.5" fill="{ASH}">STARS</text>')


def card(idx, p, stars=None):
    num = f"{idx + 1:02d}"
    tags = list(p["chips"])
    detail = "".join(
        f'<text x="{TX}" y="{156 + i * 17}" font-family="{MONO}" font-size="11.5" '
        f'fill="{SILVER_DIM}">{esc(ln)}</text>'
        for i, ln in enumerate(wrap(p["detail"])))

    numeral = (f'<text x="36" y="138" font-family="{SERIF}" font-size="118" '
               f'fill="#2a2926">{num}</text>')
    head = (f'<text x="{TX}" y="50" font-family="{MONO}" font-size="9.5" '
            f'letter-spacing="3.5" fill="{ASH}">CASE FILE {num}'
            f'<tspan letter-spacing="0.5">  —  {esc(p["repo"])}</tspan></text>'
            f'<text x="{TX - 2}" y="94" font-family="{SERIF}" font-size="40" '
            f'fill="{SILVER}">{esc(p["name"])}</text>')
    if stars:
        head += star_count(TX + len(p["name"]) * 0.43 * 40 + 18, stars)
    body = (f'<text x="{TX}" y="128" font-family="{SERIF}" font-size="20" '
            f'fill="{SILVER}">{esc(p["brief"])}</text>{detail}')
    foot = (f'<text x="{TX}" y="{H - 22}" font-family="{MONO}" font-size="11" '
            f'letter-spacing="0.5" fill="{ASH}">{esc("  ·  ".join(tags))}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(p["name"])}: {esc(p["brief"])}">
  <defs>{film_defs(W, H, seed=20 + idx)}</defs>
  {font_css(serif=True)}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  {backdrop(p["id"])}
  {reveal(0.2, numeral, dur=2.0)}
  {reveal(0.5, head)}
  {reveal(0.9, body)}
  {reveal(1.3, foot)}
  {film_overlay(W, H, bars=BAR, vignette=False)}
</svg>
'''
    write_svg(f"assets/card_{p['id']}.svg", svg)


def build():
    d = collect()
    for i, p in enumerate(profile()["projects"]):
        card(i, p, d["bugbouncer_stars"] if p["id"] == "bugbouncer" else None)


if __name__ == "__main__":
    build()
