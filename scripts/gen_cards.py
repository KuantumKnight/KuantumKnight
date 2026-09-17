"""
card_*.svg — one case file per featured project.

a thin letterboxed still: a large dim serif numeral, the name, a one-line
brief, a sentence of detail, and the stack set as plain text. on the right,
a small hairline mark drawn for that project (profile.json "art"). copy comes
from profile.json. each card is wrapped in a link in the README, so the whole
frame is clickable.
"""

import math

from lib import (INK, HAIRLINE, SILVER, SILVER_DIM, ASH, BLOOD, SERIF, MONO,
                 esc, font_css, film_defs, film_overlay, write_svg, collect,
                 profile, reveal)

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


# ----------------------------------------------------------- marks ----
# each mark lives in the right-hand box, x 690..830, y 40..200.

def hash_chain(_):
    """lotusmcp: four linked blocks of an append-only log, lit left to right."""
    x0, y, bw, bh, gap = 692, 96, 26, 20, 10
    out = [f'<text x="{x0}" y="{y - 14}" font-family="{MONO}" font-size="8" '
           f'letter-spacing="2" fill="{ASH}">APPEND-ONLY</text>']
    for i in range(4):
        x = x0 + i * (bw + gap)
        if i:
            out.append(f'<line x1="{x - gap}" y1="{y + bh / 2}" x2="{x}" y2="{y + bh / 2}" '
                       f'stroke="{SILVER_DIM}" stroke-width="0.8"/>')
        block = (f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" fill="none" '
                 f'stroke="{SILVER}" stroke-width="0.9"/>'
                 f'<line x1="{x + 5}" y1="{y + 7}" x2="{x + bw - 5}" y2="{y + 7}" stroke="{SILVER_DIM}" stroke-width="0.6"/>'
                 f'<line x1="{x + 5}" y1="{y + 12}" x2="{x + bw - 9}" y2="{y + 12}" stroke="{SILVER_DIM}" stroke-width="0.6"/>'
                 f'<text x="{x + bw / 2}" y="{y + bh + 14}" text-anchor="middle" '
                 f'font-family="{MONO}" font-size="8" fill="{ASH}">e{i + 1}</text>')
        out.append(reveal(0.9 + i * 0.35, block, dur=0.6))
    return f'<g opacity="0.8">{"".join(out)}</g>'


def localhost(_):
    """lily: a small machine, running locally — the breathing dot is the loop."""
    x, y, w, h = 712, 64, 96, 60
    return (f'<g opacity="0.8">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="none" '
            f'stroke="{SILVER}" stroke-width="0.9"/>'
            f'<line x1="{x + w / 2}" y1="{y + h}" x2="{x + w / 2}" y2="{y + h + 12}" stroke="{SILVER_DIM}" stroke-width="0.9"/>'
            f'<line x1="{x + w / 2 - 18}" y1="{y + h + 12}" x2="{x + w / 2 + 18}" y2="{y + h + 12}" stroke="{SILVER_DIM}" stroke-width="0.9"/>'
            f'<text x="{x + 10}" y="{y + 20}" font-family="{MONO}" font-size="8.5" fill="{SILVER_DIM}">lily &gt;</text>'
            f'<circle cx="{x + 47}" cy="{y + 17}" r="2.2" fill="{SILVER}">'
            f'<animate attributeName="opacity" values="1;0.25;1" dur="3.2s" repeatCount="indefinite"/></circle>'
            f'<line x1="{x + 10}" y1="{y + 32}" x2="{x + 70}" y2="{y + 32}" stroke="{HAIRLINE}" stroke-width="2"/>'
            f'<line x1="{x + 10}" y1="{y + 42}" x2="{x + 54}" y2="{y + 42}" stroke="{HAIRLINE}" stroke-width="2"/>'
            f'<text x="{x + w / 2}" y="{y + h + 32}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="9" letter-spacing="1" fill="{ASH}">127.0.0.1</text></g>')


def _star(cx, cy, r):
    pts = []
    for k in range(10):
        rad = r if k % 2 == 0 else r * 0.42
        a = math.pi / 2 + k * math.pi / 5
        pts.append(f"{cx + rad * math.cos(a):.1f},{cy - rad * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"


def star_seal(stars):
    """bugbouncer: a slowly turning seal with the star count counting up inside."""
    cx, cy, r = 762, 104, 50
    ring_r = r - 7
    ring = (f'<path id="sealpath" d="M{cx - ring_r},{cy} a{ring_r},{ring_r} 0 1,1 {2 * ring_r},0 '
            f'a{ring_r},{ring_r} 0 1,1 -{2 * ring_r},0" fill="none"/>')
    seal = (f'<g><animateTransform attributeName="transform" type="rotate" '
            f'from="0 {cx} {cy}" to="360 {cx} {cy}" dur="60s" repeatCount="indefinite"/>'
            f'<text font-family="{MONO}" font-size="7.5" letter-spacing="1.6" fill="{SILVER_DIM}">'
            f'<textPath href="#sealpath">MOST STARRED · MOST STARRED · MOST STARRED ·</textPath></text></g>')
    circles = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{SILVER}" stroke-width="0.9"/>'
               f'<circle cx="{cx}" cy="{cy}" r="{r - 14}" fill="none" stroke="{SILVER_DIM}" stroke-width="0.6"/>')

    # count up 0 -> stars once; the last frame is visible by default so a
    # renderer that ignores animation still shows the real number.
    n = 12
    t0, dur = 1.0, 1.4
    frames = []
    for k in range(1, n + 1):
        val = round(stars * k / n)
        on = t0 + dur * (k - 1) / n
        off = t0 + dur * k / n
        last = k == n
        anim = (f'<set attributeName="visibility" to="hidden" begin="0s"/>'
                f'<set attributeName="visibility" to="visible" begin="{on:.3f}s"/>')
        if not last:
            anim += f'<set attributeName="visibility" to="hidden" begin="{off:.3f}s"/>'
        frames.append(
            f'<text x="{cx}" y="{cy + 13}" text-anchor="middle" font-family="{SERIF}" '
            f'font-size="36" fill="{SILVER}" visibility="{"visible" if last else "hidden"}">'
            f'{anim}{val}</text>')

    caption = (f'<text x="{cx}" y="{cy + r + 20}" text-anchor="middle" font-family="{MONO}" '
               f'font-size="8.5" letter-spacing="2" fill="{ASH}">STARS ON GITHUB</text>')
    return (f'<defs>{ring}</defs>'
            + reveal(0.6, circles + seal + caption
                     + f'<path d="{_star(cx, cy - 22, 5)}" fill="{BLOOD}"/>', dur=1.2)
            + "".join(frames))


MARKS = {"hash_chain": hash_chain, "localhost": localhost, "star_seal": star_seal}


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
            f'letter-spacing="3.5" fill="{ASH}">CASE FILE {num}</text>'
            f'<text x="{W - 36}" y="50" text-anchor="end" font-family="{MONO}" '
            f'font-size="10.5" fill="{ASH}">github.com/{esc(p["repo"])}</text>'
            f'<text x="{TX - 2}" y="94" font-family="{SERIF}" font-size="40" '
            f'fill="{SILVER}">{esc(p["name"])}</text>')
    body = (f'<text x="{TX}" y="128" font-family="{SERIF}" font-size="20" '
            f'fill="{SILVER}">{esc(p["brief"])}</text>{detail}')
    foot = (f'<text x="{TX}" y="{H - 22}" font-family="{MONO}" font-size="11" '
            f'letter-spacing="0.5" fill="{ASH}">{esc("  ·  ".join(tags))}</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(p["name"])}: {esc(p["brief"])}">
  <defs>{film_defs(W, H, seed=20 + idx)}</defs>
  {font_css(serif=True)}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  {MARKS[p["art"]](stars)}
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
