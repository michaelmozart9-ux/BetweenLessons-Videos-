# "Guess the grade" builder: 4 levels A-D that only get harder, played back-to-back with no gaps, then a reveal.
import json, numpy as np
from plib import *

def hands(nn, split=60):
    return [(m, b, d, ("L" if m < split else "R") if h == "A" else h, v) for m, b, d, h, v in nn]

def make(HERE, piece, levels, final_beat, grades, url_after=1.0):
    """levels: [(notes, units, bpm, pedal)] for a,b,c,d. Level d contains the final chord at final_beat."""
    rng = np.random.default_rng(11); notes = []; secs = []; t = 0.0; ids = "abcd"
    for i, (nn, units, bpm, pedal) in enumerate(levels):
        q = 60 / bpm; t0 = t + (0.06 if i == 0 else 0.0); last = i == 3
        notes += place(hands(nn), bpm, t0, ids[i], pedal=pedal, rng=rng, final_beat=(final_beat if last else None))
        end = t0 + units * q
        if last: CHORD = t0 + final_beat * q; end = CHORD + 3.3
        secs.append({"id": ids[i], "start": round(t, 3), "end": round(end, 3), "grade": grades[i]}); t = end
    DUR = round(t, 2); secs[-1]["end"] = DUR
    mix = reverb(render(notes, DUR, {s["id"]: s["end"] for s in secs}), wet=0.22)
    for s in secs[1:]: add(mix, whoosh(0.35), s["start"] - 0.2, 0.011)
    add(mix, riser(0.7), secs[3]["start"] - 0.7, 0.028)
    add(mix, boom(1.4), CHORD, 0.12)
    for i, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]): add(mix, ding(f, 0.9), CHORD + 0.25 + i * 0.3, 0.03 + 0.004 * i)
    URL = secs[1]["start"] + url_after; add(mix, pop(1200), URL, 0.035)
    master(mix, DUR, f"{HERE}/audio.wav", fade=0.25)
    ui = {"chord": round(CHORD, 3), "url": round(URL, 3), "lt": round(CHORD, 3), "piece": piece, "grades": grades}
    json.dump({"duration": DUR, "fps": 30, "secs": secs, "notes": notes, "ui": ui}, open(f"{HERE}/timing.json", "w"))
    ms = [n["m"] for n in notes]
    print("dur", DUR, "chord", round(CHORD, 2), [(s["id"], s["start"]) for s in secs], "range", min(ms), max(ms), "url", round(URL, 2))
