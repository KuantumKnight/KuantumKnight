"""
card_*.svg — cinematic project "dossier" cards.

one tactical readout per featured project: index, name, repo path, terse brief,
stat chips, a faint watermark icon (baked Lucide line art), HUD corner brackets,
a slow scan shimmer.
each card is wrapped in a markdown link in the README, so the whole card is
clickable despite being an image.
"""

from lib import (BG, PANEL, BORDER, GREEN, GREY, WHITE, CYAN, RED, AMBER, LIME,
                 MONO, esc, write_svg, collect)
from icons import CARD_ICONS

W, H = 860, 168


def wrap(text, n=58, maxlines=2):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= n:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
        if len(lines) == maxlines:
            break
    if cur and len(lines) < maxlines:
        lines.append(cur)
    return lines[:maxlines]


def chip(x, y, text, accent=False):
    w = len(text) * 7.4 + 18
    col = CYAN if accent else GREEN
    return (f'<rect x="{x}" y="{y}" width="{w:.0f}" height="20" rx="4" '
            f'fill="{col}" fill-opacity="0.08" stroke="{col}" stroke-opacity="0.5"/>'
            f'<text x="{x+w/2:.0f}" y="{y+14}" text-anchor="middle" font-size="11" '
            f'fill="{col}" font-family="{MONO}">{esc(text)}</text>'), x + w + 8


def watermark(icon):
    """a baked Lucide line icon (24x24) as a faint neon watermark, right side.
    scaled ~4.5x; stroke-width 0.55 in local units renders ~2.5px at that scale."""
    inner = CARD_ICONS[icon]
    return (f'<g opacity="0.10" transform="translate(705,30) scale(4.5)" '
            f'fill="none" stroke="{GREEN}" stroke-width="0.55" '
            f'stroke-linecap="round" stroke-linejoin="round">{inner}</g>')


def card(fname, idx, name, repo, brief, chips, icon, idx_accent="01"):
    chip_svg, cx0 = "", 92
    for i, (t, acc) in enumerate(chips):
        s, cx0 = chip(cx0, 128, t, acc)
        chip_svg += s
    brief_lines = wrap(brief)
    brief_svg = "".join(
        f'<text x="92" y="{96+i*18}" font-size="13" fill="{WHITE}" font-family="{MONO}">{esc(ln)}</text>'
        for i, ln in enumerate(brief_lines))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(name)} — {esc(brief)}">
  <defs>
    <linearGradient id="shim{idx}" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{GREEN}" stop-opacity="0.06"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="cclip{idx}"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10"/></clipPath>
  </defs>

  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="10" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="2" y="2" width="5" height="{H-4}" fill="{GREEN}" opacity="0.85">
    <animate attributeName="opacity" values="0.85;0.4;0.85" dur="3s" repeatCount="indefinite"/>
  </rect>

  <!-- watermark icon -->
  {watermark(icon)}

  <!-- index -->
  <text x="34" y="86" font-size="46" font-weight="700" fill="{GREEN}" fill-opacity="0.16" font-family="{MONO}">{idx_accent}</text>

  <!-- title + repo -->
  <text x="92" y="48" font-size="22" font-weight="700" fill="{GREEN}" font-family="{MONO}">{esc(name)}</text>
  <text x="92" y="70" font-size="12" fill="{GREY}" font-family="{MONO}">› github.com/{esc(repo)}</text>

  <!-- brief -->
  {brief_svg}

  <!-- chips -->
  {chip_svg}

  <!-- hud brackets + scan shimmer -->
  <path d="M14,16 L14,8 L26,8" fill="none" stroke="{GREEN}" stroke-opacity="0.5"/>
  <path d="M{W-14},{H-16} L{W-14},{H-8} L{W-26},{H-8}" fill="none" stroke="{GREEN}" stroke-opacity="0.5"/>
  <g clip-path="url(#cclip{idx})">
    <rect x="-200" y="1" width="200" height="{H-2}" fill="url(#shim{idx})">
      <animate attributeName="x" values="-200;{W};{W}" keyTimes="0;0.6;1" dur="6s" begin="{idx*1.3}s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>
'''
    write_svg(f"assets/{fname}", svg)


def build():
    d = collect()
    bb = d["bugbouncer_stars"]
    card("card_bugbouncer.svg", 0, "bugbouncer",
         "KuantumKnight/bugbouncer",
         "local-first stability engine. catches architectural failures your tests can't see — then hands you the fix.",
         [(f"{bb}★", True), ("typescript", False), ("sqlite-wasm", False), ("next.js 16", False)],
         "bug", "01")
    card("card_synthetix.svg", 1, "synthetix",
         "KuantumKnight/Synthetix",
         "finds duplicate defects and rewrites weak bug reports into ones engineers actually act on.",
         [("python", False), ("defect-dedup", False), ("triage", False)],
         "dup", "02")
    card("card_zeroday.svg", 2, "zeroday heist · writeups",
         "KuantumKnight/ZeroDayHeist_CTF_Writeups",
         "forensics, reverse engineering, osint, steganography, crypto. full notes, not just flags.",
         [("17 flags", True), ("ctf", False), ("writeups", False)],
         "flag", "03")


if __name__ == "__main__":
    build()
