"""
card_ace.svg — the title card.

a crumpled ace of spades (scripts/tools/source/ace.png, baked into
scripts/ace_image.py) lit inside a dark frame. a sheen crosses it every few
seconds, masked by the card's own luminance so the light only catches the
paper. beside it, the billing block: who this is and what he works on, set
like the credits at the head of a film. the only red is the small spade.
"""

from lib import (INK, SILVER, SILVER_DIM, ASH, BLOOD, SERIF, MONO,
                 esc, font_css, film_defs, film_overlay, write_svg, profile, reveal)
import ace_image

W, H = 860, 480
IW = 280                                  # shown width of the card image
IH = round(IW * ace_image.H / ace_image.W)
IX, IY = 116, (H - IH) // 2
SHEEN = 7                                 # seconds between sweeps
SPADE = ("M0,-14 C6,-6 14,-2 14,5 C14,10 9,12 5,10 C3,9 2,8 1,7 L4,14 L-4,14 "
         "L-1,7 C-2,8 -3,9 -5,10 C-9,12 -14,10 -14,5 C-14,-2 -6,-6 0,-14 Z")


def card():
    mid_x, mid_y = IX + IW / 2, IY + IH / 2
    return f'''
  <use href="#ace" style="mix-blend-mode:lighten"/>
  <rect x="{IX}" y="{IY}" width="{IW}" height="{IH}" fill="url(#edge)"/>
  <g mask="url(#paper)">
    <g transform="rotate(24 {mid_x} {mid_y})">
      <rect x="{IX - 170}" y="{IY - 140}" width="160" height="{IH + 280}" fill="url(#sheen)">
        <animate attributeName="x" values="{IX - 170};{IX + IW + 10};{IX + IW + 10}" keyTimes="0;0.32;1"
                 dur="{SHEEN}s" begin="2.2s" repeatCount="indefinite"/>
      </rect>
    </g>
  </g>'''


def dossier(me, stack):
    X = 470
    rules = [
        ("works in", "ai systems, application security"),
        ("builds", "local-first tools and assistants"),
        ("off hours", "ctfs, labs, writeups"),
        ("works with", " · ".join(stack)),
    ]
    out = [
        reveal(1.0, f'<path transform="translate({X + 4} 127) scale(0.32)" d="{SPADE}" fill="{BLOOD}"/>'
                    f'<text x="{X + 16}" y="132" font-family="{MONO}" font-size="10" '
                    f'letter-spacing="3.5" fill="{ASH}">IN THE LEADING ROLE</text>'),
        reveal(1.4, f'<text x="{X - 2}" y="182" font-family="{SERIF}" font-size="46" '
                    f'fill="{SILVER}">{esc(me["name"])}</text>'),
        reveal(1.8, f'<text x="{X}" y="210" font-family="{SERIF}" font-style="italic" '
                    f'font-size="19" fill="{SILVER_DIM}">as {esc(me["handle"])}</text>'),
        reveal(2.2, f'<rect x="{X}" y="232" width="330" height="1" fill="{SILVER_DIM}" opacity="0.35"/>'),
    ]
    for i, (k, v) in enumerate(rules):
        y = 262 + i * 24
        out.append(reveal(2.5 + i * 0.25,
                          f'<text y="{y}" font-family="{MONO}" font-size="12">'
                          f'<tspan x="{X}" fill="{ASH}">{esc(k)}</tspan>'
                          f'<tspan x="{X + 96}" fill="{SILVER}">{esc(v)}</tspan></text>'))
    return "".join(out)


def build():
    p = profile()
    me = p["identity"]
    stack = ["python", "typescript", "kali"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="the ace of spades, crumpled, beside the billing block: {esc(me["name"])}, as {esc(me["handle"])}">
  <defs>{film_defs(W, H, seed=11)}
    <image id="ace" x="{IX}" y="{IY}" width="{IW}" height="{IH}" preserveAspectRatio="xMidYMid meet"
           href="data:image/jpeg;base64,{ace_image.ACE_JPEG_B64}"/>
    <mask id="paper" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <use href="#ace"/>
    </mask>
    <linearGradient id="sheen" x1="0" x2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.40" stop-color="#fff" stop-opacity="0.95"/>
      <stop offset="0.55" stop-color="#e9d9d6" stop-opacity="0.35"/>
      <stop offset="0.70" stop-color="#cfdbe3" stop-opacity="0.35"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="edge" cx="0.5" cy="0.5" r="0.62">
      <stop offset="0.72" stop-color="{INK}" stop-opacity="0"/>
      <stop offset="1" stop-color="{INK}" stop-opacity="0.85"/>
    </radialGradient>
    <radialGradient id="spot" cx="{(IX + IW / 2) / W:.3f}" cy="0.5" r="0.42">
      <stop offset="0" stop-color="#fff" stop-opacity="0.05"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
  </defs>
  {font_css(serif=True, italic=True)}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  <rect width="{W}" height="{H}" fill="url(#spot)"/>
  <g opacity="0">
    <animate attributeName="opacity" from="0" to="1" dur="2.2s" begin="0.2s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="0 14" to="0 0" dur="2.2s" begin="0.2s" fill="freeze"
                      calcMode="spline" keyTimes="0;1" keySplines="0.2 0.7 0.3 1"/>
    {card()}
  </g>
  {dossier(me, stack)}
  {film_overlay(W, H)}
</svg>
'''
    write_svg("assets/card_ace.svg", svg)


if __name__ == "__main__":
    build()
