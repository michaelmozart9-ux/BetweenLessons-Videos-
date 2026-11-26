# Ode to Joy (Beethoven 9, public domain): same melody, left hand Grade 1 -> 3 -> 5 -> 8, plan phone + grade end card. C major 4/4, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
P1 = [("E5", 0, 2), ("E5", 2, 2), ("F5", 4, 2), ("G5", 6, 2), ("G5", 8, 2), ("F5", 10, 2), ("E5", 12, 2), ("D5", 14, 2)]
P2 = [("C5", 0, 2), ("C5", 2, 2), ("D5", 4, 2), ("E5", 6, 2), ("E5", 8, 3), ("D5", 11, 1), ("D5", 12, 4)]
P4 = [("C5", 0, 2), ("C5", 2, 2), ("D5", 4, 2), ("E5", 6, 2), ("D5", 8, 3), ("C5", 11, 1)]
def mel(seq, v=0.74, octv=False, third=False):
    TH = {0: 3, 2: 3, 4: 4, 5: 3, 7: 3, 9: 4, 11: 4}; out = []
    for n, b, d in seq:
        m = P(n); out.append((m, b, d * 0.9, "R", v))
        if octv: out.append((m - 12, b, d * 0.9, "R", v - 0.16))
        if third: out.append((m - TH[m % 12], b, d * 0.9, "R", v - 0.22))
    return out
CH = {"C": ["C3", "E3", "G3"], "G": ["G2", "B2", "D3"]}
L = lambda n, b, d, v=0.48: (P(n), b, d, "L", v)
# Grade 1: one long bass note per bar
A = mel(P1, 0.72) + [L("C3", 0, 8), L("G2", 8, 8)]
# Grade 3: root + fifth, half notes
B = mel(P2, 0.72)
for b, c in [(0, "C"), (8, "G")]: r, _, f = CH[c]; B += [L(r, b, 3.8, 0.5), L(f, b + 4, 3.8, 0.44)]
# Grade 5: Alberti bass in 8ths
C = mel(P1, 0.76)
for b, c in [(0, "C"), (8, "G")]:
    r, t, f = CH[c]; C += [L(n, b + i, 0.95, 0.42) for i, n in enumerate([r, f, t, f] * 2)]
# Grade 8: tune in octaves + thirds, octave bass + rolling 8ths, final rolled C chord
D = mel(P4, 0.86, octv=True, third=True)
for b, c in [(0, "C"), (8, "G")]:
    r, t, f = CH[c]; D += [L(r, b, 3.5, 0.62), ((P(r) - 12 if P(r) >= 48 else P(r) + 12), b, 3.5, "L", 0.55), L(r, b + 4, 3.5, 0.58), ((P(r) - 12 if P(r) >= 48 else P(r) + 12), b + 4, 3.5, "L", 0.5)]
    D += [(P(n) + 12, b + i, 0.9, "L", 0.4) for i, n in enumerate([r, f, t, f, r, f, t, f]) if b + i < 12]
F = 12
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["C2", "G2", "C3", "E3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["E4", "G4", "C5", "E5", "G5"])]
make(HERE, [(A, 16, 330, None), (B, 16, 350, None), (C, 16, 380, None), (D, 12, 400, None)], F,
     {"piece": "Ode to Joy · same tune, 4 left hands 🎹", "q": "Grade 1 vs <span class='hl'>Grade 8</span>", "labels": ["1", "3", "5", "8"],
      "chips": ["Grade 1: one note", "Grade 3: root + fifth", "Grade 5: Alberti bass", "Grade 8: octaves 🔥"], "wait": "wait for Grade 8 🔥", "rows": [], "rowsize": 60,
      "endq": "Want to play <span class='hl'>this?</span> 👇<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Type the piece in → free Day 1 plan</div>", "end2": ""},
     kicks={3: [0, 4, 8]}, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Ode to Joy", "sub": "Beethoven · your grade",
           "chips": ["Bars 1–4", "Left hand"], "mins": [5, 10, 5], "tempo": 40, "bpm": 48,
           "milestone": "Bars 1–8 hands together at 50%"})
