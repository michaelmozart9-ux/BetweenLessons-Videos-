# Cartoon: "1 hour vs 15 minutes. Who practised more?" Story skit (numbers are part of the story). Für Elise (public domain). Captions only.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"hook": 0.0, "max": 2.2, "zoe": 6.2, "reveal": 9.6, "plan": 11.8, "end": 13.4}
DUR = 15.4
MEL = [("E5", 0), ("D#5", 1), ("E5", 2), ("D#5", 3), ("E5", 4), ("B4", 5), ("D5", 6), ("C5", 7), ("A4", 8), ("C4", 11), ("E4", 12), ("A4", 13),
       ("B4", 14), ("E4", 17), ("G#4", 18), ("B4", 19), ("C5", 20)]
LH = [("A2", 8), ("E3", 9), ("A3", 10), ("E2", 14), ("E3", 15), ("G#3", 16), ("A2", 20), ("E3", 21), ("A3", 22)]
notes = []; keys = []; phone_t = []
def play(who, t0, bpm, lo, hi):
    q = 60 / bpm
    for n, b in MEL + LH:
        if not (lo <= b < hi): continue
        m = P(n); t = t0 + (b - lo) * q
        notes.append({"m": m, "t": t, "rel": t + q * 1.4, "v": 0.6, "sec": "s"}); keys.append({"t": round(t, 3), "who": who, "m": m})
    return t0 + (hi - lo) * q
# hook: both play a little
play("max", 0.1, 420, 0, 8); play("zoe", 1.0, 420, 0, 8)
# Max: play a bit, phone, play a bit, phone...
t = B["max"] + 0.2
for lo, hi in [(0, 5), (5, 8), (8, 12)]:
    t = play("max", t, 420, lo, hi); phone_t.append(round(t + 0.05, 3)); t += 0.95
# Zoe: steady, full phrase, small chord
zt = play("zoe", B["zoe"] + 0.2, 400, 0, 21)
for j, n in enumerate(["A2", "E3", "A3", "C4", "E4", "A4"]): notes.append({"m": P(n), "t": zt + j * 0.05, "rel": zt + 1.6, "v": 0.66, "sec": "s"})
for j, n in enumerate(["C3", "G3", "C4", "E4", "G4", "C5"]): notes.append({"m": P(n), "t": B["plan"] + 0.1 + j * 0.08, "rel": DUR, "v": 0.38, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
for i, pt in enumerate(phone_t): add(mix, ding([1760, 1975.5, 2349.3][i], 0.4), pt, 0.035); add(mix, pop(1400), pt + 0.25, 0.025)
for k in ["max", "zoe", "plan"]: add(mix, whoosh(0.4), B[k] - 0.25, 0.012)
add(mix, riser(0.7), B["reveal"] - 0.7, 0.025); add(mix, boom(1.0), B["reveal"] + 0.05, 0.07); add(mix, ding(1568, 1.0), B["reveal"] + 0.6, 0.03)
add(mix, ding(2093, 1.0), B["end"] + 0.1, 0.03); add(mix, pop(1000), B["end"], 0.03)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.25)
CAPS = [(0.03, "1 hour vs 15 minutes. Who practised more? 🤔"), (B["max"], "Max: 1 hour… with his phone next to him 📱"),
        (B["zoe"], "Zoe: 15 minutes. Phone in another room. 🎯"), (B["reveal"], "Zoe practised MORE. 🤯"),
        (B["plan"], "Short, focused sessions: warm-up, main work, run-through."), (B["end"], "Be honest… which one are you? 👇")]
json.dump({"duration": DUR, "fps": 30, "beats": B, "caps": [{"t": round(t, 3), "text": s} for t, s in CAPS], "keys": keys, "phone": phone_t, "zc": round(zt, 3), "fc": -9, "wrong": []}, open(f"{HERE}/timing.json", "w"))
print("dur", DUR, "phone", phone_t, "zoe end", round(zt, 2))
