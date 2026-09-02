"""hero.svg — animated mechanical-knight game dossier for the profile README."""

import base64
from pathlib import Path

from lib import (BG, PANEL, BORDER, GREEN, WHITE, GREY, RED, PAPER,
                 MONO, esc, write_svg, profile)

W, H = 860, 500
ROOT = Path(__file__).resolve().parent.parent


def image_data(path):
    raw = path.read_bytes()
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


def ascii_frame(lines):
    return "".join(
        f'<tspan x="0" dy="{0 if i == 0 else 10}">{esc(line)}</tspan>'
        for i, line in enumerate(lines)
    )


ASCII_FRAMES = [
    [
        r"       /\\", r"   ___/  \\___", r" /|  _    _  |\\",
        r"/_| /_\\  /_\\ |_\\", r"|_|    /\\    |_ |",
        r"  \\__/  \\__/", r"     |::|", r"  ___|::|___",
    ],
    [
        r"       /\\  .", r" . ___/  \\___", r" /|  _  # _  |\\",
        r"/_| /_\\  /_\\ |#\\", r"|_|    /\\    |_ |",
        r"  \\__/# \\__/", r"   # |::|", r"  ___|::|___",
    ],
    [
        r"    .  /\\", r"   ___/  \\___ #", r"#/|  _    _  |\\",
        r"/_| /_\\  /_\\ |_\\", r"|_| #  /\\    |_ |",
        r"  \\__/  \\__/#", r"     |::|", r"  ___|::|___",
    ],
]


def build():
    cfg = profile()
    ident = cfg["identity"]
    projects = " / ".join(p["name"].upper() for p in cfg["projects"])
    art = image_data(ROOT / "assets" / "mechanical-knight-medallion.png")
    frames = [ascii_frame(lines) for lines in ASCII_FRAMES]

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="heroTitle heroDesc">
  <title id="heroTitle">{esc(ident['name'])} — mechanical knight developer profile</title>
  <desc id="heroDesc">Animated street-racing game dossier with a silver chess-knight machine emblem, wanted stars, ASCII telemetry, and current projects.</desc>
  <defs>
    <radialGradient id="stage" cx="67%" cy="46%" r="68%">
      <stop offset="0" stop-color="#18220f"/>
      <stop offset=".34" stop-color="#090d09"/>
      <stop offset="1" stop-color="{BG}"/>
    </radialGradient>
    <linearGradient id="slash" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="{RED}" stop-opacity=".05"/>
      <stop offset=".52" stop-color="{RED}" stop-opacity=".74"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity=".12"/>
    </linearGradient>
    <linearGradient id="scanFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
      <stop offset=".48" stop-color="{GREEN}" stop-opacity=".2"/>
      <stop offset=".52" stop-color="{WHITE}" stop-opacity=".46"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M24 0H0V24" fill="none" stroke="{WHITE}" stroke-opacity=".045"/>
      <circle cx="1" cy="1" r=".65" fill="{GREEN}" opacity=".13"/>
    </pattern>
    <pattern id="halftone" width="7" height="7" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.15" fill="{WHITE}" opacity=".1"/>
    </pattern>
    <filter id="paperNoise" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="27" result="n"/>
      <feColorMatrix in="n" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 .13 0"/>
      <feBlend in="SourceGraphic" mode="multiply"/>
    </filter>
    <filter id="limeGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="11"/>
    </filter>
    <filter id="avatarShadow" x="-35%" y="-25%" width="180%" height="170%">
      <feDropShadow dx="-11" dy="14" stdDeviation="12" flood-color="#000" flood-opacity=".8"/>
    </filter>
    <clipPath id="avatarClip"><path d="M330 14H846V486H367L340 424Z"/></clipPath>
    <clipPath id="glitchOne"><path d="M328 94H846V129H328ZM328 248H846V274H328ZM328 398H846V416H328Z"/></clipPath>
    <clipPath id="glitchTwo"><path d="M328 173H846V188H328ZM328 309H846V325H328Z"/></clipPath>
    <clipPath id="asciiClip"><rect x="31" y="326" width="337" height="139"/></clipPath>
    <clipPath id="tickerClip"><rect x="398" y="451" width="419" height="17"/></clipPath>
    <image id="avatarImage" href="{art}" x="328" y="18" width="520" height="478" preserveAspectRatio="xMidYMid slice"/>
    <style><![CDATA[
      .avatar {{ animation: avatarFloat 6s ease-in-out infinite; transform-origin: 66% 52%; }}
      .glitch-a {{ animation: glitchA 4.8s steps(1,end) infinite; }}
      .glitch-b {{ animation: glitchB 4.8s steps(1,end) infinite .08s; }}
      .scanline {{ animation: scan 4.6s linear infinite; }}
      .ticker {{ animation: ticker 11s linear infinite; }}
      .ascii-a {{ animation: frameA 3.2s steps(1,end) infinite; }}
      .ascii-b {{ animation: frameB 3.2s steps(1,end) infinite; }}
      .ascii-c {{ animation: frameC 3.2s steps(1,end) infinite; }}
      .star {{ animation: starPulse 2.4s ease-in-out infinite; }}
      .s2 {{ animation-delay: .12s; }} .s3 {{ animation-delay: .24s; }}
      .s4 {{ animation-delay: .36s; }} .s5 {{ animation-delay: .48s; }}
      .stamp {{ animation: stampJolt 5.5s steps(1,end) infinite; transform-origin: 190px 282px; }}
      @keyframes avatarFloat {{ 0%,100%{{transform:translateY(0) rotate(-.2deg)}} 50%{{transform:translateY(-7px) rotate(.35deg)}} }}
      @keyframes glitchA {{ 0%,78%,100%{{transform:translateX(0);opacity:0}} 79%{{transform:translateX(-12px);opacity:.48}} 82%{{transform:translateX(7px);opacity:.24}} 85%{{transform:translateX(0);opacity:0}} }}
      @keyframes glitchB {{ 0%,78%,100%{{transform:translateX(0);opacity:0}} 80%{{transform:translateX(13px);opacity:.35}} 83%{{transform:translateX(-5px);opacity:.18}} 86%{{transform:translateX(0);opacity:0}} }}
      @keyframes scan {{ 0%{{transform:translateY(-40px);opacity:0}} 8%{{opacity:1}} 92%{{opacity:.8}} 100%{{transform:translateY(540px);opacity:0}} }}
      @keyframes ticker {{ from{{transform:translateX(0)}} to{{transform:translateX(-496px)}} }}
      @keyframes frameA {{ 0%,31%{{opacity:1}} 32%,100%{{opacity:0}} }}
      @keyframes frameB {{ 0%,31%{{opacity:0}} 32%,64%{{opacity:1}} 65%,100%{{opacity:0}} }}
      @keyframes frameC {{ 0%,64%{{opacity:0}} 65%,96%{{opacity:1}} 97%,100%{{opacity:0}} }}
      @keyframes starPulse {{ 0%,100%{{opacity:.42;transform:translateY(0)}} 45%{{opacity:1;transform:translateY(-1px)}} }}
      @keyframes stampJolt {{ 0%,88%,100%{{transform:rotate(-1.6deg)}} 89%{{transform:translateX(-3px) rotate(-2.5deg)}} 91%{{transform:translateX(2px) rotate(.5deg)}} 93%{{transform:rotate(-1.6deg)}} }}
      @media (prefers-reduced-motion: reduce) {{
        .avatar,.glitch-a,.glitch-b,.scanline,.ticker,.ascii-a,.ascii-b,.ascii-c,.star,.stamp {{ animation:none!important; }}
        .ascii-b,.ascii-c,.glitch-a,.glitch-b,.scanline {{ opacity:0!important; }}
      }}
    ]]></style>
  </defs>

  <rect width="{W}" height="{H}" rx="9" fill="url(#stage)"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="9" fill="none" stroke="{BORDER}" stroke-width="2"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="9" fill="url(#grid)"/>
  <path d="M548 -32L721 -9 548 533 391 505Z" fill="url(#slash)" opacity=".68"/>
  <path d="M684 0H860V500H744Z" fill="url(#halftone)" opacity=".68"/>
  <text transform="translate(835 470) rotate(-90)" font-family="Impact,'Arial Narrow',sans-serif" font-size="72" letter-spacing="4" fill="{WHITE}" opacity=".045">KUANTUM</text>

  <!-- registration and dossier marks -->
  <g fill="none" stroke="{GREEN}" stroke-width="1.2" opacity=".8">
    <path d="M18 44V18H44M816 18H842V44M18 456V482H44M816 482H842V456"/>
    <path d="M24 250H51M37.5 236.5V263.5M810 250H837M823.5 236.5V263.5" opacity=".45"/>
  </g>
  <text x="31" y="37" font-family="{MONO}" font-size="9" letter-spacing="1.5" fill="{GREY}">PLAYER PROFILE // BUILD 07</text>
  <text x="697" y="483" font-family="{MONO}" font-size="8" letter-spacing="1.2" fill="{GREY}">LOCAL-FIRST / ONLINE</text>

  <!-- generated mechanical chess-knight centerpiece -->
  <ellipse cx="615" cy="247" rx="192" ry="206" fill="{GREEN}" opacity=".11" filter="url(#limeGlow)"/>
  <g clip-path="url(#avatarClip)" filter="url(#avatarShadow)">
    <g class="avatar"><use href="#avatarImage"/></g>
    <use href="#avatarImage" class="glitch-a" clip-path="url(#glitchOne)" style="mix-blend-mode:screen"/>
    <use href="#avatarImage" class="glitch-b" clip-path="url(#glitchTwo)" opacity="0"/>
  </g>
  <path d="M337 22H846V485H371" fill="none" stroke="{WHITE}" stroke-opacity=".15" stroke-dasharray="2 8"/>

  <!-- identity typography -->
  <text x="30" y="105" font-family="Impact,'Arial Narrow',sans-serif" font-size="76" letter-spacing="1" fill="{WHITE}" stroke="{BG}" stroke-width="4" paint-order="stroke" filter="url(#paperNoise)">{esc(ident['name'].split()[0]).upper()}</text>
  <text x="29" y="173" font-family="Impact,'Arial Narrow',sans-serif" font-size="66" letter-spacing="2" fill="none" stroke="{WHITE}" stroke-width="1.4" opacity=".9">M // KNIGHT</text>
  <g class="stamp">
    <path d="M27 190L349 184 354 220 31 229Z" fill="{PAPER}" filter="url(#paperNoise)"/>
    <text x="43" y="212" font-family="{MONO}" font-size="10.5" font-weight="900" letter-spacing=".6" textLength="294" lengthAdjust="spacingAndGlyphs" fill="{BG}">AI SYSTEMS / APPLICATION SECURITY / FULL-STACK</text>
  </g>
  <text x="32" y="253" font-family="{MONO}" font-size="11" letter-spacing="1.1" fill="{GREEN}">github.com/{esc(ident['handle'])}</text>
  <line x1="31" y1="266" x2="354" y2="266" stroke="{WHITE}" stroke-opacity=".28"/>

  <!-- punk project tape -->
  <g transform="rotate(-1.8 193 292)">
    <path d="M25 276L364 270 359 311 29 316Z" fill="{RED}"/>
    <path d="M35 279L44 314M60 278L69 313M332 272L341 309" stroke="{BG}" stroke-opacity=".25" stroke-width="4"/>
    <text x="43" y="298" font-family="{MONO}" font-size="10" font-weight="800" letter-spacing=".9" fill="{WHITE}">CURRENT LOADOUT</text>
    <text x="157" y="298" font-family="{MONO}" font-size="10" font-weight="800" fill="{WHITE}">{esc(projects)}</text>
  </g>

  <!-- animated ASCII helmet console -->
  <rect x="31" y="326" width="337" height="139" fill="{PANEL}" stroke="{BORDER}"/>
  <path d="M31 345H368" stroke="{BORDER}"/>
  <circle cx="44" cy="336" r="2.5" fill="{RED}"/>
  <circle cx="54" cy="336" r="2.5" fill="{GREEN}"/>
  <text x="66" y="340" font-family="{MONO}" font-size="8.5" letter-spacing="1" fill="{GREY}">ASCII KNIGHT // LIVE SIGNAL</text>
  <g clip-path="url(#asciiClip)">
    <g transform="translate(49 363)">
      <text class="ascii-a" x="0" y="0" xml:space="preserve" font-family="{MONO}" font-size="8.6" fill="{GREEN}">{frames[0]}</text>
      <text class="ascii-b" x="0" y="0" xml:space="preserve" font-family="{MONO}" font-size="8.6" fill="{WHITE}" opacity="0">{frames[1]}</text>
      <text class="ascii-c" x="0" y="0" xml:space="preserve" font-family="{MONO}" font-size="8.6" fill="{RED}" opacity="0">{frames[2]}</text>
    </g>
    <g transform="translate(190 366)" font-family="{MONO}" font-size="8.5">
      <text y="0" fill="{GREY}">STATUS</text><text x="72" y="0" fill="{GREEN}">ONLINE</text>
      <text y="19" fill="{GREY}">MODE</text><text x="72" y="19" fill="{WHITE}">BUILD / BREAK</text>
      <text y="38" fill="{GREY}">SIGNAL</text><text x="72" y="38" fill="{GREEN}">████████░░</text>
      <text y="57" fill="{GREY}">STACK</text><text x="72" y="57" fill="{WHITE}">AI + APPSEC</text>
      <text y="76" fill="{GREY}">NODE</text><text x="72" y="76" fill="{RED}">KK-07</text>
    </g>
  </g>

  <!-- wanted-level game HUD -->
  <g transform="translate(631 33)">
    <rect width="196" height="72" fill="{BG}" fill-opacity=".86" stroke="{BORDER}"/>
    <path d="M0 0H196L188 9H0Z" fill="{RED}"/>
    <text x="13" y="29" font-family="{MONO}" font-size="8.5" letter-spacing="1.5" fill="{GREY}">WANTED LEVEL // 05</text>
    <g font-family="{MONO}" font-size="26" letter-spacing="4" fill="{RED}">
      <text class="star s1" x="12" y="59">★</text><text class="star s2" x="46" y="59">★</text>
      <text class="star s3" x="80" y="59">★</text><text class="star s4" x="114" y="59">★</text>
      <text class="star s5" x="148" y="59">★</text>
    </g>
  </g>

  <!-- ticker and moving scan -->
  <g clip-path="url(#avatarClip)" opacity=".75">
    <rect class="scanline" x="338" y="-30" width="515" height="34" fill="url(#scanFade)"/>
  </g>
  <rect x="389" y="448" width="438" height="25" fill="{BG}" fill-opacity=".9" stroke="{BORDER}"/>
  <g clip-path="url(#tickerClip)">
    <text class="ticker" x="398" y="464" font-family="{MONO}" font-size="8.5" letter-spacing="1.2" fill="{GREEN}">KUANTUMKNIGHT :: AI SYSTEMS :: APPSEC :: FULL-STACK :: LOCAL-FIRST :: KUANTUMKNIGHT :: AI SYSTEMS :: APPSEC :: FULL-STACK :: LOCAL-FIRST ::</text>
  </g>
</svg>
'''
    write_svg("assets/hero.svg", svg)


if __name__ == "__main__":
    build()
