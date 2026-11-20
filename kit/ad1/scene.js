// Product ad: animated phone UI (HTML) over a 3D piano background. window.render(t) is a pure function of t.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
await Promise.all(["900 80px Inter", "800 40px Inter", "700 30px Inter"].map((f) => document.fonts.load(f)));
const T = window.__TIMING__, B = T.beats, DUR = T.duration, $ = (id) => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, k) => a + (b - a) * k, ease = (k) => 1 - Math.pow(1 - clamp(k), 3);
const back = (k) => { k = clamp(k); const c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
let seed = 5; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
// ---------- 3D background: glowing keyboard arc + floating notes
const renderer = new THREE.WebGLRenderer({ canvas: $("gl"), antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(720, 1280, false); renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.2; renderer.outputColorSpace = THREE.SRGBColorSpace;
const scene = new THREE.Scene(); scene.background = new THREE.Color("#2A1C12"); scene.fog = new THREE.FogExp2("#2A1C12", 0.05);
const camera = new THREE.PerspectiveCamera(50, 1080 / 1920, 0.1, 100);
scene.add(new THREE.HemisphereLight("#FFE9C9", "#3A2618", 1.3)); const dl = new THREE.DirectionalLight("#FFFFFF", 2); dl.position.set(-4, 8, 6); scene.add(dl);
const keys = [], isBlack = (i) => [1, 3, 6, 8, 10].includes(i % 12);
let wx = 0; const whiteX = []; for (let i = 0; i < 49; i++) { if (!isBlack(i)) { whiteX[i] = wx; wx++; } }
for (let i = 0; i < 49; i++) {
  const b = isBlack(i), x = b ? (whiteX[i - 1] + 0.5) : whiteX[i], X = (x - wx / 2) * 0.34;
  const m = new THREE.Mesh(new RoundedBoxGeometry(b ? 0.2 : 0.32, b ? 0.22 : 0.18, b ? 1.1 : 1.7, 2, 0.03), new THREE.MeshStandardMaterial({ color: b ? "#141010" : "#F6F1E7", roughness: 0.4, emissive: "#000000" }));
  m.position.set(X, b ? 0.12 : 0, b ? -0.3 : 0); scene.add(m); keys.push({ m, b, X });
}
const glowTex = (() => { const c = document.createElement("canvas"); c.width = c.height = 64; const g = c.getContext("2d"); const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.4, "rgba(255,210,140,.5)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); })();
const motes = Array.from({ length: 70 }, () => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color: "#FFC877", transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })); s.userData = { x: (rnd() - 0.5) * 12, y: rnd() * 10, z: -2 - rnd() * 8, sp: 0.2 + rnd() * 0.4, s: 0.1 + rnd() * 0.25 }; scene.add(s); return s; });
function noteTex(ch) { const c = document.createElement("canvas"); c.width = c.height = 128; const g = c.getContext("2d"); g.fillStyle = "#E0A84B"; g.font = "100px serif"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(ch, 64, 70); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; }
const nts = Array.from({ length: 14 }, (_, i) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: noteTex(i % 2 ? "♪" : "♫"), transparent: true, depthWrite: false })); s.userData = { x: (rnd() - 0.5) * 9, y: rnd() * 9, z: -1.5 - rnd() * 4, sp: 0.3 + rnd() * 0.3, ph: rnd() * 6 }; scene.add(s); return s; });
// ---------- falling notes onto the keyboard (MIDI 36..84)
const keyOf = (m) => keys[m - 36], SPEED = 6.5, HIT = 0.25, COL = { R: "#F2B84B", L: "#A99BFF", X: "#FF3B3B" };
const glows = Array.from({ length: 24 }, () => { const g = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, color: "#FFC877", transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })); g.visible = false; scene.add(g); return g; });
const bars = T.notes.map((n) => { const k = keyOf(n.m), len = Math.max(0.15, n.d * SPEED); const mesh = new THREE.Mesh(new RoundedBoxGeometry(k.b ? 0.18 : 0.28, len, 0.18, 2, 0.06), new THREE.MeshStandardMaterial({ color: COL[n.h], emissive: COL[n.h], emissiveIntensity: 0.6 }));
  mesh.position.set(k.X, -10, k.b ? -0.4 : 0.15); scene.add(mesh); return { n, k, mesh, len }; });
const STEPS = [["s1", "STEP 1", "Left hand alone", "50%"], ["s2", "STEP 2", "Right hand alone", "60%"], ["s3", "STEP 3", "Hands together", "75%"], ["s4", "STEP 4", "Full speed", "100% 🔥"]];
const CAP = [[0, "This looks impossible 😳"], [B.say, "Watch it get built in <span class='hl'>4 steps</span> 👇"], [B.s1, "Slow, one hand at a time"], [B.s3, "Then together, a bit faster"], [B.s4, "Then… 🔥"],
  [B.imagine, "Imagine playing <span class='hl'>THIS</span> 😳"], [B.plan, "Your piece, built step by step with a <span class='hl'>6-week plan</span>"]];
let lastCap = -1;
const stepAt = (t) => { let s = null; for (const st of STEPS) if (t >= B[st[0]]) s = st; return t >= B.imagine ? null : s; };
function ui(t) {
  let ci = 0; CAP.forEach(([ct], i) => { if (t >= ct) ci = i; }); if (ci !== lastCap) { $("cap").innerHTML = CAP[ci][1]; lastCap = ci; }
  $("cap").style.transform = `scale(${lerp(1.12, 1, ease((t - CAP[ci][0]) / 0.15)).toFixed(3)})`;
  $("cap").style.top = t >= B.imagine ? "760px" : "1420px"; $("cap").style.fontSize = t >= B.imagine && t < B.plan ? "104px" : "70px";
  $("chip").innerHTML = t < B.s1 ? "<b>MOONLIGHT SONATA</b> · 3RD MVT ⚡" : t < B.imagine ? "BUILT WITH <b>THE PLAN</b>" : "<b>BETWEEN LESSONS</b>";
  const st = stepAt(t), card = $("step");
  if (st) { card.style.opacity = 1; card.innerHTML = `<span class="n">${st[1]}</span><span class="w">${st[2]}</span><span class="p">${st[3]}</span>`; card.style.transform = `translateX(-50%) scale(${lerp(1.3, 1, ease((t - B[st[0]]) / 0.2)).toFixed(3)})`; }
  else card.style.opacity = 0;
  const te = $("tempo"), tv = t < B.s1 ? "100%" : st ? st[3].replace(" 🔥", "") : "100%"; te.style.opacity = t >= B.imagine ? 0 : 1; if (te.textContent !== tv) te.textContent = tv;
  const ctk = t - B.plan - 0.4; $("cta").style.opacity = ctk > 0 ? 1 : 0; $("cta").style.transform = `translateX(-50%) scale(${(ctk > 0 ? back(ctk / 0.3) * (1 + 0.03 * Math.sin(t * 6)) : 1).toFixed(3)})`;
  $("crowd").style.opacity = t >= B.imagine ? ease((t - B.imagine) / 0.4) : 0;
  let fl = 0.3 * Math.max(0, 1 - t / 0.2); for (const b of [B.s1, B.s2, B.s3, B.s4]) if (t >= b && t < b + 0.15) fl = Math.max(fl, 0.4 * (1 - (t - b) / 0.15));
  if (t >= T.chord && t < T.chord + 0.35) fl = Math.max(fl, 0.6 * (1 - (t - T.chord) / 0.35));
  if (t > DUR - 0.3) fl = Math.max(fl, (t - (DUR - 0.3)) / 0.3); $("flash").style.opacity = fl.toFixed(3); $("red").style.opacity = 0; $("phoneWrap").style.opacity = 0;
}
window.render = (t) => {
  let shake = 0; for (const c of T.crashes) if (t > c && t < c + 0.5) shake = 0.12 * Math.exp(-(t - c) * 7);
  const pull = ease((t - T.chord - 0.2) / 1.2);
  const sh = t > T.chord && t < T.chord + 0.6 ? 0.12 * Math.exp(-(t - T.chord) * 6) : 0; camera.position.set(-0.6 + Math.sin(t * 0.3) * 0.3 + sh * Math.sin(t * 90), lerp(1.8, 4.0, pull) + sh * Math.cos(t * 80), lerp(9.4, 13.0, pull)); camera.lookAt(-0.6, lerp(3.4, 3.0, pull), 0);
  keys.forEach((kk) => { kk.m.material.emissive.set("#000000"); kk.m.material.emissiveIntensity = 0; kk.m.position.y = kk.b ? 0.12 : 0; });
  bars.forEach(({ n, k, mesh, len }) => {
    const y = HIT + (n.t - t) * SPEED; const vis = y < 9 && y + len > HIT - 0.01 && t < n.t + n.d + 0.05; mesh.visible = vis;
    if (vis) { const bottom = Math.max(HIT, y); const top = y + len; const L = Math.max(0.01, top - bottom); mesh.scale.y = L / len; mesh.position.y = bottom + L / 2; }
    if (t >= n.t && t < n.t + Math.max(0.12, n.d)) { k.m.material.emissive.set(COL[n.h]); k.m.material.emissiveIntensity = 0.9; k.m.position.y = (k.b ? 0.12 : 0) - 0.05; }
  });
  let gi = 0; for (const { n, k } of bars) { const a = t - n.t; if (a >= 0 && a < 0.35 && gi < glows.length) { const g = glows[gi++]; g.visible = true; g.position.set(k.X, 0.35, 0.3); g.material.color.set(COL[n.h]); g.scale.setScalar(1.4 * (1 - a / 0.35) + 0.2); g.material.opacity = 1 - a / 0.35; } }
  for (let i = gi; i < glows.length; i++) glows[i].visible = false;
  motes.forEach((m) => { const u = m.userData; m.position.set(u.x + 0.3 * Math.sin(t * 0.5 + u.z), ((u.y + t * u.sp) % 10), u.z); m.scale.setScalar(u.s); });
  nts.forEach((nn) => (nn.visible = false));
  renderer.render(scene, camera); ui(t);
};
window.__ready = (async () => { window.render(0.5); return true; })();
