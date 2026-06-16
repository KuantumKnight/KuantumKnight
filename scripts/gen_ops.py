"""
ops.svg — recent activity feed.

an auto-updating `tail -f` of recent pushes/repos, in-theme. proves you're active
without you ever touching it.
"""

from lib import (BG, PANEL, BORDER, GREEN, CYAN, WHITE, GREY,
                 RED, AMBER, LIME, MONO, esc, write_svg, collect)

W, H = 430, 300


def trunc(s, n):
    s = s or ""
    return s if len(s) <= n else s[:n - 1] + "…"


def build():
    d = collect()
    events = d["events"][:7]
    if not events:
        events = [{"name": "KuantumKnight", "date": d["generated_date"],
                   "desc": "the readme", "stars": 1, "lang": ""}]

    rows, y = [], 60
    for e in events:
        mmdd = e["date"][5:] if e.get("date") else "--"
        name = trunc(e["name"], 22)
        meta = e.get("desc") or e.get("lang") or ""
        meta = trunc(meta, 30)
        star = f'  {e["stars"]}★' if e.get("stars") else ""
        rows.append(
            f'<text x="20" y="{y}" font-size="13" font-family="{MONO}">'
            f'<tspan fill="{GREY}">[{esc(mmdd)}] </tspan>'
            f'<tspan fill="{GREEN}">push </tspan>'
            f'<tspan fill="{WHITE}">{esc(name)}</tspan>'
            f'<tspan fill="{CYAN}">{esc(star)}</tspan>'
            f'</text>'
            f'<text x="78" y="{y+15}" font-size="11" fill="{GREY}" font-family="{MONO}">{esc(meta)}</text>'
        )
        y += 31

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="recent activity feed">
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="1" y="1" width="{W-2}" height="34" rx="10" fill="{PANEL}"/>
  <rect x="1" y="24" width="{W-2}" height="11" fill="{PANEL}"/>
  <line x1="1" y1="35" x2="{W-1}" y2="35" stroke="{BORDER}" stroke-width="1.5"/>
  <circle cx="22" cy="18" r="5" fill="{RED}" opacity="0.85"/>
  <circle cx="40" cy="18" r="5" fill="{AMBER}" opacity="0.85"/>
  <circle cx="58" cy="18" r="5" fill="{LIME}" opacity="0.85"/>
  <text x="{W-16}" y="22" text-anchor="end" font-size="12" fill="{GREY}" font-family="{MONO}">~/ops $ tail activity.log</text>

  {''.join(rows)}

  <g>
    <circle cx="26" cy="{H-18}" r="4" fill="{GREEN}">
      <animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite"/>
    </circle>
    <text x="38" y="{H-14}" font-size="11" fill="{GREY}" font-family="{MONO}">live · rebuilt {esc(d['generated_date'])}</text>
  </g>
</svg>
'''
    write_svg("assets/ops.svg", svg)


if __name__ == "__main__":
    build()
