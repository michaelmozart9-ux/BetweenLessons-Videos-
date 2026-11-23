# Cartoon: "Sat down to practise… now what?" Max replays the easy bit then crashes the hard bit at full speed; Zoe opens today's session
# (Warm-up / Main work / Run-through, tempo target) and plays the hard bars slowly, then clean. Real features only. Music: Minuet in G (Petzold, public domain).
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"hook": 0.0, "max": 2.6, "zoe": 6.9, "reveal": 11.0, "plan": 13.5, "end": 16.3}
DUR = 18.0
MEL = [("D5", 0, 1), ("G4", 1, .5), ("A4", 1.5, .5), ("B4", 2, .5), ("C5", 2.5, .5), ("D5", 3, 1), ("G4", 4, 1), ("G4", 5, 1),
       ("E5", 6, 1), ("C5", 7, .5), ("D5", 7.5, .5), ("E5", 8, .5), ("F#5", 8.5, .5), ("G5", 9, 1), ("G4", 10, 1), ("G4", 11, 1),
       ("C5", 12, 1), ("D5", 13, .5), ("C5", 13.5, .5), ("B4", 14, .5), ("A4", 14.5, .5), ("B4", 15, 1), ("C5", 16, .5), ("B4", 16.5, .5), ("A4", 17, .5), ("G4", 17.5, .5)]
LH = [("G3", 0, 2), ("A3", 2, 1), ("B3", 3, 3), ("C4", 6, 3), ("B3", 9, 3), ("A3", 12, 3), ("G3", 15, 3)]
WRONG = 14  # B4 -> A#4 when rushed
notes = []; keys = []; wrong = []
def play(who, t0, bpm, lo, hi, crash=False, v=0.62):
    q = 60 / bpm; end = t0 + (hi - lo) * q
    for n, b, d in MEL + LH:
        if not (lo <= b < hi): continue
        if crash and b > WRONG: continue
        m = P(n); t = t0 + (b - lo) * q; bad = crash and b == WRONG and (n, b, d) in MEL
        if bad: m -= 1
        notes.append({"m": m, "t": t, "rel": t + d * q * 0.95, "v": v + (0.15 if bad else 0) - (0.12 if (n, b, d) in LH else 0), "sec": "s"}); keys.append({"t": round(t, 3), "who": who, "m": m, "x": bad})
        if bad:
            for k in (-1, 1): notes.append({"m": m + k, "t": t + 0.02, "rel": t + 0.5, "v": 0.7, "sec": "s"})
            wrong.append({"t": round(t, 3), "who": who}); end = t + 0.35
    return end
# hook: Max rushes the hard bars and crashes; Zoe plays them slowly
play("max", 0.3, 190, 12, 18, crash=True); play("zoe", 0.1, 100, 12, 16, v=0.5)
# Max: the easy opening AGAIN, then the hard bars at full speed -> crash
t = play("max", B["max"] + 0.15, 160, 0, 6) + 0.25
play("max", t, 190, 12, 18, crash=True)
# Zoe: taps today's session, plays the hard bars slowly and clean
TAP = round(B["zoe"] + 0.25, 3)
zs = TAP + 0.5; ze = play("zoe", zs, 110, 12, 18, v=0.55)
ticks = [round(ze + 0.1, 3)]
# reveal: Max crashes again; Zoe plays it clean, a bit faster, then a chord
play("max", B["reveal"] + 0.1, 190, 12, 18, crash=True)
zend = play("zoe", B["reveal"] + 0.1, 165, 12, 18) - 0.05
ticks.append(round(zend + 0.1, 3))
for j, n in enumerate(["G2", "D3", "G3", "B3", "D4", "G4"]): notes.append({"m": P(n), "t": zend + j * 0.05, "rel": zend + 1.6, "v": 0.6, "sec": "s"})
for j, n in enumerate(["G2", "D3", "G3", "B3", "D4", "G4"]): notes.append({"m": P(n), "t": B["plan"] + 0.1 + j * 0.08, "rel": DUR, "v": 0.32, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
for w in wrong: add(mix, buzz(), w["t"] + 0.02, 0.045)
add(mix, tap(), TAP, 0.05); add(mix, pop(1300), TAP + 0.05, 0.03)
for i, c in enumerate(ticks): add(mix, ding([1568.0, 2093.0][i], 0.7), c, 0.03)
for k in ["max", "zoe", "plan"]: add(mix, whoosh(0.4), B[k] - 0.25, 0.012)
add(mix, pop(1300), B["plan"] + 0.35, 0.03)
add(mix, riser(0.7), B["reveal"] - 0.7, 0.025)
add(mix, ding(2093, 1.0), B["end"] + 0.1, 0.03); add(mix, pop(1000), B["end"], 0.03)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.25)
CAPS = [(0.03, "You sit down to practise… now what? 🤔"), (B["max"], "Max: the easy bit… AGAIN 🔁"),
        (wrong[1]["t"] - 0.9, "Then the hard bit at full speed…"), (wrong[1]["t"] + 0.3, "Same mistake ❌"),
        (B["zoe"], "Zoe opens today’s session 👆"), (zs + 0.3, "Main work: the hard bars, slow 🐢"),
        (B["reveal"], "Guess ❌ vs plan ✅"),
        (B["plan"], "Every session tells you what to practise"), (B["end"], "Be honest… Max or Zoe? 👇")]
plan = {"at": B["plan"], "top": 420, "dx": 170, "scale": 0.82, "day": "Week 1 · Day 2 · 20 min", "piece": "Minuet in G", "sub": "Petzold",
        "chips": ["Bars 5–8", "Right hand"], "mins": [5, 10, 5], "tempo": 45, "bpm": 54, "milestone": "Bars 1–8 hands together at 50%"}
json.dump({"duration": DUR, "fps": 30, "beats": B, "caps": [{"t": round(t, 3), "text": s} for t, s in CAPS], "keys": keys, "wrong": wrong,
           "tap": TAP, "ticks": ticks, "clean": [zs], "phone": [], "plan": plan}, open(f"{HERE}/timing.json", "w"), ensure_ascii=False)
print("dur", DUR, "wrong", wrong, "tap", TAP, "ticks", ticks, "zend", round(zend, 2), "ze", round(ze, 2))
