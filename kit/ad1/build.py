# Ad: "This looks impossible. Watch it get built in 4 steps." Moonlight Sonata 3rd mvt (Beethoven, public domain). C# minor, unit = 16th.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
CSM, G7 = {1, 4, 8}, {8, 0, 3, 6}
def arp(pcs, lo, n):
    out, m = [], P(lo)
    while len(out) < n:
        if m % 12 in pcs: out.append(m)
        m += 1
    return out
SRC = []  # (midi, beat, dur, vel)
for b in range(0, 12, 2): SRC += [(P("C#2"), b, 2, 0.55), (P("C#3"), b, 2, 0.5)]
SRC += [(m, 1 + i, 1, 0.55 + 0.03 * i) for i, m in enumerate(arp(CSM, "E2", 11))]
for b in (12, 14): SRC += [(P(n), b, 1.6, 0.92) for n in ["C#2", "C#3", "G#4", "C#5", "E5", "G#5"]]
for b in range(16, 28, 2): SRC += [(P("G#2"), b, 2, 0.55), (P("G#3"), b, 2, 0.5)]
SRC += [(m, 17 + i, 1, 0.55 + 0.03 * i) for i, m in enumerate(arp(G7, "B#2", 11))]
SRC += [(m, 28 + i * 0.5, 0.5, 0.85 - 0.02 * i) for i, m in enumerate(sorted(arp(G7, "B#3", 8), reverse=True))]
notes = []; vis = []
def play(t0, bpm, lo, hi, hand=None):
    q = 60 / bpm
    for m, b, d, v in SRC:
        if not (lo <= b < hi): continue
        h = "L" if m < 60 else "R"
        if hand and h != hand: continue
        t = t0 + (b - lo) * q; notes.append({"m": m, "t": t, "rel": t + d * q * 1.1, "v": v, "sec": "s"}); vis.append({"m": m, "t": round(t, 3), "d": round(d * q * 0.9, 3), "h": h})
    return t0 + (hi - lo) * q
B = {"hook": 0.0, "say": 2.65, "s1": 3.3, "s2": 5.7, "s3": 8.3, "s4": 10.4}
play(0.05, 660, 0, 28)
play(B["s1"], 330, 0, 12, "L"); play(B["s2"], 396, 0, 16, "R"); play(B["s3"], 495, 0, 16)
CH = round(play(B["s4"] + 0.05, 660, 0, 32), 3)
for j, n in enumerate(["C#2", "G#2", "C#3", "E3"]): notes.append({"m": P(n), "t": CH + j * 0.06, "rel": CH + 3.4, "v": 0.9, "sec": "s"}); vis.append({"m": P(n), "t": round(CH + j * 0.06, 3), "d": 1.0, "h": "L"})
for j, n in enumerate(["G#3", "C#4", "E4", "G#4", "C#5", "E5", "G#5"]): notes.append({"m": P(n), "t": CH + 0.25 + j * 0.06, "rel": CH + 3.4, "v": 0.85, "sec": "s"}); vis.append({"m": P(n), "t": round(CH + 0.25 + j * 0.06, 3), "d": 1.0, "h": "R"})
B["imagine"] = round(CH + 0.3, 3); B["plan"] = round(CH + 2.0, 3); DUR = round(CH + 5.0, 2)
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.22)
def applause(d, seed=3, dens=140):
    r = np.random.default_rng(seed); n = int(d * SR); out = np.zeros(n, np.float32)
    for _ in range(int(d * dens)):
        s = int(r.uniform(0, n - 2000)); L = int(r.uniform(400, 1200)); c = r.normal(0, 1, L).astype(np.float32) * np.exp(-np.linspace(0, 6, L)).astype(np.float32); out[s:s + L] += c * r.uniform(0.3, 1.0)
    out = np.convolve(out, np.ones(3) / 3, "same").astype(np.float32); x = np.linspace(0, d, n); env = np.minimum(1, x / 0.3) * np.minimum(1, (d - x) / 1.0)
    return (out * env).astype(np.float32)
add(mix, applause(3.6), CH + 0.2, 0.09)
for k in ["s1", "s2", "s3", "s4"]: add(mix, whoosh(0.4), B[k] - 0.22, 0.012); add(mix, pop(1000), B[k] + 0.05, 0.025)
add(mix, riser(0.9), B["s4"] - 0.9, 0.025)
for b in range(0, 32, 2): add(mix, kick(), B["s4"] + 0.05 + b * 60 / 660, 0.05)
add(mix, boom(1.4), CH, 0.12); add(mix, ding(2093, 1.0), B["plan"] + 0.2, 0.03); add(mix, sparkle(), CH + 0.3, 0.03)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.3)
json.dump({"duration": DUR, "fps": 30, "beats": B, "chord": CH, "crashes": [], "notes": vis}, open(f"{HERE}/timing.json", "w"))
print("dur", DUR, "chord", CH, "range", min(v["m"] for v in vis), max(v["m"] for v in vis))
