# Guess the song #4: Twinkle Twinkle (traditional), Canon in D (Pachelbel), Eine kleine Nachtmusik (Mozart), Flight of the Bumblebee (Rimsky-Korsakov). All public domain.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
def seq(spec, b=0, v=0.74, stac=0.9, h="R", sh=0):
    out = []
    for n, d in spec:
        if n != "r": out.append((P(n) + sh, b, d * stac, h, v))
        b += d
    return out
# 1 Twinkle (unit = 8th)
A = seq([("C5", 2), ("C5", 2), ("G5", 2), ("G5", 2), ("A5", 2), ("A5", 2), ("G5", 4)]) + N(("C3", 0, 8), ("F3", 8, 4), ("C3", 12, 6), h="L", v=0.5)
# 2 Canon in D: one melody note per bass note
CM = ["F#5", "E5", "D5", "C#5", "B4", "A4", "B4", "C#5"]; CB = [("D3", "A3"), ("A2", "E3"), ("B2", "F#3"), ("F#2", "C#3"), ("G2", "D3"), ("D2", "A2"), ("G2", "D3"), ("A2", "E3")]
B = seq([(n, 2) for n in CM], v=0.72, stac=0.98)
for i, (lo, hi) in enumerate(CB): B += N((lo, i * 2, 2), h="L", v=0.5) + N((hi, i * 2, 2), h="L", v=0.38)
# 3 Eine kleine Nachtmusik: opening in octaves
EK = [("G4", 2), ("r", 1), ("D4", 1), ("G4", 2), ("r", 1), ("D4", 1), ("G4", 1), ("D4", 1), ("G4", 1), ("B4", 1), ("D5", 4)]
C = seq(EK, v=0.8, stac=0.8) + seq(EK, v=0.6, stac=0.8, h="L", sh=-12)
# 4 Flight of the Bumblebee (16ths, an octave down to fit the keyboard)
FB = ["E5", "D#5", "D5", "C#5", "D5", "C#5", "C5", "B4", "C5", "B4", "A#4", "A4", "G#4", "G4", "F#4", "F4"]
D = []
for k, sh in enumerate([0, -12]): D += [(P(n) + sh, k * 16 + i, 0.9, "A", 0.78) for i, n in enumerate(FB)]
D += N(("A2", 0, 2), ("A2", 8, 2), ("A2", 16, 2), ("E2", 24, 2), h="L", v=0.6)
F = 34
D += [(P(n), F + j * 0.06, 26, "L", 0.9) for j, n in enumerate(["A2", "E3", "A3", "C4"])]
D += [(P(n), F + 0.25 + j * 0.06, 26, "R", 0.84 + 0.02 * j) for j, n in enumerate(["E4", "A4", "C5", "E5", "A5"])]
make(HERE, [(A, 22, 420, None), (B, 22, 400, None), (C, 22, 420, None), (D, 34, 720, None)], F,
     {"piece": "Guess the song #4 🎵", "q": "Easy → <span class='hl'>Impossible</span> 💀", "labels": ["#1", "#2", "#3", "#4"],
      "chips": ["Easy", "Medium", "Hard", "Impossible 💀"], "answers": ["Twinkle Twinkle ✅", "Canon in D ✅", "Eine kleine Nachtmusik ✅", "Flight of the Bumblebee ✅"],
      "wait": "#4 is IMPOSSIBLE 💀",
      "rows": ["1 · Twinkle Twinkle", "2 · Canon in D (Pachelbel)", "3 · Eine kleine Nachtmusik", "4 · Flight of the Bumblebee"], "rowsize": 52,
      "endq": "How many did<br><span class='hl'>you</span> get? 👇", "end2": "Day 1 free · no card 👇"}, answers=True)
