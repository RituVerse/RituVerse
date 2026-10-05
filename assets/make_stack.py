#!/usr/bin/env python3
"""Generate the self-hosted Tech Stack SVG (assets/stack.svg).

Grouped skill chips on a dark glass panel. No external dependencies,
no fabricated technologies — only what Ritu actually uses.
"""
from pathlib import Path

GROUPS = [
    ("LANGUAGES",   "#22d3ee", ["C++", "JavaScript", "HTML5", "CSS3"]),
    ("CORE",        "#8b5cf6", ["Data Structures & Algorithms", "Problem Solving", "ECE Fundamentals"]),
    ("WEB",         "#38bdf8", ["Responsive Web Design", "Fetch API", "CSS Grid & Flexbox", "DOM & Events", "CSS Animations"]),
    ("TOOLS",       "#a78bfa", ["Git", "GitHub", "VS Code", "Canva", "Vercel"]),
    ("OTHER",       "#67e8f9", ["UI-focused Design", "Technical Presentations", "Project Documentation", "Team Leadership"]),
]

W = 900
PAD = 28
ROW_H = 58
LABEL_W = 120
CHIP_H = 30
CHIP_GAP = 10
FONT = "'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,monospace"


def chip_width(text: str) -> int:
    return int(len(text) * 7.4) + 26


def main() -> None:
    rows = []
    y = PAD + 10
    for name, color, items in GROUPS:
        # wrap chips into lines
        lines, cur, cur_w = [], [], 0
        max_w = W - PAD * 2 - LABEL_W
        for it in items:
            w = chip_width(it)
            if cur and cur_w + w + CHIP_GAP > max_w:
                lines.append(cur); cur, cur_w = [], 0
            cur.append((it, w)); cur_w += w + CHIP_GAP
        if cur:
            lines.append(cur)
        rows.append((name, color, lines, y))
        y += ROW_H * len(lines) - (ROW_H - CHIP_H - 14) * (len(lines) - 1)
    H = y + PAD - 6

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack: languages, core skills, web, tools and other skills">']
    out.append('''  <defs>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0f172a"/>
      <stop offset="1" stop-color="#070b18"/>
    </linearGradient>
    <linearGradient id="border" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#22d3ee" stop-opacity="0.6"/>
      <stop offset="1" stop-color="#8b5cf6" stop-opacity="0.6"/>
    </linearGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#22d3ee" stroke-opacity="0.06"/>
    </pattern>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>''')
    out.append(f'  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="url(#panel)" stroke="url(#border)"/>')
    out.append(f'  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="url(#grid)"/>')

    for name, color, lines, y0 in rows:
        # category label
        out.append(f'  <circle cx="{PAD+6}" cy="{y0+CHIP_H/2}" r="3" fill="{color}" filter="url(#glow)"/>')
        out.append(f'  <text x="{PAD+18}" y="{y0+CHIP_H/2+5}" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{color}">{name}</text>')
        yy = y0
        for line in lines:
            x = PAD + LABEL_W
            for text, w in line:
                safe = text.replace("&", "&amp;")
                out.append(f'  <rect x="{x}" y="{yy}" width="{w}" height="{CHIP_H}" rx="8" fill="{color}" fill-opacity="0.08" stroke="{color}" stroke-opacity="0.45"/>')
                out.append(f'  <text x="{x + w/2}" y="{yy+CHIP_H/2+4.5}" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="#e2e8f0">{safe}</text>')
                x += w + CHIP_GAP
            yy += CHIP_H + 14
    out.append('</svg>')
    Path(__file__).with_name("stack.svg").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote stack.svg ({W}x{H})")


if __name__ == "__main__":
    main()
