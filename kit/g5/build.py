# Guess the song #5: Happy Birthday (Hill, public domain), Beethoven's 5th, The Entertainer (Joplin, d. 1917), Moonlight Sonata 3rd mvt (Beethoven). All public domain.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
def seq(spec, b=0, v=0.74, stac=0.9, h="R", sh=0):
    out = []
    for n, d in spec:
        if n != "r": out.append((P(n) + sh, b, d * stac, h, v))
        b += d
    return out
# 1 Happy Birthday (unit = 8th)
A = seq([("G4", 1.5), ("G4", 0.5), ("A4", 2), ("G4", 2), ("C5", 2), ("B4", 4)], v=0.74) + N(("C3", 2, 4), ("G2", 6, 6), h="L", v=0.5)
# 2 Beethoven 5: two motifs, melody + octave below
M5 = [("r", 1), ("G4", 1), ("G4", 1), ("G4", 1), ("Eb4", 4), ("r", 1), ("F4", 1), ("F4", 1), ("F4", 1), ("D4", 6)]
B = seq(M5, v=0.82, stac=0.8) + seq(M5, v=0.62, stac=0.8, h="L", sh=-12)
# 3 The Entertainer (unit = 16th), ragtime oom-pah left hand
ENT = [("D4", 1), ("D#4", 1), ("E4", 2), ("C5", 2), ("E4", 2), ("C5", 2), ("E4", 2), ("C5", 6),
       ("C5", 1), ("D5", 1), ("D#5", 1), ("E5", 1), ("C5", 1), ("D5", 1), ("E5", 2), ("B4", 1), ("D5", 2), ("C5", 5)]
C = seq(ENT, v=0.78, stac=0.85)
for b in range(2, 36, 4):
    root, ch = ("G2", ["F3", "B3"]) if 26 <= b < 30 else ("C3", ["E3", "G3"])
    C += [(P(root), b, 1.6, "L", 0.5)] + [(P(x), b + 2, 1.4, "L", 0.42) for x in ch]
# 4 Moonlight Sonata 3rd mvt (unit = 16th): rising arpeggios + two stabs per bar
CM = ["G#2", "C#3", "E3", "G#3", "C#4", "E4", "G#4", "C#5", "E5", "G#5"]
G7 = ["G#2", "C3", "D#3", "F#3", "G#3", "C4", "D#4", "F#4", "G#4", "C5"]
D = []
for k, (arp, stab, bass) in enumerate([(CM, ["G#4", "C#5", "E5"], "C#2"), (G7, ["F#4", "G#4", "C5", "D#5"], "C2")]):
    b0 = 16 * k
    D += [(P(n), b0 + 2 + j, 0.9, "A", 0.7 + 0.015 * j) for j, n in enumerate(arp)]
    D += [(P(n), b0 + st, 0.8, "R", 0.88) for st in (12, 14) for n in stab]
    D += [(P(bass), b0, 4, "L", 0.62), (P(bass) + 12, b0, 4, "L", 0.52), (P(bass), b0 + 8, 4, "L", 0.6), (P(bass) + 12, b0 + 8, 4, "L", 0.5)]
F = 32
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["C#2", "G#2", "C#3", "E3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.84 + 0.02 * j) for j, n in enumerate(["G#3", "C#4", "E4", "G#4", "C#5"])]
make(HERE, [(A, 12, 300, None), (B, 18, 420, None), (C, 36, 560, None), (D, 32, 640, None)], F,
     {"piece": "Guess the song #5 🎵", "q": "Easy → <span class='hl'>Impossible</span> 💀", "labels": ["#1", "#2", "#3", "#4"],
      "chips": ["Easy", "Medium", "Hard", "Impossible 💀"], "answers": ["Happy Birthday ✅", "Beethoven's 5th ✅", "The Entertainer ✅", "Moonlight Sonata 3 ✅"],
      "wait": "#4 is IMPOSSIBLE 💀", "rows": [], "rowsize": 52,
      "endq": "How many did <span class='hl'>you</span> get?<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Want to play one? Type it in → free Day 1 plan</div>", "end2": ""},
     answers=True, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Moonlight Sonata, 3rd mvt", "sub": "Beethoven · your grade",
           "chips": ["Bars 1–2", "Right hand"], "mins": [5, 10, 5], "tempo": 40, "bpm": 64,
           "milestone": "Bars 1–8 hands separate at 50%"})
