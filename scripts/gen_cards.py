"""card_*.svg — three factual project posters in the punk-collage system."""

import base64
from pathlib import Path

from lib import (BG, BORDER, GREEN, WHITE, GREY, RED, PAPER, MONO, esc,
                 write_svg, profile)

W, H = 270, 354
ROOT = Path(__file__).resolve().parent.parent

THEMES = {
    "black": {"base": BG, "ink": WHITE, "accent": GREEN, "veil": "#050706"},
    "red": {"base": RED, "ink": PAPER, "accent": PAPER, "veil": "#8f1814"},
    "paper": {"base": PAPER, "ink": BG, "accent": RED, "veil": "#e7e1d3"},
}


def wrap(text, n=35, maxlines=2):
    words, lines, cur = text.split(), [], ""
    for word in words:
        nxt = (cur + " " + word).strip()
        if len(nxt) <= n:
            cur = nxt
        else:
            lines.append(cur)
            cur = word
        if len(lines) == maxlines:
            break
    if cur and len(lines) < maxlines:
        lines.append(cur)
    return lines[:maxlines]


def card(project, index):
    theme = THEMES[project["theme"]]
    ink, accent, base = theme["ink"], theme["accent"], theme["base"]
    title = project["name"].upper()
    brief = wrap(project["brief"])
    detail = wrap(project["detail"], 38, 2)
    chips = "  /  ".join(project["chips"]).upper()
    poster_path = ROOT / "assets" / project["poster"]
    poster_data = ("data:image/jpeg;base64,"
                   + base64.b64encode(poster_path.read_bytes()).decode("ascii"))
    text_lines = "".join(
        f'<text x="18" y="{286+i*17}" font-family="{MONO}" font-size="12" '
        f'fill="{ink}">{esc(line)}</text>' for i, line in enumerate(brief)
    )
    detail_lines = "".join(
        f'<text x="18" y="{321+i*14}" font-family="{MONO}" font-size="9.5" '
        f'fill="{ink}" opacity=".72">{esc(line)}</text>' for i, line in enumerate(detail)
    )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(project['name'])}: {esc(project['brief'])}">
  <defs>
    <filter id="grain{index}" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence baseFrequency=".8" numOctaves="2" seed="{17+index}" result="noise"/>
      <feColorMatrix in="noise" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 .08 0"/>
      <feBlend in="SourceGraphic" mode="multiply"/>
    </filter>
    <clipPath id="rip{index}">
      <path d="M8 8L256 3 266 26 261 84 268 139 262 205 268 259 259 348 14 351 6 326 10 264 3 204 9 145 4 82Z"/>
    </clipPath>
    <linearGradient id="fade{index}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{theme['veil']}" stop-opacity=".05"/>
      <stop offset=".72" stop-color="{theme['veil']}" stop-opacity=".16"/>
      <stop offset="1" stop-color="{theme['veil']}" stop-opacity=".98"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#rip{index})">
    <rect width="{W}" height="{H}" fill="{base}"/>
    <image href="{poster_data}" x="0" y="66" width="{W}" height="222"
           preserveAspectRatio="xMidYMid slice"/>
    <rect y="60" width="{W}" height="232" fill="url(#fade{index})"/>
    <rect width="{W}" height="76" fill="{base}" opacity=".96"/>
    <rect y="266" width="{W}" height="88" fill="{base}" opacity=".96"/>
    <rect width="{W}" height="{H}" filter="url(#grain{index})" opacity=".25"/>
  </g>

  <path d="M8 8L256 3 266 26 261 84 268 139 262 205 268 259 259 348 14 351 6 326 10 264 3 204 9 145 4 82Z"
        fill="none" stroke="{BORDER}" stroke-width="1.4"/>
  <path d="M18 12L92 7 95 24 21 29Z" fill="{PAPER}" opacity=".25"/>
  <text x="18" y="49" font-family="Impact,'Arial Narrow',sans-serif" font-size="30"
        letter-spacing=".8" fill="{ink}">{esc(title)}</text>
  <text x="250" y="26" text-anchor="end" font-family="{MONO}" font-size="10"
        fill="{accent}">0{index+1}</text>
  <text x="18" y="68" font-family="{MONO}" font-size="8.5" fill="{accent}">github.com/{esc(project['repo'])}</text>
  {text_lines}
  {detail_lines}
  <text x="18" y="348" font-family="{MONO}" font-size="8.5" fill="{accent}">{esc(chips)}</text>

  <path d="M244 322v16h-16" fill="none" stroke="{accent}" stroke-width="1.5"/>
  <circle cx="251" cy="105" r="3.5" fill="{accent}">
    <animate attributeName="opacity" values="1;.15;1" dur="{1.6+index*.3}s" repeatCount="indefinite"/>
  </circle>
</svg>
'''
    write_svg(f"assets/card_{project['id']}.svg", svg)


def build():
    for i, project in enumerate(profile()["projects"]):
        card(project, i)


if __name__ == "__main__":
    build()
