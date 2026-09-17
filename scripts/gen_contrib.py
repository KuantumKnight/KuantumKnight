"""
contrib.svg — the year, scanned.

a github-style calendar (months across, mon/wed/fri down the side). active
days rest at a faint shade; a silver scan line sweeps left to right and each
day flares to its true intensity as the line passes, then settles back.
loops. today is the one red cell, and never moves.
"""

from datetime import datetime, timedelta
from lib import (INK, SILVER, ASH, BLOOD, RAMP, MONO, font_css, film_defs,
                 film_overlay, write_svg, collect, panel_head)

CELL, GAP = 11, 3
STRIDE = CELL + GAP
GX, GY = 52, 92          # grid origin (room for header, weekday + month labels)
COLS = 53
P = 8.0                  # full scan cycle (s)
SWEEP = 0.85             # fraction of the cycle the line takes to cross
DECAY = 0.46             # fraction of the cycle a flared day takes to settle
REST = 0.35              # resting opacity of an active day between passes
W = GX + COLS * STRIDE + 30
H = 236


def _grid(cal):
    """-> (cells[(col,row,level)], month_marks[(col,label)])"""
    dates, real = [], True
    for c in cal:
        try:
            dates.append(datetime.strptime(c["date"], "%Y-%m-%d"))
        except (ValueError, KeyError):
            real = False
            break
    cells, months = [], []
    if real and dates:
        mn = min(dates)
        first_sun = mn - timedelta(days=(mn.weekday() + 1) % 7)
        maxcol = (max(dates) - first_sun).days // 7
        cutoff = max(0, maxcol - (COLS - 1))
        for c, dt in zip(cal, dates):
            col = (dt - first_sun).days // 7 - cutoff
            if col < 0:
                continue
            row = (dt.weekday() + 1) % 7
            cells.append((col, row, c.get("level", 0)))
        # month marks from chronologically-sorted dates, one per (year, month)
        seen = set()
        for dt in sorted(dates):
            col = (dt - first_sun).days // 7 - cutoff
            if col < 0 or col >= COLS - 1:
                continue
            key = (dt.year, dt.month)
            if key not in seen:
                seen.add(key)
                months.append((col, dt.strftime("%b").lower()))
    else:
        for i, c in enumerate(cal):
            cells.append((i // 7, i % 7, c.get("level", 0)))
    return cells, months


def build():
    d = collect()
    cells, months = _grid(d["calendar"])
    maxj = max((c[0] for c in cells), default=COLS - 1) or 1
    today = max(cells, key=lambda c: (c[0], c[1])) if cells else None

    base, dev = [], []
    for cell in cells:
        col, row, lvl = cell
        x, y = GX + col * STRIDE, GY + row * STRIDE
        base.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                    f'rx="1.5" fill="{RAMP[0]}"/>')
        if cell == today:
            dev.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                       f'rx="1.5" fill="{BLOOD}"/>')
        elif lvl:
            begin = round((col / maxj) * SWEEP * P, 3)
            dev.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="1.5" '
                f'fill="{RAMP[min(lvl, 4)]}" opacity="{REST}"><animate attributeName="opacity" '
                f'values="{REST};1;{REST};{REST}" keyTimes="0;0.03;{DECAY};1" dur="{P}s" '
                f'begin="{begin}s" repeatCount="indefinite"/></rect>')

    grid_w, grid_h = maxj * STRIDE + CELL, 7 * STRIDE - GAP
    beam = f'''<g clip-path="url(#gclip)">
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="0 0;{maxj * STRIDE} 0;{maxj * STRIDE} 0" keyTimes="0;{SWEEP};1" dur="{P}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{SWEEP};{SWEEP + 0.01};1" dur="{P}s" repeatCount="indefinite"/>
      <rect x="{GX - 22}" y="{GY - 4}" width="28" height="{grid_h + 8}" fill="url(#beam)"/>
      <line x1="{GX + CELL / 2:.1f}" y1="{GY - 4}" x2="{GX + CELL / 2:.1f}" y2="{GY + grid_h + 4}" stroke="{SILVER}" stroke-width="1" opacity="0.8"/>
    </g>
  </g>'''

    # a partial first month leaves two labels nearly on top of each other
    spaced = []
    for col, t in months:
        if spaced and col - spaced[-1][0] < 3:
            spaced.pop()
        spaced.append((col, t))
    months = spaced

    label = f'font-size="9.5" fill="{ASH}" font-family="{MONO}"'
    wlabels = "".join(
        f'<text x="{GX - 10}" y="{GY + r * STRIDE + CELL - 1}" text-anchor="end" {label}>{t}</text>'
        for r, t in ((1, "mon"), (3, "wed"), (5, "fri")))
    mlabels = "".join(
        f'<text x="{GX + col * STRIDE}" y="{GY - 10}" {label}>{t}</text>'
        for col, t in months)

    lx = W - 190
    legend = (f'<text x="{lx}" y="{H - 20}" {label}>less</text>'
              + "".join(f'<rect x="{lx + 32 + i * 15}" y="{H - 29}" width="11" height="11" '
                        f'rx="1.5" fill="{RAMP[i + 1]}"/>' for i in range(4))
              + f'<text x="{lx + 32 + 4 * 15 + 4}" y="{H - 20}" {label}>more</text>'
              + f'<rect x="24" y="{H - 29}" width="11" height="11" rx="1.5" fill="{BLOOD}"/>'
              + f'<text x="42" y="{H - 20}" {label}>today</text>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="contribution calendar: {d['contrib_total']} active days in the past year">
  <defs>{film_defs(W, H, seed=41)}
    <linearGradient id="beam" x1="0" x2="1">
      <stop offset="0" stop-color="{SILVER}" stop-opacity="0"/>
      <stop offset="1" stop-color="{SILVER}" stop-opacity="0.16"/>
    </linearGradient>
    <clipPath id="gclip"><rect x="{GX - 4}" y="{GY - 4}" width="{grid_w + 8}" height="{grid_h + 8}"/></clipPath>
  </defs>
  {font_css()}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  {panel_head(W, "the year", f"{d['contrib_total']} active days")}
  {mlabels}
  {wlabels}
  <g>{"".join(base)}</g>
  <g>{"".join(dev)}</g>
  {beam}
  {legend}
  {film_overlay(W, H, vignette=False)}
</svg>
'''
    write_svg("assets/contrib.svg", svg)


if __name__ == "__main__":
    build()
