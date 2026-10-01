"""Generate the README card SVGs (light + dark) in the portfolio's style.

Run:  python tools/generate.py
Edit the data lists below, re-run, then commit the files in assets/.
"""
import os
import xml.dom.minidom

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")

THEMES = {
    "light": dict(paper="#f5f5f0", dot="#dcdfd5", card="#ffffff", line="#d8ddd4", ink="#17221e",
                  muted="#68726d", chip="#e9ece4", chipline="#dce2d8"),
    "dark": dict(paper="#141d18", dot="#ffffff14", card="#1c2a24", line="#28352d", ink="#eef1ea",
                 muted="#94a099", chip="#ffffff0f", chipline="#ffffff1f"),
}
W = 1000
FONT = "Poppins,'Segoe UI',Arial,sans-serif"

# ---------------------------------------------------------------- data
ABOUT_TITLE = "Designing clear, useful digital experiences."
ABOUT_LINES = [
    "I'm a UI/UX designer who takes ideas from user flows and wireframes to polished",
    "prototypes and design systems — and I build what I design, so handoffs just work.",
]
ABOUT_FACTS = [
    ("SPECIALTY", "UI/UX Design", "#6d5efc"),
    ("LOCATION", "Phnom Penh, Cambodia", "#3aa0ff"),
    ("FOCUS", "Prototyping · Design Systems", "#ed5d37"),
    ("BUILDS WITH", "React · Laravel · Flutter · TS · Node.js", "#4f8b45"),
]

TOOLKIT = [
    ("Design", "#6d5efc", [("Figma", "#F24E1E"), ("FigJam", "#A259FF"), ("Adobe XD", "#FF61F6"),
                           ("Photoshop", "#31A8FF"), ("Blender", "#E87D0D"), ("Video Editing", "#6d5efc")]),
    ("Frontend", "#3aa0ff", [("HTML5", "#E34F26"), ("CSS3", "#1572B6"), ("JavaScript", "#F7DF1E"),
                             ("TypeScript", "#3178C6"), ("React", "#61DAFB")]),
    ("Backend & Data", "#ed5d37", [("Node.js", "#339933"), ("PHP", "#777BB4"), ("Laravel", "#FF2D20"),
                                   ("Java", "#ED8B00"), ("Spring Boot", "#6DB33F"), ("Python", "#3776AB"),
                                   ("PostgreSQL", "#4169E1")]),
    ("Mobile & DevOps", "#4f8b45", [("Flutter", "#02569B"), ("Docker", "#2496ED"), ("Git", "#F05032")]),
]

IMPROVING = [
    ("Blender", "3D", "#E87D0D", "3D assets and mockups for UI presentations"),
    ("Java", "Jv", "#ED8B00", "Solid OOP and backend fundamentals"),
    ("Spring Boot", "SB", "#6DB33F", "Build secure, production-ready backends"),
    ("REST API", "API", "#ed5d37", "Clean endpoint design, auth and docs"),
    ("Python", "Py", "#3776AB", "Automation, scripting and data handling"),
    ("Docker", "Dk", "#2496ED", "Containerise and deploy my own projects"),
    ("Next.js", "N", "#111111", "Production React apps with routing and SSR"),
    ("Tailwind CSS", "Tw", "#06B6D4", "Turn Figma designs into code faster"),
    ("Framer", "Fr", "#0055FF", "High-fidelity, interactive prototypes"),
    ("Accessibility", "A11y", "#6d5efc", "WCAG — designs that work for everyone"),
]

# icon paths drawn on a 24x24 grid (stroke icons)
ICONS = {
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "arrow": '<path d="M7 17 17 7M8 7h9v9"/>',
    "send": '<path d="M22 2 11 13M22 2l-7 20-4-9-9-4Z"/>',
    "download": '<path d="M12 3v12m-5-5 5 5 5-5M5 21h14"/>',
}
BUTTONS = [  # file, label, sub, icon, primary
    ("email", "Email me", "rinlyhour9@gmail.com", "mail", False),
    ("portfolio", "My Portfolio", "portfolio-rinlyhour.vercel.app", "arrow", True),
    ("telegram", "Telegram", "@LyyHourRinn", "send", False),
    ("resume", "Resume", "Download PDF", "download", False),
]


# ---------------------------------------------------------------- helpers
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def text_w(s, size):
    """Rough text width for Poppins/Segoe UI."""
    return len(s) * size * 0.56


def head(w, h, t, extra_css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
 <pattern id="d" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="11" cy="11" r="1.5" fill="{t['dot']}"/></pattern>
 <linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#7b5cff"/><stop offset=".5" stop-color="#3aa0ff"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient>
</defs>
<style>
 text{{font-family:{FONT}}}
 .c{{opacity:0;animation:in .6s ease-out forwards}}
 @keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
 .p{{animation:pl 1.6s ease-in-out infinite}}
 @keyframes pl{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}{extra_css}
</style>'''


def panel(h, t):
    return (f'<rect width="{W}" height="{h}" rx="18" fill="{t["paper"]}"/>\n'
            f'<rect width="{W}" height="{h}" rx="18" fill="url(#d)"/>')


def eyebrow(label, sub, t):
    w = text_w(label, 12.5) * 1.12 + 46
    return f'''<rect x="30" y="28" width="{w:.0f}" height="28" rx="14" fill="#6d5efc" opacity=".12"/>
<circle cx="46" cy="42" r="4" fill="#d6f36b" stroke="#4f8b45" class="p"/>
<text x="58" y="47" font-size="12.5" font-weight="600" fill="#6d5efc" letter-spacing="1.5">{label}</text>
<text x="30" y="82" font-size="13.5" fill="{t['muted']}">{esc(sub)}</text>
<rect x="810" y="38" width="160" height="4" rx="2" fill="url(#g)"/>'''


def save(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    xml.dom.minidom.parse(path)


# ---------------------------------------------------------------- cards
def about(t):
    h = 300
    o = [head(W, h, t), panel(h, t), eyebrow("ABOUT ME", "A little about who I am and how I work.", t)]
    o.append(f'<g class="c"><text x="30" y="132" font-size="26" font-weight="800" fill="{t["ink"]}">{esc(ABOUT_TITLE)}</text>')
    for i, line in enumerate(ABOUT_LINES):
        o.append(f'<text x="30" y="{164 + i * 22}" font-size="14.5" fill="{t["muted"]}">{esc(line)}</text>')
    o.append('</g>')
    gap = 14
    need = [max(text_w(v, 13.5) * 1.1, 120) + 44 for _, v, _ in ABOUT_FACTS]
    scale = (W - 60 - gap * (len(need) - 1)) / sum(need)
    x = 30
    for i, (label, value, col) in enumerate(ABOUT_FACTS):
        fw, y = need[i] * scale, 210
        o.append(f'''<g class="c" style="animation-delay:{.15 + i * .1:.2f}s">
 <rect x="{x:.0f}" y="{y}" width="{fw:.0f}" height="64" rx="14" fill="{t['card']}" stroke="{t['line']}"/>
 <rect x="{x}" y="{y + 16}" width="4" height="32" rx="2" fill="{col}"/>
 <text x="{x + 18}" y="{y + 26}" font-size="10.5" font-weight="600" fill="{t['muted']}" letter-spacing="1.2">{label}</text>
 <text x="{x + 18}" y="{y + 47}" font-size="13.5" font-weight="700" fill="{t['ink']}">{esc(value)}</text>
</g>''')
        x += fw + gap
    o.append('</svg>')
    return "\n".join(o)


def toolkit(t):
    cw, pad_in, chip_h, chip_gap = 460, 22, 30, 10
    # lay out chips per group
    groups = []
    for title, col, items in TOOLKIT:
        rows, row, x = [], [], 0
        for name, c in items:
            w = text_w(name, 13) + 36
            if row and x + w > cw - 2 * pad_in:
                rows.append(row); row, x = [], 0
            row.append((name, c, x, w)); x += w + chip_gap
        rows.append(row)
        groups.append((title, col, rows))
    card_h = lambda g: 62 + len(g[2]) * (chip_h + chip_gap) + 10
    row_h = [max(card_h(groups[i]), card_h(groups[i + 1])) for i in (0, 2)]
    top = 108
    h = top + row_h[0] + 20 + row_h[1] + 28
    o = [head(W, h, t), panel(h, t), eyebrow("TOOLKIT", "Tools I design with and the stack I build with.", t)]
    for i, (title, col, rows) in enumerate(groups):
        x = 30 + (i % 2) * (cw + 20)
        y = top + (0 if i < 2 else row_h[0] + 20)
        ch = row_h[i // 2]
        o.append(f'''<g class="c" style="animation-delay:{i * .12:.2f}s">
 <rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{t['card']}" stroke="{t['line']}"/>
 <rect x="{x + pad_in}" y="{y + 22}" width="22" height="22" rx="7" fill="{col}"/>
 <text x="{x + pad_in + 33}" y="{y + 39}" font-size="16" font-weight="700" fill="{t['ink']}">{esc(title)}</text>''')
        for r, row in enumerate(rows):
            cy = y + 62 + r * (chip_h + chip_gap)
            for name, c, cx, w in row:
                X = x + pad_in + cx
                o.append(f''' <rect x="{X:.0f}" y="{cy}" width="{w:.0f}" height="{chip_h}" rx="15" fill="{t['chip']}" stroke="{t['chipline']}"/>
 <circle cx="{X + 15:.0f}" cy="{cy + 15}" r="4.5" fill="{c}"/>
 <text x="{X + 26:.0f}" y="{cy + 20}" font-size="13" font-weight="500" fill="{t['ink']}">{esc(name)}</text>''')
        o.append('</g>')
    o.append('</svg>')
    return "\n".join(o)


def improving(t):
    cw, ch, top = 460, 92, 108
    rows = (len(IMPROVING) + 1) // 2
    h = top + rows * ch + (rows - 1) * 16 + 28
    o = [head(W, h, t), panel(h, t),
         eyebrow("CURRENTLY LEARNING", "From designer to developer — the skills I'm building to ship what I design, end to end.", t)]
    for i, (n, ab, col, goal) in enumerate(IMPROVING):
        x, y = 30 + (i % 2) * (cw + 20), top + (i // 2) * (ch + 16)
        fs = 14 if len(ab) > 2 else 18
        dot = t["ink"] if col == "#111111" else col
        o.append(f'''<g class="c" style="animation-delay:{i * .1:.2f}s">
 <rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{t['card']}" stroke="{t['line']}"/>
 <rect x="{x + 18}" y="{y + 18}" width="56" height="56" rx="14" fill="{col}"/>
 <text x="{x + 46}" y="{y + 52}" text-anchor="middle" font-size="{fs}" font-weight="800" fill="#fff">{ab}</text>
 <text x="{x + 92}" y="{y + 40}" font-size="17" font-weight="700" fill="{t['ink']}">{esc(n)}</text>
 <text x="{x + 92}" y="{y + 64}" font-size="13" fill="{t['muted']}">{esc(goal)}</text>
 <rect x="{x + cw - 108}" y="{y + 22}" width="88" height="22" rx="11" fill="{t['chip']}"/>
 <circle cx="{x + cw - 95}" cy="{y + 33}" r="3.5" fill="{dot}" class="p" style="animation-delay:{i * .2:.1f}s"/>
 <text x="{x + cw - 86}" y="{y + 37}" font-size="10.5" font-weight="600" fill="{t['muted']}">in progress</text>
</g>''')
    o.append('</svg>')
    return "\n".join(o)


def button(label, sub, icon, primary, t):
    w, h = 236, 64
    bg = "url(#g)" if primary else t["card"]
    stroke = "none" if primary else t["line"]
    ink = "#ffffff" if primary else t["ink"]
    muted = "#ffffffcc" if primary else t["muted"]
    tile = "#ffffff33" if primary else "#6d5efc1f"
    ic = "#ffffff" if primary else "#6d5efc"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#7b5cff"/><stop offset=".5" stop-color="#3aa0ff"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>
<style>text{{font-family:{FONT}}}</style>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="{bg}" stroke="{stroke}"/>
<rect x="12" y="12" width="40" height="40" rx="12" fill="{tile}"/>
<g transform="translate(20 20) scale(1)" fill="none" stroke="{ic}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>
<text x="64" y="29" font-size="14.5" font-weight="700" fill="{ink}">{esc(label)}</text>
<text x="64" y="47" font-size="11.5" fill="{muted}">{esc(sub)}</text>
</svg>'''


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "buttons"), exist_ok=True)
    for name, t in THEMES.items():
        save(f"about-{name}.svg", about(t))
        save(f"toolkit-{name}.svg", toolkit(t))
        save(f"improving-{name}.svg", improving(t))
        for f, label, sub, icon, primary in BUTTONS:
            save(f"buttons/{f}-{name}.svg", button(label, sub, icon, primary, t))
    print("generated")
