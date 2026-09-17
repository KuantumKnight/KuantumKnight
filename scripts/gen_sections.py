"""
banner_*.svg + divider.svg — film slates between scenes, and a quiet rule.

each slate is a strip of ink with a scene number, a serif title, and a caption,
exposed once with a slow fade — like a title card cut into the reel. every
slate carries its own background so it reads on light and dark github themes.
"""

from datetime import date

from lib import (INK, HAIRLINE, SILVER, SILVER_DIM, ASH, BLOOD, SERIF, MONO,
                 esc, font_css, film_defs, film_overlay, write_svg, profile)

W = 860


def slate(fname, scene, title, caption):
    H = 96
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="scene {scene}: {esc(title)}">
  <defs>{film_defs(W, H, seed=int(scene))}
    <linearGradient id="rule" x1="0" x2="1">
      <stop offset="0" stop-color="{SILVER_DIM}" stop-opacity="0.6"/>
      <stop offset="1" stop-color="{SILVER_DIM}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  {font_css(serif=True, italic=True)}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="1.6s" begin="0.2s" fill="freeze"/>
    <rect x="36" y="26" width="2" height="44" fill="{BLOOD}"/>
    <text x="56" y="38" font-family="{MONO}" font-size="10" letter-spacing="3.5" fill="{ASH}">SCENE {scene}</text>
    <text x="55" y="68" font-family="{SERIF}" font-size="32" fill="{SILVER}">{esc(title)}</text>
    <text x="{W-36}" y="68" text-anchor="end" font-family="{SERIF}" font-style="italic" font-size="16" fill="{SILVER_DIM}">{esc(caption)}</text>
    <rect x="56" y="80" width="{W-92}" height="1" fill="url(#rule)"/>
  </g>
  {film_overlay(W, H, vignette=False)}
</svg>
'''
    write_svg(f"assets/{fname}", svg)


def divider():
    H = 28
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="">
  <defs>{film_defs(W, H, seed=9)}</defs>
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <line x1="300" y1="14" x2="410" y2="14" stroke="{HAIRLINE}"/>
  <line x1="450" y1="14" x2="560" y2="14" stroke="{HAIRLINE}"/>
  <path transform="translate(430 14) scale(0.5)" fill="{ASH}"
        d="M0,-14 C6,-6 14,-2 14,5 C14,10 9,12 5,10 C3,9 2,8 1,7 L4,14 L-4,14 L-1,7 C-2,8 -3,9 -5,10 C-9,12 -14,10 -14,5 C-14,-2 -6,-6 0,-14 Z"/>
  {film_overlay(W, H, vignette=False)}
</svg>
'''
    write_svg("assets/divider.svg", svg)


def roman(n):
    out = ""
    for v, r in ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
                 (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
                 (5, "V"), (4, "IV"), (1, "I")):
        while n >= v:
            out += r
            n -= v
    return out


def credits():
    """end credits: a short roll that rises into place once and holds."""
    p = profile()
    me, c = p["identity"], p["contact"]
    H, BAR = 340, 30
    mid = W / 2
    lines = [
        ("correspondence", c["email"]),
        ("on the record", c["github"].replace("https://", "")),
        ("elsewhere", c["linkedin"].replace("https://www.", "")),
    ]
    roles = "".join(
        f'<text x="{mid - 14}" y="{178 + i * 26}" text-anchor="end" font-family="{SERIF}" '
        f'font-style="italic" font-size="16" fill="{SILVER_DIM}">{esc(k)}</text>'
        f'<text x="{mid + 14}" y="{178 + i * 26}" font-family="{MONO}" font-size="12" '
        f'fill="{SILVER}">{esc(v)}</text>'
        for i, (k, v) in enumerate(lines))
    roll = f'''<g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="2s" begin="0.3s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="0 60" to="0 0" dur="5s" begin="0.3s"
                      fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.25 0.6 0.3 1"/>
    <text x="{mid}" y="84" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="4" fill="{ASH}">WRITTEN AND DIRECTED BY</text>
    <text x="{mid}" y="126" text-anchor="middle" font-family="{SERIF}" font-size="44" fill="{SILVER}">{esc(me["name"])}</text>
    {roles}
    <path transform="translate({mid} 270) scale(0.4)" fill="{BLOOD}"
          d="M0,-14 C6,-6 14,-2 14,5 C14,10 9,12 5,10 C3,9 2,8 1,7 L4,14 L-4,14 L-1,7 C-2,8 -3,9 -5,10 C-9,12 -14,10 -14,5 C-14,-2 -6,-6 0,-14 Z"/>
    <text x="{mid}" y="298" text-anchor="middle" font-family="{MONO}" font-size="9" letter-spacing="4" fill="{ASH}">{esc(me["handle"].upper())} · {roman(date.today().year)}</text>
  </g>'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="end credits: written and directed by {esc(me["name"])}; {esc(c["email"])}">
  <defs>{film_defs(W, H, seed=77)}</defs>
  {font_css(serif=True, italic=True)}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  {roll}
  {film_overlay(W, H, bars=BAR)}
</svg>
'''
    write_svg("assets/credits.svg", svg)


def build():
    slate("banner_work.svg", "01", "Work", "current projects")
    slate("banner_notes.svg", "02", "Field Notes", "writeups and side builds")
    slate("banner_telemetry.svg", "03", "Record", "public activity, refreshed every six hours")
    slate("banner_stack.svg", "04", "Kit", "what i build with")
    slate("banner_contact.svg", "05", "Contact", "email, github, linkedin")
    divider()
    credits()


if __name__ == "__main__":
    build()
