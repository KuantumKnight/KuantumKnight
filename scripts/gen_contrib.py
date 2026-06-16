"""
contrib.svg — the OG contribution chart, scanned.

a rectangular github-style calendar (months across the top, Mon/Wed/Fri down
the side, 53x7 rounded cells). the grid sits EMPTY; a glowing vertical scan line
sweeps left->right and, as it passes each column, the days you contributed
reveal at their TRUE intensity shade — then phosphor-fade back to empty.
cinematic: scanlines, beam glow, HUD ticks. SMIL-driven, no js.
"""

from datetime import datetime, timedelta
from lib import (BG, PANEL, BORDER, GRID, GREEN, GREY, RED, AMBER, LIME, RAMP,
                 MONO, write_svg, collect)

CELL, GAP = 11, 3
STRIDE = CELL + GAP
GX, GY = 44, 60          # grid origin (room for weekday + month labels)
COLS = 53
P = 8.0                  # full scan cycle (s)
SWEEP = 0.85             # fraction of cycle the beam takes to cross
DECAY = 0.46             # fraction of cycle a revealed cell takes to fade
W = GX + COLS * STRIDE + 20
H = 208


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
    beam_w = maxj * STRIDE

    base, reveal = [], []
    for col, row, lvl in cells:
        x = GX + col * STRIDE
        y = GY + row * STRIDE
        base.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                    f'rx="2.5" fill="{GRID}"/>')
        if lvl >= 1:                                   # reveal to true shade
            begin = round((col / maxj) * SWEEP * P, 3)
            reveal.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" '
                f'fill="{RAMP[min(lvl,4)]}" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;0;0" '
                f'keyTimes="0;0.03;{DECAY};1" dur="{P}s" begin="{begin}s" '
                f'repeatCount="indefinite"/></rect>')

    # weekday labels (Mon / Wed / Fri, like the og chart)
    wlabels = "".join(
        f'<text x="{GX-8}" y="{GY+r*STRIDE+CELL-1}" text-anchor="end" '
        f'font-size="9" fill="{GREY}" font-family="{MONO}">{lbl}</text>'
        for r, lbl in ((1, "mon"), (3, "wed"), (5, "fri")))
    mlabels = "".join(
        f'<text x="{GX+col*STRIDE}" y="{GY-8}" font-size="9" fill="{GREY}" '
        f'font-family="{MONO}">{lbl}</text>' for col, lbl in months)

    # legend
    lx = W - 200
    legend = (f'<text x="{lx}" y="{H-14}" font-size="10" fill="{GREY}" font-family="{MONO}">less</text>'
              + "".join(f'<rect x="{lx+30+i*15}" y="{H-23}" width="11" height="11" rx="2" fill="{RAMP[i+1] if i<4 else RAMP[4]}"/>' for i in range(4))
              + f'<text x="{lx+30+4*15+4}" y="{H-14}" font-size="10" fill="{GREY}" font-family="{MONO}">more</text>')

    grid_h = 7 * STRIDE

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="contribution chart scanned by a sweep line: {d['contrib_total']} active days">
  <defs>
    <linearGradient id="beam" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{GREEN}" stop-opacity="0.85"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="crt" width="3" height="3" patternUnits="userSpaceOnUse">
      <rect width="3" height="1" fill="{GREEN}" opacity="0.05"/>
    </pattern>
    <clipPath id="gclip"><rect x="{GX-4}" y="{GY-4}" width="{beam_w+CELL+8}" height="{grid_h+4}"/></clipPath>
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

  {mlabels}
  {wlabels}

  <!-- empty base grid -->
  <g>{''.join(base)}</g>

  <!-- per-cell shade reveal + the sweeping beam, clipped to the grid -->
  <g clip-path="url(#gclip)">
    {''.join(reveal)}
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="0 0;{beam_w} 0;{beam_w} 0" keyTimes="0;{SWEEP};1" dur="{P}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.9;0.9;0;0" keyTimes="0;{SWEEP};{SWEEP+0.01};1" dur="{P}s" repeatCount="indefinite"/>
      <rect x="{GX-9}" y="{GY-4}" width="20" height="{grid_h+2}" fill="url(#beam)"/>
      <line x1="{GX+1}" y1="{GY-4}" x2="{GX+1}" y2="{GY+grid_h-2}" stroke="#d8fff0" stroke-width="1.4" opacity="0.9"/>
    </g>
  </g>

  <!-- scanlines + hud corner ticks -->
  <rect x="{GX-4}" y="{GY-4}" width="{beam_w+CELL+8}" height="{grid_h+4}" fill="url(#crt)"/>
  <path d="M{GX-10},{GY+8} L{GX-10},{GY-6} L{GX+4},{GY-6}" fill="none" stroke="{GREEN}" stroke-opacity="0.5"/>
  <path d="M{GX+beam_w+CELL+10},{GY+grid_h-12} L{GX+beam_w+CELL+10},{GY+grid_h+2} L{GX+beam_w+CELL-4},{GY+grid_h+2}" fill="none" stroke="{GREEN}" stroke-opacity="0.5"/>

  {legend}
</svg>
'''
    write_svg("assets/contrib.svg", svg)


if __name__ == "__main__":
    build()
