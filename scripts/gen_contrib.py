"""
contrib.svg — the contribution year as a radar-swept threat grid.

the deliberate replacement for the overused contribution snake. same data,
custom art: a green intensity grid with a scan beam sweeping across it forever.
"""

from datetime import datetime, timedelta
from lib import (BG, PANEL, BORDER, GREEN, GREY, RED, AMBER, LIME, RAMP,
                 MONO, esc, write_svg, collect)

W, H = 880, 184
CELL, GAP = 12, 3
GX, GY = 24, 56          # grid origin


def _positions(cal):
    """map each cell to (col,row); real dates -> true calendar, else sequential."""
    dates = []
    real = True
    for c in cal:
        try:
            dates.append(datetime.strptime(c["date"], "%Y-%m-%d"))
        except (ValueError, KeyError):
            real = False
            break
    out = []
    if real and dates:
        mn = min(dates)
        first_sun = mn - timedelta(days=(mn.weekday() + 1) % 7)
        for c, dt in zip(cal, dates):
            col = (dt - first_sun).days // 7
            row = (dt.weekday() + 1) % 7
            out.append((col, row, c.get("level", 0)))
    else:
        for i, c in enumerate(cal):
            out.append((i // 7, i % 7, c.get("level", 0)))
    return out


def build():
    d = collect()
    cells = _positions(d["calendar"])
    maxcol = max((c[0] for c in cells), default=52)
    # keep to the most recent 53 columns
    cutoff = max(0, maxcol - 52)

    rects = []
    for col, row, lvl in cells:
        if col < cutoff:
            continue
        x = GX + (col - cutoff) * (CELL + GAP)
        y = GY + row * (CELL + GAP)
        fill = RAMP[max(0, min(lvl, 4))]
        rects.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                     f'rx="2.5" fill="{fill}"/>')

    grid_w = 53 * (CELL + GAP)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="contribution radar: {d['contrib_total']} active days">
  <defs>
    <linearGradient id="beam2" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{GREEN}" stop-opacity="0.85"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="gridclip">
      <rect x="{GX-2}" y="{GY-2}" width="{grid_w+4}" height="{7*(CELL+GAP)+4}"/>
    </clipPath>
    <style>
      .sweep {{ animation:scan 6s linear infinite; }}
      @keyframes scan {{ from{{transform:translateX(-40px)}} to{{transform:translateX({grid_w+60}px)}} }}
    </style>
  </defs>

  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="1" y="1" width="{W-2}" height="34" rx="10" fill="{PANEL}"/>
  <rect x="1" y="24" width="{W-2}" height="11" fill="{PANEL}"/>
  <line x1="1" y1="35" x2="{W-1}" y2="35" stroke="{BORDER}" stroke-width="1.5"/>
  <circle cx="22" cy="18" r="5" fill="{RED}" opacity="0.85"/>
  <circle cx="40" cy="18" r="5" fill="{AMBER}" opacity="0.85"/>
  <circle cx="58" cy="18" r="5" fill="{LIME}" opacity="0.85"/>
  <text x="78" y="22" font-size="12" fill="{GREY}" font-family="{MONO}">~/contrib $ ./scan --year</text>
  <text x="{W-16}" y="22" text-anchor="end" font-size="12" fill="{GREY}" font-family="{MONO}">{d['contrib_total']} active days</text>

  <g>{''.join(rects)}</g>

  <!-- radar sweep, clipped to the grid -->
  <g clip-path="url(#gridclip)">
    <g class="sweep"><rect x="{GX}" y="{GY-2}" width="34" height="{7*(CELL+GAP)+4}" fill="url(#beam2)"/></g>
  </g>

  <text x="{GX}" y="{H-14}" font-size="11" fill="{GREY}" font-family="{MONO}">less</text>
  <rect x="{GX+34}" y="{H-24}" width="11" height="11" rx="2" fill="{RAMP[1]}"/>
  <rect x="{GX+49}" y="{H-24}" width="11" height="11" rx="2" fill="{RAMP[2]}"/>
  <rect x="{GX+64}" y="{H-24}" width="11" height="11" rx="2" fill="{RAMP[3]}"/>
  <rect x="{GX+79}" y="{H-24}" width="11" height="11" rx="2" fill="{RAMP[4]}"/>
  <text x="{GX+96}" y="{H-14}" font-size="11" fill="{GREY}" font-family="{MONO}">more</text>
</svg>
'''
    write_svg("assets/contrib.svg", svg)


if __name__ == "__main__":
    build()
