# Paid ad A (adult learners): stuck on the same bar -> plan with tempo targets -> full speed. Mozart, Turkish March (public domain).
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
PH = [("B4", 1), ("A4", 1), ("G#4", 1), ("A4", 1), ("C5", 4), ("D5", 1), ("C5", 1), ("B4", 1), ("C5", 1), ("E5", 4),
      ("F5", 1), ("E5", 1), ("D#5", 1), ("E5", 1), ("B5", 1), ("A5", 1), ("G#5", 1), ("A5", 1), ("B5", 1), ("A5", 1), ("G#5", 1), ("A5", 1), ("C6", 4)]
LHP = [("A3", 4), ("C4", 6), ("E4", 6), ("A3", 8), ("C4", 10), ("E4", 10), ("A3", 12), ("C4", 14), ("E4", 14), ("E3", 16), ("B3", 18), ("E3", 20), ("B3", 22), ("A3", 24), ("C4", 26), ("E4", 26)]
notes = []; vis = []
def play(t0, bpm, lo, hi, wrong=(), stop=None):
    q = 60 / bpm; b = 0
    for n, d in PH:
        if lo <= b < hi and (stop is None or b < stop):
            m = P(n); h = "R"
            if b in wrong: m -= 1; h = "X"
            t = t0 + (b - lo) * q; notes.append({"m": m, "t": t, "rel": t + d * q * 0.9, "v": 0.74, "sec": "s"}); vis.append({"m": m, "t": round(t, 3), "d": round(d * q * 0.85, 3), "h": h})
        b += d
    for n, bb in LHP:
        if lo <= bb < hi and (stop is None or bb < stop):
            t = t0 + (bb - lo) * q; notes.append({"m": P(n), "t": t, "rel": t + q * 1.1, "v": 0.5, "sec": "s"}); vis.append({"m": P(n), "t": round(t, 3), "d": round(q, 3), "h": "L"})
    return t0 + ((min(hi, stop) if stop else hi) - lo) * q
crashes = []
for t0 in (0.05, 2.45):
    e = play(t0, 640, 0, 28, wrong=(18, 19), stop=20); crashes.append(round(e, 3))
    for j, n in enumerate(["G4", "G#4", "A4", "B4"]): notes.append({"m": P(n), "t": e + j * 0.01, "rel": e + 0.6, "v": 0.85, "sec": "s"}); vis.append({"m": P(n), "t": round(e, 3), "d": 0.2, "h": "X"})
B = {"fail1": 0.0, "fail2": 2.45, "plan": 5.0, "rate": 9.6, "full": 13.5}
play(5.3, 256, 16, 28); TAP = 10.0
play(10.3, 384, 16, 28); play(12.1, 512, 16, 28)
end = play(13.6, 640, 0, 28); CH = round(end, 3)
for j, n in enumerate(["A2", "E3", "A3", "C4"]): notes.append({"m": P(n), "t": CH + j * 0.06, "rel": CH + 2.6, "v": 0.88, "sec": "s"}); vis.append({"m": P(n), "t": round(CH + j * 0.06, 3), "d": 0.9, "h": "L"})
for j, n in enumerate(["E4", "A4", "C5", "E5", "A5"]): notes.append({"m": P(n), "t": CH + 0.25 + j * 0.06, "rel": CH + 2.6, "v": 0.85, "sec": "s"}); vis.append({"m": P(n), "t": round(CH + 0.25 + j * 0.06, 3), "d": 0.9, "h": "R"})
DUR = round(CH + 5.6, 2); B["offer"] = round(CH + 0.9, 3)
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
for c in crashes: add(mix, buzz(), c - 0.19, 0.04); add(mix, buzz(), c, 0.06)
add(mix, scratch(), crashes[1] + 0.15, 0.05)
for k in ["plan", "rate", "full"]: add(mix, whoosh(0.4), B[k] - 0.22, 0.012)
add(mix, click(), TAP, 0.04); add(mix, pop(1200), TAP + 0.02, 0.025); add(mix, ding(1975.5, 0.8), TAP + 0.35, 0.03)
for j in range(3): add(mix, pop(900 + 100 * j), B["plan"] + 0.6 + j * 0.25, 0.022)
add(mix, riser(0.8), B["full"] - 0.8, 0.025)
for b in range(0, 28, 4): add(mix, kick(), 13.6 + b * 60 / 640, 0.06)
add(mix, boom(1.4), CH, 0.11)
def applause(d, seed=3, dens=140):
    r = np.random.default_rng(seed); n = int(d * SR); out = np.zeros(n, np.float32)
    for _ in range(int(d * dens)):
        s = int(r.uniform(0, n - 2000)); L = int(r.uniform(400, 1200)); c = r.normal(0, 1, L).astype(np.float32) * np.exp(-np.linspace(0, 6, L)).astype(np.float32); out[s:s + L] += c * r.uniform(0.3, 1.0)
    out = np.convolve(out, np.ones(3) / 3, "same").astype(np.float32); x = np.linspace(0, d, n); env = np.minimum(1, x / 0.3) * np.minimum(1, (d - x) / 1.0)
    return (out * env).astype(np.float32)
add(mix, applause(2.6), CH + 0.15, 0.08)
for j in range(4): add(mix, pop(1000 + 150 * j), B["offer"] + 0.5 + j * 0.4, 0.03)
add(mix, ding(2093, 1.0), B["offer"] + 2.3, 0.03)
for j, n in enumerate(["F3", "C4", "F4", "A4", "C5"]): pass
master(mix, DUR, f"{HERE}/audio.wav", fade=0.3)
json.dump({"duration": DUR, "fps": 30, "beats": B, "tap": TAP, "chord": CH, "crashes": crashes, "notes": vis}, open(f"{HERE}/timing.json", "w"))
print("dur", DUR, "chord", CH, "crashes", crashes, "range", min(v["m"] for v in vis), max(v["m"] for v in vis))
