"""
banner_*.svg + divider.svg — cinematic section headers and a data-stream divider.

banners are HUD title bars ('>> SELECTED WORK ────┤ // 3 featured'); the divider
is a thin rule with a glowing packet that streams across it. used to break the
README into sections without relying on (un-styleable) markdown headings.
"""

from lib import BG, GREEN, GREY, CYAN, MONO, write_svg

BW, BH = 860, 52
HOT = "#d8fff0"


def banner(fname, title, subtitle):
    title = title.upper()
    tx = 14 + len(title) * 13.5 + 40        # where the rule starts after the title
    ticks = "".join(f'<line x1="{x}" y1="30" x2="{x}" y2="36" stroke="{GREEN}" '
                    f'stroke-opacity="0.3" stroke-width="1"/>'
                    for x in range(int(tx) + 20, BW - 180, 26))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" role="img" aria-label="{title} {subtitle}">
  <text x="14" y="40" font-size="13" font-weight="700" fill="{GREEN}" font-family="{MONO}">&gt;&gt;</text>
  <text x="42" y="40" font-size="20" font-weight="700" fill="{GREEN}" font-family="{MONO}" letter-spacing="2">{title}</text>
  <line x1="{tx}" y1="33" x2="{BW-176}" y2="33" stroke="{GREEN}" stroke-opacity="0.25" stroke-width="1.5"/>
  {ticks}
  <rect x="{BW-168}" y="26" width="9" height="9" fill="{GREEN}">
    <animate attributeName="opacity" values="1;0.2;1" dur="1.6s" repeatCount="indefinite"/>
  </rect>
  <text x="{BW-152}" y="40" font-size="12" fill="{GREY}" font-family="{MONO}">{subtitle}</text>
</svg>
'''
    write_svg(f"assets/{fname}", svg)


def divider():
    W, H = 860, 22
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="divider">
  <defs>
    <linearGradient id="pkt" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="{HOT}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{HOT}" stop-opacity="1"/>
      <stop offset="1" stop-color="{HOT}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <line x1="0" y1="11" x2="{W}" y2="11" stroke="{GREEN}" stroke-opacity="0.18" stroke-width="1"/>
  <path d="M{W//2-7},11 L{W//2},5 L{W//2+7},11 L{W//2},17 Z" fill="{BG}" stroke="{GREEN}" stroke-opacity="0.6"/>
  <rect x="0" y="10" width="90" height="2" fill="url(#pkt)">
    <animate attributeName="x" values="-90;{W};{W}" keyTimes="0;0.7;1" dur="5s" repeatCount="indefinite"/>
  </rect>
</svg>
'''
    write_svg("assets/divider.svg", svg)


def build():
    banner("banner_work.svg", "selected work", "// 3 featured")
    banner("banner_telemetry.svg", "telemetry", "// live · self-rebuilding")
    banner("banner_stack.svg", "loadout", "// stack")
    banner("banner_contact.svg", "whois", "// reach")
    divider()


if __name__ == "__main__":
    build()
