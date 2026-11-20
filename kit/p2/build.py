# Cartoon series ep 2: "3 types of piano students PART 2". Für Elise (public domain). Captions only.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"hook": 0.0, "k1": 1.7, "k2": 5.4, "k3": 8.6, "plan": 12.9, "end": 14.6}
DUR = 16.6
MEL = [("E5", 0), ("D#5", 1), ("E5", 2), ("D#5", 3), ("E5", 4), ("B4", 5), ("D5", 6), ("C5", 7), ("A4", 8), ("C4", 11), ("E4", 12), ("A4", 13),
       ("B4", 14), ("E4", 17), ("G#4", 18), ("B4", 19), ("C5", 20)]
LH = [("A2", 8), ("E3", 9), ("A3", 10), ("E2", 14), ("E3", 15), ("G#3", 16), ("A2", 20), ("E3", 21), ("A3", 22)]
notes = []; keys = []; wrong = []; clicks = []
def add_note(who, m, t, d, v=0.6): notes.append({"m": m, "t": t, "rel": t + d, "v": v, "sec": "s"}); keys.append({"t": round(t, 3), "who": who, "m": m})
# #1 metronome hater: metronome ticks steady, he speeds up every beat, then crashes
t = B["k1"] + 0.15; q = 60 / 380
for i in range(8): clicks.append(round(B["k1"] + 0.15 + i * 0.3, 3))
for n, b in sorted(MEL + LH, key=lambda x: x[1]):
    if b >= 13: break
    tt = B["k1"] + 0.15 + sum(q * (0.97 ** k) for k in range(b)); add_note("k1", P(n), tt, 0.25)
fc = B["k1"] + 0.15 + sum(q * (0.97 ** k) for k in range(13))
for j, n in enumerate(["C3", "C#3", "D3", "F#3", "G3", "G#3"]): notes.append({"m": P(n), "t": fc + j * 0.01, "rel": fc + 0.9, "v": 0.85, "sec": "s"})
wrong.append(round(fc, 3))
# #2 tutorial watcher: plays nothing (phone audio blips)
phone_t = [round(B["k2"] + 0.4 + i * 0.9, 3) for i in range(3)]
# #3 smart: clean, chord
q3 = 60 / 380
for n, b in MEL + LH: add_note("k3", P(n), B["k3"] + 0.15 + b * q3, q3 * (2.5 if b in (8, 14, 20) else 1.2))
zc = B["k3"] + 0.15 + 20 * q3
for j, n in enumerate(["A2", "E3", "A3", "C4", "E4", "A4", "C5", "E5"]): notes.append({"m": P(n), "t": zc + j * 0.05, "rel": zc + 2.4, "v": 0.72, "sec": "s"})
for j, n in enumerate(["C3", "G3", "C4", "E4", "G4", "C5"]): notes.append({"m": P(n), "t": B["plan"] + 0.1 + j * 0.08, "rel": DUR, "v": 0.38, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
for c in clicks: add(mix, click(), c, 0.05)
add(mix, buzz(), fc, 0.06); add(mix, boom(0.8), fc, 0.07); add(mix, scratch(), fc + 0.2, 0.06)
for p in phone_t: add(mix, ding(1760, 0.3), p, 0.03); add(mix, pop(1400), p + 0.3, 0.02)
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
CAPS = [(0.05, "PART 2. Which one are you? 👀"), (B["k1"], "#1 hates the metronome… and speeds up every bar"), (fc + 0.3, "😬"),
        (B["k2"], "#2 watches 3 hours of tutorials. Plays 0 minutes 📱"), (B["k3"], "#3 practises slowly with a tempo target first"), (zc, "NAILED IT 🔥"),
        (B["plan"], "Want to be #3? Every session has a tempo target."), (B["end"], "1, 2 or 3? 👇 Follow for part 3 👀")]
json.dump({"duration": DUR, "fps": 30, "beats": B, "caps": [{"t": round(t, 3), "text": s} for t, s in CAPS], "keys": keys, "wrong": wrong, "zc": round(zc, 3), "fc": round(fc, 3), "phone": phone_t, "clicks": clicks}, open(f"{HERE}/timing.json", "w"))
print("dur", DUR, "fc", round(fc, 2), "zc", round(zc, 2))
