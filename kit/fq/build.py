# Product-led: only 20 minutes a day? Für Elise (Beethoven, public domain) as one 20-min session: Warm-up 5 / Main work 10 / Run-through 5, then the goal. A minor 3/8, unit = 16th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
RH = [(0, "E5", 1), (1, "D#5", 1), (2, "E5", 1), (3, "D#5", 1), (4, "E5", 1), (5, "B4", 1), (6, "D5", 1), (7, "C5", 1), (8, "A4", 2),
      (11, "C4", 1), (12, "E4", 1), (13, "A4", 1), (14, "B4", 2), (17, "E4", 1), (18, "G#4", 1), (19, "B4", 1), (20, "C5", 2),
      (23, "E4", 1), (24, "E5", 1), (25, "D#5", 1), (26, "E5", 1), (27, "D#5", 1), (28, "E5", 1), (29, "B4", 1), (30, "D5", 1), (31, "C5", 1), (32, "A4", 2)]
LH = [(8, "A2"), (9, "E3"), (10, "A3"), (14, "E2"), (15, "E3"), (16, "G#3"), (20, "A2"), (21, "E3"), (22, "A3"), (32, "A2"), (33, "E3"), (34, "A3")]
def play(lo=0, hi=99, shift=0, v=0.76, lh=True, rh=True):
    out = [(P(n), b - shift, d * 0.85, "R", v) for b, n, d in RH if rh and lo <= b < hi]
    return out + [(P(n), b - shift, 0.9, "L", v - 0.26) for b, n in LH if lh and lo <= b < hi]
A = [(P(n), b, 0.85, "R", 0.6) for b, n in enumerate(["E5", "D#5", "E5", "D#5", "E5", "D#5", "E5", "D#5", "E5", "B4", "D5", "C5"])]   # warm-up: the E–D# turn, right hand
B = play(0, 11, v=0.66)                 # main work: bars 1–4, hands together, tempo target
C = play(0, 23, v=0.72)                 # run-through: bars 1–8
D = play(0, 32, v=0.84)                 # goal: full tempo
F = 32
D += [(P(n), F + j * 0.06, 26, "L", 0.85) for j, n in enumerate(["A2", "E3", "A3"])]
D += [(P(n), F + 0.25 + j * 0.06, 26, "R", 0.78 + 0.02 * j) for j, n in enumerate(["C4", "E4", "A4", "C5", "E5"])]
make(HERE, [(A, 12, 300, None), (B, 11, 230, None), (C, 23, 380, None), (D, 32, 460, None)], F,
     {"piece": "Only 20 min a day? ⏱️", "q": "<span class='hl'>Für Elise</span> in 20 min", "labels": ["1", "2", "3", "🎯"],
      "chips": ["Warm-up · 5 min", "Main work · 10 min · slow 🐢", "Run-through · 5 min", "The goal: full tempo 🎯"], "wait": "wait for the goal 🎯", "rows": [], "rowsize": 60,
      "endq": "Only <span class='hl'>20 minutes?</span> 👇<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Pick 20-min sessions → free Day 1 plan</div>", "end2": ""},
     kicks={3: [0, 6, 12, 18, 24]}, tail=6.8, ec=3.8,
     plan={"at": 1.0, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Für Elise", "sub": "Beethoven · 5 days a week",
           "chips": ["Bars 1–4", "20-min sessions"], "mins": [5, 10, 5], "tempo": 40, "bpm": 56,
           "milestone": "Bars 1–8 hands together at 50%"})
