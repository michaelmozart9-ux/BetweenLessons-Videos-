# Moonlight Sonata 1st mvt (Beethoven, public domain) but it gets EPIC. C# minor, unit = triplet 8th (12 per bar).
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
BARS = [("C#2", [["G#3", "C#4", "E4"]] * 4), ("A2", [["A3", "C#4", "E4"]] * 2 + [["A3", "D4", "F#4"]] * 2)]
def trip(sh=0, v=0.5, stac=1.0, dbl=False):
    out = []
    for bi, (bass, groups) in enumerate(BARS):
        for gi, g in enumerate(groups):
            for k, n in enumerate(g):
                b = bi * 12 + gi * 3 + k; out.append((P(n) + sh, b, 1.1 * stac, "A", v + (0.06 if k == 0 else 0)))
                if dbl: out.append((P(n) + sh + 12, b, 1.1 * stac, "R", v - 0.12))
    return out
def bass(oct2=False, v=0.55):
    out = []
    for bi, (b, _) in enumerate(BARS):
        out.append((P(b), bi * 12, 12, "L", v))
        if oct2: out.append((P(b) + 12, bi * 12, 12, "L", v - 0.1))
    return out
MEL = [("G#4", 0, 4.5), ("G#4", 4.5, 1.5), ("G#4", 6, 6), ("A4", 12, 6), ("F#4", 18, 6)]
def mel(sh=0, v=0.8): return [(P(n) + sh, b, d, "R", v) for n, b, d in MEL]
A = trip() + bass(True)                                        # 🌙 original
B = trip(12, 0.42, 0.5)                                        # 🎶 music box
B = [(m if m <= 84 else m - 12, b, d, "R", v) for m, b, d, h, v in B]
C = trip(0, 0.5, 0.8) + mel(0, 0.76)                           # 🔊 trap
for bi, (bs, _) in enumerate(BARS): C += N((bs, bi * 12, 2), (bs, bi * 12 + 6, 1.5), (bs, bi * 12 + 9, 1.5), h="L", v=0.68) + [(P(bs) + 12, bi * 12 + 6, 1.5, "L", 0.5)]
D = trip(0, 0.55, 1.0, True) + mel(0, 0.86) + mel(12, 0.66) + bass(True, 0.66)   # 🔥 epic
F = 24
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["C#2", "G#2", "C#3", "E3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.84 + 0.02 * j) for j, n in enumerate(["G#3", "C#4", "E4", "G#4", "C#5", "E5"])]
make(HERE, [(A, 24, 330, 12), (B, 24, 360, 12), (C, 24, 400, None), (D, 24, 440, 12)], F,
     {"piece": "Moonlight Sonata 🌙", "q": "but it gets <span class='hl'>EPIC</span> 😳", "labels": ["🌙", "🎶", "🔊", "🔥"],
      "chips": ["Original", "Music box", "Trap", "EPIC"], "wait": "wait for 🔥",
      "rows": ["🌙 Original", "🎶 Music box", "🔊 Trap", "🔥 Epic"], "rowsize": 84,
      "endq": "Which was <span class='hl'>best?</span> 👇", "end2": "Learn the real one · Day 1 free 👇"},
     kicks={2: list(range(0, 24, 3)), 3: list(range(0, 24, 1))})
