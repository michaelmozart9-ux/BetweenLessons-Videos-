# Paid ad B (parents): "Your kid has lessons... but what do they practise at home?" Für Elise (public domain). Captions only.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"hook": 0.0, "idle": 2.6, "plan": 5.2, "focus": 9.6, "gift": 13.2}
DUR = 16.6
MEL = [("E5", 0), ("D#5", 1), ("E5", 2), ("D#5", 3), ("E5", 4), ("B4", 5), ("D5", 6), ("C5", 7), ("A4", 8), ("C4", 11), ("E4", 12), ("A4", 13),
       ("B4", 14), ("E4", 17), ("G#4", 18), ("B4", 19), ("C5", 20)]
LH = [("A2", 8), ("E3", 9), ("A3", 10), ("E2", 14), ("E3", 15), ("G#3", 16), ("A2", 20), ("E3", 21), ("A3", 22)]
notes = []; keys = []
def note(m, t, d, v=0.5): notes.append({"m": m, "t": t, "rel": t + d, "v": v, "sec": "s"}); keys.append({"t": round(t, 3), "who": "max", "m": m})
# hook: aimless noodling (random-ish notes, own material)
rng = np.random.default_rng(4)
for i, m in enumerate([60, 62, 64, 62, 60, 67, 65, 64, 60, 59, 60, 64]): note(m, 0.15 + i * 0.2 + rng.uniform(0, 0.05), 0.3, 0.42)
# idle: easy opening again, twice, then stops (phone)
for rep in range(2):
    for n, b in MEL[:8]: note(P(n), B["idle"] + 0.1 + rep * 1.05 + b * 0.12, 0.2, 0.5)
phone_t = B["idle"] + 2.3
# focus: clean full phrase + chord
q = 60 / 400
for n, b in MEL + LH: note(P(n), B["focus"] + 0.15 + b * q, q * (2.5 if b in (8, 14, 20) else 1.2), 0.6)
zc = B["focus"] + 0.15 + 20 * q
for j, n in enumerate(["A2", "E3", "A3", "C4", "E4", "A4"]): notes.append({"m": P(n), "t": zc + j * 0.05, "rel": zc + 1.6, "v": 0.66, "sec": "s"})
for j, n in enumerate(["C3", "G3", "C4", "E4", "G4", "C5"]): notes.append({"m": P(n), "t": B["plan"] + 0.1 + j * 0.08, "rel": B["plan"] + 3.8, "v": 0.38, "sec": "s"})
for j, n in enumerate(["F3", "C4", "F4", "A4", "C5", "F5"]): notes.append({"m": P(n), "t": B["gift"] + 0.3 + j * 0.07, "rel": DUR, "v": 0.5, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
add(mix, ding(1760, 0.4), phone_t, 0.03); add(mix, pop(1400), phone_t + 0.2, 0.02)
for k in ["idle", "plan", "focus", "gift"]: add(mix, whoosh(0.4), B[k] - 0.22, 0.012)
for i in range(3): add(mix, pop(900 + 120 * i), 0.4 + i * 0.6, 0.02)
for j in range(5): add(mix, pop(900 + 80 * j), B["plan"] + 0.8 + j * 0.2, 0.022)
add(mix, ding(1568, 0.9), zc + 0.05, 0.03); add(mix, ding(2093, 0.9), zc + 0.6, 0.028)
add(mix, boom(0.8), B["gift"] + 0.45, 0.05); add(mix, sparkle(), B["gift"] + 0.5, 0.03); add(mix, ding(2093, 1.0), B["gift"] + 1.4, 0.03)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.3)
CAPS = [(0.03, "Your kid has lessons… but what do they practise at home? 🤔"), (B["idle"], "Practice time ≠ progress"),
        (B["plan"], "A daily practice plan for the piece they're learning"), (B["focus"], "Between lessons, they know exactly what to do ✅"),
        (B["gift"], "€17 once · 7-day money-back · Day 1 free 👇")]
json.dump({"duration": DUR, "fps": 30, "beats": B, "caps": [{"t": round(t, 3), "text": s} for t, s in CAPS], "keys": keys, "phone": [round(phone_t, 3)], "zc": round(zc, 3), "fc": -9, "wrong": []}, open(f"{HERE}/timing.json", "w"))
print("dur", DUR, "zc", round(zc, 2))
