# Guess the grade: Canon in D (Pachelbel, d. 1706, public domain). Grades 1/3/5/8 hidden, revealed at the end of each level. D major, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
BASS = ["D3", "A2", "B2", "F#2", "G2", "D2", "G2", "A2"]          # ground bass, one per 4 units
FIFTH = {"D": 7, "A": 7, "B": 7, "F#": 7, "G": 7}
HALF = ["F#5", "E5", "D5", "C#5", "B4", "A4", "B4", "C#5"]        # violin 1 entry
EIGHTH = ["D5", "F#5", "A5", "G5", "F#5", "D5", "F#5", "E5", "D5", "B4", "D5", "A4", "G4", "B4", "A4", "G4"]
THIRD = {"D3": "F#3", "A2": "C#3", "B2": "D3", "F#2": "A2", "G2": "B2", "D2": "F#2"}
# Grade 1: half-note tune + one bass note per harmony (first 4 harmonies)
A = [(P(n), 4 * i, 3.8, "R", 0.7) for i, n in enumerate(HALF[:4])] + [(P(n) + (12 if P(n) < 45 else 0), 4 * i, 3.8, "L", 0.45) for i, n in enumerate(BASS[:4])]
# Grade 3: 8th-note variation (first half) + bass root then fifth
B = [(P(n), 2 * i, 1.8, "R", 0.72) for i, n in enumerate(EIGHTH[:8])]
for i, n in enumerate(BASS[:4]): r = P(n) + (12 if P(n) < 45 else 0); B += [(r, 4 * i, 1.8, "L", 0.46), (r + 7, 4 * i + 2, 1.8, "L", 0.42)]
# Grade 5: full 8th variation + the canon line underneath + broken-chord LH
C = [(P(n), 2 * i, 1.8, "R", 0.74) for i, n in enumerate(EIGHTH)] + [(P(n) - 12, 4 * i, 3.8, "R", 0.42) for i, n in enumerate(HALF)]
for i, n in enumerate(BASS): r = P(n); C += [(r + o, 4 * i + j, 0.9, "L", 0.44 - 0.03 * (j % 2)) for j, o in enumerate([0, 7, 12, 7])]
# Grade 8: tune in octaves + 8th filler between, canon line, octave bass, run into rolled D major
D = []
for i, n in enumerate(EIGHTH):
    D += [(P(n), 2 * i, 1.6, "R", 0.84), (P(n) - 12, 2 * i, 1.6, "R", 0.6), (P(["F#4", "C#5", "D5", "A4", "B4", "F#4", "B4", "C#5"][i // 2]), 2 * i + 1, 0.8, "R", 0.42)]
D += [(P(n) - 12, 4 * i, 3.8, "R", 0.44) for i, n in enumerate(HALF)]
for i, n in enumerate(BASS): r = P(n); r = r - 12 if r - 12 >= 36 else r; D += [(r, 4 * i, 1.8, "L", 0.62), (r + 12, 4 * i, 1.8, "L", 0.5), (r + 12 + 7, 4 * i + 2, 1.6, "L", 0.44), (r + 24, 4 * i + 3, 0.9, "L", 0.4)]
RUN = ["A4", "B4", "C#5", "D5", "E5", "F#5", "G5", "A5"]
D += [(P(n), 32 + j * 0.5, 0.5, "R", 0.6 + 0.03 * j) for j, n in enumerate(RUN)] + [(P("A2"), 32, 4, "L", 0.62), (P("A3"), 32, 4, "L", 0.5)]
F = 36
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["D2", "A2", "D3", "F#3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["A4", "D5", "F#5", "A5"])]
make(HERE, [(A, 16, 320, None), (B, 16, 400, None), (C, 32, 480, None), (D, 36, 540, None)], F,
     {"piece": "Guess the grade: Canon in D 🎻", "q": "Grade 1? 5? <span class='hl'>8?</span>", "labels": ["A", "B", "C", "D"],
      "chips": ["Grade ? 🤔", "Grade ? 🤔", "Grade ? 🤔", "Grade ? 🔥"], "answers": ["Grade 1 ✅", "Grade 3 ✅", "Grade 5 ✅", "Grade 8 ✅"],
      "wait": "comment your guess 👇", "rows": [], "rowsize": 60,
      "endq": "Which one can <span class='hl'>you</span> play?<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Type the piece in → free Day 1 plan</div>", "end2": ""},
     answers=True, kicks={3: [0, 8, 16, 24]}, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Canon in D", "sub": "Pachelbel · your grade",
           "chips": ["Bars 1–4", "Right hand"], "mins": [5, 10, 5], "tempo": 40, "bpm": 32,
           "milestone": "Bars 1–8 hands together at 50%"})
