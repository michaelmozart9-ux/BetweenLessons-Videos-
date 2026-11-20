# Product ad: "How Between Lessons works". Soft piano bed (own chord progression) + UI sound effects. Writes audio.wav + timing.json.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"hook": 0.0, "s1": 2.4, "s2": 5.6, "s3": 8.6, "card": 10.8, "s4": 13.4, "s5": 16.6, "s6": 19.6}
DUR = 23.5
taps = {"piece": 3.9, "grade": 4.8, "days": [6.1, 6.35, 6.6, 6.85, 7.1], "len": 7.8, "easy": 14.6}
# bed: C - G - Am - F, broken chords, 2.0s per chord, builds a bit after s3
notes = []; prog = [["C3", "G3", "C4", "E4"], ["G2", "D3", "G3", "B3"], ["A2", "E3", "A3", "C4"], ["F2", "C3", "F3", "A3"]]
t = 0.0; i = 0
while t < DUR - 1.5:
    ch = prog[i % 4]
    for k, n in enumerate(ch): notes.append({"m": P(n), "t": t + k * 0.12, "rel": t + 2.0, "v": 0.42, "sec": "s"})
    top = [P(ch[3]) + 12, P(ch[2]) + 12, P(ch[3]) + 12 + (2 if i % 2 else 0)]
    for k, m in enumerate(top): notes.append({"m": m, "t": t + 0.6 + k * 0.45, "rel": t + 0.6 + k * 0.45 + 0.6, "v": 0.3 + (0.08 if t > B["s3"] else 0), "sec": "s"})
    t += 2.0; i += 1
for j, n in enumerate(["C3", "G3", "C4", "E4", "G4", "C5"]): notes.append({"m": P(n), "t": B["s6"] + 0.1 + j * 0.07, "rel": DUR, "v": 0.55, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.24) * 0.8
for k in ["s1", "s2", "s3", "s4", "s5", "s6"]: add(mix, whoosh(0.4), B[k] - 0.22, 0.012)
for tt in [taps["piece"], taps["grade"], taps["len"], taps["easy"]]: add(mix, click(), tt, 0.04); add(mix, pop(1200), tt + 0.02, 0.025)
for j, tt in enumerate(taps["days"]): add(mix, pop(900 + 80 * j), tt, 0.026)
for j in range(6): add(mix, pop(700 + 60 * j), B["s3"] + 0.3 + j * 0.2, 0.02)
add(mix, ding(1568, 0.8), B["card"] + 0.1, 0.025); add(mix, ding(1975.5, 0.8), taps["easy"] + 0.4, 0.03)
add(mix, ding(2093, 1.0), B["s5"] + 1.6, 0.03); add(mix, sparkle(), B["s5"] + 1.7, 0.025)
for j in range(3): add(mix, pop(1000 + 150 * j), B["s6"] + 0.5 + j * 0.35, 0.03)
add(mix, buzz(), 0.35, 0.025); add(mix, buzz(), 0.75, 0.025); add(mix, buzz(), 1.15, 0.025)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.4)
json.dump({"duration": DUR, "fps": 30, "beats": B, "taps": taps}, open(f"{HERE}/timing.json", "w"))
print("dur", DUR)
