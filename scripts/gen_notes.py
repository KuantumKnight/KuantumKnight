"""
note_*.svg — field notes, one row per entry, in two columns.

github can't put several links inside one image, so each entry is its own
small strip (serif name, mono note, a tag on the right) and the README pairs
the strips side by side, each wrapped in its own link.
"""

import re

from lib import (INK, HAIRLINE, SILVER, SILVER_DIM, ASH, SERIF, MONO, esc,
                 font_css, film_defs, film_overlay, write_svg, profile, reveal,
                 panel_head)

W = 416
ROW_H, HEAD_H = 50, 56


def slug(repo):
    return re.sub(r"[^a-z0-9]+", "-", repo.split("/")[-1].lower()).strip("-")


def frame(h, body, label, seed, serif=True):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{esc(label)}">
  <defs>{film_defs(W, h, seed=seed)}</defs>
  {font_css(serif=serif)}
  <rect width="{W}" height="{h}" fill="{INK}"/>
  {body}
  {film_overlay(W, h, vignette=False)}
</svg>
'''


def head(fname, label, note, seed):
    # panel_head draws its label at y=34 and rule at y=46; that fits HEAD_H.
    write_svg(f"assets/{fname}",
              frame(HEAD_H, panel_head(W, label, note), label, seed, serif=False))


def row(e, i, seed):
    body = (f'<text x="24" y="22" font-family="{SERIF}" font-size="18" '
            f'fill="{SILVER}">{esc(e["name"])}</text>'
            f'<text x="24" y="39" font-family="{MONO}" font-size="10.5" '
            f'fill="{SILVER_DIM}">{esc(e["note"])}</text>'
            f'<text x="{W - 24}" y="22" text-anchor="end" font-family="{MONO}" '
            f'font-size="10" fill="{ASH}">{esc(e.get("count", ""))}</text>')
    svg = frame(ROW_H,
                reveal(0.3 + i * 0.15, body, dur=0.9)
                + f'<rect x="24" y="{ROW_H - 1}" width="{W - 48}" height="1" fill="{HAIRLINE}"/>',
                f'{e["name"]}: {e["note"]}', seed)
    write_svg(f"assets/note_{slug(e['repo'])}.svg", svg)


def build():
    notes = profile()["field_notes"]
    head("notes_head_ctf.svg", "writeups", f"{len(notes['ctf'])} entries", 51)
    head("notes_head_builds.svg", "other builds", f"{len(notes['builds'])} entries", 52)
    for col, entries in enumerate((notes["ctf"], notes["builds"])):
        for i, e in enumerate(entries):
            row(e, i, 60 + col * 10 + i)
    # pad for uneven columns
    write_svg("assets/note_blank.svg", frame(ROW_H, "", "", 59, serif=False))


if __name__ == "__main__":
    build()
