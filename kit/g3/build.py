# Guess the song #3: Happy Birthday, Gymnopedie No.1 (Satie), Minuet in G (Petzold), Toccata in D minor (Bach). All public domain.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
def seq(spec, b=0, v=0.74, stac=0.9, h="R", sh=0):
    out = []
    for n, d in spec:
        if n != "r": out.append((P(n) + sh, b, d * stac, h, v))
        b += d
    return out
A = seq([("G4", 1.5), ("G4", 0.5), ("A4", 4), ("G4", 4), ("C5", 4), ("B4", 8)]) + N(("C3", 2, 12), ("G2", 14, 8), h="L", v=0.5)
B = seq([("r", 2), ("F#5", 2), ("A5", 2), ("G5", 2), ("F#5", 2), ("C#5", 2), ("B4", 2), ("C#5", 2), ("D5", 2), ("A4", 6)], v=0.72)
for i in range(4):
    b0 = i * 6; bass, ch = (("G2", ["B3", "D4", "F#4"]) if i % 2 == 0 else ("D2", ["A3", "C#4", "F#4"]))
    B += N((bass, b0, 2), h="L", v=0.5) + N(*[(c, b0 + 2, 4) for c in ch], h="L", v=0.38)
C = seq([("D5", 2), ("G4", 1), ("A4", 1), ("B4", 1), ("C5", 1), ("D5", 2), ("G4", 2), ("G4", 2), ("E5", 2), ("C5", 1), ("D5", 1), ("E5", 1), ("F#5", 1), ("G5", 2), ("G4", 2), ("G4", 2)], v=0.76)
C += N(("G2", 0, 6), ("B2", 6, 6), ("C3", 12, 6), ("B2", 18, 6), h="L", v=0.5) + N(("D3", 0, 4), ("D3", 12, 4), ("E3", 12, 4), h="L", v=0.36)
TOC = [("A5", 0.5), ("G5", 0.5), ("A5", 3), ("G5", 0.5), ("F5", 0.5), ("E5", 0.5), ("D5", 0.5), ("C#5", 2), ("D5", 4), ("A4", 0.5), ("G4", 0.5), ("A4", 3), ("E4", 1), ("F4", 1), ("C#4", 1), ("D4", 3)]
D = seq(TOC, v=0.84, stac=0.95) + seq(TOC, v=0.62, stac=0.95, sh=-12)
D += N(("D2", 0, 12), ("D3", 0, 12), ("D2", 12, 10), h="L", v=0.55)
F = 22
D += [(P(n), F + j * 0.06, 26, "L", 0.9) for j, n in enumerate(["D2", "A2", "D3", "F3"])]
D += [(P(n), F + 0.25 + j * 0.06, 26, "R", 0.84 + 0.02 * j) for j, n in enumerate(["C#4", "E4", "G4", "Bb4", "D5"])]
make(HERE, [(A, 22, 480, None), (B, 22, 400, 6), (C, 24, 500, None), (D, 22, 380, None)], F,
     {"piece": "Guess the song #3 🎵", "q": "Easy → <span class='hl'>Impossible</span> 💀", "labels": ["#1", "#2", "#3", "#4"],
      "chips": ["Easy", "Medium", "Hard", "Impossible 💀"], "answers": ["Happy Birthday ✅", "Gymnopédie No. 1 ✅", "Minuet in G ✅", "Toccata in D minor ✅"],
      "wait": "#4 is IMPOSSIBLE 💀",
      "rows": ["1 · Happy Birthday", "2 · Gymnopédie No. 1 (Satie)", "3 · Minuet in G", "4 · Toccata in D minor (Bach)"], "rowsize": 54,
      "endq": "How many did<br><span class='hl'>you</span> get? 👇", "end2": "Follow for #4 👀 · Free practice plan 👇"}, answers=True)
