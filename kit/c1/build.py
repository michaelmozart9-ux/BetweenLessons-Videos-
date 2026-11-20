# Cartoon: "Me practising alone vs when someone is listening". Für Elise (public domain). Captions only.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"alone": 0.0, "listen": 2.9, "fix": 6.6, "plan": 10.8, "end": 12.4}
DUR = 14.4
MEL = [("E5", 0), ("D#5", 1), ("E5", 2), ("D#5", 3), ("E5", 4), ("B4", 5), ("D5", 6), ("C5", 7), ("A4", 8), ("C4", 11), ("E4", 12), ("A4", 13),
       ("B4", 14), ("E4", 17), ("G#4", 18), ("B4", 19), ("C5", 20)]
LH = [("A2", 8), ("E3", 9), ("A3", 10), ("E2", 14), ("E3", 15), ("G#3", 16), ("A2", 20), ("E3", 21), ("A3", 22)]
notes = []; keys = []; wrong = []; buzzes = []
def play(t0, bpm, upto, wrongs=(), stop=None):
    q = 60 / bpm
    for n, b in MEL + LH:
        if b >= upto or (stop is not None and b >= stop): continue
        m = P(n); t = t0 + b * q
        if b in wrongs: m += 1; wrong.append(round(t, 3)); buzzes.append(t)
        notes.append({"m": m, "t": t, "rel": t + q * (2.5 if b in (8, 14, 20) else 1.2), "v": 0.62 if b < 8 else 0.55, "sec": "s"}); keys.append({"t": round(t, 3), "who": "max", "m": m})
    return t0 + upto * q
play(0.05, 440, 21)
play(B["listen"] + 0.5, 440, 11, wrongs=(3, 6), stop=9); fc = B["listen"] + 0.5 + 9 * 60 / 440
for j, n in enumerate(["C3", "C#3", "D3", "F#3", "G3", "G#3"]): notes.append({"m": P(n), "t": fc + j * 0.01, "rel": fc + 0.9, "v": 0.85, "sec": "s"})
zc = play(B["fix"] + 0.3, 420, 20) + 0.0
for j, n in enumerate(["A2", "E3", "A3", "C4", "E4", "A4", "C5", "E5"]): notes.append({"m": P(n), "t": zc + j * 0.05, "rel": zc + 2.2, "v": 0.72, "sec": "s"})
for j, n in enumerate(["C3", "G3", "C4", "E4", "G4", "C5"]): notes.append({"m": P(n), "t": B["plan"] + 0.1 + j * 0.08, "rel": DUR, "v": 0.38, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
for t in buzzes: add(mix, buzz(), t, 0.04)
add(mix, buzz(), fc, 0.06); add(mix, boom(0.8), fc, 0.07); add(mix, scratch(), fc + 0.2, 0.06); wrong.append(round(fc, 3))
add(mix, pop(500), B["listen"] + 0.05, 0.04); add(mix, whoosh(0.4), B["listen"] - 0.2, 0.012)
def applause(d, seed=3, dens=60):
    r = np.random.default_rng(seed); n = int(d * SR); out = np.zeros(n, np.float32)
    for _ in range(int(d * dens)):
        s = int(r.uniform(0, n - 2000)); L = int(r.uniform(400, 1200)); c = r.normal(0, 1, L).astype(np.float32) * np.exp(-np.linspace(0, 6, L)).astype(np.float32); out[s:s + L] += c * r.uniform(0.3, 1.0)
    out = np.convolve(out, np.ones(3) / 3, "same").astype(np.float32); x = np.linspace(0, d, n); env = np.minimum(1, x / 0.2) * np.minimum(1, (d - x) / 0.6)
    return (out * env).astype(np.float32)
add(mix, applause(2.0, 4, 25), zc + 0.15, 0.08)
for k in ["fix", "plan"]: add(mix, whoosh(0.4), B[k] - 0.25, 0.012)
add(mix, ding(1568, 1.0), zc + 0.05, 0.03); add(mix, sparkle(), zc + 0.2, 0.03); add(mix, ding(2093, 1.0), B["end"] + 0.1, 0.03); add(mix, pop(1000), B["end"], 0.03)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.25)
CAPS = [(0.03, "Me practising alone: 😌"), (B["listen"], "Me when someone is listening: 😰"), (fc + 0.4, "Why is this SO true 😭"),
        (B["fix"], "The fix: end every practice with a full run-through 🎤"), (zc, "NAILED IT 🔥"),
        (B["plan"], "Every session in the plan ends with a run-through."), (B["end"], "Tag someone who does this 😭👇")]
json.dump({"duration": DUR, "fps": 30, "beats": B, "caps": [{"t": round(t, 3), "text": s} for t, s in CAPS], "keys": keys, "wrong": sorted(wrong), "zc": round(zc, 3), "fc": round(fc, 3)}, open(f"{HERE}/timing.json", "w"))
print("dur", DUR, "fc", round(fc, 2), "zc", round(zc, 2))
