"""
card_*.svg — one case file per featured project.

a thin letterboxed still: a large dim serif numeral, the name, a one-line
brief, a sentence of detail, and the stack set as plain text. the project's
icon sits faintly on the right. copy comes from profile.json. each card is
wrapped in a link in the README, so the whole frame is clickable.
"""

from lib import (INK, SILVER, SILVER_DIM, ASH, SERIF, MONO, esc, font_css,
                 film_defs, film_overlay, write_svg, collect, profile, reveal)
from icons import CARD_ICONS

W, H = 860, 220
BAR = 10
TX = 190                     # text column


def wrap(text, n=84, maxlines=2):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if cur and len(cur) + len(w) + 1 > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    return lines[:maxlines]


def watermark(icon):
    """a baked Lucide line icon (24x24), large and faint, right side."""
    if icon not in CARD_ICONS:
        return ""
    return (f'<g opacity="0.08" transform="translate(700,52) scale(5)" '
            f'fill="none" stroke="{SILVER}" stroke-width="0.4" '
            f'stroke-linecap="round" stroke-linejoin="round">{CARD_ICONS[icon]}</g>')


def card(idx, p, stars=None):
    num = f"{idx + 1:02d}"
    tags = list(p["chips"])
    if stars:
        tags.insert(0, f"{stars} stars")
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
  {watermark(p.get("icon"))}
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
