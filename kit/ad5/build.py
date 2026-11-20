# Ad: "Can a plan fix the WORST practiser?" Max's story. Für Elise (public domain). Captions only.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"fail": 0.0, "plan": 2.8, "d1": 5.8, "d4": 8.0, "d7": 10.0, "nail": 11.3, "imagine": 15.4, "end": 17.2}
DUR = 19.4
MEL = [("E5", 0), ("D#5", 1), ("E5", 2), ("D#5", 3), ("E5", 4), ("B4", 5), ("D5", 6), ("C5", 7), ("A4", 8), ("C4", 11), ("E4", 12), ("A4", 13),
       ("B4", 14), ("E4", 17), ("G#4", 18), ("B4", 19), ("C5", 20)]
LH = [("A2", 8), ("E3", 9), ("A3", 10), ("E2", 14), ("E3", 15), ("G#3", 16), ("A2", 20), ("E3", 21), ("A3", 22)]
notes = []; keys = []; wrong = []; buzzes = []
def play(who, t0, bpm, upto, wrongs=(), stop=None):
    q = 60 / bpm
    for n, b in MEL + LH:
        if b >= upto or (stop is not None and b >= stop): continue
        m = P(n); t = t0 + b * q
        if b in wrongs: m += 1; wrong.append(round(t, 3)); buzzes.append(t)
        notes.append({"m": m, "t": t, "rel": t + q * (2.5 if b in (8, 14, 20) else 1.2), "v": 0.62 if b < 8 else 0.55, "sec": "s"}); keys.append({"t": round(t, 3), "who": who, "m": m})
    return t0 + (stop or upto) * q
fc = play("room", 0.05, 560, 12, wrongs=(4, 7), stop=10)
for j, n in enumerate(["C3", "C#3", "D3", "F#3", "G3", "G#3"]): notes.append({"m": P(n), "t": fc + j * 0.01, "rel": fc + 0.9, "v": 0.85, "sec": "s"})
play("room", B["d1"] + 0.15, 230, 9, wrongs=(6,)); play("room", B["d4"] + 0.15, 330, 13, wrongs=(11,))
zc = play("stage", B["nail"] + 0.1, 420, 21)
zc = B["nail"] + 0.1 + 20 * 60 / 420
for j, n in enumerate(["A2", "E3", "A3", "C4", "E4", "A4", "C5", "E5"]): notes.append({"m": P(n), "t": zc + j * 0.05, "rel": zc + 2.6, "v": 0.74, "sec": "s"})
for j, n in enumerate(["C3", "G3", "C4", "E4", "G4", "C5"]): notes.append({"m": P(n), "t": B["plan"] + 0.1 + j * 0.08, "rel": B["plan"] + 2.9, "v": 0.38, "sec": "s"})
for j, n in enumerate(["F3", "C4", "F4", "A4", "C5", "F5"]): notes.append({"m": P(n), "t": B["imagine"] + 0.1 + j * 0.07, "rel": DUR, "v": 0.5, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
for t in buzzes: add(mix, buzz(), t, 0.04)
add(mix, buzz(), fc, 0.06); add(mix, boom(0.8), fc, 0.07); add(mix, scratch(), fc + 0.2, 0.06); wrong.append(round(fc, 3))
def applause(d, seed=3, dens=150):
    r = np.random.default_rng(seed); n = int(d * SR); out = np.zeros(n, np.float32)
    for _ in range(int(d * dens)):
        s = int(r.uniform(0, n - 2000)); L = int(r.uniform(400, 1200)); c = r.normal(0, 1, L).astype(np.float32) * np.exp(-np.linspace(0, 6, L)).astype(np.float32); out[s:s + L] += c * r.uniform(0.3, 1.0)
    out = np.convolve(out, np.ones(3) / 3, "same").astype(np.float32); x = np.linspace(0, d, n); env = np.minimum(1, x / 0.3) * np.minimum(1, (d - x) / 1.0)
    return (out * env).astype(np.float32)
add(mix, applause(4.2), zc + 0.1, 0.1)
for k in ["plan", "d1", "d4", "d7", "imagine"]: add(mix, whoosh(0.4), B[k] - 0.22, 0.012)
add(mix, riser(1.0), B["nail"] - 1.0, 0.022)
add(mix, ding(1568, 1.0), zc + 0.05, 0.03); add(mix, sparkle(), zc + 0.2, 0.03); add(mix, ding(2093, 1.0), B["end"] + 0.1, 0.03); add(mix, pop(1000), B["end"], 0.03)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.3)
CAPS = [(0.03, "Max has failed this piece 5 times 😭"), (B["plan"], "So he tried a plan: 20 min a day, slow first, a tempo target every session"),
        (B["d1"], "Day 1: slow 🐢"), (B["d4"], "Day 4: faster"), (B["d7"], "Day 7. The recital. 😬"), (zc, "NAILED IT 🔥"),
        (B["imagine"], "Now imagine that's YOU 🎤"), (B["end"], "Get a plan for your piece. Day 1 free 👇")]
json.dump({"duration": DUR, "fps": 30, "beats": B, "caps": [{"t": round(t, 3), "text": s} for t, s in CAPS], "keys": keys, "wrong": sorted(wrong), "zc": round(zc, 3), "fc": round(fc, 3)}, open(f"{HERE}/timing.json", "w"))
print("dur", DUR, "fc", round(fc, 2), "zc", round(zc, 2))
