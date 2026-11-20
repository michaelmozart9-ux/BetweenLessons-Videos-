# Carol of the Bells (Leontovych, public domain) but it gets EPIC: Music box -> Original -> Trap -> EPIC. G minor, unit = 8th.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from lv import *
def ost(b0, sh=0, v=0.72, stac=1.0, h="R"):
    return [(P("Bb4") + sh, b0, 2 * stac, h, v + 0.05), (P("A4") + sh, b0 + 2, 1 * stac, h, v), (P("Bb4") + sh, b0 + 3, 1 * stac, h, v), (P("G4") + sh, b0 + 4, 2 * stac, h, v)]
BASS = ["G", "F", "Eb", "D"]
A = []
for i in range(4): A += ost(i * 6, 12, 0.55, 0.5)                                                    # 🎶 music box: high, staccato, no bass
A += [(P(n), i * 6 + 3, 0.5, "R", 0.32) for i, n in enumerate(["G5", "F5", "Eb5", "D5"])]
B = []
for i in range(4): B += ost(i * 6) + N((BASS[i] + "3", i * 6, 6), h="L", v=0.5)                   # 🔔 original
C = []
for i in range(4):                                                                                   # 🔊 trap: 808-ish octave bass hits
    C += ost(i * 6, 0, 0.76, 0.8) + N((BASS[i] + "2", i * 6, 1.4), (BASS[i] + "2", i * 6 + 3, 1), (BASS[i] + "3", i * 6 + 4.5, 1), h="L", v=0.66)
D = []
for i in range(4):                                                                                   # 🔥 epic: octaves + falling bells + big bass
    D += ost(i * 6, 0, 0.84) + ost(i * 6, 12, 0.62) + N((BASS[i] + "2", i * 6, 6), h="L", v=0.68) + [(P(BASS[i] + "3"), i * 6, 6, "L", 0.55)]
    if i >= 2: D += [(m, i * 6 + k * 0.5, 0.5, "R", 0.5) for k, m in enumerate(sorted([P(f"{x}{o}") for x in (["Eb", "G", "Bb"] if i == 2 else ["D", "F#", "A"]) for o in (5, 6) if P(f"{x}{o}") <= 84], reverse=True) * 2) if k < 12]
F = 24
D += [(P(n), F + j * 0.06, 30, "L", 0.9) for j, n in enumerate(["G2", "D3", "G3", "Bb3"])]
D += [(P(n), F + 0.25 + j * 0.06, 30, "R", 0.82 + 0.02 * j) for j, n in enumerate(["G4", "Bb4", "D5", "G5", "Bb5"])]
make(HERE, [(A, 24, 420, None), (B, 24, 440, 6), (C, 24, 460, None), (D, 24, 480, 6)], F,
     {"piece": "Carol of the Bells 🔔", "q": "but it gets <span class='hl'>EPIC</span> 😳", "labels": ["🎶", "🔔", "🔊", "🔥"],
      "chips": ["Music box", "Original", "Trap", "EPIC"], "wait": "wait for 🔥",
      "rows": ["🎶 Music box", "🔔 Original", "🔊 Trap", "🔥 Epic"], "rowsize": 84,
      "endq": "Which was <span class='hl'>best?</span> 👇", "end2": "Learn the real one · Day 1 free 👇"},
     kicks={2: list(range(0, 24, 3)), 3: list(range(0, 24, 1))})
