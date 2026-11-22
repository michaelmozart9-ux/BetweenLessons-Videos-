# Brahms' Lullaby (Wiegenlied Op.49 No.4, public domain) but it gets harder: each line one grade up. C major 3/4, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
def seq(spec, v=0.74, stac=0.95, sh=0):
    out, b = [], 0
    for n, d in spec: out.append((P(n) + sh, b, d * stac, "R", v)); b += d
    return out
L1 = [("E5", 1), ("E5", 1), ("G5", 4), ("E5", 1), ("E5", 1), ("G5", 4)]                       # 12 units
L2 = [("E5", 1), ("G5", 1), ("C6", 3), ("B5", 1), ("A5", 2), ("A5", 2), ("G5", 4)]            # 14 units
H2 = [(0, "C"), (6, "F"), (10, "C")]; ROOT = {"C": "C3", "F": "F2", "G": "G2"}; TRI = {"C": ["C3", "E3", "G3"], "F": ["F2", "A2", "C3"]}
A = seq(L1) + N(("C3", 0, 12), h="L", v=0.48)                                                      # grade 1: tune + one bass note
B = seq(L2)                                                                                         # grade 3: waltz bass (root, chord, chord)
for b0, c in H2:
    for k in range(0, 6 if b0 < 10 else 4, 2): B += N((ROOT[c] if k == 0 else TRI[c][1], b0 + k, 1.6), h="L", v=0.5 if k == 0 else 0.4) + ([(P(TRI[c][2]), b0 + k, 1.6, "L", 0.38)] if k else [])
C = seq(L1, 0.76) + [(m - (4 if m % 12 in (4, 11) else 3), b, d, "R", 0.48) for m, b, d, h, v in seq(L1)]   # grade 5: thirds + broken chords
for i in range(12): C += [(P("C3") + [0, 7, 12, 16, 12, 7][i % 6], i, 0.95, "L", 0.48)]
D = seq(L2[:-1], 0.86) + seq(L2[:-1], 0.6, 0.95, -12) + [(P("G5"), 10, 2, "R", 0.86), (P("G4"), 10, 2, "R", 0.6)]   # grade 8: octaves
for b0, c in [(0, "C"), (6, "F"), (10, "C")]:
    for k in range(0, 6 if b0 < 10 else 2, 2): D += [(P(ROOT[c]) - (12 if P(ROOT[c]) - 12 >= 36 else 0), b0 + k, 0.9, "L", 0.6), (P(TRI[c][1]) + 12, b0 + k + 1, 0.9, "L", 0.46), (P(TRI[c][2]) + 12, b0 + k + 1, 0.9, "L", 0.44)]
D += [(P(n), 12 + j * 0.25, 0.25, "R", 0.5 + 0.03 * j) for j, n in enumerate(["G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5"])]
F = 14
D += [(P(n), F + j * 0.06, 20, "L", 0.9) for j, n in enumerate(["C2", "G2", "C3", "E3"])]
D += [(P(n), F + 0.25 + j * 0.06, 20, "R", 0.82 + 0.02 * j) for j, n in enumerate(["G4", "C5", "E5", "G5", "C6"])]
make(HERE, [(A, 12, 250, None), (B, 14, 270, None), (C, 12, 290, None), (D, 14, 300, None)], F,
     {"piece": "Brahms' Lullaby 🌙", "q": "but it gets <span class='hl'>harder</span> 😳", "labels": ["1", "3", "5", "8"],
      "chips": ["Grade 1", "Grade 3", "Grade 5", "Grade 8 🔥"], "wait": "wait for Grade 8 🔥", "rows": [], "rowsize": 60,
      "endq": "Which grade can<br><span class='hl'>you</span> play? 👇", "end2": "Free plan for your grade 👇"},
     kicks={3: [0, 3, 6, 9]})
