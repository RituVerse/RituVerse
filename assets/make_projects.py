#!/usr/bin/env python3
"""Generate self-hosted SVG project cards (assets/project-*.svg).

Only real repositories owned by RituVerse are included; descriptions are
derived from the repositories' own READMEs / metadata.
"""
from pathlib import Path

FONT = "'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,monospace"

PROJECTS = [
    dict(
        slug="portfolio", index="01", featured=True,
        title="Personal Portfolio",
        repo="RituVerse/my-portfolio",
        accent="#22d3ee",
        tags=["HTML5", "CSS3", "JavaScript", "Canvas API", "Responsive"],
        lines=[
            "A dark, futuristic portfolio built from scratch with zero frameworks.",
            "Particle-network canvas background, typing animation, scroll-reveal sections,",
            "3D tilt project cards, animated skill bars and a mobile hamburger menu.",
        ],
        footer="Live on GitHub Pages",
    ),
    dict(
        slug="weather", index="02", featured=False,
        title="Weather App",
        repo="RituVerse/weather-app",
        accent="#38bdf8",
        tags=["HTML", "CSS", "JavaScript", "Fetch API"],
        lines=[
            "Search any city and get live temperature, conditions",
            "and a weather icon from the OpenWeatherMap API.",
            "Enter-key support, input validation and error states.",
        ],
        footer="Vanilla JS · API integration",
    ),
    dict(
        slug="netflix", index="03", featured=False,
        title="Netflix Clone",
        repo="RituVerse/Netflix-Clone",
        accent="#8b5cf6",
        tags=["HTML", "CSS", "Responsive Layout"],
        lines=[
            "A responsive Netflix India landing page recreated in",
            "pure HTML & CSS — focused on layout, visual hierarchy,",
            "spacing and responsive behaviour across screen sizes.",
        ],
        footer="Pure HTML & CSS",
    ),
]


def chip_w(t: str) -> int:
    return int(len(t) * 6.6) + 20


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def card(p: dict) -> str:
    W = 900 if p["featured"] else 440
    H = 210
    a = p["accent"]
    pad = 26
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Project: {p["title"]}">']
    o.append(f'''  <defs>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0f172a"/>
      <stop offset="1" stop-color="#070b18"/>
    </linearGradient>
    <linearGradient id="border" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{a}" stop-opacity="0.75"/>
      <stop offset="1" stop-color="#8b5cf6" stop-opacity="0.35"/>
    </linearGradient>
    <radialGradient id="halo" cx="0" cy="0" r="1">
      <stop offset="0" stop-color="{a}" stop-opacity="0.28"/>
      <stop offset="1" stop-color="{a}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <path d="M 24 0 L 0 0 0 24" fill="none" stroke="{a}" stroke-opacity="0.07"/>
    </pattern>
    <clipPath id="clip"><rect width="{W}" height="{H}" rx="16"/></clipPath>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>''')
    o.append(f'  <g clip-path="url(#clip)">')
    o.append(f'    <rect width="{W}" height="{H}" fill="url(#panel)"/>')
    o.append(f'    <rect width="{W}" height="{H}" fill="url(#grid)"/>')
    o.append(f'    <ellipse cx="{W}" cy="0" rx="{int(W*0.55)}" ry="{int(H*0.9)}" fill="url(#halo)"/>')
    # top accent line
    o.append(f'    <rect x="0" y="0" width="{W}" height="2" fill="{a}" fill-opacity="0.9"/>')
    o.append(f'  </g>')
    o.append(f'  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="url(#border)"/>')

    # index + repo path
    o.append(f'  <text x="{pad}" y="{pad+10}" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{a}">PROJECT {p["index"]}</text>')
    o.append(f'  <text x="{W-pad}" y="{pad+10}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="#64748b">{p["repo"]}</text>')
    # title
    o.append(f'  <text x="{pad}" y="{pad+46}" font-family="{FONT}" font-size="26" font-weight="800" fill="#f1f5f9">{esc(p["title"])}</text>')
    if p["featured"]:
        o.append(f'  <rect x="{pad+250}" y="{pad+28}" width="86" height="22" rx="11" fill="{a}" fill-opacity="0.12" stroke="{a}" stroke-opacity="0.6"/>')
        o.append(f'  <text x="{pad+293}" y="{pad+43}" text-anchor="middle" font-family="{MONO}" font-size="10.5" letter-spacing="2" fill="{a}">FEATURED</text>')
    # description
    y = pad + 76
    for ln in p["lines"]:
        safe = esc(ln)
        o.append(f'  <text x="{pad}" y="{y}" font-family="{FONT}" font-size="13.5" fill="#cbd5e1">{safe}</text>')
        y += 20
    # tags
    x = pad
    ty = H - pad - 24
    for t in p["tags"]:
        w = chip_w(t)
        o.append(f'  <rect x="{x}" y="{ty}" width="{w}" height="24" rx="7" fill="{a}" fill-opacity="0.08" stroke="{a}" stroke-opacity="0.4"/>')
        o.append(f'  <text x="{x+w/2}" y="{ty+16}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#e2e8f0">{esc(t)}</text>')
        x += w + 8
    # footer / status hint (bottom-right on wide cards, under repo path on narrow cards)
    if p["featured"]:
        fx, fy = W - pad - 4, ty + 12
    else:
        fx, fy = W - pad - 4, pad + 30
    o.append(f'  <circle cx="{fx}" cy="{fy}" r="3" fill="{a}" filter="url(#glow)"><animate attributeName="opacity" values="1;0.3;1" dur="2.4s" repeatCount="indefinite"/></circle>')
    o.append(f'  <text x="{fx-10}" y="{fy+4}" text-anchor="end" font-family="{MONO}" font-size="11" fill="#94a3b8">{esc(p["footer"])}</text>')
    o.append('</svg>')
    return "\n".join(o) + "\n"


def main() -> None:
    here = Path(__file__).parent
    for p in PROJECTS:
        (here / f'project-{p["slug"]}.svg').write_text(card(p), encoding="utf-8")
        print(f'wrote project-{p["slug"]}.svg')


if __name__ == "__main__":
    main()
