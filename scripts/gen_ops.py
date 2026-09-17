"""
ops.svg — the scope.

recent pushes as blips on a radar. distance from the centre is how long ago
(closer is newer, out to four weeks); bearings step by the golden angle in
order of recency, so blips spread evenly around the scope. a silver sweep turns with a
fading trail, and each blip flares as the sweep crosses it. the newest blip
is the frame's one red mark.
"""

import math
from datetime import date

from lib import (INK, HAIRLINE, SILVER, SILVER_DIM, ASH, BLOOD, MONO, esc,
                 font_css, film_defs, film_overlay, write_svg, collect, panel_head)

W, H = 430, 300
CX, CY, R = 215, 168, 92
R0 = 16                   # radius for "today", so blips clear the centre
SPAN = 28                 # days at the outer ring
TURN = 6                  # seconds per sweep


def trunc(s, n):
    s = s or ""
    return s if len(s) <= n else s[:n - 1] + "…"


def radius(days):
    # square root spreads the recent days, where most pushes land
    return R0 + math.sqrt(min(max(days, 0), SPAN) / SPAN) * (R - R0)


def polar(r, deg):
    a = math.radians(deg)
    return CX + r * math.sin(a), CY - r * math.cos(a)


def scope():
    rings = "".join(
        f'<circle cx="{CX}" cy="{CY}" r="{radius(d):.1f}" fill="none" stroke="{HAIRLINE}" stroke-width="1"/>'
        for d in (14, 28))
    rings += (f'<circle cx="{CX}" cy="{CY}" r="{R0}" fill="none" stroke="{HAIRLINE}" stroke-dasharray="2 3"/>'
              f'<line x1="{CX - R - 8}" y1="{CY}" x2="{CX + R + 8}" y2="{CY}" stroke="{HAIRLINE}"/>'
              f'<line x1="{CX}" y1="{CY - R - 8}" x2="{CX}" y2="{CY + R + 8}" stroke="{HAIRLINE}"/>')
    caps = "".join(
        f'<text x="{CX + 4}" y="{CY - radius(d) - 3:.1f}" font-family="{MONO}" '
        f'font-size="8" fill="{ASH}">{t}</text>'
        for d, t in ((14, "2w"), (28, "4w")))
    ticks = "".join(
        f'<line x1="{polar(R, a)[0]:.1f}" y1="{polar(R, a)[1]:.1f}" '
        f'x2="{polar(R + 4, a)[0]:.1f}" y2="{polar(R + 4, a)[1]:.1f}" stroke="{ASH}" stroke-width="0.8"/>'
        for a in range(0, 360, 30))
    return rings + caps + ticks


def sweep():
    trail = 50
    x0, y0 = polar(R, -trail)
    wedge = (f'M{CX},{CY} L{x0:.1f},{y0:.1f} A{R},{R} 0 0,1 {CX},{CY - R} Z')
    return (f'<g><animateTransform attributeName="transform" type="rotate" '
            f'from="0 {CX} {CY}" to="360 {CX} {CY}" dur="{TURN}s" repeatCount="indefinite"/>'
            f'<path d="{wedge}" fill="url(#trail)"/>'
            f'<line x1="{CX}" y1="{CY}" x2="{CX}" y2="{CY - R}" stroke="{SILVER}" stroke-width="1.1" opacity="0.85"/></g>')


def blips(events, today):
    seen, picked = set(), []
    for e in events:
        if e["name"] in seen or not e.get("date"):
            continue
        seen.add(e["name"])
        picked.append(e)
        if len(picked) == 6:
            break

    dots, labels = [], []
    for i, e in enumerate(picked):
        try:
            days = (today - date.fromisoformat(e["date"])).days
        except ValueError:
            continue
        if days > SPAN:
            continue
        deg = (35 + i * 137.5) % 360        # golden angle: even spread by rank
        x, y = polar(radius(days), deg)
        col = BLOOD if i == 0 else SILVER
        begin = deg / 360 * TURN
        dots.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{col}" opacity="0.4">'
            f'<animate attributeName="opacity" values="1;0.4;0.4" keyTimes="0;0.35;1" '
            f'dur="{TURN}s" begin="{begin:.2f}s" repeatCount="indefinite"/></circle>')
        labels.append([x, y, i, e["name"]])

    # labels sit beside their blip, on the outer side; nudge apart vertically
    # so neighbours on the same side never overprint.
    out = dots
    for right in (True, False):
        side = sorted((l for l in labels if (l[0] >= CX) == right), key=lambda l: l[1])
        last = -1e9
        for l in side:
            ly = max(l[1] + 3, last + 11)
            last = ly
            x, _, i, name = l
            out.append(
                f'<text x="{x + (7 if right else -7):.1f}" y="{ly:.1f}" '
                f'text-anchor="{"start" if right else "end"}" font-family="{MONO}" '
                f'font-size="9" fill="{SILVER if i == 0 else SILVER_DIM}">{esc(trunc(name, 18))}</text>')
    return "".join(out), len(labels)


def build():
    d = collect()
    try:
        today = date.fromisoformat(d["generated_date"])
    except ValueError:
        today = date.today()
    dots, n = blips(d["events"], today)
    note = f"{n} repos in range" if n else "no pushes in range"

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="radar of recent pushes: {note}">
  <defs>{film_defs(W, H, seed=37)}
    <linearGradient id="trail" x1="1" x2="0" y1="0" y2="0">
      <stop offset="0" stop-color="{SILVER}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{SILVER}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  {font_css()}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  {panel_head(W, "log", "recent pushes")}
  {scope()}
  {sweep()}
  {dots}
  <text x="24" y="{H - 16}" font-family="{MONO}" font-size="10" fill="{ASH}">checked {esc(d['generated'])} · {note}</text>
  {film_overlay(W, H, vignette=False)}
</svg>
'''
    write_svg("assets/ops.svg", svg)


if __name__ == "__main__":
    build()
