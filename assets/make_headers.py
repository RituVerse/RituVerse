#!/usr/bin/env python3
"""Generate consistent section-header SVGs for the RituVerse profile README.

Usage:  python3 assets/make_headers.py
Outputs: assets/section-<slug>.svg
"""
from pathlib import Path

SECTIONS = [
    ("about",        "01", "ABOUT THE BUILDER"),
    ("stack",        "02", "TECH STACK"),
    ("projects",     "03", "PROJECT UNIVERSE"),
    ("achievements", "04", "ACHIEVEMENTS"),
    ("dsa",          "05", "DSA JOURNEY"),
    ("opensource",   "06", "OPEN SOURCE"),
    ("stats",        "07", "GITHUB ACTIVITY"),
    ("connect",      "08", "LET'S CONNECT"),
]

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="64" viewBox="0 0 900 64" role="img" aria-label="{label}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#22d3ee"/>
      <stop offset="1" stop-color="#8b5cf6"/>
    </linearGradient>
    <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#22d3ee" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/>
    </linearGradient>
    <filter id="glow" x="-10%" y="-50%" width="120%" height="200%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <!-- index chip -->
  <rect x="0.5" y="14.5" width="54" height="34" rx="8" fill="#0b1220" stroke="url(#g)" stroke-opacity="0.8"/>
  <text x="27.5" y="37" text-anchor="middle" font-family="'JetBrains Mono','Fira Code',Consolas,monospace" font-size="15" font-weight="700" fill="url(#g)">{index}</text>
  <!-- title -->
  <text x="72" y="39" font-family="'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif" font-size="22" font-weight="800" letter-spacing="5" fill="#e2e8f0">{label}</text>
  <!-- trailing line -->
  <rect x="{line_x}" y="31" width="{line_w}" height="1.5" fill="url(#line)"/>
  <circle cx="{dot_x}" cy="31.75" r="3" fill="#22d3ee" filter="url(#glow)">
    <animate attributeName="cx" values="{dot_x};{dot_end};{dot_x}" dur="6s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;0.2;1" dur="6s" repeatCount="indefinite"/>
  </circle>
</svg>
"""

def main() -> None:
    out_dir = Path(__file__).parent
    for slug, index, label in SECTIONS:
        # Approximate rendered width of the title (bold caps + 5px letter spacing)
        text_w = int(len(label) * 20.5)
        line_x = 72 + text_w + 18
        line_w = max(60, 900 - line_x)
        svg = TEMPLATE.format(
            label=label, index=index,
            line_x=line_x, line_w=line_w,
            dot_x=line_x, dot_end=line_x + min(line_w - 10, 260),
        )
        (out_dir / f"section-{slug}.svg").write_text(svg, encoding="utf-8")
        print(f"wrote section-{slug}.svg")

if __name__ == "__main__":
    main()
