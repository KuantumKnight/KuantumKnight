"""
ops.svg — the log.

the last few commits, set as a plain log: date, repo, message. the newest
entry carries the frame's one red mark. rows fade in top to bottom.
"""

from lib import (INK, SILVER, SILVER_DIM, ASH, BLOOD, MONO, esc, font_css,
                 film_defs, film_overlay, write_svg, collect, reveal, panel_head)

W, H = 430, 300


def trunc(s, n):
    s = s or ""
    return s if len(s) <= n else s[:n - 1] + "…"


def build():
    d = collect()
    events = d["events"][:6]
    if not events:
        events = [{"name": "KuantumKnight", "date": d["generated_date"],
                   "desc": "the readme"}]

    rows = []
    for i, e in enumerate(events):
        y = 76 + i * 34
        mmdd = e["date"][5:].replace("-", ".") if e.get("date") else "--.--"
        mark = (f'<rect x="24" y="{y - 7}" width="5" height="5" fill="{BLOOD}"/>'
                if i == 0 else "")
        body = (f'{mark}<text y="{y}" font-family="{MONO}" font-size="11.5">'
                f'<tspan x="38" fill="{ASH}">{esc(mmdd)}</tspan>'
                f'<tspan x="84" fill="{SILVER}">{esc(trunc(e["name"], 36))}</tspan></text>'
                f'<text x="84" y="{y + 15}" font-family="{MONO}" font-size="10.5" '
                f'fill="{SILVER_DIM}">{esc(trunc(e.get("desc") or e.get("lang"), 50))}</text>')
        rows.append(reveal(0.3 + i * 0.2, body, dur=0.9))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="recent pushes">
  <defs>{film_defs(W, H, seed=37)}</defs>
  {font_css()}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  {panel_head(W, "log", "recent pushes")}
  {"".join(rows)}
  <text x="24" y="{H - 20}" font-family="{MONO}" font-size="10" fill="{ASH}">checked {esc(d['generated'])}</text>
  {film_overlay(W, H, vignette=False)}
</svg>
'''
    write_svg("assets/ops.svg", svg)


if __name__ == "__main__":
    build()
