"""
contrib.svg — the year, developed.

a github-style calendar (months across, mon/wed/fri down the side). the grid
starts as an unexposed sheet; active days develop in column by column at
their true intensity, once, then hold. today is the one red cell.
"""

from datetime import datetime, timedelta
from lib import (INK, ASH, BLOOD, RAMP, MONO, font_css, film_defs,
                 film_overlay, write_svg, collect, panel_head)

CELL, GAP = 11, 3
STRIDE = CELL + GAP
GX, GY = 52, 92          # grid origin (room for header, weekday + month labels)
COLS = 53
DEVELOP = 2.6            # seconds for the exposure to cross the year
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
        fill = BLOOD if cell == today else (RAMP[min(lvl, 4)] if lvl else None)
        if fill:
            begin = round(0.4 + (col / maxj) * DEVELOP, 3)
            dev.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="1.5" '
                f'fill="{fill}" opacity="0"><animate attributeName="opacity" '
                f'from="0" to="1" dur="0.9s" begin="{begin}s" fill="freeze"/></rect>')

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
  <defs>{film_defs(W, H, seed=41)}</defs>
  {font_css()}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  {panel_head(W, "the year", f"{d['contrib_total']} active days")}
  {mlabels}
  {wlabels}
  <g>{"".join(base)}</g>
  <g>{"".join(dev)}</g>
  {legend}
  {film_overlay(W, H, vignette=False)}
</svg>
'''
    write_svg("assets/contrib.svg", svg)


if __name__ == "__main__":
    build()
