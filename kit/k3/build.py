# Cartoon: "3 types of piano students. Which one are you?" Für Elise (public domain). Captions only.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"hook": 0.0, "k1": 1.7, "k2": 5.3, "k3": 8.4, "plan": 12.7, "end": 14.4}
DUR = 16.4
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
def crash_at(t):
    for j, n in enumerate(["C3", "C#3", "D3", "F#3", "G3", "G#3"]): notes.append({"m": P(n), "t": t + j * 0.01, "rel": t + 0.9, "v": 0.85, "sec": "s"})
# #1 restarter: nice start, restarts, then crashes at the hard bit
play("k1", B["k1"] + 0.1, 400, 8); r1 = B["k1"] + 0.1 + 8 * 60 / 400 + 0.15
play("k1", r1, 400, 11, stop=11); fc1 = r1 + 11 * 60 / 400; crash_at(fc1)
# #2 speedrunner
play("k2", B["k2"] + 0.1, 560, 21, wrongs=(3, 7, 13, 18)); fc2 = B["k2"] + 0.1 + 21 * 60 / 560
# #3 smart: clean, chord
play("k3", B["k3"] + 0.15, 380, 21); zc = B["k3"] + 0.15 + 20 * 60 / 380
for j, n in enumerate(["A2", "E3", "A3", "C4", "E4", "A4", "C5", "E5"]): notes.append({"m": P(n), "t": zc + j * 0.05, "rel": zc + 2.4, "v": 0.72, "sec": "s"})
for j, n in enumerate(["C3", "G3", "C4", "E4", "G4", "C5"]): notes.append({"m": P(n), "t": B["plan"] + 0.1 + j * 0.08, "rel": DUR, "v": 0.38, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
for t in buzzes: add(mix, buzz(), t, 0.035)
add(mix, buzz(), fc1, 0.06); add(mix, boom(0.8), fc1, 0.07); add(mix, scratch(), fc1 + 0.2, 0.06); wrong.append(round(fc1, 3))
def applause(d, seed=3, dens=90):
    r = np.random.default_rng(seed); n = int(d * SR); out = np.zeros(n, np.float32)
    for _ in range(int(d * dens)):
        s = int(r.uniform(0, n - 2000)); L = int(r.uniform(400, 1200)); c = r.normal(0, 1, L).astype(np.float32) * np.exp(-np.linspace(0, 6, L)).astype(np.float32); out[s:s + L] += c * r.uniform(0.3, 1.0)
    out = np.convolve(out, np.ones(3) / 3, "same").astype(np.float32); x = np.linspace(0, d, n); env = np.minimum(1, x / 0.3) * np.minimum(1, (d - x) / 0.8)
    return (out * env).astype(np.float32)
add(mix, applause(2.8, 2, 150), zc + 0.1, 0.09)
for k in ["k1", "k2", "k3", "plan"]: add(mix, whoosh(0.4), B[k] - 0.25, 0.012)
for i in range(3): add(mix, pop(800 + 200 * i), 0.25 + i * 0.3, 0.03)
add(mix, ding(1568, 1.0), zc + 0.05, 0.03); add(mix, sparkle(), zc + 0.2, 0.03); add(mix, ding(2093, 1.0), B["end"] + 0.1, 0.03); add(mix, pop(1000), B["end"], 0.03)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.25)
CAPS = [(0.05, "Which one are you? 👀"), (B["k1"], "#1 starts from bar 1. Every. Time."), (fc1 + 0.3, "…and never practises the hard bit 😬"),
        (B["k2"], "#2 plays everything full speed."), (B["k3"], "#3 practises the hard bit slowly first."), (zc, "NAILED IT 🔥"),
        (B["plan"], "Want to be #3? Every session has a tempo target."), (B["end"], "Which one are you? 1, 2 or 3 👇")]
caps = [{"t": round(t, 3), "text": s} for t, s in CAPS]
json.dump({"duration": DUR, "fps": 30, "beats": B, "caps": caps, "keys": keys, "wrong": sorted(wrong), "zc": round(zc, 3), "fc": round(fc1, 3)}, open(f"{HERE}/timing.json", "w"))
print("dur", DUR, "crash1", round(fc1, 2), "zc", round(zc, 2))
