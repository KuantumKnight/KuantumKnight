"""card_*.svg — animated full-width project loadout rows."""

import base64
from pathlib import Path

from lib import (BG, BORDER, GREEN, WHITE, GREY, RED, PAPER, MONO, esc,
                 profile, write_svg)

W, H = 860, 190
ROOT = Path(__file__).resolve().parent.parent

THEMES = {
    "black": {
        "base": BG, "panel": "#0b0d0c", "ink": WHITE,
        "muted": GREY, "accent": GREEN, "veil": "#050706",
    },
    "red": {
        "base": "#220806", "panel": RED, "ink": PAPER,
        "muted": "#f1aaa4", "accent": RED, "veil": "#370907",
    },
    "paper": {
        "base": PAPER, "panel": "#d8d1c3", "ink": BG,
        "muted": "#55574f", "accent": RED, "veil": "#ddd6c8",
    },
}


def wrap(text, n=51, maxlines=2):
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
    base, panel = theme["base"], theme["panel"]
    ink, muted, accent = theme["ink"], theme["muted"], theme["accent"]
    title = project["name"].upper()
    brief = wrap(project["brief"], 49, 1)
    detail = wrap(project["detail"], 55, 2)
    chips = "  /  ".join(project["chips"]).upper()
    poster_path = ROOT / "assets" / project["poster"]
    poster_data = ("data:image/jpeg;base64,"
                   + base64.b64encode(poster_path.read_bytes()).decode("ascii"))
    brief_lines = "".join(
        f'<text x="105" y="{112+i*16}" font-family="{MONO}" font-size="12" '
        f'font-weight="700" fill="{ink}">{esc(line)}</text>'
        for i, line in enumerate(brief)
    )
    detail_lines = "".join(
        f'<text x="105" y="{135+i*14}" font-family="{MONO}" font-size="10" '
        f'fill="{muted}">{esc(line)}</text>'
        for i, line in enumerate(detail)
    )
    delay = index * .42

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(project['name'])}: {esc(project['brief'])}">
  <defs>
    <filter id="grain" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence baseFrequency=".74" numOctaves="2" seed="{19+index}" result="noise"/>
      <feColorMatrix in="noise" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 .1 0"/>
      <feBlend in="SourceGraphic" mode="multiply"/>
    </filter>
    <clipPath id="posterClip"><path d="M500 1H859V189H458Z"/></clipPath>
    <clipPath id="frameClip"><rect x="1" y="1" width="858" height="188"/></clipPath>
    <linearGradient id="posterVeil" x1="0" x2="1">
      <stop stop-color="{theme['veil']}" stop-opacity="1"/>
      <stop offset=".27" stop-color="{theme['veil']}" stop-opacity=".48"/>
      <stop offset="1" stop-color="{theme['veil']}" stop-opacity=".05"/>
    </linearGradient>
    <linearGradient id="sweep" x1="0" x2="1">
      <stop stop-color="{accent}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{accent}" stop-opacity=".28"/>
      <stop offset="1" stop-color="{accent}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="speed" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="skewX(-24)">
      <rect width="5" height="16" fill="{ink}" opacity=".035"/>
    </pattern>
    <style><![CDATA[
      .poster {{ animation: poster 8s ease-in-out infinite; transform-origin:680px 95px; }}
      .sweep {{ animation: sweep {5.5 + index * .5:.1f}s cubic-bezier(.15,.7,.2,1) infinite; animation-delay:{delay:.2f}s; }}
      .lamp {{ animation: lamp 1.8s steps(2,end) infinite; animation-delay:{delay:.2f}s; }}
      .chev {{ animation: chev 1.3s ease-in-out infinite; animation-delay:{delay:.2f}s; }}
      .meter {{ animation: meter 3.2s ease-in-out infinite; transform-origin:left center; }}
      @keyframes poster {{ 0%,100%{{transform:scale(1.02) translateX(0)}} 50%{{transform:scale(1.055) translateX(-5px)}} }}
      @keyframes sweep {{ 0%{{transform:translateX(-230px);opacity:0}} 12%{{opacity:1}} 72%{{transform:translateX(1080px);opacity:.9}} 73%,100%{{transform:translateX(1080px);opacity:0}} }}
      @keyframes lamp {{ 0%,100%{{opacity:1}} 50%{{opacity:.18}} }}
      @keyframes chev {{ 0%,100%{{transform:translateX(0)}} 50%{{transform:translateX(7px)}} }}
      @keyframes meter {{ 0%,100%{{transform:scaleX(.78)}} 50%{{transform:scaleX(1)}} }}
      @media (prefers-reduced-motion: reduce) {{ .poster,.sweep,.lamp,.chev,.meter {{ animation:none!important; }} .sweep {{ display:none; }} }}
    ]]></style>
  </defs>

  <rect x="1" y="1" width="858" height="188" fill="{base}" stroke="{BORDER}" stroke-width="2"/>
  <rect x="1" y="1" width="858" height="188" fill="url(#speed)"/>
  <path d="M1 1H88L64 189H1Z" fill="{panel}"/>
  <path d="M88 1H99L75 189H64Z" fill="{accent}"/>

  <g clip-path="url(#posterClip)">
    <image class="poster" href="{poster_data}" x="458" y="-8" width="414" height="206" preserveAspectRatio="xMidYMid slice"/>
    <rect x="458" width="414" height="190" fill="url(#posterVeil)"/>
    <rect x="458" width="414" height="190" filter="url(#grain)" opacity=".24"/>
  </g>
  <path d="M500 1H859V189H458Z" fill="none" stroke="{accent}" stroke-opacity=".42"/>

  <text x="18" y="45" font-family="{MONO}" font-size="9" letter-spacing="1.4" fill="{muted}">LOADOUT</text>
  <text x="18" y="93" font-family="Impact,'Arial Narrow',sans-serif" font-size="46" fill="{accent}">{index+1:02}</text>
  <text x="18" y="116" font-family="{MONO}" font-size="8.5" fill="{muted}">ACTIVE</text>
  <circle class="lamp" cx="55" cy="113" r="3.5" fill="{accent}"/>

  <text x="104" y="51" font-family="Impact,'Arial Narrow',sans-serif" font-size="40" letter-spacing="1.2" fill="{ink}">{esc(title)}</text>
  <text x="105" y="72" font-family="{MONO}" font-size="9" fill="{accent}">github.com/{esc(project['repo'])}</text>
  <line x1="105" y1="86" x2="443" y2="86" stroke="{ink}" stroke-opacity=".22"/>
  {brief_lines}
  {detail_lines}
  <text x="105" y="176" font-family="{MONO}" font-size="8.5" font-weight="700" letter-spacing=".7" fill="{accent}">{esc(chips)}</text>

  <g transform="translate(770 141)">
    <rect width="70" height="30" fill="{base}" fill-opacity=".84" stroke="{accent}"/>
    <text x="10" y="19" font-family="{MONO}" font-size="8" fill="{accent}">OPEN</text>
    <g class="chev" fill="none" stroke="{accent}" stroke-width="1.6"><path d="M47 8l10 7-10 7M56 8l10 7-10 7"/></g>
  </g>
  <rect x="105" y="181" width="338" height="2" fill="{ink}" opacity=".1"/>
  <rect class="meter" x="105" y="181" width="278" height="2" fill="{accent}"/>
  <g clip-path="url(#frameClip)"><rect class="sweep" x="-230" y="0" width="170" height="{H}" fill="url(#sweep)" transform="skewX(-24)"/></g>
</svg>
'''
    write_svg(f"assets/card_{project['id']}.svg", svg)


def build():
    for i, project in enumerate(profile()["projects"]):
        card(project, i)


if __name__ == "__main__":
    build()
