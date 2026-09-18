"""
stack.svg — the kit, laid out.

each tool is a flat silver mark on ink, numbered and captioned like an
equipment layout shot, set in a single row and brought up left to right.
logos are baked vector paths (see scripts/logos.py) recoloured to silver —
no runtime network, no third-party widgets.
"""

from lib import (INK, HAIRLINE, SILVER, ASH, MONO, font_css, film_defs,
                 film_overlay, write_svg, reveal, panel_head)
from logos import LOGOS

W, H = 860, 190
ICON = 28

# ordered as the stack flows: language → ml → models → serving → local
# runtime → backend → frontend → tooling → security
TECHS = [
    ("python", "python"), ("pytorch", "pytorch"),
    ("huggingface", "huggingface"), ("vllm", "vllm"), ("ollama", "ollama"),
    ("fastapi", "fastapi"), ("typescript", "typescript"), ("react", "react"),
    ("git", "git"), ("kali linux", "kalilinux"),
]


def item(i, cx, name, slug):
    s = ICON / 24.0
    top = 80
    body = (f'<text x="{cx}" y="{top - 12}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="8.5" fill="{ASH}">{i + 1:02d}</text>'
            f'<g transform="translate({cx - ICON / 2:.1f},{top}) scale({s:.4f})">'
            f'<path d="{LOGOS[slug]}" fill="{SILVER}"/></g>'
            f'<rect x="{cx - 14}" y="{top + ICON + 14}" width="28" height="1" fill="{HAIRLINE}"/>'
            f'<text x="{cx}" y="{top + ICON + 34}" text-anchor="middle" font-family="{MONO}" '
            f'font-size="10.5" fill="{ASH}">{name}</text>')
    return reveal(0.3 + i * 0.12, body, dur=0.8)


def build():
    step = (W - 48) / len(TECHS)
    items = "".join(item(i, 24 + step * (i + 0.5), n, s)
                    for i, (n, s) in enumerate(TECHS))
    names = ", ".join(n for n, _ in TECHS)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="tools: {names}">
  <defs>{film_defs(W, H, seed=43)}</defs>
  {font_css()}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  {panel_head(W, "kit", f"{len(TECHS)} tools")}
  {items}
  {film_overlay(W, H, vignette=False)}
</svg>
'''
    write_svg("assets/stack.svg", svg)


if __name__ == "__main__":
    build()
