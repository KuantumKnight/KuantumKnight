"""
card_joker.svg — the character card.

a joker, printed in ink on warm card stock, lit inside a dark frame. the only
red is the corner index. a foil sheen crosses the face every few seconds (an
<img> svg can't follow the cursor, so the light moves on its own). beside the
card, a dossier set like a card's rules text.
"""

from lib import (INK, SILVER, SILVER_DIM, ASH, BLOOD, SERIF, MONO,
                 esc, font_css, film_defs, film_overlay, write_svg, profile)

W, H = 860, 480
CX, CY, CW, CH = 120, 40, 280, 400       # card box
PAPER = "#e6e1d6"
PRINT = "#161515"
SHEEN = 7                                # seconds between sweeps


def jester(cx, cy):
    """cap, bells and domino mask as flat print, centered on (cx, cy)."""
    prong_l = ("M-46,30 C-58,4 -74,-18 -80,-52 C-62,-34 -38,-18 -20,28 Z")
    prong_c = ("M-22,28 C-16,-8 -6,-40 0,-74 C6,-40 16,-8 22,28 Z")
    band = "M-54,26 Q0,42 54,26 L52,44 Q0,60 -52,44 Z"
    diamonds = "".join(
        f'<path d="M{x},{36 + abs(x) * 0.05:.1f} l5,5 l-5,5 l-5,-5 Z" fill="{PAPER}"/>'
        for x in range(-40, 41, 16))
    bells = "".join(
        f'<circle cx="{x}" cy="{y}" r="6.5" fill="{PAPER}" stroke="{PRINT}" stroke-width="1.6"/>'
        f'<line x1="{x-3}" y1="{y+1.5}" x2="{x+3}" y2="{y+1.5}" stroke="{PRINT}" stroke-width="1.2"/>'
        for x, y in ((-82, -57), (0, -80), (82, -57)))
    mask = ("M-56,78 C-40,64 -15,68 0,76 C15,68 40,64 56,78 C53,95 30,103 12,95 "
            "C6,91 3,87 0,87 C-3,87 -6,91 -12,95 C-30,103 -53,95 -56,78 Z")
    return f'''<g transform="translate({cx} {cy})">
      <path d="{prong_l}" fill="{PRINT}"/>
      <path d="{prong_l}" transform="scale(-1 1)" fill="{PRINT}"/>
      <path d="{prong_c}" fill="url(#hatch)" stroke="{PRINT}" stroke-width="1.6"/>
      <path d="{band}" fill="{PRINT}"/>{diamonds}{bells}
      <path d="{mask}" fill="{PRINT}"/>
      <ellipse cx="-25" cy="83" rx="9" ry="4.5" fill="{PAPER}"/>
      <ellipse cx="25" cy="83" rx="9" ry="4.5" fill="{PAPER}"/>
    </g>'''


def index(x, y, flip=False):
    letters = "".join(
        f'<text x="{x}" y="{y + i * 13}" text-anchor="middle">{c}</text>'
        for i, c in enumerate("JOKER"))
    g = (f'<g font-family="{MONO}" font-weight="700" font-size="11" fill="{BLOOD}">'
         f'{letters}</g>')
    if flip:
        g = f'<g transform="rotate(180 {CX + CW / 2} {CY + CH / 2})">{g}</g>'
    return g


def card():
    r = 14
    x2, y2 = CX + CW, CY + CH
    mid = CX + CW / 2
    return f'''
  <ellipse cx="{mid}" cy="{y2 + 10}" rx="{CW * 0.46}" ry="10" fill="#000" opacity="0.7" filter="url(#soft)"/>
  <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{r}" fill="{PAPER}"/>
  <rect x="{CX + 28}" y="{CY + 24}" width="{CW - 56}" height="{CH - 48}" rx="4" fill="none" stroke="{PRINT}" stroke-width="1"/>
  <rect x="{CX + 32}" y="{CY + 28}" width="{CW - 64}" height="{CH - 56}" rx="2" fill="none" stroke="{PRINT}" stroke-width="0.4"/>
  {index(CX + 15, CY + 26)}
  {index(CX + 15, CY + 26, flip=True)}
  {jester(mid, CY + 176)}
  <text x="{mid}" y="{CY + 330}" text-anchor="middle" font-family="{SERIF}" font-style="italic" font-size="24" fill="{PRINT}">the joker</text>
  <text x="{mid}" y="{CY + 350}" text-anchor="middle" font-family="{MONO}" font-size="8" letter-spacing="3.5" fill="{PRINT}" opacity="0.7">KUANTUMKNIGHT</text>
  <g clip-path="url(#face)">
    <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" fill="url(#foil)" opacity="0.22"/>
    <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" filter="url(#kk-grain)" opacity="0.8"/>
    <g transform="rotate(24 {mid} {CY + CH / 2})">
      <rect x="{CX - 160}" y="{CY - 120}" width="150" height="{CH + 240}" fill="url(#sheen)">
        <animate attributeName="x" values="{CX - 160};{x2 + 10};{x2 + 10}" keyTimes="0;0.32;1"
                 dur="{SHEEN}s" begin="2.2s" repeatCount="indefinite"/>
      </rect>
    </g>
  </g>
  <rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{r}" fill="none" stroke="#000" stroke-opacity="0.35"/>'''


def dossier(me, stack):
    X = 470
    lines = [
        ("label", "CARD 00 — THE JOKER"),
        ("name", me["name"]),
        ("alias", f"plays as {me['handle']}"),
    ]
    rules = [
        ("works in", "ai systems, application security"),
        ("builds", "local-first tools and assistants"),
        ("off hours", "ctfs, labs, writeups"),
        ("carries", " · ".join(stack)),
    ]
    out = []

    def reveal(delay, body):
        return (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
                f'dur="1.2s" begin="{delay}s" fill="freeze"/>{body}</g>')

    out.append(reveal(1.0, f'<text x="{X}" y="132" font-family="{MONO}" font-size="10" '
                           f'letter-spacing="3.5" fill="{ASH}">{lines[0][1]}</text>'))
    out.append(reveal(1.4, f'<text x="{X - 2}" y="182" font-family="{SERIF}" font-size="46" '
                           f'fill="{SILVER}">{esc(lines[1][1])}</text>'))
    out.append(reveal(1.8, f'<text x="{X}" y="210" font-family="{SERIF}" font-style="italic" '
                           f'font-size="19" fill="{SILVER_DIM}">{esc(lines[2][1])}</text>'))
    out.append(reveal(2.2, f'<rect x="{X}" y="232" width="330" height="1" fill="{SILVER_DIM}" opacity="0.35"/>'))
    for i, (k, v) in enumerate(rules):
        y = 262 + i * 24
        out.append(reveal(2.5 + i * 0.25,
                          f'<text y="{y}" font-family="{MONO}" font-size="12">'
                          f'<tspan x="{X}" fill="{ASH}">{esc(k)}</tspan>'
                          f'<tspan x="{X + 96}" fill="{SILVER}">{esc(v)}</tspan></text>'))
    out.append(reveal(3.8, f'<text x="{X}" y="390" font-family="{SERIF}" font-style="italic" '
                           f'font-size="15" fill="{SILVER_DIM}">This card may be played as any other card.</text>'))
    return "".join(out)


def build():
    p = profile()
    stack = ["python", "typescript", "kali"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="a joker playing card beside a short dossier: {esc(p["identity"]["name"])}, plays as {esc(p["identity"]["handle"])}">
  <defs>{film_defs(W, H, seed=11)}
    <clipPath id="face"><rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="14"/></clipPath>
    <pattern id="hatch" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="4" height="4" fill="{PAPER}"/><rect width="1.3" height="4" fill="{PRINT}"/>
    </pattern>
    <pattern id="foil" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(-30)">
      <rect width="5" height="0.6" fill="#fff"/>
    </pattern>
    <linearGradient id="sheen" x1="0" x2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.40" stop-color="#fff" stop-opacity="0.55"/>
      <stop offset="0.55" stop-color="{BLOOD}" stop-opacity="0.16"/>
      <stop offset="0.70" stop-color="#9fb8c8" stop-opacity="0.18"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="spot" cx="{(CX + CW / 2) / W:.3f}" cy="0.45" r="0.42">
      <stop offset="0" stop-color="#fff" stop-opacity="0.07"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <filter id="soft" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="8"/></filter>
  </defs>
  {font_css(serif=True, italic=True, mono=(400, 700))}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#spot)"/>
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="1.8s" begin="0.2s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="0 14" to="0 0" dur="1.8s" begin="0.2s" fill="freeze"
                      calcMode="spline" keyTimes="0;1" keySplines="0.2 0.7 0.3 1"/>
    {card()}
  </g>
  {dossier(p["identity"], stack)}
  {film_overlay(W, H)}
</svg>
'''
    write_svg("assets/card_joker.svg", svg)


if __name__ == "__main__":
    build()
