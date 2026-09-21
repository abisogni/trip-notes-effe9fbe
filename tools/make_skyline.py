#!/usr/bin/env python3
"""Generate a city skyline SVG in the trip-site palette.

  python3 tools/make_skyline.py --city copenhagen --landmarks spiral,dragon,round,tower --out skyline.svg
  python3 tools/make_skyline.py --city paris --landmarks eiffel,twin,dome --out skyline.svg

Landmarks (pick 2-5; they are spread across the width, in order):
  spiral   tower with external spiral spire (e.g. Church of Our Saviour)
  dragon   three twisted tails on a spire (Borsen)
  round    squat round tower with lantern (Round Tower)
  tower    slim pointed civic tower (city hall)
  eiffel   lattice tower
  twin     gothic twin towers (Notre-Dame style)
  dome     large dome with lantern (basilica / cathedral)
  clock    square clock tower with pyramid roof (Big Ben style)
  minaret  slender minaret pair
  windmill windmill
The row of gabled townhouses along the bottom is seeded by --city so each
city is stable but different. Colours match the site's CSS variables.
"""
import argparse, math, random, zlib

W, H, BASE = 1600, 300, 262
COLS = ["#b86a6a", "#a8882e", "#5e8c76", "#7a6ea0", "#c9a08a", "#8fae9c", "#d3b96a", "#a99bcb"]

def g(op, body): return f'<g fill="#1c1814" opacity="{op}">{body}</g>'

def spiral(x):
    s = g(0.16, f'<rect x="{x-22}" y="{BASE-120}" width="44" height="120"/>'
                f'<path d="M{x-22} {BASE-120} L{x-16} {BASE-150} L{x+16} {BASE-150} L{x+22} {BASE-120}Z"/>'
                f'<path d="M{x-14} {BASE-150} L{x} {BASE-262} L{x+14} {BASE-150}Z"/><circle cx="{x}" cy="{BASE-268}" r="5"/>')
    pts = []
    for i in range(41):
        t = i / 40
        pts.append(f'{x + math.sin(t*math.pi*5)*14*(1-t):.1f},{BASE-150-t*108:.1f}')
    return s + f'<polyline points="{" ".join(pts)}" fill="none" stroke="#f6f2ec" stroke-width="2" opacity="0.7"/>'

def dragon(x):
    s = g(0.16, f'<rect x="{x-60}" y="{BASE-70}" width="120" height="70"/>'
                f'<path d="M{x-60} {BASE-70} L{x-40} {BASE-92} L{x+40} {BASE-92} L{x+60} {BASE-70}Z"/>'
                f'<path d="M{x-6} {BASE-92} L{x} {BASE-210} L{x+6} {BASE-92}Z"/>')
    for ph in (0, 2.1, 4.2):
        pts = [f'{x + math.sin((i/30)*math.pi*3+ph)*10*(1-(i/30)*0.6):.1f},{BASE-92-(i/30)*100:.1f}' for i in range(31)]
        s += f'<polyline points="{" ".join(pts)}" fill="none" stroke="#1c1814" stroke-width="3" opacity="0.2"/>'
    return s

def round_(x): return g(0.14, f'<rect x="{x-26}" y="{BASE-130}" width="52" height="130"/><rect x="{x-32}" y="{BASE-142}" width="64" height="14"/><rect x="{x-14}" y="{BASE-176}" width="28" height="36"/><path d="M{x-16} {BASE-176} L{x} {BASE-206} L{x+16} {BASE-176}Z"/>')
def tower(x): return g(0.14, f'<rect x="{x-18}" y="{BASE-190}" width="36" height="190"/><path d="M{x-22} {BASE-190} L{x} {BASE-236} L{x+22} {BASE-190}Z"/><rect x="{x-70}" y="{BASE-70}" width="140" height="70"/>')
def eiffel(x): return g(0.15, f'<path d="M{x-70} {BASE} L{x-46} {BASE-70} L{x-30} {BASE-70} L{x-18} {BASE-150} L{x-6} {BASE-235} L{x} {BASE-262} L{x+6} {BASE-235} L{x+18} {BASE-150} L{x+30} {BASE-70} L{x+46} {BASE-70} L{x+70} {BASE}Z"/>') + f'<path d="M{x-40} {BASE-70} H{x+40} M{x-20} {BASE-150} H{x+20}" stroke="#f6f2ec" stroke-width="3" opacity="0.6"/><path d="M{x-24} {BASE} Q{x} {BASE-60} {x+24} {BASE}" fill="#f6f2ec" opacity="0.5"/>'
def twin(x): return g(0.15, f'<rect x="{x-70}" y="{BASE-160}" width="46" height="160"/><rect x="{x+24}" y="{BASE-160}" width="46" height="160"/><rect x="{x-24}" y="{BASE-110}" width="48" height="110"/>' + ''.join(f'<rect x="{x+dx-6}" y="{BASE-150+i*18}" width="12" height="9" fill="#f6f2ec" opacity="0.6"/>' for dx in (-47, 47) for i in range(6)))
def dome(x): return g(0.15, f'<rect x="{x-70}" y="{BASE-60}" width="140" height="60"/><path d="M{x-56} {BASE-60} A56 60 0 0 1 {x+56} {BASE-60}Z"/><rect x="{x-6}" y="{BASE-150}" width="12" height="30"/><path d="M{x-8} {BASE-150} L{x} {BASE-172} L{x+8} {BASE-150}Z"/>')
def clock(x): return g(0.15, f'<rect x="{x-22}" y="{BASE-190}" width="44" height="190"/><path d="M{x-26} {BASE-190} L{x} {BASE-250} L{x+26} {BASE-190}Z"/><rect x="{x-60}" y="{BASE-70}" width="120" height="70"/>') + f'<circle cx="{x}" cy="{BASE-160}" r="13" fill="#f6f2ec" opacity="0.75"/>'
def minaret(x): return g(0.15, ''.join(f'<rect x="{x+dx-6}" y="{BASE-170}" width="12" height="170"/><rect x="{x+dx-10}" y="{BASE-120}" width="20" height="6"/><path d="M{x+dx-7} {BASE-170} L{x+dx} {BASE-205} L{x+dx+7} {BASE-170}Z"/>' for dx in (-50, 50)) + f'<rect x="{x-44}" y="{BASE-60}" width="88" height="60"/>')
def windmill(x): return g(0.15, f'<path d="M{x-24} {BASE} L{x-14} {BASE-110} L{x+14} {BASE-110} L{x+24} {BASE}Z"/><path d="M{x-14} {BASE-110} L{x} {BASE-130} L{x+14} {BASE-110}Z"/>') + f'<path d="M{x} {BASE-112} L{x-70} {BASE-170} M{x} {BASE-112} L{x+70} {BASE-54} M{x} {BASE-112} L{x+56} {BASE-176} M{x} {BASE-112} L{x-56} {BASE-48}" stroke="#1c1814" stroke-width="5" opacity="0.18"/>'

LM = {"spiral": spiral, "dragon": dragon, "round": round_, "tower": tower, "eiffel": eiffel,
      "twin": twin, "dome": dome, "clock": clock, "minaret": minaret, "windmill": windmill}

def build(city, landmarks):
    rnd = random.Random(zlib.crc32(city.encode()))
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice">']
    n = len(landmarks)
    for i, name in enumerate(landmarks):
        out.append(LM[name](int(W * (i + 0.6) / (n + 0.2))))
    x = -20
    while x < W + 40:
        w, h, c = rnd.choice([54, 62, 70, 78, 86]), rnd.choice([70, 84, 98, 112, 126]), rnd.choice(COLS)
        y = BASE - h
        out.append(f'<g opacity="0.62"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>')
        gable = rnd.choice(["step", "tri", "curve"])
        if gable == "step":
            out.append(f'<rect x="{x+w*0.25:.0f}" y="{y-16}" width="{w*0.5:.0f}" height="16" fill="{c}"/><rect x="{x+w*0.38:.0f}" y="{y-24}" width="{w*0.24:.0f}" height="8" fill="{c}"/>')
        elif gable == "tri":
            out.append(f'<path d="M{x} {y} L{x+w/2} {y-26} L{x+w} {y}Z" fill="{c}"/>')
        else:
            out.append(f'<path d="M{x} {y} Q{x+w/2} {y-34} {x+w} {y}Z" fill="{c}"/>')
        for r in range(max(2, h // 30)):
            for cc in range(max(2, w // 22)):
                wx, wy = x + 8 + cc * ((w - 16) / max(2, w // 22)) + 2, y + 10 + r * 28
                if wy + 14 < BASE - 4:
                    out.append(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="9" height="14" fill="#f6f2ec" opacity="0.8"/>')
        out.append('</g>')
        x += w + rnd.choice([0, 0, 2])
    out.append(f'<rect x="0" y="{BASE}" width="{W}" height="{H-BASE}" fill="#7a6ea0" opacity="0.10"/>')
    for i in range(16):
        yy, xx = BASE + 6 + (i % 3) * 10, i * 110 + (i % 2) * 40
        out.append(f'<path d="M{xx} {yy} q12 -5 24 0 t24 0 t24 0" fill="none" stroke="#5e8c76" stroke-width="1.5" opacity="0.35"/>')
    out.append('</svg>')
    return "\n".join(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--city", required=True)
    ap.add_argument("--landmarks", default="tower,dome,spiral", help="comma list, see above")
    ap.add_argument("--out", default="skyline.svg")
    a = ap.parse_args()
    names = [n.strip() for n in a.landmarks.split(",") if n.strip()]
    bad = [n for n in names if n not in LM]
    if bad: ap.error(f"unknown landmarks {bad}; choose from {sorted(LM)}")
    open(a.out, "w").write(build(a.city, names))
    print(f"wrote {a.out} ({a.city}: {', '.join(names)})")
