# Same melody, 4 left hands: Greensleeves (traditional, public domain). 6/8, unit = 8th, pickup at 0, bars at 1/7/13/19.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
GS = [("A4", 1), ("C5", 2), ("D5", 1), ("E5", 1.5), ("F5", 0.5), ("E5", 1), ("D5", 2), ("B4", 1), ("G4", 1.5), ("A4", 0.5), ("B4", 1),
      ("C5", 2), ("A4", 1), ("A4", 1.5), ("G#4", 0.5), ("A4", 1), ("B4", 2), ("G#4", 1), ("E4", 3)]
def mel(v=0.76, sh=0, h="R"):
    out, b = [], 0
    for n, d in GS: out.append((P(n) + sh, b, d * 0.92, h, v)); b += d
    return out
BARS = [(1, "A2", ["E3", "A3", "C4"]), (7, "G2", ["D3", "G3", "B3"]), (13, "A2", ["E3", "A3", "C4"]), (19, "E2", ["B2", "E3", "G#3"])]
L = lambda n, b, d, v=0.5: (P(n), b, d, "L", v)
A = mel() + [L(r, b, 6) for b, r, _ in BARS]
B = mel()
for b, r, c in BARS:
    for i, n in enumerate([r, c[0], c[1], c[2], c[1], c[0]]): B.append(L(n, b + i, 6 - i, 0.46))
C = mel()
for b, r, c in BARS:
    B5 = c[0]
    C += [L(r, b, 1, 0.55)] + [L(n, b + 1, 0.8, 0.38) for n in c[1:]] + [L(n, b + 2, 0.8, 0.36) for n in c[1:]]
    C += [L(B5, b + 3, 1, 0.5)] + [L(n, b + 4, 0.8, 0.38) for n in c[1:]] + [L(n, b + 5, 0.8, 0.36) for n in c[1:]]
D = mel(0.86) + mel(0.58, -12)
for b, r, c in BARS:
    D += [L(r, b, 3, 0.62), (P(r) + 12, b, 3, "L", 0.5), L(c[0], b + 3, 3, 0.56), (P(c[0]) + 12, b + 3, 3, "L", 0.45)]
F = 25
D += [(P(n), F + j * 0.06, 26, "L", 0.9) for j, n in enumerate(["A2", "E3", "A3", "C4"])]
D += [(P(n), F + 0.25 + j * 0.06, 26, "R", 0.84 + 0.02 * j) for j, n in enumerate(["E4", "A4", "C5", "E5", "A5"])]
make(HERE, [(A, 25, 400, None), (B, 25, 410, None), (C, 25, 420, None), (D, 25, 430, None)], F,
     {"piece": "Greensleeves · same melody 🎹", "q": "4 <span class='hl'>left hands</span> 🔥", "labels": ["1", "2", "3", "4"],
      "chips": ["Left hand: 1 note", "Left hand: broken chords", "Left hand: waltz", "Left hand: EPIC octaves 🔥"], "wait": "wait for #4 🔥",
      "rows": ["1 · one note", "2 · broken chords", "3 · waltz", "4 · octaves 🔥"], "rowsize": 60,
      "endq": "Which left hand<br>is <span class='hl'>best?</span> 👇", "end2": "Day 1 free · no card 👇"},
     kicks={3: [1, 7, 13, 19]})
