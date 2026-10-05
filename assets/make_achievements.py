#!/usr/bin/env python3
"""Generate the self-hosted Achievements panel (assets/achievements.svg).

Four real milestones, presented as a vertical constellation timeline.
No exaggeration: SIH is an internal-round selection, not a national qualification.
"""
from pathlib import Path

FONT = "'Segoe UI',Inter,Roboto,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,monospace"

ITEMS = [
    dict(
        tag="HACKATHON", accent="#f59e0b",
        title="AI Web Forge Hackathon",
        badge="3RD RANK",
        lines=["Secured 3rd place with my team — building and presenting a web solution under time pressure."],
    ),
    dict(
        tag="HACKATHON", accent="#22d3ee",
        title="Smart India Hackathon 2026 · Team Optimus-X",
        badge="INTERNAL ROUND",
        lines=["Selected for the SIH internal round. Contributed to the technology-based solution,",
               "project documentation, design, technical presentation and the feasibility & impact pitch."],
    ),
    dict(
        tag="OPEN SOURCE", accent="#8b5cf6",
        title="GirlScript Summer of Code",
        badge="PARTICIPANT",
        lines=["Participated in GSSoC and gained hands-on open-source experience with Git and GitHub workflows."],
    ),
    dict(
        tag="LEADERSHIP", accent="#38bdf8",
        title="National Service Scheme (NSS)",
        badge="TEAM LEADER",
        lines=["Led a team at an NSS event — coordinating people, tasks and timelines."],
    ),
]

W = 900
PAD = 28
X_LINE = PAD + 14
X_TEXT = X_LINE + 36


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main() -> None:
    # compute heights
    blocks = []
    y = PAD + 8
    for it in ITEMS:
        h = 30 + 20 * len(it["lines"]) + 26
        blocks.append((it, y, h))
        y += h
    H = y + PAD - 10

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Achievements timeline">']
    o.append('''  <defs>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0f172a"/>
      <stop offset="1" stop-color="#070b18"/>
    </linearGradient>
    <linearGradient id="border" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#22d3ee" stop-opacity="0.6"/>
      <stop offset="1" stop-color="#8b5cf6" stop-opacity="0.6"/>
    </linearGradient>
    <linearGradient id="rail" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#f59e0b" stop-opacity="0.9"/>
      <stop offset="0.35" stop-color="#22d3ee" stop-opacity="0.9"/>
      <stop offset="0.7" stop-color="#8b5cf6" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#38bdf8" stop-opacity="0.9"/>
    </linearGradient>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#22d3ee" stroke-opacity="0.06"/>
    </pattern>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.5" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>''')
    o.append(f'  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="url(#panel)" stroke="url(#border)"/>')
    o.append(f'  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="url(#grid)"/>')

    first_y = blocks[0][1] + 14
    last_y = blocks[-1][1] + 14
    o.append(f'  <line x1="{X_LINE}" y1="{first_y}" x2="{X_LINE}" y2="{last_y}" stroke="url(#rail)" stroke-width="1.5" stroke-dasharray="3 5"/>')
    # travelling spark along the rail
    o.append(f'  <circle cx="{X_LINE}" cy="{first_y}" r="2.5" fill="#e2e8f0" filter="url(#glow)"><animate attributeName="cy" values="{first_y};{last_y};{first_y}" dur="9s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;1;0" dur="9s" repeatCount="indefinite"/></circle>')

    for it, y0, h in blocks:
        a = it["accent"]
        cy = y0 + 14
        # node
        o.append(f'  <circle cx="{X_LINE}" cy="{cy}" r="7" fill="#0b1220" stroke="{a}" stroke-width="1.5"/>')
        o.append(f'  <circle cx="{X_LINE}" cy="{cy}" r="3" fill="{a}" filter="url(#glow)"/>')
        # tag
        o.append(f'  <text x="{X_TEXT}" y="{y0+4}" font-family="{MONO}" font-size="10.5" letter-spacing="3" fill="{a}">{esc(it["tag"])}</text>')
        # title
        o.append(f'  <text x="{X_TEXT}" y="{y0+26}" font-family="{FONT}" font-size="18" font-weight="800" fill="#f1f5f9">{esc(it["title"])}</text>')
        # badge (right)
        bw = int(len(it["badge"]) * 7.6) + 26
        o.append(f'  <rect x="{W-PAD-bw}" y="{y0+8}" width="{bw}" height="24" rx="12" fill="{a}" fill-opacity="0.12" stroke="{a}" stroke-opacity="0.65"/>')
        o.append(f'  <text x="{W-PAD-bw/2}" y="{y0+24}" text-anchor="middle" font-family="{MONO}" font-size="10.5" letter-spacing="2" font-weight="700" fill="{a}">{esc(it["badge"])}</text>')
        # lines
        yy = y0 + 48
        for ln in it["lines"]:
            o.append(f'  <text x="{X_TEXT}" y="{yy}" font-family="{FONT}" font-size="13.5" fill="#cbd5e1">{esc(ln)}</text>')
            yy += 20
    o.append('</svg>')
    Path(__file__).with_name("achievements.svg").write_text("\n".join(o) + "\n", encoding="utf-8")
    print(f"wrote achievements.svg ({W}x{H})")


if __name__ == "__main__":
    main()
