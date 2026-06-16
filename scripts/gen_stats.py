"""
stats.svg — the live metrics console.

a hand-built terminal readout of real numbers (stars, repos, followers, language
mix), pulled live by the pipeline. deliberately NOT the github-readme-stats card.
"""

from lib import (BG, PANEL, BORDER, GRID, GREEN, CYAN, WHITE, GREY,
                 RED, AMBER, LIME, MONO, esc, write_svg, collect)

W, H = 430, 300


def kpi(x, value, label):
    return (f'<text x="{x}" y="86" text-anchor="middle" font-size="30" '
            f'font-weight="700" fill="{GREEN}" font-family="{MONO}">{esc(value)}</text>'
            f'<text x="{x}" y="104" text-anchor="middle" font-size="11" '
            f'fill="{GREY}" font-family="{MONO}">{esc(label)}</text>')


def bar(y, name, pct):
    tx, tw = 132, 220                       # track x / width
    fw = max(4, int(tw * pct / 100))
    return (
        f'<text x="20" y="{y+12}" font-size="13" fill="{WHITE}" font-family="{MONO}">{esc(name)}</text>'
        f'<rect x="{tx}" y="{y}" width="{tw}" height="14" rx="3" fill="{GRID}"/>'
        f'<rect x="{tx}" y="{y}" width="{fw}" height="14" rx="3" fill="{GREEN}"/>'
        f'<text x="{tx+tw+8}" y="{y+12}" font-size="12" fill="{CYAN}" font-family="{MONO}">{pct}%</text>'
    )


# keep labels short enough to never crash into the bar track
ALIASES = {"jupyter notebook": "jupyter", "objective-c": "objc",
           "dockerfile": "docker"}


def label(name):
    n = ALIASES.get(name.lower(), name.lower())
    return n[:12]


def build():
    d = collect()
    bars, y = [], 158
    for name, pct in d["langs"][:5]:
        bars.append(bar(y, label(name), pct))
        y += 23

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="live stats: {d['stars']} stars, {d['repos']} repos">
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="1" y="1" width="{W-2}" height="34" rx="10" fill="{PANEL}"/>
  <rect x="1" y="24" width="{W-2}" height="11" fill="{PANEL}"/>
  <line x1="1" y1="35" x2="{W-1}" y2="35" stroke="{BORDER}" stroke-width="1.5"/>
  <circle cx="22" cy="18" r="5" fill="{RED}" opacity="0.85"/>
  <circle cx="40" cy="18" r="5" fill="{AMBER}" opacity="0.85"/>
  <circle cx="58" cy="18" r="5" fill="{LIME}" opacity="0.85"/>
  <text x="{W-16}" y="22" text-anchor="end" font-size="12" fill="{GREY}" font-family="{MONO}">~/stats $ ./metrics --live</text>

  {kpi(78, str(d['stars'])+'★', 'stars')}
  {kpi(215, str(d['repos']), 'repos')}
  {kpi(352, str(d['followers']), 'followers')}

  <line x1="20" y1="124" x2="{W-20}" y2="124" stroke="{BORDER}" stroke-width="1"/>
  <text x="20" y="146" font-size="12" fill="{GREY}" font-family="{MONO}">// language distribution</text>
  {''.join(bars)}

  <text x="20" y="{H-14}" font-size="11" fill="{GREY}" font-family="{MONO}">last sync · {esc(d['generated'])}</text>
</svg>
'''
    write_svg("assets/stats.svg", svg)


if __name__ == "__main__":
    build()
