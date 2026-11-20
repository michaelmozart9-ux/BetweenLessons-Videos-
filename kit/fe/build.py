# Guess the grade: Für Elise (Beethoven, public domain). A minor, unit = 16th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from gtg import *
MEL = [("E5", 0, 1), ("D#5", 1, 1), ("E5", 2, 1), ("D#5", 3, 1), ("E5", 4, 1), ("B4", 5, 1), ("D5", 6, 1), ("C5", 7, 1),
       ("A4", 8, 3), ("C4", 11, 1), ("E4", 12, 1), ("A4", 13, 1), ("B4", 14, 3), ("E4", 17, 1), ("G#4", 18, 1), ("B4", 19, 1),
       ("C5", 20, 3), ("E4", 23, 1), ("E5", 24, 1), ("D#5", 25, 1)]
LH = [("A2", 8), ("E3", 9), ("A3", 10), ("E2", 14), ("E3", 15), ("G#3", 16), ("A2", 20), ("E3", 21), ("A3", 22)]
def mel(upto=26, v=0.72, skip_arp=False):
    return [(P(n), b, d, "R", v) for n, b, d in MEL if b < upto and not (skip_arp and b in (11, 12, 13, 17, 18, 19, 23))]
A = mel(20, skip_arp=True) + [(P("A2"), 8, 6, "L", 0.5), (P("E2"), 14, 6, "L", 0.5)]                       # grade 1
B = mel(26) + [(P(n), b, 1.6, "L", 0.5) for n, b in LH]                                                        # grade 3 (as written)
C = mel(26, 0.76) + [(P(n), b, 1.6, "L", 0.5) for n, b in LH] + [(P(n) - 12, b, 1.6, "L", 0.42) for n, b in LH if n in ("A2", "E2") and False]
C += [(P(n) - (3 if n in ("C5", "A4") else 4), b, d, "R", 0.48) for n, b, d in MEL if b in (8, 14, 20)]   # grade 5: harmony on long notes
D = mel(26, 0.84) + [(P(n) - 12, b, d, "R", 0.6) for n, b, d in MEL if b < 26 and P(n) >= 69]               # grade 8: octaves
D += [(P(n), b, 1, "L", 0.55) for n, b in LH] + [(P(n) - 12 if P(n) - 12 >= 36 else P(n), b, 1, "L", 0.48) for n, b in LH if n in ("A2", "E2")]
for b0, ch in [(0, ["A2", "E3", "A3", "C4"]), (2, ["A2", "E3", "A3", "C4"])]: pass
D += [(P(n), 26 + j * 0.5, 0.5, "R", 0.55 + 0.04 * j) for j, n in enumerate(["A4", "B4", "C5", "D5", "E5", "F5", "G#5", "A5"])] + [(P("E2"), 26, 4, "L", 0.6), (P("E3"), 26, 4, "L", 0.5)]
F = 30
D += [(P(n), F + j * 0.06, 26, "L", 0.9) for j, n in enumerate(["A2", "E3", "A3", "C4"])]
D += [(P(n), F + 0.25 + j * 0.06, 26, "R", 0.82 + 0.03 * j) for j, n in enumerate(["E4", "A4", "C5", "E5", "A5"])]
make(HERE, "Für Elise 🎹", [(A, 20, 360, None), (B, 26, 400, None), (C, 26, 430, None), (D, 30, 460, None)], F, [1, 3, 5, 8])
