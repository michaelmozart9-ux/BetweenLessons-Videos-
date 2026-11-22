# Cartoon series ep 4: "3 types of piano students PART 4". Pedal holder, no-warm-up, smart one. Jingle Bells (Pierpont 1857, public domain).
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"hook": 0.0, "k1": 1.7, "k2": 5.2, "k3": 8.6, "plan": 13.2, "end": 14.9}
DUR = 16.9
# chorus, unit = 8th: E E E- | E E E- | E G C. D | E---
MEL = [("E5", 0, 1), ("E5", 1, 1), ("E5", 2, 2), ("E5", 4, 1), ("E5", 5, 1), ("E5", 6, 2), ("E5", 8, 1), ("G5", 9, 1), ("C5", 10, 1.5), ("D5", 11.5, 0.5), ("E5", 12, 4)]
LH = [("C3", 0, 2), ("G3", 2, 2), ("C3", 4, 2), ("G3", 6, 2), ("C3", 8, 2), ("G2", 10, 2), ("C3", 12, 4)]
notes = []; keys = []; wrong = []
def add_note(who, m, t, d, v=0.6): notes.append({"m": m, "t": t, "rel": t + d, "v": v, "sec": "s"}); keys.append({"t": round(t, 3), "who": who, "m": m})
# 1: pedal holder: plays the chorus but every note rings until the end of his turn -> mush
q1 = 60 / 400; t1 = B["k1"] + 0.2
for n, b, d in MEL + LH: add_note("k1", P(n), t1 + b * q1, B["k2"] - 0.1 - (t1 + b * q1), 0.62)
for n, b in [("F5", 13), ("A4", 14), ("B4", 15)]: add_note("k1", P(n), t1 + b * q1, B["k2"] - 0.1 - (t1 + b * q1), 0.5)  # extra clutter under the pedal
pedal_t = [round(B["k1"] + 0.4 + i * 1.0, 3) for i in range(3)]
# 2: no warm-up: straight in at full speed, cold hands -> crash on bar 3
q2 = 60 / 640; t2 = B["k2"] + 0.9
for n, b, d in MEL[:8]: add_note("k2", P(n), t2 + b * q2, d * q2 * 0.9, 0.7)
fc = t2 + 9 * q2 + 0.05
for j, n in enumerate(["C4", "C#4", "D4", "F#4", "G4", "G#4"]): notes.append({"m": P(n), "t": fc + j * 0.01, "rel": fc + 0.9, "v": 0.85, "sec": "s"})
wrong.append(round(fc, 3))
# 3: smart one: warm-up scale, then the chorus at a steady tempo, both hands -> big chord
t3 = B["k3"] + 0.25
for i, n in enumerate(["C4", "D4", "E4", "F4", "G4"]): add_note("k3", P(n), t3 + i * 0.13, 0.13, 0.45)
q3 = 60 / 330; t3b = t3 + 0.95
for n, b, d in MEL: add_note("k3", P(n), t3b + b * q3, d * q3 * 0.92, 0.68)
for n, b, d in LH[:-1]: add_note("k3", P(n), t3b + b * q3, d * q3 * 0.9, 0.45)
zc = t3b + 12 * q3
for j, n in enumerate(["C2", "G2", "C3", "E3", "G3", "C4", "E4", "G4", "C5", "E5"]): notes.append({"m": P(n), "t": zc + j * 0.05, "rel": zc + 2.4, "v": 0.74, "sec": "s"})
for j, n in enumerate(["C3", "G3", "C4", "E4", "G4", "C5"]): notes.append({"m": P(n), "t": B["plan"] + 0.1 + j * 0.08, "rel": DUR, "v": 0.36, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
for e in pedal_t: add(mix, pop(500), e, 0.03)
add(mix, buzz(), fc, 0.06); add(mix, boom(0.8), fc, 0.07); add(mix, scratch(), fc + 0.2, 0.06)
def applause(d, seed=3, dens=150):
    r = np.random.default_rng(seed); n = int(d * SR); out = np.zeros(n, np.float32)
    for _ in range(int(d * dens)):
        s = int(r.uniform(0, n - 2000)); L = int(r.uniform(400, 1200)); c = r.normal(0, 1, L).astype(np.float32) * np.exp(-np.linspace(0, 6, L)).astype(np.float32); out[s:s + L] += c * r.uniform(0.3, 1.0)
    out = np.convolve(out, np.ones(3) / 3, "same").astype(np.float32); x = np.linspace(0, d, n); env = np.minimum(1, x / 0.3) * np.minimum(1, (d - x) / 0.8)
    return (out * env).astype(np.float32)
add(mix, applause(2.8), zc + 0.1, 0.09)
for k in ["k1", "k2", "k3", "plan"]: add(mix, whoosh(0.4), B[k] - 0.25, 0.012)
for i in range(3): add(mix, pop(800 + 200 * i), 0.25 + i * 0.3, 0.03)
add(mix, ding(1568, 1.0), zc + 0.05, 0.03); add(mix, sparkle(), zc + 0.2, 0.03); add(mix, ding(2093, 1.0), B["end"] + 0.1, 0.03); add(mix, pop(1000), B["end"], 0.03)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.25)
CAPS = [(0.05, "PART 4. Which one are you? 👀"), (B["k1"], "#1 holds the pedal down. The WHOLE time."), (B["k2"], "#2 skips the warm-up. Full speed, cold hands…"), (fc + 0.3, "…💥"),
        (B["k3"], "#3: warm-up, main work, run-through"), (zc, "NAILED IT 🔥"),
        (B["plan"], "Want to be #3? Every session planned for you."), (B["end"], "1, 2 or 3? 👇 Follow for part 5 👀")]
json.dump({"duration": DUR, "fps": 30, "beats": B, "caps": [{"t": round(t, 3), "text": s} for t, s in CAPS], "keys": keys, "wrong": wrong, "zc": round(zc, 3), "fc": round(fc, 3), "phone": pedal_t, "clicks": []}, open(f"{HERE}/timing.json", "w"))
print("dur", DUR, "fc", round(fc, 2), "zc", round(zc, 2))
