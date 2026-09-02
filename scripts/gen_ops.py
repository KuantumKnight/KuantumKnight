"""
ops.svg — recent activity feed.

an auto-updating `tail -f` of recent pushes/repos, in-theme. proves you're active
without you ever touching it.
"""

from pathlib import Path

from lib import (BG, PANEL, BORDER, GREEN, CYAN, WHITE, GREY,
                 RED, AMBER, LIME, MONO, esc, write_svg, collect)

W, H = 430, 300


def trunc(s, n):
    s = s or ""
    return s if len(s) <= n else s[:n - 1] + "…"


def build():
    d = collect()
    events = d["events"][:7]
    if not events and Path("assets/ops.svg").exists():
        print("[stale] keeping assets/ops.svg — activity feed unavailable")
        return
    if not events:
        events = [{"kind": "repo", "name": "KuantumKnight",
                   "date": d["generated_date"], "desc": "data unavailable",
                   "stars": None, "lang": ""}]

    rows, y = [], 60
    for e in events:
        mmdd = e["date"][5:] if e.get("date") else "--"
        name = trunc(e["name"], 22)
        meta = e.get("desc") or e.get("lang") or ""
        meta = trunc(meta, 30)
        star = f'  {e["stars"]}★' if e.get("stars") else ""
        kind = e.get("kind", "repo")
        rows.append(
            f'<g class="event-row" style="animation-delay:{len(rows)*.18:.2f}s">'
            f'<text x="20" y="{y}" font-size="13" font-family="{MONO}">'
            f'<tspan fill="{GREY}">[{esc(mmdd)}] </tspan>'
            f'<tspan fill="{GREEN}">{esc(kind)} </tspan>'
            f'<tspan fill="{WHITE}">{esc(name)}</tspan>'
            f'<tspan fill="{CYAN}">{esc(star)}</tspan>'
            f'</text>'
            f'<text x="78" y="{y+15}" font-size="11" fill="{GREY}" font-family="{MONO}">{esc(meta)}</text>'
            f'</g>'
        )
        y += 31

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="recent activity feed">
  <defs>
    <linearGradient id="sweep" x1="0" x2="1"><stop stop-color="{RED}" stop-opacity="0"/><stop offset=".5" stop-color="{RED}" stop-opacity=".13"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></linearGradient>
    <clipPath id="frame"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="8"/></clipPath>
    <style><![CDATA[
      .event-row {{ animation: event 4.2s ease-in-out infinite; }}
      .sweep {{ animation: sweep 6.8s linear infinite; }}
      .lamp {{ animation: lamp 1.7s steps(2,end) infinite; }}
      @keyframes event {{ 0%,100%{{opacity:.66;transform:translateX(0)}} 45%{{opacity:1;transform:translateX(3px)}} }}
      @keyframes sweep {{ from{{transform:translateX(-160px)}} to{{transform:translateX(590px)}} }}
      @keyframes lamp {{ 0%,100%{{opacity:1}} 50%{{opacity:.16}} }}
      @media (prefers-reduced-motion: reduce) {{ .event-row,.sweep,.lamp {{ animation:none!important; }} .sweep {{ display:none; }} }}
    ]]></style>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="1" y="1" width="{W-2}" height="34" rx="10" fill="{PANEL}"/>
  <rect x="1" y="24" width="{W-2}" height="11" fill="{PANEL}"/>
  <line x1="1" y1="35" x2="{W-1}" y2="35" stroke="{BORDER}" stroke-width="1.5"/>
  <circle class="lamp" cx="22" cy="18" r="5" fill="{RED}" opacity="0.85"/>
  <circle cx="40" cy="18" r="5" fill="{AMBER}" opacity="0.85"/>
  <circle cx="58" cy="18" r="5" fill="{LIME}" opacity="0.85"/>
  <text x="{W-16}" y="22" text-anchor="end" font-size="11" letter-spacing=".5" fill="{GREY}" font-family="{MONO}">OPS // TAIL ACTIVITY.LOG</text>

  {''.join(rows)}

  <g>
    <circle class="lamp" cx="26" cy="{H-18}" r="4" fill="{GREEN}"/>
    <text x="38" y="{H-14}" font-size="11" fill="{GREY}" font-family="{MONO}">live · rebuilt {esc(d['generated_date'])}</text>
  </g>
  <g clip-path="url(#frame)"><rect class="sweep" x="-160" y="0" width="110" height="{H}" fill="url(#sweep)" transform="skewX(-18)"/></g>
</svg>
'''
    write_svg("assets/ops.svg", svg)


if __name__ == "__main__":
    build()
