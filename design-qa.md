# Design QA — KuantumKnight profile README v2

## Evidence

- Source visual truth: C:\Users\Sarvesh M\.codex\generated_images\01a05403-831c-7ae0-8e89-263a72d010bf\exec-7a354bd6-1b3d-4e86-9b8a-2889a5dbd94a.png
- Browser-rendered desktop implementation: C:\Users\Sarvesh M\.codex\visualizations\2026\08\30\01a05403-831c-7ae0-8e89-263a72d010bf\readme-v2-desktop-final.png
- Browser-rendered mobile implementation: C:\Users\Sarvesh M\.codex\visualizations\2026\08\30\01a05403-831c-7ae0-8e89-263a72d010bf\readme-v2-mobile-final.png
- Combined comparison input: C:\Users\Sarvesh M\.codex\visualizations\2026\08\30\01a05403-831c-7ae0-8e89-263a72d010bf\design-comparison-final.png
- Source pixels: 1487 × 1058.
- Desktop capture: 920 × 1100 at device scale 1; the README content column is 860 CSS px.
- Mobile capture: 420 × 3200 at device scale 1; assets scale or wrap inside the narrow content column.
- State: dark GitHub-style surface, top of profile, initial animation state.

## Full-view comparison

The combined board was inspected as one comparison input. The implementation preserves the source's primary hierarchy: chrome knight on the left, condensed identity on the right, vertical handle, dirty-paper role strip, green ASCII signal, five red game stars, and three black/red/paper project posters. The implementation intentionally extends the one-frame concept into a vertically readable GitHub profile rather than compressing telemetry, stack, notes, and contact into the hero.

## Focused region comparison

The desktop capture was inspected at native size for the hero and three poster cards. The generated chrome and engraved project artwork remain sharp at rendered size; transparent edges have no visible halo. Project names, repository paths, descriptions, and stack labels are code-rendered and legible rather than baked into generated imagery. A separate focused comparison was unnecessary after the native desktop inspection because the complete above-the-fold region is visible in the combined board.

## Required fidelity surfaces

- Fonts and typography: condensed Impact/Arial Narrow fallback and monospace text preserve the source's editorial/game-menu contrast. The implementation is intentionally cleaner than the distressed mock so GitHub text remains readable. No clipping remains in the concise AI SYSTEMS · APPSEC · FULL-STACK strip.
- Spacing and layout rhythm: 860 px hero and section strips align; three 270 px posters fit the desktop row with balanced gaps. On narrow screens, cards wrap to a single column and telemetry panels stack.
- Colors and tokens: ink black, dirty paper, liquid silver, signal green, proofing red, and restrained cyan are consistent across generated and live-data panels.
- Image quality and asset fidelity: the hero uses a real generated transparent chrome-knight asset. Each project uses a real generated poster illustration. No placeholder imagery remains.
- Copy and content: generic slogans, fake coordinates, QR codes, fake metrics, and invented claims were removed. Visible copy comes from profile.json and public GitHub data.
- Icons: working-set logos reuse the existing Simple Icons sources. Technologies without a bundled logo use text labels instead of invented marks.
- Accessibility: README images include descriptive alt text and all project/contact actions are standard links. Motion is decorative and does not gate content. A reduced-motion variant remains optional follow-up polish.
- Browser/interaction check: the static README preview rendered in headless Chrome with no reported console or asset-loading errors. There is no JavaScript UI; project, field-note, and contact destinations are ordinary anchors in README.md.

## Comparison history

1. Initial implementation: project poster artwork did not render because nested SVG resources were external, and the ASCII strip appeared empty at the initial frame.
   - Fix: optimized the three generated poster sources and embedded them directly in the standalone card SVGs; added a visible resting ASCII knight while retaining the moving frame.
   - Post-fix evidence: readme-v2-full-r2.png.
2. Second pass: the long role label approached the hero's right edge at narrow scale, and the original transparent hero source exceeded its useful display density.
   - Fix: shortened only the visible label to factual APPSEC, preserved the full accessible role, and downscaled the transparent source from 1024 × 1536 to 620 × 930 while retaining alpha.
   - Post-fix evidence: readme-v2-desktop-final.png and readme-v2-mobile-final.png.

## Findings

No actionable P0, P1, or P2 findings remain.

## Follow-up polish

- [P3] Add explicit reduced-motion static states inside the animated SVG generators.
- [P3] Recheck the final profile once merged because GitHub's image proxy can introduce short cache delays.

## Final result

final result: passed
