# Morning Mood (Grieg, Peer Gynt, public domain) but it gets EPIC: calm -> brighter -> bigger -> EPIC, then the plan phone. E major 6/8, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
DU = [2, 1, 2, 1, 3, 3]
G1 = ["G#5", "E5", "D#5", "C#5", "D#5", "E5"]
G3 = ["D#5", "E5", "G#5", "E5", "G#5", "A5"]; D3 = [2, 1, 2, 1, 2, 1]
G4 = ["E5", "A5", "G#5", "E5", "D#5", "C#5"]
def grp(names, durs, b0):
    out, b = [], b0
    for n, d in zip(names, durs): out.append((P(n), b, d)); b += d
    return out
TH = {8: 4, 4: 3, 3: 4, 1: 4, 9: 3, 6: 3}  # diatonic third below in E major (pitch class -> semitones)
def mel(seq, v=0.7, stac=0.92, octv=False, third=False, drop=None):
    out = []
    for m, b, d in seq:
        if drop is not None and b >= drop: continue
        out.append((m, b, d * stac, "R", v))
        if octv: out.append((m - 12, b, d * stac, "R", v - 0.14))
        if third: out.append((m - TH[m % 12], b, d * stac, "R", v - 0.2))
    return out
ROOT = {"E": "E2", "A": "A2", "B": "B2"}
PAT = {"E": ["E2", "B2", "E3", "G#3", "E3", "B2"], "A": ["A2", "E3", "A3", "C#4", "A3", "E3"], "B": ["B2", "F#3", "B3", "D#4", "B3", "F#3"]}
def rolling(harm, v=0.5, units=1):
    out = []
    for b0, b1, c in harm:
        for u in range(b0, b1): out.append((P(PAT[c][u % 6]), u, 0.95, "L", v))
    return out
# A 🌅 calm: group 1, one soft held bass
A = mel(grp(G1, DU, 0), 0.5) + [(P("E3"), 0, 12, "L", 0.36), (P("B3"), 6, 6, "L", 0.3)]
# B ☀️ brighter: group 1 again with thirds, broken bass on each dotted quarter
B = mel(grp(G1, DU, 0), 0.64, third=True) + [(P(n), b, 2.8, "L", 0.42) for b, n in [(0, "E2"), (3, "B2"), (6, "E3"), (9, "B2")]]
# C 😳 bigger: groups 3-4 in octaves, rolling 8ths
C = mel(grp(G3, D3, 0) + grp(G4, DU, 12), 0.72, octv=True) + rolling([(0, 9, "E"), (9, 18, "A"), (18, 24, "B")], 0.48)
# D 🔥 EPIC: groups 1-2, octaves + thirds, octave bass + driving 8ths, chord on the last E
D = mel(grp(G1, DU, 0) + grp(G1, DU, 12), 0.84, octv=True, third=True, drop=21) + rolling([(0, 6, "E"), (6, 9, "B"), (9, 18, "E"), (18, 21, "B")], 0.56)
D += [(P(ROOT[c]), b, 2.5, "L", 0.62) for b, c in [(0, "E"), (3, "E"), (6, "B"), (9, "E"), (12, "E"), (15, "E"), (18, "B")]]
F = 21
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["E2", "B2", "E3", "G#3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["G#4", "B4", "E5", "G#5", "B5"])]
make(HERE, [(A, 12, 300, None), (B, 12, 330, None), (C, 24, 380, None), (D, 21, 420, None)], F,
     {"piece": "Morning Mood 🌅", "q": "but it gets <span class='hl'>EPIC</span> 😳", "labels": ["🌅", "☀️", "😳", "🔥"],
      "chips": ["Calm", "Brighter", "Bigger", "EPIC"], "wait": "wait for 🔥", "rows": [], "rowsize": 60,
      "endq": "Want to play <span class='hl'>this?</span> 👇<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Type the piece in → free Day 1 plan</div>", "end2": ""},
     kicks={3: [0, 3, 6, 9, 12, 15, 18]}, tail=4.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Morning Mood", "sub": "Grieg · Peer Gynt",
           "chips": ["Opening theme", "Right hand"], "mins": [5, 10, 5], "tempo": 40, "bpm": 40,
           "milestone": "Opening theme hands together at 50%"})
