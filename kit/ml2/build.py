# Mary Had a Little Lamb (traditional, public domain) but it gets harder: each line one grade up. C major, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
def seq(spec, v=0.76, stac=0.88, sh=0):
    out, b = [], 0
    for n, d in spec: out.append((P(n) + sh, b, d * stac, "R", v)); b += d
    return out
LA = [("E5", 2), ("D5", 2), ("C5", 2), ("D5", 2), ("E5", 2), ("E5", 2), ("E5", 4)]
LB = [("D5", 2), ("D5", 2), ("D5", 4), ("E5", 2), ("G5", 2), ("G5", 4)]
LC = [("E5", 2), ("D5", 2), ("C5", 2), ("D5", 2), ("E5", 2), ("E5", 2), ("E5", 2), ("E5", 2)]
LD = [("D5", 2), ("D5", 2), ("E5", 2), ("D5", 2)]
CH = {"C": ["C", "E", "G"], "G": ["G", "B", "D"]}
A = seq(LA) + N(("C3", 0, 16), h="L", v=0.5)
B = seq(LB)
for i, c in enumerate(["G", "G", "C", "C"]): B += N((c + "2", i * 4, 1.6), h="L", v=0.56) + N(*[(x + "3", i * 4 + 2, 1.4) for x in CH[c][1:]], h="L", v=0.44)
C = seq(LC) + [(m - (4 if m % 12 in (4, 7, 11) else 3), b, d, "R", 0.5) for m, b, d, h, v in seq(LC)]
for i, c in enumerate(["C", "C", "C", "C"]):
    r = P(c + "2"); C += [(r + o, i * 4 + k, 1.1, "L", 0.5) for k, o in enumerate([0, 7, 12, 16])]
D = seq(LD, 0.86) + seq(LD, 0.62, 0.88, -12)
for b, c in zip(range(8), ["G2", "B2", "D3", "B2", "G2", "B2", "D3", "F3"]): D += N((c, b, 1), h="L", v=0.6) + [(P(c) + 12, b, 1, "L", 0.46)]
D += [(P(n), 6 + j * 0.2, 0.25, "R", 0.5 + 0.025 * j) for j, n in enumerate(["G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5", "A5", "B5"])]
F = 8
D += [(P(n), F + j * 0.06, 20, "L", 0.9) for j, n in enumerate(["C2", "G2", "C3", "E3"])]
D += [(P(n), F + 0.25 + j * 0.06, 20, "R", 0.82 + 0.02 * j) for j, n in enumerate(["G4", "C5", "E5", "G5", "C6"])]
make(HERE, [(A, 16, 420, None), (B, 16, 440, None), (C, 16, 460, None), (D, 8, 400, None)], F,
     {"piece": "Mary Had a Little Lamb 🐑", "q": "but it gets <span class='hl'>harder</span> 😳", "labels": ["1", "3", "5", "8"],
      "chips": ["Grade 1", "Grade 3", "Grade 5", "Grade 8 🔥"], "wait": "wait for Grade 8 🔥", "rows": [], "rowsize": 60,
      "endq": "Which grade can<br><span class='hl'>you</span> play? 👇", "end2": "Free plan for your grade 👇"},
     kicks={3: [0, 2, 4, 6]})
