"""stack.svg — current working set as torn module tickets."""

from lib import BG, BORDER, GREEN, WHITE, GREY, RED, PAPER, MONO, write_svg, profile
from logos import LOGOS

W, H = 860, 252


def logo_markup(slug, x, y, size, color):
    if not slug or slug not in LOGOS:
        return ""
    scale = size / 24
    return (f'<g transform="translate({x},{y}) scale({scale:.4f})">'
            f'<path d="{LOGOS[slug]}" fill="{color}"/></g>')


def build():
    techs = profile()["stack"]
    cells = []
    for i, tech in enumerate(techs):
        col, row = i % 5, i // 5
        x, y = 18 + col * 168, 45 + row * 98
        paper = (i % 4 == 2)
        red = (i % 5 == 3)
        base = PAPER if paper else (RED if red else "#0b0d0c")
        ink = BG if paper else WHITE
        accent = RED if paper else (PAPER if red else GREEN)
        path = (f"M{x+4} {y+4}L{x+153} {y}L{x+160} {y+72}"
                f"L{x+7} {y+78}L{x} {y+18}Z")
        icon = logo_markup(tech.get("logo"), x + 14, y + 14, 27, accent)
        label_y = y + (57 if icon else 42)
        cells.append(
            f'<path d="{path}" fill="{base}" stroke="{BORDER}" stroke-width="1.2"/>'
            f'{icon}'
            f'<text x="{x+14}" y="{label_y}" font-family="{MONO}" font-size="13" '
            f'font-weight="700" fill="{ink}">{tech["name"].upper()}</text>'
            f'<text x="{x+143}" y="{y+18}" text-anchor="end" font-family="{MONO}" '
            f'font-size="8" fill="{accent}">{i+1:02}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Current working stack">
  <defs>
    <pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse">
      <path d="M18 0H0V18" fill="none" stroke="{WHITE}" stroke-opacity=".04"/>
    </pattern>
    <clipPath id="scanclip"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="6"/></clipPath>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="6" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="6" fill="url(#grid)"/>
  <text x="18" y="27" font-family="{MONO}" font-size="10" fill="{GREY}">MODULE INDEX / EDIT profile.json TO CHANGE</text>
  <text x="842" y="27" text-anchor="end" font-family="{MONO}" font-size="10" fill="{GREEN}">{len(techs):02} LOADED</text>
  {''.join(cells)}
  <g clip-path="url(#scanclip)">
    <rect x="-140" y="0" width="110" height="{H}" fill="{GREEN}" opacity=".035" transform="skewX(-14)">
      <animate attributeName="x" values="-140;920;920" keyTimes="0;.68;1" dur="6.5s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>
'''
    write_svg("assets/stack.svg", svg)


if __name__ == "__main__":
    build()
