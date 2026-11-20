# Guess the famous classical piece: Brahms Lullaby, Vivaldi Spring, Habanera (Bizet), Flight of the Bumblebee (Rimsky-Korsakov). All public domain.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
def seq(spec, b=0, v=0.74, stac=0.9, h="R", sh=0):
    out = []
    for n, d in spec: out.append((P(n) + sh, b, d * stac, h, v)); b += d
    return out
# 1 Brahms Lullaby (3/4, unit 8th)
A = seq([("E5", 1), ("E5", 1), ("G5", 4), ("E5", 1), ("E5", 1), ("G5", 4), ("E5", 1), ("G5", 1), ("C6", 2), ("B5", 3), ("A5", 1), ("A5", 2), ("G5", 4)])
A += [(P(n), b, 1.6, "L", 0.4) for b, n in [(2, "C3"), (4, "G3"), (6, "E4"), (8, "C3"), (10, "G3"), (12, "E4"), (14, "C3"), (16, "A3"), (18, "F4"), (20, "G2"), (22, "D3"), (24, "B3")]]
# 2 Vivaldi Spring (unit 8th)
B = seq([("E5", 2), ("G#5", 1), ("G#5", 1), ("G#5", 1), ("F#5", 0.5), ("E5", 0.5), ("B5", 4), ("B5", 1), ("A5", 0.5), ("G#5", 0.5), ("G#5", 1), ("G#5", 1), ("F#5", 0.5), ("E5", 0.5), ("B5", 4)], v=0.76)
B += [(P(n), b, 0.9, "L", 0.48) for b in range(0, 22) for n in (["E3", "B3"] if b % 2 == 0 else ["G#3"])]
# 3 Habanera (unit 16th), chromatic fall over the habanera bass
HB = [("D5", 3), ("C#5", 1), ("C5", 2), ("C5", 2), ("B4", 3), ("Bb4", 1), ("A4", 2), ("Ab4", 1), ("G4", 1)]
C = seq(HB, 0, 0.78) + seq(HB, 16, 0.8)
for bar in range(4): b0 = bar * 8; C += N(("D2", b0, 3), ("A2", b0 + 3, 1), ("D3", b0 + 4, 2), ("A2", b0 + 6, 2), h="L", v=0.58)
# 4 Flight of the Bumblebee (unit 16th), chromatic, octaves, then crash
FB = ["E5", "D#5", "D5", "C#5", "C5", "B4", "C5", "C#5", "C5", "B4", "A#4", "A4", "G#4", "G4", "G#4", "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5"]
D = seq([(n, 1) for n in FB], v=0.82) + seq([(n, 1) for n in FB], v=0.6, sh=-12)
for b in range(0, 24, 4): D += N(("A2", b, 1), ("E3", b + 2, 1), h="L", v=0.55)
F = 24
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["A2", "E3", "A3", "C4"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["E4", "A4", "C5", "E5", "A5"])]
make(HERE, [(A, 26, 460, None), (B, 22, 480, None), (C, 32, 760, None), (D, 24, 900, None)], F,
     {"piece": "Guess the classical piece 🎻", "q": "Easy → <span class='hl'>Impossible</span> 💀", "labels": ["#1", "#2", "#3", "#4"],
      "chips": ["Easy", "Medium", "Hard", "Impossible 💀"], "answers": ["Brahms' Lullaby ✅", "Vivaldi: Spring ✅", "Habanera (Carmen) ✅", "Flight of the Bumblebee ✅"],
      "wait": "#4 is IMPOSSIBLE 💀",
      "rows": ["1 · Brahms' Lullaby", "2 · Vivaldi: Spring", "3 · Habanera (Bizet)", "4 · Flight of the Bumblebee"], "rowsize": 56,
      "endq": "How many did<br><span class='hl'>you</span> get? 👇", "end2": "Want to PLAY them? Day 1 is free 👇"}, answers=True,
     kicks={3: [0, 4, 8, 12, 16, 20]})
