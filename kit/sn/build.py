# Silent Night (Gruber, 1818, public domain) but it gets EPIC: calm -> brighter -> bigger -> EPIC, plan phone + grade end card. C major 6/8, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
B12 = [("G4", 0, 3), ("A4", 3, 1), ("G4", 4, 2), ("E4", 6, 6)]           # "Si-lent night"
B56 = [("D5", 0, 4), ("D5", 4, 2), ("B4", 6, 6)]                          # "all is calm"
B78 = [("C5", 0, 4), ("C5", 4, 2), ("G4", 6, 6)]                          # "all is bright"
def sh(fig, b0): return [(n, b + b0, d) for n, b, d in fig]
TH = {0: 3, 2: 3, 4: 4, 5: 3, 7: 3, 9: 4, 11: 4}
def mel(seq, v=0.7, stac=0.92, octv=False, third=False):
    out = []
    for n, b, d in seq:
        m = P(n); out.append((m, b, d * stac, "R", v))
        if octv: out.append((m - 12, b, d * stac, "R", v - 0.14))
        if third: out.append((m - TH[m % 12], b, d * stac, "R", v - 0.2))
    return out
PAT = {"C": ["C3", "G3", "C4", "E4", "C4", "G3"], "G": ["G2", "D3", "G3", "B3", "G3", "D3"]}
def rolling(harm, v=0.5):
    return [(P(PAT[c][u % 6]), u, 0.95, "L", v) for b0, b1, c in harm for u in range(b0, b1)]
A = mel(B12, 0.5) + [(P("C3"), 0, 12, "L", 0.36), (P("G3"), 0, 12, "L", 0.3)]                          # 🌙 calm
B = mel(B12, 0.64, third=True) + [(P(n), b, 2.8, "L", 0.42) for b, n in [(0, "C3"), (3, "G3"), (6, "C3"), (9, "G3")]]  # ✨ brighter
C = mel(sh(B56, 0) + sh(B78, 12), 0.74, octv=True) + rolling([(0, 12, "G"), (12, 24, "C")], 0.48)          # 😳 bigger
D = mel(sh(B56, 0) + [("C5", 12, 4), ("C5", 16, 2)], 0.86, octv=True, third=True) + rolling([(0, 12, "G"), (12, 18, "C")], 0.56)
D += [(P(n), b, 2.5, "L", 0.64) for b, n in [(0, "G2"), (3, "G2"), (6, "G2"), (9, "G2"), (12, "C2"), (15, "C2")]]
F = 18
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["C2", "G2", "C3", "E3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["E4", "G4", "C5", "E5", "G5"])]
make(HERE, [(A, 12, 280, 12), (B, 12, 310, None), (C, 24, 380, None), (D, 18, 420, None)], F,
     {"piece": "Silent Night 🌟", "q": "but it gets <span class='hl'>EPIC</span> 😳", "labels": ["🌙", "✨", "😳", "🔥"],
      "chips": ["Calm", "Brighter", "Bigger", "EPIC"], "wait": "wait for 🔥", "rows": [], "rowsize": 60,
      "endq": "Want to play <span class='hl'>this</span> for Christmas? 🎄<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Type the piece in → free Day 1 plan</div>", "end2": ""},
     kicks={3: [0, 3, 6, 9, 12, 15]}, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Silent Night", "sub": "Gruber · your grade",
           "chips": ["Bars 1–4", "Right hand"], "mins": [5, 10, 5], "tempo": 40, "bpm": 32,
           "milestone": "Bars 1–8 hands together at 50%"})
