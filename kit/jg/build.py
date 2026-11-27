# Guess the grade: Jingle Bells (James Lord Pierpont, 1857, public domain). Grades 1/3/5/8 hidden, revealed per level. C major, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
CH1 = [("E5",0,2),("E5",2,2),("E5",4,4),("E5",8,2),("E5",10,2),("E5",12,4),("E5",16,2),("G5",18,2),("C5",20,3),("D5",23,1),("E5",24,8)]
CH2 = [("F5",0,2),("F5",2,2),("F5",4,3),("F5",7,1),("F5",8,2),("E5",10,2),("E5",12,2),("E5",14,1),("E5",15,1),("E5",16,2),("D5",18,2),("D5",20,2),("E5",22,2),("D5",24,4),("G5",28,4)]
def mel(m, sh=0, v=0.72, lo=0, d0=None, d1=None):
    return [(P(n) - lo, t - sh, d * 0.95, "R", v) for n, t, d in m if (d0 is None or t >= d0) and (d1 is None or t < d1)]
# Grade 1: bars 1-2, melody an octave down + one long C per bar
A = mel(CH1, lo=12, d1=16) + [(P("C3"), 0, 7.8, "L", 0.45), (P("C3"), 8, 7.8, "L", 0.45)]
# Grade 3: bars 3-4 + root/fifth quarters
B = mel(CH1, sh=16, lo=12, d0=16)
for i in range(8): B.append((P("C3") + (7 if i % 2 else 0), 2 * i, 1.8, "L", 0.44))
# Grade 5: second phrase, melody + oom-pah LH (F, C, G, G)
C = mel(CH2, v=0.74)
for b, (r, ch) in enumerate([("F2", ["A3", "C4"]), ("C3", ["E3", "G3"]), ("G2", ["B3", "D4"]), ("G2", ["B3", "F4"])]):
    for q in range(4):
        t = 8 * b + 2 * q
        C += [(P(r), t, 1.8, "L", 0.5)] if q % 2 == 0 else [(P(n), t, 1.6, "L", 0.4) for n in ch]
# Grade 8: chorus in octaves + off-beat chord fills + stride bass + run + rolled C
D = []
for n, t, d in CH1:
    D += [(P(n), t, d * 0.9, "R", 0.84), (P(n) - 12, t, d * 0.9, "R", 0.6)]
for i in range(16): D.append((P(["G4", "C5"][i % 2]), 2 * i + 1, 0.8, "R", 0.4))
for q in range(16):
    t = 2 * q
    D += [(P("C2"), t, 1.8, "L", 0.62), (P("C3"), t, 1.8, "L", 0.5)] if q % 2 == 0 else [(P(n), t, 1.6, "L", 0.44) for n in ["E3", "G3", "C4"]]
RUN = ["G4", "A4", "B4", "C5", "D5", "E5", "F5", "G5"]
D += [(P(n), 32 + j * 0.5, 0.5, "R", 0.6 + 0.03 * j) for j, n in enumerate(RUN)] + [(P("G2"), 32, 4, "L", 0.62), (P("G3"), 32, 4, "L", 0.5)]
F = 36
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["C2", "G2", "C3", "E3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["G4", "C5", "E5", "G5"])]
make(HERE, [(A, 16, 320, None), (B, 16, 380, None), (C, 32, 460, None), (D, 36, 540, None)], F,
     {"piece": "Guess the grade: Jingle Bells 🔔", "q": "Grade 1? 5? <span class='hl'>8?</span>", "labels": ["A", "B", "C", "D"],
      "chips": ["Grade ? 🤔", "Grade ? 🤔", "Grade ? 🤔", "Grade ? 🔥"], "answers": ["Grade 1 ✅", "Grade 3 ✅", "Grade 5 ✅", "Grade 8 ✅"],
      "wait": "comment your guess 👇", "rows": [], "rowsize": 60,
      "endq": "Which one can <span class='hl'>you</span> play?<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Type the piece in → free Day 1 plan</div>", "end2": ""},
     answers=True, kicks={3: [0, 8, 16, 24]}, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Jingle Bells", "sub": "Pierpont · your grade",
           "chips": ["Chorus", "Right hand"], "mins": [5, 10, 5], "tempo": 40, "bpm": 48,
           "milestone": "Chorus hands together at 60%"})
