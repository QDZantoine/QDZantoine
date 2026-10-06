#!/usr/bin/env python3
"""
Bannière d'en-tête du profil, aux couleurs d'Heliara (soleil levant orange sur
anthracite chaud). Les rôles défilent en fondu, le soleil "respire".

    python scripts/render_header_svg.py [output.svg]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "header.svg")

W, H = 860, 300
BG = "#0b0b0d"
BG2 = "#151517"
FRAME = "#2a2a2e"
INK = "#f2f2f0"
MUTED = "#8f8f89"
ORANGE = "#f0824b"
ORANGE_DEEP = "#e9591f"

NAME = "Antoine Quendez"
ROLES = ["Développeur full stack", "Formateur web & IA", "Co-fondateur d'Heliara"]
TAGLINE = "Je conçois des outils qui s'adaptent au métier, pas l'inverse."
LOCATION = "MONTPELLIER · BÉZIERS · FRANCE"
STACK = "TypeScript  ·  React  ·  Node.js  ·  IA auto-hébergée"

ROLE_DUR = 3.2                     # secondes d'affichage par rôle
CYCLE = ROLE_DUR * len(ROLES)
SANS = "'Schibsted Grotesk', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "'Spline Sans Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# soleil levant, en bas à droite
SUN_X, SUN_Y, SUN_R = 700, 300, 92

# part du cycle pendant laquelle un rôle est visible (fondu compris)
share = 100 / len(ROLES)
fade = share * 0.15

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
    '<style>',
    f'.name{{font:700 54px {SANS};fill:{INK};letter-spacing:-1.5px}}',
    f'.role{{font:600 24px {SANS};fill:{ORANGE};opacity:0;animation:role {CYCLE}s infinite}}',
    f'.tag{{font:italic 400 17px {SANS};fill:{MUTED}}}',
    f'.mono{{font:500 12px {MONO};fill:{MUTED};letter-spacing:2px}}',
    f'.stack{{font:500 13px {MONO};fill:{INK};opacity:.75}}',
    f'@keyframes role{{0%{{opacity:0;transform:translateY(8px)}}'
    f'{fade:.1f}%{{opacity:1;transform:translateY(0)}}'
    f'{share - fade:.1f}%{{opacity:1;transform:translateY(0)}}'
    f'{share:.1f}%{{opacity:0;transform:translateY(-8px)}}100%{{opacity:0}}}}',
    '.in{opacity:0;animation:in .8s ease-out forwards}',
    '@keyframes in{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}',
    '.sun{transform-origin:700px 300px;animation:rise 1.6s cubic-bezier(.2,.7,.2,1) both,breathe 6s 1.6s ease-in-out infinite}',
    '@keyframes rise{from{transform:translateY(60px);opacity:0}to{transform:none;opacity:1}}',
    '@keyframes breathe{50%{transform:scale(1.04)}}',
    '.ray{transform-origin:700px 300px;animation:spin 60s linear infinite}',
    '@keyframes spin{to{transform:rotate(360deg)}}',
    '.dot{animation:pulse 2s ease-in-out infinite}',
    '@keyframes pulse{50%{opacity:.25}}',
    '@media (prefers-reduced-motion: reduce){*{animation:none!important;opacity:1!important}}',
    '</style>',
    '<defs>',
    f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG2}"/>'
    f'<stop offset="1" stop-color="{BG}"/></linearGradient>',
    f'<radialGradient id="halo" cx="{SUN_X}" cy="{SUN_Y}" r="330" gradientUnits="userSpaceOnUse">'
    f'<stop offset="0" stop-color="{ORANGE_DEEP}" stop-opacity=".38"/>'
    f'<stop offset=".45" stop-color="{ORANGE_DEEP}" stop-opacity=".10"/>'
    f'<stop offset="1" stop-color="{ORANGE_DEEP}" stop-opacity="0"/></radialGradient>',
    f'<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ORANGE}"/>'
    f'<stop offset="1" stop-color="{ORANGE_DEEP}"/></linearGradient>',
    f'<clipPath id="card"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
    '</defs>',
    '<g clip-path="url(#card)">',
    f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
    f'<rect width="{W}" height="{H}" fill="url(#halo)"/>',
]

# rayons fins autour du soleil
parts.append('<g class="ray">')
for i in range(24):
    angle = i * 15
    parts.append(
        f'<line x1="{SUN_X}" y1="{SUN_Y - SUN_R - 18}" x2="{SUN_X}" y2="{SUN_Y - SUN_R - 46}" '
        f'stroke="{ORANGE}" stroke-opacity=".35" stroke-width="2" stroke-linecap="round" '
        f'transform="rotate({angle} {SUN_X} {SUN_Y})"/>'
    )
parts.append('</g>')

# soleil + anneaux
parts.append('<g class="sun">')
for k, (r, op) in enumerate([(SUN_R + 70, .10), (SUN_R + 120, .06)]):
    parts.append(f'<circle cx="{SUN_X}" cy="{SUN_Y}" r="{r}" fill="none" stroke="{ORANGE}" stroke-opacity="{op}"/>')
parts.append(f'<circle cx="{SUN_X}" cy="{SUN_Y}" r="{SUN_R}" fill="url(#sun)"/>')
parts.append('</g>')

# horizon
parts.append(f'<line x1="0" y1="{H - 0.5}" x2="{W}" y2="{H - 0.5}" stroke="{ORANGE}" stroke-opacity=".5"/>')

# textes
x = 48
parts.append(f'<g class="in" style="animation-delay:.1s">'
             f'<circle class="dot" cx="{x + 4}" cy="60" r="4" fill="{ORANGE}"/>'
             f'<text class="mono" x="{x + 18}" y="64">{LOCATION}</text></g>')
parts.append(f'<text class="name in" x="{x - 3}" y="128" style="animation-delay:.25s">{NAME}</text>')
for i, role in enumerate(ROLES):
    parts.append(f'<text class="role" x="{x}" y="170" style="animation-delay:{i * ROLE_DUR:.1f}s">'
                 f'{role.replace("&", "&amp;")}</text>')
parts.append(f'<text class="tag in" x="{x}" y="214" style="animation-delay:.5s">« {TAGLINE} »</text>')
parts.append(f'<text class="stack in" x="{x}" y="262" style="animation-delay:.7s">{STACK}</text>')

parts.append('</g>')
parts.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{FRAME}"/>')
parts.append('</svg>')

svg = "".join(parts)
open(OUT, "w").write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(svg) // 1024} KB")
