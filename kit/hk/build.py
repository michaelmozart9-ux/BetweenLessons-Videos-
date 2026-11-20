# In the Hall of the Mountain King (Grieg, public domain) but it gets EPIC: sneaky -> faster -> FASTER -> EPIC. B minor, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
MEL = [("B3", 0, 1), ("C#4", 1, 1), ("D4", 2, 1), ("E4", 3, 1), ("F#4", 4, 1), ("D4", 5, 1), ("F#4", 6, 2),
       ("F4", 8, 1), ("C#4", 9, 1), ("F4", 10, 2), ("E4", 12, 1), ("C4", 13, 1), ("E4", 14, 2),
       ("B3", 16, 1), ("C#4", 17, 1), ("D4", 18, 1), ("E4", 19, 1), ("F#4", 20, 1), ("D4", 21, 1), ("F#4", 22, 1), ("B4", 23, 1),
       ("A4", 24, 1), ("F#4", 25, 1), ("D4", 26, 1), ("F#4", 27, 1), ("A4", 28, 4)]
def mel(hi, sh=0, v=0.6, stac=0.5): return [(P(n) + sh, b, d * stac, "R", v) for n, b, d in MEL if b < hi]
def bass(hi, step=2, oct2=False, v=0.45):
    out = []
    for b in range(0, hi, step):
        n = "F#2" if (b // 2) % 2 else "B2"
        out.append((P(n), b, 0.5, "L", v));
        if oct2: out.append((P(n) + 12, b, 0.5, "L", v - 0.08))
    return out
A = mel(16, 0, 0.45, 0.45) + bass(16, 2, v=0.36)                       # 🤫 sneaky
B = mel(16, 0, 0.62, 0.55) + bass(16, 2, v=0.46)                       # 🏃 faster
C = mel(16, 12, 0.72, 0.6) + mel(16, 0, 0.6, 0.6) + bass(16, 1, v=0.55) # 😳 FASTER: octaves, driving bass
D = mel(32, 0, 0.84, 0.7) + mel(32, 12, 0.66, 0.7) + bass(32, 1, oct2=True, v=0.6)  # 🔥 EPIC
F = 32
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["B2", "F#3", "B3", "D4"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["F#4", "B4", "D5", "F#5", "B5"])]
make(HERE, [(A, 16, 300, None), (B, 16, 380, None), (C, 16, 460, None), (D, 32, 540, None)], F,
     {"piece": "Mountain King 👹", "q": "but it gets <span class='hl'>EPIC</span> 😳", "labels": ["🤫", "🏃", "😳", "🔥"],
      "chips": ["Sneaky", "Faster", "FASTER", "EPIC"], "wait": "wait for 🔥",
      "rows": ["🤫 Sneaky", "🏃 Faster", "😳 FASTER", "🔥 Epic"], "rowsize": 84,
      "endq": "Which was <span class='hl'>best?</span> 👇", "end2": "Learn the real one · Day 1 free 👇"},
     kicks={2: list(range(0, 16, 2)), 3: list(range(0, 32, 2))})
