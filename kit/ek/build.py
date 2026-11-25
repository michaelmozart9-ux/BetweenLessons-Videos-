# Eine kleine Nachtmusik (Mozart K.525, public domain) but it gets HARDER. G major 4/4, unit = 8th. Bars 1-4 of the opening.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
MEL = [("G4", 0, 2), ("D4", 3, 1), ("G4", 4, 2), ("D4", 7, 1), ("G4", 8, 1), ("D4", 9, 1), ("G4", 10, 1), ("B4", 11, 1), ("D5", 12, 4),
       ("C5", 16, 2), ("A4", 19, 1), ("C5", 20, 2), ("A4", 23, 1), ("C5", 24, 1), ("A4", 25, 1), ("F#4", 26, 1), ("A4", 27, 1), ("D4", 28, 4)]
def mel(lo, hi, sh=0, v=0.7, stac=0.85, off=0): return [(P(n) + sh, b - off, d * stac, "R", v) for n, b, d in MEL if lo <= b < hi]
# chords: G for bars 1-2 (units 0-15), D7 for bars 3-4 (16-31)
def alb(lo, hi, off=0, v=0.42, oct_=0):
    out = []
    for b in range(lo, hi):
        ch = ["G2", "D3", "B2", "D3"] if b < 16 else ["D2", "C3", "A2", "C3"]
        out.append((P(ch[b % 4]) + oct_, b - off, 0.9, "L", v + (0.06 if b % 4 == 0 else 0)))
    return out
A = mel(0, 16, 0, 0.7) + [(P("G3"), 0, 7.6, "L", 0.45), (P("D3"), 8, 7.6, "L", 0.45)]                      # 1: tune + held bass
B = mel(16, 32, 0, 0.72, off=16) + [(P(n), b, 1.8, "L", 0.45) for b, n in zip(range(0, 16, 2), ["D3", "A3", "C4", "A3"] * 2)]  # 2: tune continues, bass on beats
C = mel(0, 32, 0, 0.76) + mel(0, 32, -12, 0.55) + alb(0, 32, v=0.42)                                 # 3: octaves + Alberti
D = mel(0, 32, 0, 0.86) + mel(0, 32, -12, 0.64) + [(P(n) + 7 if P(n) + 7 <= 84 else P(n) - 5, b, 0.5, "R", 0.42) for n, b, d in MEL if d >= 2]
for b in range(0, 32, 2):                                                                                    # 4: stride bass
    r = P("G2") if b < 16 else P("D2"); D += [(r, b, 0.9, "L", 0.62), (r + 12, b, 0.9, "L", 0.5)]
    D += [(P(x), b + 1, 0.8, "L", 0.42) for x in (["B2", "D3"] if b < 16 else ["C3", "F#3"])]
RUN = ["D4", "E4", "F#4", "G4", "A4", "B4", "C5", "D5"]
D += [(P(n), 32 + j * 0.5, 0.5, "R", 0.6 + 0.03 * j) for j, n in enumerate(RUN)] + [(P("D2"), 32, 4, "L", 0.62), (P("D3"), 32, 4, "L", 0.5)]
F = 36
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["G2", "D3", "G3", "B3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["D4", "G4", "B4", "D5", "G5"])]
make(HERE, [(A, 16, 300, None), (B, 16, 340, None), (C, 32, 440, None), (D, 36, 520, None)], F,
     {"piece": "Eine kleine Nachtmusik 🎻", "q": "but it gets <span class='hl'>HARDER</span> 😳", "labels": ["1", "2", "3", "4"],
      "chips": ["Level 1 · beginner", "Level 2", "Level 3 · octaves", "Level 4 🔥"], "wait": "wait for level 4 🔥", "rows": [], "rowsize": 60,
      "endq": "Want to play <span class='hl'>level 4?</span> 👇<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Type the piece in → free Day 1 plan</div>", "end2": ""},
     kicks={3: list(range(0, 32, 4))}, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Eine kleine Nachtmusik", "sub": "Mozart · your grade",
           "chips": ["Bars 1–4", "Right hand"], "mins": [5, 10, 5], "tempo": 40, "bpm": 56,
           "milestone": "Bars 1–8 hands together at 50%"})
