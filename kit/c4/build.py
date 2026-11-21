# Cartoon: "Missed a practice day. Max vs Zoe." Max crams two days at double speed and crashes; Zoe's plan just waits (real product fact: a missed day just waits).
# Music: Ode to Joy (Beethoven, public domain). Captions only.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"hook": 0.0, "max": 2.6, "zoe": 6.7, "reveal": 10.8, "plan": 13.3, "end": 15.1}
DUR = 17.2
MEL = [("E5", 0), ("E5", 1), ("F5", 2), ("G5", 3), ("G5", 4), ("F5", 5), ("E5", 6), ("D5", 7),
       ("C5", 8), ("C5", 9), ("D5", 10), ("E5", 11), ("E5", 12), ("D5", 13.5), ("D5", 14)]
LH = [("C3", 0), ("G2", 4), ("C3", 8), ("G2", 12)]
WRONG = 7  # D5 -> C#5 when cramming
notes = []; keys = []; wrong = []
def play(who, t0, bpm, lo, hi, crash=False, v=0.62):
    q = 60 / bpm; end = t0 + (hi - lo) * q
    for n, b in MEL + LH:
        if not (lo <= b < hi): continue
        if crash and b > WRONG: continue
        m = P(n); t = t0 + (b - lo) * q; bad = crash and b == WRONG and (n, b) in MEL
        if bad: m -= 1
        dur = q * 3.5 if (n, b) in LH else q * (1.9 if b == 14 else 0.95)
        notes.append({"m": m, "t": t, "rel": t + dur, "v": v + (0.15 if bad else 0), "sec": "s"}); keys.append({"t": round(t, 3), "who": who, "m": m, "x": bad})
        if bad:
            for k in (-1, 1): notes.append({"m": m + k, "t": t + 0.02, "rel": t + 0.5, "v": 0.7, "sec": "s"})
            wrong.append({"t": round(t, 3), "who": who}); end = t + 0.35
    return end
# hook: Max crams and crashes, Zoe plays calmly
play("max", 0.08, 300, 0, 16, crash=True); play("zoe", 0.3, 190, 0, 8, v=0.5)
# Max: "two days in one", full speed, crash twice
t = B["max"] + 0.15
for lo in (0, 3): t = play("max", t, 300, lo, 16, crash=True) + 0.45
# Zoe: opens the app, Day 2 waited for her, plays it clean at her normal tempo
TAP = round(B["zoe"] + 0.35, 3)
zs = TAP + 0.8; ze = play("zoe", zs, 190, 0, 8)
ticks = [round(ze + 0.1, 3)]
# reveal: Max crashes again, Zoe finishes the phrase, then a chord
play("max", B["reveal"] + 0.1, 300, 0, 16, crash=True)
zend = play("zoe", B["reveal"] + 0.1, 220, 8, 16) - 0.3
ticks.append(round(zend + 0.1, 3))
for j, n in enumerate(["C3", "G3", "C4", "E4", "G4", "C5"]): notes.append({"m": P(n), "t": zend + j * 0.05, "rel": zend + 1.6, "v": 0.6, "sec": "s"})
for j, n in enumerate(["C3", "G3", "C4", "E4", "G4", "C5"]): notes.append({"m": P(n), "t": B["plan"] + 0.1 + j * 0.08, "rel": DUR, "v": 0.34, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
for w in wrong: add(mix, buzz(), w["t"] + 0.02, 0.045)
add(mix, tap(), TAP, 0.05); add(mix, pop(1300), TAP + 0.05, 0.03)
for i, c in enumerate(ticks): add(mix, ding([1568.0, 2093.0][i], 0.7), c, 0.03)
for k in ["max", "zoe", "plan"]: add(mix, whoosh(0.4), B[k] - 0.25, 0.012)
add(mix, riser(0.7), B["reveal"] - 0.7, 0.025)
add(mix, ding(2093, 1.0), B["end"] + 0.1, 0.03); add(mix, pop(1000), B["end"], 0.03)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.25)
CAPS = [(0.03, "You missed ONE practice day 😱 Now what?"), (B["max"], "Max: “I’ll do two days in one!” 🏎️"),
        (wrong[2]["t"] + 0.3, "Double speed… same mistake ❌"),
        (B["zoe"], "Zoe opens her plan 👆"), (TAP + 0.6, "Missed day? It just waits ⏸️"), (zs + 0.4, "Same session, same tempo ✅"),
        (B["reveal"], "Cramming ❌ vs calm ✅"),
        (B["plan"], "Miss a day? Your plan just waits."), (B["end"], "Be honest… Max or Zoe? 👇")]
json.dump({"duration": DUR, "fps": 30, "beats": B, "caps": [{"t": round(t, 3), "text": s} for t, s in CAPS], "keys": keys, "wrong": wrong,
           "tap": TAP, "ticks": ticks, "clean": [zs], "phone": []}, open(f"{HERE}/timing.json", "w"), ensure_ascii=False)
print("dur", DUR, "wrong", wrong, "tap", TAP, "ticks", ticks, "zend", round(zend, 2))
