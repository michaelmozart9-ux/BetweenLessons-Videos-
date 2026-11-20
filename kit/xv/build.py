# Practising the hard bar: wrong vs right. Mozart, Turkish March (public domain). A minor, unit = 16th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
PH = [("B4", 1), ("A4", 1), ("G#4", 1), ("A4", 1), ("C5", 4), ("D5", 1), ("C5", 1), ("B4", 1), ("C5", 1), ("E5", 4),
      ("F5", 1), ("E5", 1), ("D#5", 1), ("E5", 1), ("B5", 1), ("A5", 1), ("G#5", 1), ("A5", 1), ("B5", 1), ("A5", 1), ("G#5", 1), ("A5", 1), ("C6", 4)]
def mel(lo=0, hi=99, v=0.76, wrong=(), stop=None, shift=0):
    out, b = [], 0
    for n, d in PH:
        if lo <= b < hi and (stop is None or b < stop):
            m = P(n); h = "R"
            if b in wrong: m -= 1; h = "X"
            out.append((m, b - shift, d * 0.8, h, v))
        b += d
    return out
LHP = [("A3", 4), ("C4", 6), ("E4", 6), ("A3", 8), ("C4", 10), ("E4", 10), ("A3", 12), ("C4", 14), ("E4", 14), ("E3", 16), ("B3", 18), ("E3", 20), ("B3", 22), ("A3", 24), ("C4", 26), ("E4", 26)]
def lh(lo=0, hi=99, stop=None, shift=0, v=0.48): return [(P(n), b - shift, 1, "L", v) for n, b in LHP if lo <= b < hi and (stop is None or b < stop)]
def fail(): return mel(0, 28, 0.78, wrong=(18, 19), stop=20) + lh(0, 28, stop=20) + [(P(n), 20, 2, "X", 0.85) for n in ["G4", "G#4", "A4", "B4"]]
A = fail(); B = fail()
C = mel(16, 28, 0.7, shift=16) + lh(16, 28, shift=16) + [(m, b + 12, d, h, v) for m, b, d, h, v in mel(16, 28, 0.74, shift=16) + lh(16, 28, shift=16)]
D = mel(0, 28, 0.84) + mel(0, 28, 0.6, shift=0)[:0] + lh(0, 28, v=0.55) + [(P(n) - 12, b, d, "L", 0.42) for n, b, d in [("A3", 4, 1), ("A3", 8, 1), ("A3", 12, 1), ("E3", 16, 1), ("E3", 20, 1), ("A3", 24, 1)]]
F = 28
D += [(P(n), F + j * 0.06, 26, "L", 0.9) for j, n in enumerate(["A2", "E3", "A3", "C4"])]
D += [(P(n), F + 0.25 + j * 0.06, 26, "R", 0.82 + 0.02 * j) for j, n in enumerate(["E4", "A4", "C5", "E5", "A5"])]
# c: first loop at 60% (384), second loop 80% -> place both at one tempo by stretching beats: second half uses beats*0.75
C = [(m, (b if b < 12 else 12 + (b - 12) * 0.75), d * (1 if b < 12 else 0.75), h, v) for m, b, d, h, v in C]
make(HERE, [(A, 23, 640, None), (B, 23, 640, None), (C, 21, 384, None), (D, 28, 640, None)], F,
     {"piece": "Practising the hard bar 🎹", "q": "❌ vs <span class='hl'>✅</span>", "labels": ["❌", "❌", "✅", "🔥"],
      "chips": ["Full speed · attempt 1", "Attempt 2… same mistake 🔁", "Slow: 60% → 80%", "100% · NAILED IT"], "wait": "wait for ✅",
      "rows": ["❌ Full speed = same mistake", "✅ Slow → fast = nailed it"], "rowsize": 62,
      "endq": "Which one do<br><span class='hl'>you</span> do? 😅👇", "end2": "The plan sets your tempo every session 👇"},
     kicks={3: [0, 4, 8, 12, 16, 20, 24]}, sfx=[("buzz", 0, 18, 0.04), ("buzz", 0, 20, 0.06), ("buzz", 1, 18, 0.04), ("buzz", 1, 20, 0.06), ("scratch", 1, 20.5, 0.05)])
