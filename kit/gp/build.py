# Gymnopédie No.1 (Satie, public domain): no pedal vs TOO much pedal vs just right. 3/4, unit = quarter.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
MEL = [("F#5", 0), ("A5", 1), ("G5", 2), ("F#5", 3), ("C#5", 4), ("B4", 5), ("C#5", 6), ("D5", 7), ("A4", 8)]
CH = [("G2", ["B3", "D4", "F#4"]), ("D2", ["A3", "C#4", "F#4"]), ("G2", ["B3", "D4", "F#4"])]
def lvl(bars, v=0.62, lv=0.42):
    out = [(P(n), b, 1, "R", v) for n, b in MEL if b < bars * 3]
    for i in range(bars):
        bs, ch = CH[i % 2 if i < 2 else 2]
        out.append((P(bs), i * 3, 1, "L", lv + 0.06))
        out += [(P(n), i * 3 + 1, 2, "L", lv) for n in ch]
    return out
A = lvl(2, 0.6); B = lvl(2, 0.62); C = lvl(2, 0.64)
D = lvl(3, 0.7, 0.46)
F = 9
D += [(P(n), F + j * 0.07, 30, "L", 0.62) for j, n in enumerate(["D2", "A3", "C#4"])]
D += [(P(n), F + 0.2 + j * 0.07, 30, "R", 0.6 + 0.03 * j) for j, n in enumerate(["F#4", "A4", "F#5"])]
make(HERE, [(A, 6, 105, None), (B, 6, 105, 99), (C, 6, 105, 3), (D, 9, 100, 3)], F,
     {"piece": "Gymnopédie No. 1 🎹", "q": "Too much <span class='hl'>pedal?</span> 😬", "labels": ["🧱", "🌊", "✅", "✨"],
      "chips": ["No pedal · dry", "TOO much pedal · mud", "Change it every bar ✅", "Just right ✨"], "wait": "listen for the mud 🌊",
      "rows": ["🧱 No pedal = dry", "🌊 Never lift = mud", "✅ Lift on each new chord"], "rowsize": 62,
      "endq": "Which one do<br><span class='hl'>you</span> do? 😅👇", "end2": "A day-by-day plan for your piece 👇"},
     sfx=[("ding", 2, 0, 0.02)])
