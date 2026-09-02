"""Section labels and divider strips for the punk-collage README."""

from lib import BG, BORDER, GREEN, WHITE, GREY, RED, PAPER, MONO, write_svg

BW, BH = 860, 62


def banner(fname, title, subtitle, mark=""):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" role="img" aria-label="{title}: {subtitle}">
  <defs>
    <filter id="rough"><feTurbulence baseFrequency=".8" numOctaves="2" seed="9" result="n"/><feBlend in="SourceGraphic" in2="n" mode="multiply"/></filter>
  </defs>
  <rect width="{BW}" height="{BH}" fill="{BG}"/>
  <path d="M4 12L362 7 369 52 10 57Z" fill="{PAPER}"/>
  <path d="M376 31H842" stroke="{WHITE}" stroke-opacity=".28"/>
  <path d="M376 25H612" stroke="{RED}" stroke-width="3"/>
  <text x="20" y="45" font-family="Impact,'Arial Narrow',sans-serif" font-size="31"
        letter-spacing="2" fill="{BG}">{title.upper()}</text>
  <text x="385" y="50" font-family="{MONO}" font-size="11" fill="{GREY}">{subtitle}</text>
  <text x="830" y="24" text-anchor="end" font-family="{MONO}" font-size="17"
        letter-spacing="4" fill="{RED}">{mark}</text>
  <rect x="4" y="2" width="{BW-8}" height="{BH-4}" fill="none" stroke="{BORDER}" stroke-dasharray="2 7"/>
</svg>
'''
    write_svg(f"assets/{fname}", svg)


def divider():
    W, H = 860, 26
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="divider">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <path d="M0 13H{W}" stroke="{WHITE}" stroke-opacity=".2" stroke-dasharray="3 7"/>
  <path d="M-120 11H0L20 13 0 15H-120Z" fill="{GREEN}">
    <animate attributeName="d" values="M-120 11H0L20 13 0 15H-120Z;M740 11H840L860 13 840 15H740Z;M740 11H840L860 13 840 15H740Z" keyTimes="0;.72;1" dur="5.5s" repeatCount="indefinite"/>
  </path>
  <rect x="407" y="5" width="46" height="16" fill="{RED}" transform="rotate(-3 430 13)"/>
  <text x="430" y="17" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{PAPER}">KK-07</text>
</svg>
'''
    write_svg("assets/divider.svg", svg)


def build():
    banner("banner_work.svg", "selected work", "three current builds", "★★★★★")
    banner("banner_notes.svg", "field notes", "writeups and earlier systems")
    banner("banner_telemetry.svg", "live activity", "public GitHub data")
    banner("banner_stack.svg", "working set", "tools used in current projects")
    banner("banner_contact.svg", "contact", "direct links")
    divider()


if __name__ == "__main__":
    build()
