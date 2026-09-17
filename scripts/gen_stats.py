"""
stats.svg — the ledger.

three live counts set as big serif numerals, then the language mix as hairline
rules. real numbers from the pipeline, fading in once.
"""

from lib import (INK, HAIRLINE, SILVER, SILVER_DIM, ASH, SERIF, MONO, esc,
                 font_css, film_defs, film_overlay, write_svg, collect, reveal,
                 panel_head)

W, H = 430, 300

# keep labels short enough to never crash into the rule
ALIASES = {"jupyter notebook": "jupyter", "objective-c": "objc",
           "dockerfile": "docker"}


def label(name):
    return ALIASES.get(name.lower(), name.lower())[:12]


def count(x, value, name):
    return (f'<text x="{x}" y="112" font-family="{SERIF}" font-size="50" '
            f'fill="{SILVER}">{esc(value)}</text>'
            f'<text x="{x + 2}" y="132" font-family="{MONO}" font-size="10" '
            f'letter-spacing="2" fill="{ASH}">{esc(name.upper())}</text>')


def lang(y, name, pct):
    tx, tw = 128, 230
    fw = max(2, round(tw * pct / 100))
    return (f'<text x="24" y="{y + 4}" font-family="{MONO}" font-size="11.5" '
            f'fill="{SILVER_DIM}">{esc(name)}</text>'
            f'<rect x="{tx}" y="{y}" width="{tw}" height="1" fill="{HAIRLINE}"/>'
            f'<rect x="{tx}" y="{y - 1}" width="{fw}" height="3" fill="{SILVER}"/>'
            f'<text x="{W - 24}" y="{y + 4}" text-anchor="end" font-family="{MONO}" '
            f'font-size="11" fill="{SILVER_DIM}">{pct}%</text>')


def build():
    d = collect()
    langs = "".join(lang(180 + i * 18, label(n), p)
                    for i, (n, p) in enumerate(d["langs"][:5]))
    counts = (count(24, str(d["stars"]), "stars")
              + count(160, str(d["repos"]), "repos")
              + count(296, str(d["followers"]), "followers"))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{d['stars']} stars, {d['repos']} public repositories, {d['followers']} followers">
  <defs>{film_defs(W, H, seed=31)}</defs>
  {font_css(serif=True)}
  <rect width="{W}" height="{H}" fill="{INK}"/>
  {panel_head(W, "ledger", "public github")}
  {reveal(0.3, counts, dur=1.8)}
  {reveal(1.0, f'<text x="24" y="158" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{ASH}">LANGUAGES, BY BYTES</text>{langs}')}
  <text x="24" y="{H - 20}" font-family="{MONO}" font-size="10" fill="{ASH}">counted {esc(d['generated'])}</text>
  {film_overlay(W, H, vignette=False)}
</svg>
'''
    write_svg("assets/stats.svg", svg)


if __name__ == "__main__":
    build()
