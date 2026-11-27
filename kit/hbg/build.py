# Guess the grade: Happy Birthday (melody public domain in the US since 2016 and the EU since 2017). C major 3/4, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
SONG = [("G4",0,1.5),("G4",1.5,.5),("A4",2,2),("G4",4,2),("C5",6,2),("B4",8,4),("G4",12,1.5),("G4",13.5,.5),("A4",14,2),("G4",16,2),("D5",18,2),("C5",20,4),
        ("G4",24,1.5),("G4",25.5,.5),("G5",26,2),("E5",28,2),("C5",30,2),("B4",32,2),("A4",34,2),("F5",36,1.5),("F5",37.5,.5),("E5",38,2),("C5",40,2),("D5",42,2),("C5",44,6)]
BARS = [(2, "C3", ["E3", "G3", "C4"]), (8, "G2", ["F3", "G3", "B3"]), (14, "G2", ["F3", "G3", "B3"]), (20, "C3", ["E3", "G3", "C4"]),
        (26, "C3", ["E3", "G3", "Bb3"]), (32, "F2", ["F3", "A3", "C4"]), (38, "C3", ["E3", "G3", "C4"]), (44, "C3", ["E3", "G3", "C4"])]
def mel(a, b, v=0.72, lo=0):
    return [(P(n) - lo, t - a, d * 0.95, "R", v) for n, t, d in SONG if a <= t < b]
def waltz(a, b, v=0.44, full=True):
    out = []
    for s, r, ch in BARS:
        if not (a <= s < b): continue
        out.append((P(r), s - a, 1.8, "L", v + 0.06))
        if full: out += [(P(n), s - a + k, 1.6, "L", v - 0.04) for k in (2, 4) for n in ch]
    return out
# Grade 1: phrase 1, melody + one bass note per bar
A = mel(0, 12) + waltz(0, 12, full=False)
# Grade 3: phrase 2 + waltz LH
B = mel(12, 24) + waltz(12, 24)
# Grade 5: phrases 3-4 (the big "happy birthday dear…") + waltz LH
C = mel(24, 50, v=0.76) + waltz(24, 50, v=0.46)
# Grade 8: whole song, melody in octaves, octave bass, thicker chords, run up, rolled C
D = []
for n, t, d in SONG[:-1]:
    D += [(P(n), t, d * 0.9, "R", 0.84), (P(n) - 12, t, d * 0.9, "R", 0.58)]
for s, r, ch in BARS[:-1]:
    lo = P(r) - 12 if P(r) - 12 >= 36 else P(r); D += [(lo, s, 1.8, "L", 0.62), (lo + 12, s, 1.8, "L", 0.5)] + [(P(n), s + k, 1.6, "L", 0.44) for k in (2, 4) for n in ch]
RUN = ["E4", "F4", "G4", "A4", "B4", "C5", "D5", "E5"]
D += [(P(n), 44 + j * 0.25, 0.3, "R", 0.6 + 0.03 * j) for j, n in enumerate(RUN)] + [(P("G2"), 44, 2, "L", 0.6), (P("G3"), 44, 2, "L", 0.5)]
F = 46
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["C2", "G2", "C3", "E3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["G4", "C5", "E5", "C6"])]
make(HERE, [(A, 12, 260, None), (B, 12, 300, None), (C, 26, 400, None), (D, 46, 560, None)], F,
     {"piece": "Guess the grade: Happy Birthday 🎂", "q": "Grade 1? 5? <span class='hl'>8?</span>", "labels": ["A", "B", "C", "D"],
      "chips": ["Grade ? 🤔", "Grade ? 🤔", "Grade ? 🤔", "Grade ? 🔥"], "answers": ["Grade 1 ✅", "Grade 3 ✅", "Grade 5 ✅", "Grade 8 ✅"],
      "wait": "comment your guess 👇", "rows": [], "rowsize": 60,
      "endq": "Which one can <span class='hl'>you</span> play?<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Type the piece in → free Day 1 plan</div>", "end2": ""},
     answers=True, kicks={3: [0, 12, 24, 36]}, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Happy Birthday", "sub": "Party version · your grade",
           "chips": ["Bars 1–4", "Hands separate"], "mins": [5, 10, 5], "tempo": 50, "bpm": 45,
           "milestone": "Whole song hands together at 70%"})
