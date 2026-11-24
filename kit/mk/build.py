# Product-led tempo ladder: In the Hall of the Mountain King (Grieg, public domain) at the plan's tempo targets 40% -> 60% -> 80% -> 100%. B minor, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
MEL = [("B3", 0, 1), ("C#4", 1, 1), ("D4", 2, 1), ("E4", 3, 1), ("F#4", 4, 1), ("D4", 5, 1), ("F#4", 6, 2),
       ("F4", 8, 1), ("C#4", 9, 1), ("F4", 10, 2), ("E4", 12, 1), ("C4", 13, 1), ("E4", 14, 2),
       ("B3", 16, 1), ("C#4", 17, 1), ("D4", 18, 1), ("E4", 19, 1), ("F#4", 20, 1), ("D4", 21, 1), ("F#4", 22, 1), ("B4", 23, 1),
       ("A4", 24, 1), ("F#4", 25, 1), ("D4", 26, 1), ("F#4", 27, 1), ("A4", 28, 4)]
def mel(hi, sh=0, v=0.6, stac=0.6): return [(P(n) + sh, b, d * stac, "R", v) for n, b, d in MEL if b < hi]
def bass(hi, step=2, oct2=False, v=0.45):
    out = []
    for b in range(0, hi, step):
        n = "F#2" if (b // 2) % 2 else "B2"
        out.append((P(n), b, 0.5, "L", v))
        if oct2: out.append((P(n) + 12, b, 0.5, "L", v - 0.08))
    return out
A = mel(8, 12, 0.6, 0.85)                                              # 40%: right hand alone, slow and clean
B = mel(16, 12, 0.66, 0.75) + bass(16, 2, v=0.42)                      # 60%: hands together
C = mel(16, 12, 0.74, 0.65) + mel(16, 0, 0.6, 0.65) + bass(16, 1, v=0.52)  # 80%: octaves
D = mel(32, 12, 0.86, 0.7) + mel(32, 0, 0.66, 0.7) + bass(32, 1, oct2=True, v=0.6)  # 100%
F = 32
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["B2", "F#3", "B3", "D4"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["F#4", "B4", "D5", "F#5", "B5"])]
make(HERE, [(A, 8, 216, None), (B, 16, 324, None), (C, 16, 432, None), (D, 32, 540, None)], F,
     {"piece": "Can't play Mountain King fast? 👹", "q": "Don't start at <span class='hl'>100%</span>", "labels": ["40%", "60%", "80%", "100%"],
      "chips": ["Week 1 · tempo target 🐢", "Week 3", "Week 6", "Full speed 🔥"], "wait": "wait for 100% 🔥", "rows": [], "rowsize": 60,
      "endq": "Can't play it fast <span class='hl'>yet?</span> 👇<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Too easy? Next session +5% 🐢→🔥</div>", "end2": ""},
     kicks={3: list(range(0, 32, 2))}, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Hall of the Mountain King", "sub": "Grieg · your grade",
           "chips": ["Bars 1–8", "Hands separate"], "mins": [5, 10, 5], "tempo": 40, "bpm": 54,
           "milestone": "Bars 1–8 hands together at 50%"})
