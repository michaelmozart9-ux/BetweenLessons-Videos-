# Product-led: practising Für Elise (Beethoven, public domain) wrong vs right. Full speed = same mistake; plan's tempo target = clean. A minor 3/8, unit = 16th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
RH = [(0, "E5", 1), (1, "D#5", 1), (2, "E5", 1), (3, "D#5", 1), (4, "E5", 1), (5, "B4", 1), (6, "D5", 1), (7, "C5", 1), (8, "A4", 2),
      (11, "C4", 1), (12, "E4", 1), (13, "A4", 1), (14, "B4", 2), (17, "E4", 1), (18, "G#4", 1), (19, "B4", 1), (20, "C5", 2),
      (23, "E4", 1), (24, "E5", 1), (25, "D#5", 1), (26, "E5", 1), (27, "D#5", 1), (28, "E5", 1), (29, "B4", 1), (30, "D5", 1), (31, "C5", 1), (32, "A4", 2)]
LH = [(8, "A2"), (9, "E3"), (10, "A3"), (14, "E2"), (15, "E3"), (16, "G#3"), (20, "A2"), (21, "E3"), (22, "A3"), (32, "A2"), (33, "E3"), (34, "A3")]
WRONG = 30
def play(lo=0, hi=99, shift=0, v=0.76, crash=False, stac=0.85):
    out = []
    for b, n, d in RH:
        if not (lo <= b < hi) or (crash and b > WRONG): continue
        m, h = P(n), "R"
        if crash and b == WRONG: m -= 1; h = "X"
        out.append((m, b - shift, d * stac, h, v))
    for b, n in LH:
        if lo <= b < hi and not (crash and b > WRONG): out.append((P(n), b - shift, 0.9, "L", v - 0.26))
    if crash: out += [(P(n), WRONG + 1 - shift, 2, "X", 0.85) for n in ["B4", "C5", "C#5", "D5"]]
    return out
A = play(0, 33, crash=True)                      # ❌ full speed, attempt 1
B = play(23, 33, shift=23, crash=True)           # ❌ attempt 9, same bar, same mistake
C = play(23, 34, shift=23, v=0.66)               # ✅ the plan's tempo target: 40%
D = play(0, 32, v=0.84)                          # 🔥 later: clean at full speed
F = 32
D += [(P(n), F + j * 0.06, 26, "L", 0.85) for j, n in enumerate(["A2", "E3", "A3"])]
D += [(P(n), F + 0.25 + j * 0.06, 26, "R", 0.78 + 0.02 * j) for j, n in enumerate(["C4", "E4", "A4", "C5", "E5"])]
make(HERE, [(A, 33, 420, None), (B, 10, 420, None), (C, 11, 168, None), (D, 32, 400, None)], F,
     {"piece": "Stop practising Für Elise like this", "q": "❌ vs <span class='hl'>✅</span>", "labels": ["❌", "❌", "✅", "🔥"],
      "chips": ["Full speed · attempt 1", "Attempt 9… same mistake 🔁", "Plan: 40% tempo target 🐢", "Weeks later · clean 🔥"], "wait": "wait for ✅",
      "rows": ["❌ Full speed = same mistake", "✅ Tempo target = clean"], "rowsize": 62,
      "endq": "Stuck on a bar? 👇<div style='font-size:44px;font-weight:800;color:#F2C66B;margin-top:14px'>Type your piece in → free Day 1 plan</div>", "end2": ""},
     kicks={3: [0, 6, 12, 18, 24]}, sfx=[("buzz", 0, WRONG, 0.045), ("buzz", 0, WRONG + 1, 0.06), ("buzz", 1, WRONG - 23, 0.045), ("buzz", 1, WRONG - 22, 0.06), ("scratch", 1, WRONG - 21.5, 0.05)],
     tail=5.0,
     plan={"at": 1.3, "top": 430, "day": "Week 1 · Day 1 · 20 min", "piece": "Für Elise", "sub": "Beethoven",
           "chips": ["Bars 1–8", "Hands separate"], "mins": [5, 10, 5], "tempo": 40, "bpm": 56,
           "milestone": "Bars 1–8 hands together at 50%"})
