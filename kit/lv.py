# Generic 4-section builder (sections a-d, no gaps, energy only rises), end reveal card, optional per-section answer reveals + kicks.
import json, numpy as np
from plib import *

def hands(nn, split=60):
    return [(m, b, d, ("L" if m < split else "R") if h == "A" else h, v) for m, b, d, h, v in nn]

def make(HERE, levels, final_beat, ui, answers=False, kicks=None, url_after=1.0, sfx=None, tail=3.3, plan=None, ec=None):
    """ec: seconds after the final chord when the big end card (Which grade are you? / betweenlessons.org) appears"""
    """plan: dict for plan.js phone (its 'at' is seconds after the final chord); tail: seconds after the chord"""
    """levels: [(notes, units, bpm, pedal)]; kicks: {section_index: [beats]}"""
    rng = np.random.default_rng(11); notes = []; secs = []; t = 0.0; ids = "abcd"; t0s = []; reveal = []
    for i, (nn, units, bpm, pedal) in enumerate(levels):
        q = 60 / bpm; t0 = t + (0.06 if i == 0 else 0.0); last = i == 3; t0s.append((t0, q))
        notes += place(hands(nn), bpm, t0, ids[i], pedal=pedal, rng=rng, final_beat=(final_beat if last else None))
        end = t0 + units * q
        if last: CHORD = t0 + final_beat * q; end = CHORD + tail
        secs.append({"id": ids[i], "start": round(t, 3), "end": round(end, 3)}); reveal.append(round((CHORD if last else end) - 0.7, 3)); t = end
    DUR = round(t, 2); secs[-1]["end"] = DUR
    mix = reverb(render(notes, DUR, {s["id"]: s["end"] for s in secs}), wet=0.22)
    for s in secs[1:]: add(mix, whoosh(0.35), s["start"] - 0.2, 0.011)
    add(mix, riser(0.7), secs[3]["start"] - 0.7, 0.028)
    for i, bs in (kicks or {}).items():
        t0, q = t0s[i]
        for b in bs: add(mix, kick(), t0 + b * q, 0.07)
    for kind, i, b, g in (sfx or []):
        t0, q = t0s[i]; add(mix, {"buzz": buzz, "scratch": scratch, "ding": lambda: ding(1568.0, 0.7)}[kind](), t0 + b * q, g)
    add(mix, boom(1.4), CHORD, 0.12)
    if answers:
        for r in reveal: add(mix, ding(1568.0, 0.7), r, 0.03)
    nrows = len(ui.get("rows", []))
    for i in range(nrows): add(mix, ding([1046.5, 1318.5, 1568.0, 2093.0, 2637.0][i % 5], 0.9), CHORD + 0.25 + i * 0.3, 0.028 + 0.003 * i)
    URL = secs[1]["start"] + url_after; add(mix, pop(1200), URL, 0.035)
    if plan: plan = dict(plan, at=round(CHORD + plan['at'], 3)); ui = dict(ui, plan=plan); add(mix, whoosh(0.4), plan['at'] - 0.2, 0.012); add(mix, pop(1300), plan['at'] + 0.3, 0.03)
    if ec is not None: add(mix, whoosh(0.4), CHORD + ec - 0.2, 0.012); add(mix, ding(2093.0, 1.2), CHORD + ec + 0.2, 0.035)
    master(mix, DUR, f"{HERE}/audio.wav", fade=0.25)
    ui = dict(ui, chord=round(CHORD, 3), url=round(URL, 3), lt=round(CHORD, 3), revealAt=(reveal if answers else None))
    if ec is not None: ui['ec'] = round(CHORD + ec, 3)
    json.dump({"duration": DUR, "fps": 30, "secs": secs, "notes": notes, "ui": ui}, open(f"{HERE}/timing.json", "w"))
    ms = [n["m"] for n in notes]
    print("dur", DUR, "chord", round(CHORD, 2), [(s["id"], s["start"]) for s in secs], "range", min(ms), max(ms), "url", round(URL, 2))

def N(*xs, h="A", v=0.65):  # ("E5", beat, dur) -> note tuples
    return [(P(n), b, d, h, v) for n, b, d in xs]
