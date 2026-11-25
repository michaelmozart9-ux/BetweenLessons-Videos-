# Product-led: Turkish March falls apart hands together -> hands separate first (plan feature). Mozart K.331, public domain. A minor, unit = 16th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
MEL = [("B4", 0, 1), ("A4", 1, 1), ("G#4", 2, 1), ("A4", 3, 1), ("C5", 4, 2), ("D5", 8, 1), ("C5", 9, 1), ("B4", 10, 1), ("C5", 11, 1), ("E5", 12, 2),
       ("F5", 16, 1), ("E5", 17, 1), ("D#5", 18, 1), ("E5", 19, 1), ("B5", 20, 1), ("A5", 21, 1), ("G#5", 22, 1), ("A5", 23, 1),
       ("B5", 24, 1), ("A5", 25, 1), ("G#5", 26, 1), ("A5", 27, 1), ("C6", 28, 4)]
LH = [("A2", 4, "C3E3"), ("A2", 8, "C3E3"), ("A2", 12, "C3E3"), ("E2", 16, "B2E3"), ("A2", 20, "C3E3"), ("E2", 24, "B2E3"), ("A2", 28, "C3E3")]
def mel(upto, v=0.72, sh=0): return [(P(n) + sh, b, d, "R", v) for n, b, d in MEL if b < upto]
def oom(upto=32, v=0.5):
    out = []
    for n, b, ch in LH:
        if b >= upto: continue
        out.append((P(n), b, 1.8, "L", v)); out += [(P(ch[i:i + 2]), b + 2, 1.6, "L", v - 0.08) for i in (0, 2)]
    return out
A = mel(16, 0.7)                                       # right hand alone, slow
B = [(m, b - 4, d, h, v) for m, b, d, h, v in oom(20, 0.55) if b >= 4]   # left hand alone
C = mel(32, 0.74) + oom(32, 0.5)                       # hands together, slow
D = mel(32, 0.84) + [(P(n) - 12, b, d, "R", 0.58) for n, b, d in MEL] + oom(32, 0.58) + [(P(n) - 12 if P(n) - 12 >= 36 else P(n), b, 1.8, "L", 0.5) for n, b, ch in LH]
D += [(P(n), 32 + j * 0.5, 0.5, "R", 0.55 + 0.04 * j) for j, n in enumerate(["A4", "B4", "C5", "D5", "E5", "F5", "G#5", "A5"])] + [(P("E2"), 32, 4, "L", 0.6), (P("E3"), 32, 4, "L", 0.5)]
F = 36
D += [(P(n), F + j * 0.06, 26, "L", 0.9) for j, n in enumerate(["A2", "E3", "A3", "C4"])]
D += [(P(n), F + 0.25 + j * 0.06, 26, "R", 0.82 + 0.03 * j) for j, n in enumerate(["E4", "A4", "C5", "E5", "A5"])]
make(HERE, [(A, 16, 300, None), (B, 16, 330, None), (C, 32, 400, None), (D, 36, 540, None)], F,
     {"piece": "Turkish March falls apart? 😩", "q": "Split the <span class='hl'>hands</span> first", "labels": ["RH", "LH", "2H", "🔥"],
      "chips": ["Right hand alone 🐢", "Left hand alone", "Hands together, slow", "Hands together 🔥"], "wait": "wait for full speed 🔥", "rows": [], "rowsize": 60,
      "endq": "Stuck on <span class='hl'>hands together?</span><div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Your plan does hands separate first</div>", "end2": ""},
     kicks={3: [0, 8, 16, 24]}, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Turkish March", "sub": "Mozart · your grade",
           "chips": ["Bars 1–4", "Hands separate"], "mins": [5, 10, 5], "tempo": 40, "bpm": 48,
           "milestone": "Bars 1–8 hands together at 50%"})
