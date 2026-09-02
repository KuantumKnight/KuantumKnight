"""Animated section, mission, contact, and footer strips for the README."""

from lib import (BG, PANEL, BORDER, GREEN, WHITE, GREY, RED, PAPER, MONO,
                 esc, profile, write_svg)

BW, BH = 860, 68


def banner(fname, title, subtitle, mark=""):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" role="img" aria-label="{esc(title)}: {esc(subtitle)}">
  <defs>
    <pattern id="speed" width="18" height="18" patternUnits="userSpaceOnUse" patternTransform="skewX(-24)">
      <rect width="7" height="18" fill="{WHITE}" opacity=".035"/>
    </pattern>
    <linearGradient id="beam" x1="0" x2="1">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{GREEN}" stop-opacity=".58"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="frame"><rect x="1" y="1" width="{BW-2}" height="{BH-2}"/></clipPath>
    <style><![CDATA[
      .beam {{ animation: beam 5.4s cubic-bezier(.2,.7,.2,1) infinite; }}
      .pulse {{ animation: pulse 1.7s steps(2,end) infinite; }}
      .tick {{ animation: tick 2.8s steps(4,end) infinite; }}
      @keyframes beam {{ 0%{{transform:translateX(-230px);opacity:0}} 12%{{opacity:1}} 72%{{transform:translateX(1040px);opacity:.8}} 73%,100%{{transform:translateX(1040px);opacity:0}} }}
      @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:.25}} }}
      @keyframes tick {{ 0%,100%{{transform:translateX(0)}} 50%{{transform:translateX(7px)}} }}
      @media (prefers-reduced-motion: reduce) {{ .beam,.pulse,.tick {{ animation:none!important; }} .beam {{ display:none; }} }}
    ]]></style>
  </defs>
  <rect x="1" y="1" width="{BW-2}" height="{BH-2}" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>
  <rect x="1" y="1" width="{BW-2}" height="{BH-2}" fill="url(#speed)"/>
  <path d="M1 8L322 8 295 60H1Z" fill="{PAPER}"/>
  <path d="M300 8H375L347 60H272Z" fill="{RED}"/>
  <path d="M365 34H838" stroke="{WHITE}" stroke-opacity=".24"/>
  <path d="M365 28H610" stroke="{GREEN}" stroke-width="3"/>
  <g class="tick">
    <path d="M626 24l12 10-12 10M646 24l12 10-12 10M666 24l12 10-12 10" fill="none" stroke="{RED}" stroke-width="2"/>
  </g>
  <text x="18" y="46" font-family="Impact,'Arial Narrow',sans-serif" font-size="33" letter-spacing="2" fill="{BG}">// {esc(title.upper())}</text>
  <text x="381" y="53" font-family="{MONO}" font-size="10.5" letter-spacing=".8" fill="{GREY}">{esc(subtitle.upper())}</text>
  <g class="pulse">
    <circle cx="824" cy="19" r="3.5" fill="{GREEN}"/>
    <text x="814" y="22" text-anchor="end" font-family="{MONO}" font-size="9" letter-spacing="1" fill="{GREEN}">LIVE</text>
  </g>
  <text x="838" y="53" text-anchor="end" font-family="{MONO}" font-size="15" letter-spacing="3" fill="{RED}">{esc(mark)}</text>
  <g clip-path="url(#frame)"><rect class="beam" x="-230" y="0" width="180" height="{BH}" fill="url(#beam)" transform="skewX(-24)"/></g>
</svg>
'''
    write_svg(f"assets/{fname}", svg)


def note_panel(note, index):
    W, H = 860, 74
    name = note["name"].upper()
    number = f"{index + 1:02}"
    accent = GREEN if index != 1 else RED
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(name)}: {esc(note['note'])}">
  <defs>
    <linearGradient id="scan" x1="0" x2="1"><stop stop-color="{accent}" stop-opacity="0"/><stop offset=".5" stop-color="{accent}" stop-opacity=".22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>
    <clipPath id="clip"><path d="M1 1H859V73H1Z"/></clipPath>
    <style><![CDATA[
      .scan {{ animation: scan {5.1 + index * .45:.2f}s linear infinite; }}
      .check {{ animation: check 2.2s steps(2,end) infinite; }}
      .arrow {{ animation: arrow 1.4s ease-in-out infinite; }}
      @keyframes scan {{ from{{transform:translateX(-180px)}} to{{transform:translateX(1040px)}} }}
      @keyframes check {{ 0%,72%,100%{{opacity:1}} 80%{{opacity:.28}} }}
      @keyframes arrow {{ 0%,100%{{transform:translateX(0)}} 50%{{transform:translateX(6px)}} }}
      @media (prefers-reduced-motion: reduce) {{ .scan,.check,.arrow {{ animation:none!important; }} .scan {{ display:none; }} }}
    ]]></style>
  </defs>
  <path d="M1 1H859V73H1Z" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>
  <path d="M1 1H117L96 73H1Z" fill="{BG}"/>
  <path d="M117 1H128L107 73H96Z" fill="{accent}"/>
  <text x="18" y="30" font-family="{MONO}" font-size="9" letter-spacing="1.4" fill="{GREY}">MISSION</text>
  <text x="18" y="58" font-family="Impact,'Arial Narrow',sans-serif" font-size="31" fill="{accent}">{number}</text>
  <text x="143" y="31" font-family="Impact,'Arial Narrow',sans-serif" font-size="25" letter-spacing="1" fill="{WHITE}">{esc(name)}</text>
  <text x="144" y="54" font-family="{MONO}" font-size="11" fill="{GREY}">{esc(note['note'])}</text>
  <g class="check">
    <rect x="701" y="18" width="118" height="38" fill="{BG}" stroke="{accent}"/>
    <text x="760" y="42" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1" fill="{accent}">[✓] UNLOCKED</text>
  </g>
  <g class="arrow" fill="none" stroke="{accent}" stroke-width="2"><path d="M826 26l12 11-12 11"/></g>
  <g clip-path="url(#clip)"><rect class="scan" x="-180" width="130" height="{H}" fill="url(#scan)" transform="skewX(-18)"/></g>
</svg>
'''
    slug = ("blackbox" if index == 0 else "zeroday" if index == 1 else "synthetix")
    write_svg(f"assets/note_{slug}.svg", svg)


def contact_tile(fname, label, value, index, accent):
    W, H = 270, 68
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}: {esc(value)}">
  <defs>
    <linearGradient id="s" x1="0" x2="1"><stop stop-color="{accent}" stop-opacity="0"/><stop offset=".5" stop-color="{accent}" stop-opacity=".23"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></linearGradient>
    <style><![CDATA[
      .rail {{ animation: rail {4.4 + index * .4:.1f}s linear infinite; }}
      .lamp {{ animation: lamp 1.8s steps(2,end) infinite; animation-delay:{index * .18:.2f}s; }}
      @keyframes rail {{ from{{transform:translateX(-100px)}} to{{transform:translateX(360px)}} }}
      @keyframes lamp {{ 0%,100%{{opacity:1}} 50%{{opacity:.2}} }}
      @media (prefers-reduced-motion: reduce) {{ .rail,.lamp {{ animation:none!important; }} .rail {{ display:none; }} }}
    ]]></style>
  </defs>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" fill="{PANEL}" stroke="{BORDER}" stroke-width="2"/>
  <path d="M1 1H44L32 67H1Z" fill="{accent}"/>
  <text x="18" y="42" font-family="Impact,'Arial Narrow',sans-serif" font-size="24" fill="{BG}">{index+1:02}</text>
  <circle class="lamp" cx="249" cy="18" r="3.5" fill="{accent}"/>
  <text x="57" y="27" font-family="{MONO}" font-size="9" letter-spacing="1.5" fill="{accent}">{esc(label.upper())} // LINK</text>
  <text x="57" y="49" font-family="{MONO}" font-size="10.5" fill="{WHITE}">{esc(value)}</text>
  <rect class="rail" x="-100" y="0" width="80" height="{H}" fill="url(#s)" transform="skewX(-20)"/>
</svg>
'''
    write_svg(f"assets/{fname}", svg)


def divider():
    W, H = 860, 30
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="animated speed divider">
  <defs><style><![CDATA[
    .dash {{ animation: dash 3.8s linear infinite; }}
    .tag {{ animation: tag 2.7s steps(2,end) infinite; }}
    @keyframes dash {{ from{{transform:translateX(-260px)}} to{{transform:translateX(900px)}} }}
    @keyframes tag {{ 0%,92%,100%{{transform:translateX(0)}} 94%{{transform:translateX(-3px)}} 96%{{transform:translateX(3px)}} }}
    @media (prefers-reduced-motion: reduce) {{ .dash,.tag {{ animation:none!important; }} }}
  ]]></style></defs>
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <path d="M0 15H{W}" stroke="{WHITE}" stroke-opacity=".2" stroke-dasharray="3 8"/>
  <g class="dash" fill="{GREEN}"><path d="M-260 11h86l18 4-18 4h-86zM-145 11h42l18 4-18 4h-42z"/></g>
  <g class="tag"><path d="M397 4h66l-8 22h-66z" fill="{RED}"/><text x="426" y="19" text-anchor="middle" font-family="{MONO}" font-size="9" font-weight="700" fill="{PAPER}">KK-07</text></g>
</svg>
'''
    write_svg("assets/divider.svg", svg)


def footer():
    W, H = 860, 42
    line = "PROFILE PIPELINE // profile.json + PUBLIC GITHUB DATA // FAIL-SOFT ASSET REBUILD // "
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Profile assets are generated from profile.json and public GitHub data">
  <defs>
    <clipPath id="lane"><rect x="92" y="0" width="768" height="{H}"/></clipPath>
    <style><![CDATA[
      .copy {{ animation: copy 13s linear infinite; }}
      .lamp {{ animation: lamp 1.7s steps(2,end) infinite; }}
      @keyframes copy {{ from{{transform:translateX(0)}} to{{transform:translateX(-620px)}} }}
      @keyframes lamp {{ 0%,100%{{opacity:1}} 50%{{opacity:.2}} }}
      @media (prefers-reduced-motion: reduce) {{ .copy,.lamp {{ animation:none!important; }} }}
    ]]></style>
  </defs>
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="{BORDER}"/>
  <path d="M1 1h98L85 41H1Z" fill="{PAPER}"/>
  <circle class="lamp" cx="18" cy="21" r="4" fill="{RED}"/>
  <text x="31" y="25" font-family="{MONO}" font-size="9" font-weight="800" fill="{BG}">AUTO-RUN</text>
  <g clip-path="url(#lane)"><text class="copy" x="112" y="25" font-family="{MONO}" font-size="9.5" letter-spacing="1.1" fill="{GREY}">{line}{line}</text></g>
</svg>
'''
    write_svg("assets/footer.svg", svg)


def build():
    banner("banner_work.svg", "selected work", "three active systems / choose loadout", "★★★★★")
    banner("banner_notes.svg", "field notes", "missions cleared / proof archive", "03/03")
    banner("banner_telemetry.svg", "live activity", "public github telemetry", "SYNC")
    banner("banner_stack.svg", "working set", "equipment / runtime loadout", "10")
    banner("banner_contact.svg", "contact", "direct encrypted links", "OPEN")
    for i, note in enumerate(profile()["field_notes"]):
        note_panel(note, i)
    contact = profile()["contact"]
    contact_tile("contact_github.svg", "github", "@KuantumKnight", 0, GREEN)
    contact_tile("contact_email.svg", "email", contact["email"], 1, RED)
    contact_tile("contact_linkedin.svg", "linkedin", "s4rv3sh-m", 2, PAPER)
    divider()
    footer()


if __name__ == "__main__":
    build()
