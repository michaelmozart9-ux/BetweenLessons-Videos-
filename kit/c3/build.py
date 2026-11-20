# Cartoon: "The hard bar. Max vs Zoe." Max keeps crashing at full speed; Zoe taps "Too hard" -> next session 5% slower (real product mechanic).
# Music: Minuet in G (Petzold, formerly attributed to Bach; public domain). Captions only.
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
from plib import *
B = {"hook": 0.0, "max": 2.6, "zoe": 6.7, "reveal": 10.8, "plan": 12.9, "end": 14.7}
DUR = 16.8
# beats in quarters (3/4). Bar 3 run E5 C5 D5 E5 F#5 is "the hard bar".
MEL = [("D5", 0), ("G4", 1), ("A4", 1.5), ("B4", 2), ("C5", 2.5), ("D5", 3), ("G4", 4), ("G4", 5),
       ("E5", 6), ("C5", 7), ("D5", 7.5), ("E5", 8), ("F#5", 8.5), ("G5", 9), ("G4", 10), ("G4", 11)]
LH = [("G3", 0), ("B3", 3), ("C4", 6), ("B3", 9)]
WRONG = 8.5  # F#5 -> F5 when rushing
notes = []; keys = []; wrong = []
def play(who, t0, bpm, lo, hi, crash=False, v=0.62):
    q = 60 / bpm; end = t0 + (hi - lo) * q
    for n, b in MEL + LH:
        if not (lo <= b < hi): continue
        if crash and b > WRONG: continue
        m = P(n); t = t0 + (b - lo) * q; bad = crash and b == WRONG
        if bad: m -= 1
        dur = q * 3 if (n, b) in LH else q * 1.2
        notes.append({"m": m, "t": t, "rel": t + dur, "v": v + (0.15 if bad else 0), "sec": "s"}); keys.append({"t": round(t, 3), "who": who, "m": m, "x": bad})
        if bad:
            for k in (-1, 1): notes.append({"m": m + k, "t": t + 0.02, "rel": t + 0.5, "v": 0.7, "sec": "s"})
            wrong.append({"t": round(t, 3), "who": who}); end = t + 0.35
    return end
# hook: both rush the hard bar and crash
play("max", 0.08, 240, 3, 12, crash=True); play("zoe", 0.35, 240, 3, 12, crash=True)
# Max: full speed, crash, again, crash, again, crash
t = B["max"] + 0.15
for lo in (0, 6):
    t = play("max", t, 240, lo, 12, crash=True) + 0.4
# Zoe: crash once, taps "Too hard" -> next session 95%: clean x2
zt = play("zoe", B["zoe"] + 0.15, 240, 6, 12, crash=True)
TAP = round(zt + 0.35, 3)
clean = []
t = TAP + 0.75
for i in range(1):
    clean.append(round(t, 3)); t = play("zoe", t, 228, 6, 12) + 0.35
# reveal: Max crashes again, Zoe plays it clean then a chord
play("max", B["reveal"] + 0.1, 240, 6, 12, crash=True)
zend = play("zoe", B["reveal"] + 0.1, 228, 6, 12)
for j, n in enumerate(["G2", "D3", "G3", "B3", "D4", "G4"]): notes.append({"m": P(n), "t": zend + j * 0.05, "rel": zend + 1.5, "v": 0.6, "sec": "s"})
for j, n in enumerate(["G2", "D3", "G3", "B3", "D4", "G4"]): notes.append({"m": P(n), "t": B["plan"] + 0.1 + j * 0.08, "rel": DUR, "v": 0.34, "sec": "s"})
mix = reverb(render(notes, DUR, {"s": DUR}), wet=0.2)
for w in wrong: add(mix, buzz(), w["t"] + 0.02, 0.045)
add(mix, tap(), TAP, 0.05); add(mix, pop(1300), TAP + 0.05, 0.03)
for i, c in enumerate(clean): add(mix, ding([1568.0, 2093.0][i], 0.7), c + 1.1, 0.03)
for k in ["max", "zoe", "plan"]: add(mix, whoosh(0.4), B[k] - 0.25, 0.012)
add(mix, riser(0.7), B["reveal"] - 0.7, 0.025); add(mix, ding(1568, 1.0), zend + 0.1, 0.035)
add(mix, ding(2093, 1.0), B["end"] + 0.1, 0.03); add(mix, pop(1000), B["end"], 0.03)
master(mix, DUR, f"{HERE}/audio.wav", fade=0.25)
CAPS = [(0.03, "This bar is TOO HARD 😩 What do you do?"), (B["max"], "Max: full speed. Again. And again. ❌"),
        (B["zoe"], "Zoe: same mistake… 😬"), (TAP, "So she taps “Too hard” 👆"), (TAP + 0.7, "Next session: 5% slower 🐢"), (B["reveal"], "Slower… and it finally clicks ✅"),
        (B["plan"], "Too hard → 5% slower. Too easy → 5% faster."), (B["end"], "Be honest… Max or Zoe? 👇")]
json.dump({"duration": DUR, "fps": 30, "beats": B, "caps": [{"t": round(t, 3), "text": s} for t, s in CAPS], "keys": keys, "wrong": wrong,
           "tap": TAP, "clean": clean, "phone": []}, open(f"{HERE}/timing.json", "w"), ensure_ascii=False)
print("dur", DUR, "wrong", wrong, "tap", TAP, "clean", clean, "zend", round(zend, 2))
