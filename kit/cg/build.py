# Carol of the Bells (Leontovych, d. 1921, public domain): Grade 1 vs 3 vs 5 vs 8, then plan phone + "Which grade are you?" end card. G minor 3/4, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
OST = [("Bb4", 0, 2), ("A4", 2, 1), ("Bb4", 3, 1), ("G4", 4, 2)]          # the 4-note bell figure, one bar
UP = [("D5", 0, 2), ("C5", 2, 1), ("D5", 3, 1), ("Bb4", 4, 2)]            # the same figure a third higher
def bar(fig, b0, v=0.72, sh=0, stac=0.85, h="R"): return [(P(n) + sh, b0 + b, d * stac, h, v) for n, b, d in fig]
BASS = ["G2", "F2", "Eb2", "D2"]
# Grade 1: tune + one held bass note
A = bar(OST, 0, 0.7) + bar(OST, 6, 0.7) + [(P("G3"), 0, 12, "L", 0.45)]
# Grade 3: 4 bars, descending bass line (one note per bar)
B = sum([bar(OST, 6 * i, 0.72) for i in range(4)], []) + [(P(n) + 12, 6 * i, 5.6, "L", 0.48) for i, n in enumerate(BASS)]
# Grade 5: bars 3-4 go up a third over the bell figure, bass root + fifth on each beat
C = bar(OST, 0, 0.74) + bar(OST, 6, 0.74) + bar(UP, 12, 0.8) + bar(OST, 12, 0.5) + bar(UP, 18, 0.8) + bar(OST, 18, 0.5)
for i, n in enumerate(BASS): C += [(P(n), 6 * i, 1.8, "L", 0.5), (P(n) + 7, 6 * i + 2, 1.6, "L", 0.42), (P(n) + 12, 6 * i + 4, 1.6, "L", 0.42)]
# Grade 8: upper line in octaves + bell figure, octave stride bass, run up into a rolled G minor chord
D = []
for i in range(4):
    D += bar(UP if i % 2 else OST, 6 * i, 0.86) + bar(UP if i % 2 else OST, 6 * i, 0.64, sh=-12)
    D += bar(OST, 6 * i, 0.5, sh=12, stac=0.5) if i >= 2 else []
    n = BASS[i]; D += [(P(n), 6 * i, 1.8, "L", 0.62), (P(n) + 12, 6 * i, 1.8, "L", 0.52)] + [(P(x), 6 * i + o, 1.4, "L", 0.42) for o in (2, 4) for x in ([BASS[i][:-1] + "3", "Bb3", "D4"] if i == 0 else [n[:-1] + "3"])]
RUN = ["G4", "A4", "Bb4", "C5", "D5", "Eb5", "F#5", "G5"]
D += [(P(n), 24 + j * 0.5, 0.5, "R", 0.6 + 0.03 * j) for j, n in enumerate(RUN[:-1])] + [(P("D2"), 24, 4, "L", 0.62), (P("D3"), 24, 4, "L", 0.5)]
F = 28
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["G2", "D3", "G3", "Bb3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["D4", "G4", "Bb4", "D5", "G5"])]
make(HERE, [(A, 12, 330, None), (B, 24, 400, None), (C, 24, 420, None), (D, 28, 480, None)], F,
     {"piece": "Carol of the Bells 🔔", "q": "Grade 1 vs <span class='hl'>Grade 8</span>", "labels": ["1", "3", "5", "8"],
      "chips": ["Grade 1", "Grade 3", "Grade 5", "Grade 8 🔥"], "wait": "wait for Grade 8 🔥", "rows": [], "rowsize": 60,
      "endq": "Want to play <span class='hl'>this?</span> 👇<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Type the piece in → free Day 1 plan</div>", "end2": ""},
     kicks={3: [0, 6, 12, 18]}, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Carol of the Bells", "sub": "Leontovych · your grade",
           "chips": ["Bars 1–8", "Right hand"], "mins": [5, 10, 5], "tempo": 40, "bpm": 60,
           "milestone": "Bars 1–8 hands together at 50%"})
