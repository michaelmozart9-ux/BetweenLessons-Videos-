# Guess the grade: Rondo alla Turca / Turkish March (Mozart K.331, public domain). A minor, unit = 16th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from gtg import *
MEL = [("B4", 0, 1), ("A4", 1, 1), ("G#4", 2, 1), ("A4", 3, 1), ("C5", 4, 2), ("D5", 8, 1), ("C5", 9, 1), ("B4", 10, 1), ("C5", 11, 1), ("E5", 12, 2),
       ("F5", 16, 1), ("E5", 17, 1), ("D#5", 18, 1), ("E5", 19, 1), ("B5", 20, 1), ("A5", 21, 1), ("G#5", 22, 1), ("A5", 23, 1),
       ("B5", 24, 1), ("A5", 25, 1), ("G#5", 26, 1), ("A5", 27, 1), ("C6", 28, 4)]
# left hand: bass on the beat, chord on the off-beat (A minor; E major under bar 2's D#)
LH = [("A2", 4, "C3E3"), ("A2", 8, "C3E3"), ("A2", 12, "C3E3"), ("E2", 16, "B2E3"), ("A2", 20, "C3E3"), ("E2", 24, "B2E3"), ("A2", 28, "C3E3")]
def mel(upto, v=0.72, sh=0): return [(P(n) + sh, b, d, "R", v) for n, b, d in MEL if b < upto]
def oom(v=0.5, full=True):
    out = []
    for n, b, ch in LH:
        out.append((P(n), b, 1.8, "L", v))
        if full: out += [(P(ch[i:i + 2]), b + 2, 1.6, "L", v - 0.08) for i in (0, 2)]
    return out
A = mel(20) + [(P("A2"), 4, 8, "L", 0.5), (P("E2"), 12, 8, "L", 0.5)]                                   # grade 1: tune + one bass note
B = mel(32) + [(m, b, d, h, v) for m, b, d, h, v in oom(0.5, False)] + [(P("C3"), b + 2, 1.6, "L", 0.42) for n, b, ch in LH]  # grade 3
C = mel(32, 0.76) + oom(0.5) + [(P(n) - (3 if n in ("C5", "E5") else 4), b, d, "R", 0.48) for n, b, d in MEL if d >= 2]       # grade 5: thirds on long notes
D = mel(32, 0.84) + [(P(n) - 12, b, d, "R", 0.6) for n, b, d in MEL]                                       # grade 8: octaves
D += oom(0.58) + [(P(n) - 12 if P(n) - 12 >= 36 else P(n), b, 1.8, "L", 0.5) for n, b, ch in LH]
D += [(P(n), 32 + j * 0.5, 0.5, "R", 0.55 + 0.04 * j) for j, n in enumerate(["A4", "B4", "C5", "D5", "E5", "F5", "G#5", "A5"])] + [(P("E2"), 32, 4, "L", 0.6), (P("E3"), 32, 4, "L", 0.5)]
F = 36
D += [(P(n), F + j * 0.06, 26, "L", 0.9) for j, n in enumerate(["A2", "E3", "A3", "C4"])]
D += [(P(n), F + 0.25 + j * 0.06, 26, "R", 0.82 + 0.03 * j) for j, n in enumerate(["E4", "A4", "C5", "E5", "A5"])]
make(HERE, "Turkish March 🎹", [(A, 20, 380, None), (B, 32, 470, None), (C, 32, 500, None), (D, 36, 540, None)], F, [1, 3, 5, 8])
