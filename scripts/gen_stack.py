"""
stack.svg — the tech stack as a neon hologram array.

each tech is a glowing green holographic hex-badge carrying its real brand logo,
arranged in a grid wired by faint circuit lines, with per-badge flicker, a
constant bloom glow, and a hologram scanline sweeping down the panel. cinematic,
on-palette. logos are baked vector paths (see scripts/logos.py) recoloured into
the neon palette — no runtime network, no third-party widgets.
"""

import math
from lib import BG, PANEL, BORDER, GREEN, GREY, RED, AMBER, LIME, MONO, write_svg
from logos import LOGOS

W, H = 820, 312
HOT = "#d8fff0"
ICON = 26  # logo box, fits inside the R=30 hex


def pol(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.sin(a), cy - r * math.cos(a))


def hexpath(cx, cy, r):
    pts = [pol(cx, cy, r, d) for d in range(0, 360, 60)]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


# ---- glyph: a real brand logo, scaled from its 24x24 viewBox to ICON px,
#      centred on (cx, cy) and recoloured to `col` --------------------------
def logo(slug):
    d = LOGOS[slug]

    def render(cx, cy, col):
        s = ICON / 24.0
        tx, ty = cx - 12 * s, cy - 12 * s
        return (f'<g transform="translate({tx:.2f},{ty:.2f}) scale({s:.4f})">'
                f'<path d="{d}" fill="{col}"/></g>')

    return render


# ordered as the stack flows: language → ML framework → models → LLM serving →
# local runtime → backend API → frontend → tooling → security
# display name -> simpleicons slug (logos baked in scripts/logos.py)
TECHS = [
    ("python",      logo("python")),
    ("pytorch",     logo("pytorch")),
    ("huggingface", logo("huggingface")),
    ("vllm",        logo("vllm")),
    ("ollama",      logo("ollama")),
    ("fastapi",     logo("fastapi")),
    ("typescript",  logo("typescript")),
    ("react",       logo("react")),
    ("git",         logo("git")),
    ("kali linux",  logo("kalilinux")),
]

COLS, R = 5, 30
XS = [110 + i * 150 for i in range(COLS)]
YS = [104, 228]


def badge(cx, cy, name, glyph, col, frameop, nameop=True):
    out = (f'<path d="{hexpath(cx, cy, R)}" fill="{GREEN}" fill-opacity="0.05" '
           f'stroke="{col}" stroke-opacity="{frameop}" stroke-width="1.6"/>'
           f'{glyph(cx, cy, col)}')
    if nameop:
        out += (f'<text x="{cx}" y="{cy+R+18}" text-anchor="middle" font-size="11" '
                f'fill="{GREY}" font-family="{MONO}">{name}</text>')
    return out


def build():
    glow, crisp, wires = [], [], []
    for i, (name, glyph) in enumerate(TECHS):
        cx, cy = XS[i % COLS], YS[i // COLS]
        # circuit wire to next in row
        if (i % COLS) != COLS - 1 and (i + 1) < len(TECHS):
            nx = XS[(i + 1) % COLS]
            wires.append(f'<line x1="{cx+R}" y1="{cy}" x2="{nx-R}" y2="{cy}" '
                         f'stroke="{GREEN}" stroke-opacity="0.12" stroke-width="1" stroke-dasharray="3 4"/>')
        glow.append(badge(cx, cy, name, glyph, HOT, 0.9, nameop=False))
        begin = round((i * 0.37) % 3.3, 2)
        crisp.append(
            f'<g opacity="1"><animate attributeName="opacity" '
            f'values="1;0.55;1;0.8;1;0.65;1" keyTimes="0;0.08;0.18;0.45;0.6;0.82;1" '
            f'dur="3.3s" begin="{begin}s" repeatCount="indefinite"/>'
            f'{badge(cx, cy, name, glyph, GREEN, 0.55)}</g>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="tech stack hologram: python, pytorch, huggingface, vllm, ollama, fastapi, typescript, react, git, kali linux">
  <defs>
    <filter id="bloom" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.6"/></filter>
  </defs>

  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="1" y="1" width="{W-2}" height="34" rx="10" fill="{PANEL}"/>
  <rect x="1" y="24" width="{W-2}" height="11" fill="{PANEL}"/>
  <line x1="1" y1="35" x2="{W-1}" y2="35" stroke="{BORDER}" stroke-width="1.5"/>
  <circle cx="22" cy="18" r="5" fill="{RED}" opacity="0.85"/>
  <circle cx="40" cy="18" r="5" fill="{AMBER}" opacity="0.85"/>
  <circle cx="58" cy="18" r="5" fill="{LIME}" opacity="0.85"/>
  <text x="78" y="22" font-size="12" fill="{GREY}" font-family="{MONO}">~/stack $ ./loadout --modules</text>
  <text x="{W-16}" y="22" text-anchor="end" font-size="12" fill="{GREY}" font-family="{MONO}">{len(TECHS)} modules online</text>

  {''.join(wires)}

  <!-- constant bloom (static, filtered once) -->
  <g filter="url(#bloom)" opacity="0.5">{''.join(glow)}</g>
  <!-- crisp, flickering badges -->
  {''.join(crisp)}
</svg>
'''
    write_svg("assets/stack.svg", svg)


if __name__ == "__main__":
    build()
