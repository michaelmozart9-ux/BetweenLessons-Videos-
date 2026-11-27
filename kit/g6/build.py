# Guess the song #6: Hall of the Mountain King (Grieg, d. 1907), Swan Lake (Tchaikovsky, d. 1893), Carol of the Bells (Leontovych, d. 1921), Toccata and Fugue in D minor (Bach). All public domain.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
def seq(spec, b=0, v=0.74, stac=0.9, h="R", sh=0):
    out = []
    for n, d in spec:
        if n != "r": out.append((P(n) + sh, b, d * stac, h, v))
        b += d
    return out
# 1 Mountain King (unit = 8th), A minor
MK = [("A4", 1), ("B4", 1), ("C5", 1), ("D5", 1), ("E5", 1), ("C5", 1), ("E5", 2), ("D#5", 1), ("B4", 1), ("D#5", 2), ("D5", 1), ("A#4", 1), ("D5", 2)]
A = seq(MK, v=0.74, stac=0.75) + N(("A2", 0, 8), ("B2", 8, 4), ("A2", 12, 4), h="L", v=0.48)
# 2 Swan Lake theme (unit = 8th), B minor, melody + held chords
SW = [("F#5", 6), ("B4", 1), ("C#5", 1), ("D5", 1), ("E5", 1), ("F#5", 3), ("D5", 1), ("F#5", 3), ("D5", 1), ("F#5", 3), ("B4", 1), ("D5", 1), ("B4", 1), ("G4", 1), ("D5", 1), ("B4", 6)]
B = seq(SW, v=0.8, stac=0.92)
for b0, ch in [(0, ["B2", "F#3", "D4"]), (8, ["B2", "F#3", "D4"]), (16, ["G2", "D3", "B3"]), (24, ["B2", "F#3", "D4"])]:
    B += [(P(n), b0, 7.6, "L", 0.42) for n in ch]
# 3 Carol of the Bells (unit = 8th), bell figure + rising third, bass on each beat
OST = [("Bb4", 2), ("A4", 1), ("Bb4", 1), ("G4", 2)]; UP = [("D5", 2), ("C5", 1), ("D5", 1), ("Bb4", 2)]
C = seq(OST, 0, 0.76) + seq(OST, 6, 0.76) + seq(UP, 12, 0.82) + seq(OST, 12, 0.5) + seq(UP, 18, 0.82) + seq(OST, 18, 0.5)
for i, n in enumerate(["G2", "F2", "Eb2", "D2"]):
    C += [(P(n), 6 * i, 1.8, "L", 0.52), (P(n) + 7, 6 * i + 2, 1.6, "L", 0.42), (P(n) + 12, 6 * i + 4, 1.6, "L", 0.42)]
# 4 Toccata in D minor (unit = 16th): mordent motif in octaves, twice, then a fast run down into a rolled D minor chord
TC = [("A5", 1), ("G5", 1), ("A5", 6), ("r", 2), ("G5", 1), ("F5", 1), ("E5", 1), ("D5", 1), ("C#5", 4), ("D5", 6)]
D = seq(TC, 0, 0.9, 0.92) + seq(TC, 0, 0.7, 0.92, sh=-12) + seq(TC, 0, 0.66, 0.92, h="L", sh=-24) + seq(TC, 0, 0.56, 0.92, h="L", sh=-36)
D += seq(TC, 24, 0.86, 0.92, sh=-12) + seq(TC, 24, 0.66, 0.92, sh=-24) + seq(TC, 24, 0.6, 0.92, h="L", sh=-36)
RUN = ["D6", "C#6", "Bb5", "A5", "G5", "F5", "E5", "D5", "C#5", "Bb4", "A4", "G4", "F4", "E4", "D4", "C#4"]
RUN = [n for n in RUN if P(n) <= 84]
D += [(P(n), 48 + j * 0.5, 0.5, "R", 0.85 - 0.01 * j) for j, n in enumerate(RUN)] + [(P(n) - 12, 48 + j * 0.5, 0.5, "L", 0.6) for j, n in enumerate(RUN) if P(n) - 12 >= 36]
F = 48 + len(RUN) * 0.5 + 0.5
D += [(P(n), F + j * 0.06, 30, "L", 0.92) for j, n in enumerate(["D2", "A2", "D3", "F3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.84 + 0.02 * j) for j, n in enumerate(["A3", "D4", "F4", "A4", "D5"])]
make(HERE, [(A, 16, 330, None), (B, 32, 640, None), (C, 24, 460, None), (D, 56, 800, None)], F,
     {"piece": "Guess the song #6 🎵", "q": "Easy → <span class='hl'>Impossible</span> 💀", "labels": ["#1", "#2", "#3", "#4"],
      "chips": ["Easy", "Medium", "Hard", "Impossible 💀"], "answers": ["Mountain King ✅", "Swan Lake ✅", "Carol of the Bells ✅", "Bach Toccata ✅"],
      "wait": "#4 is IMPOSSIBLE 💀", "rows": [], "rowsize": 52,
      "endq": "How many did <span class='hl'>you</span> get?<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Want to play one? Type it in → free Day 1 plan</div>", "end2": ""},
     answers=True, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Carol of the Bells", "sub": "Leontovych · your grade",
           "chips": ["Bars 1–4", "Right hand"], "mins": [5, 10, 5], "tempo": 40, "bpm": 48,
           "milestone": "Bars 1–8 hands together at 60%"})
