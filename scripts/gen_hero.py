"""hero.svg — liquid-silver punk dossier with a moving ASCII knight."""

import base64
from pathlib import Path

from lib import (BG, PANEL, BORDER, GREEN, CYAN, WHITE, GREY, RED, PAPER,
                 SILVER, MONO, esc, write_svg, profile)

W, H = 860, 470
ROOT = Path(__file__).resolve().parent.parent


def image_data(path):
    raw = path.read_bytes()
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


def ascii_knight():
    lines = [
        r"        __",
        r"    _.-'  '-._",
        "   /   _/\\\\_   \\\\",
        "  /___/    \\\\___\\\\",
        "     /  /\\\\  \\\\",
        "    /__/  \\\\__\\\\",
        r"       |  |",
        r"    ___|__|___",
    ]
    return "".join(
        f'<tspan x="0" dy="{0 if i == 0 else 9}">{esc(line)}</tspan>'
        for i, line in enumerate(lines)
    )


def build():
    cfg = profile()
    ident = cfg["identity"]
    display_role = "AI SYSTEMS · APPSEC · FULL-STACK"
    projects = " / ".join(p["name"].upper() for p in cfg["projects"])
    art = image_data(ROOT / "assets" / "silver-knight.png")

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(ident['name'])}, {esc(ident['role'])}">
  <defs>
    <filter id="paperNoise" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency=".72" numOctaves="2" seed="17" result="n"/>
      <feColorMatrix in="n" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 .10 0"/>
      <feBlend in="SourceGraphic" mode="screen"/>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
    <pattern id="grid" width="22" height="22" patternUnits="userSpaceOnUse">
      <path d="M22 0H0V22" fill="none" stroke="{WHITE}" stroke-opacity=".045"/>
    </pattern>
    <clipPath id="artClip"><path d="M18 18H365L350 451H26Z"/></clipPath>
    <clipPath id="asciiClip"><rect x="382" y="228" width="444" height="88"/></clipPath>
  </defs>

  <rect width="{W}" height="{H}" rx="7" fill="{BG}"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="7" fill="none" stroke="{BORDER}" stroke-width="2"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="7" fill="url(#grid)"/>

  <!-- torn foil fragments -->
  <path d="M5 58L101 41 117 74 16 93Z" fill="{SILVER}" opacity=".16"/>
  <path d="M310 6L369 22 348 53 294 37Z" fill="{SILVER}" opacity=".22"/>
  <path d="M733 18L851 7 842 42 760 48Z" fill="{PAPER}" opacity=".12"/>
  <path d="M559 432L676 413 693 459 575 467Z" fill="{SILVER}" opacity=".13"/>

  <!-- generated centerpiece -->
  <ellipse cx="199" cy="265" rx="150" ry="184" fill="{GREEN}" opacity=".08" filter="url(#softGlow)"/>
  <g clip-path="url(#artClip)">
    <image href="{art}" x="19" y="-15" width="350" height="525" preserveAspectRatio="xMidYMid meet"/>
  </g>
  <path d="M18 18H365L350 451H26Z" fill="none" stroke="{WHITE}" stroke-opacity=".22" stroke-dasharray="2 7"/>

  <!-- vertical identity spine -->
  <text transform="translate(34 430) rotate(-90)" font-family="{MONO}" font-size="19" font-weight="800"
        letter-spacing="4" fill="{WHITE}">{esc(ident['handle']).upper()}</text>
  <text x="44" y="448" font-family="{MONO}" font-size="10" fill="{GREEN}">KK-07</text>

  <!-- name -->
  <text x="382" y="92" font-family="Impact,'Arial Narrow',sans-serif" font-size="67"
        letter-spacing="1" fill="{WHITE}" filter="url(#paperNoise)">{esc(ident['name']).upper()}</text>
  <path d="M377 109L832 102 824 142 385 150Z" fill="{PAPER}"/>
  <text x="398" y="135" font-family="{MONO}" font-size="13" font-weight="800"
        letter-spacing="1.2" fill="{BG}">{display_role}</text>
  <text x="383" y="181" font-family="{MONO}" font-size="11" fill="{GREEN}">github.com/{esc(ident['handle'])}</text>
  <line x1="382" y1="196" x2="826" y2="196" stroke="{WHITE}" stroke-opacity=".26"/>

  <!-- moving ASCII knight -->
  <rect x="382" y="215" width="444" height="112" fill="{PANEL}" stroke="{BORDER}"/>
  <text x="395" y="234" font-family="{MONO}" font-size="9" fill="{GREY}">ASCII SIGNAL / LIVE LOOP</text>
  <g clip-path="url(#asciiClip)">
    <g transform="translate(535 241)" opacity=".42">
      <text x="0" y="0" xml:space="preserve" font-family="{MONO}" font-size="8" fill="{GREEN}">
        {ascii_knight()}
      </text>
    </g>
    <g transform="translate(-150 241)">
      <animateTransform attributeName="transform" type="translate"
        values="-150 241;560 241;560 241" keyTimes="0;.72;1" dur="8s" repeatCount="indefinite"/>
      <text x="0" y="0" xml:space="preserve" font-family="{MONO}" font-size="8" fill="{GREEN}">
        {ascii_knight()}
      </text>
    </g>
    <rect x="382" y="215" width="46" height="112" fill="{GREEN}" opacity=".08">
      <animate attributeName="x" values="382;780;780" keyTimes="0;.72;1" dur="8s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- game-star motif and current work -->
  <text x="382" y="362" font-family="{MONO}" font-size="14" fill="{GREEN}">05</text>
  <text x="421" y="365" font-family="{MONO}" font-size="27" letter-spacing="7" fill="{RED}">★★★★★</text>
  <line x1="382" y1="380" x2="826" y2="380" stroke="{RED}" stroke-width="2"/>
  <text x="382" y="409" font-family="{MONO}" font-size="11" fill="{GREY}">SELECTED WORK</text>
  <text x="382" y="436" font-family="{MONO}" font-size="16" font-weight="700" fill="{WHITE}">{esc(projects)}</text>

  <path d="M841 67v-22h-22M841 403v22h-22" fill="none" stroke="{GREEN}" stroke-width="1.5"/>
  <circle cx="836" cy="234" r="3" fill="{GREEN}">
    <animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/>
  </circle>
</svg>
'''
    write_svg("assets/hero.svg", svg)


if __name__ == "__main__":
    build()
