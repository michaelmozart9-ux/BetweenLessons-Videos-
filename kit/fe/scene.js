// Falling-notes keyboard engine. window.render(t) must be a pure function of t (no clocks, no Math.random).
import * as THREE from "three";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
await Promise.all(["900 80px Inter", "800 40px Inter", "700 30px Inter", "700 30px Cormorant"].map((f) => document.fonts.load(f)));
const T = window.__TIMING__, UI = T.ui, NOTES = T.notes, SEC = Object.fromEntries(T.secs.map((s) => [s.id, s]));
const $ = (id) => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, k) => a + (b - a) * k, ease = (k) => 1 - Math.pow(1 - clamp(k), 3);
const easeIO = (k) => { k = clamp(k); return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
const v3 = (x, y, z) => new THREE.Vector3(x, y, z);
let seed = 5; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
const CHORD = UI.chord, URL = UI.url, DUR = T.duration, IDS = ["a", "b", "c", "d"];
const secAt = (t) => (t < SEC.b.start ? "a" : t < SEC.c.start ? "b" : t < SEC.d.start ? "c" : "d");

// ---------- renderer / scene
const renderer = new THREE.WebGLRenderer({ canvas: $("gl"), antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(1080, 1920, false);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.5; renderer.outputColorSpace = THREE.SRGBColorSpace; renderer.localClippingEnabled = true;
const scene = new THREE.Scene(); scene.background = new THREE.Color("#22170F"); scene.fog = new THREE.FogExp2("#22170F", 0.018);
const camera = new THREE.PerspectiveCamera(45, 1080 / 1920, 0.05, 120);
scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture; scene.environmentIntensity = 0.5;
scene.add(new THREE.AmbientLight("#FFE9C9", 0.9));
const keyL = new THREE.DirectionalLight("#FFE2B0", 2.4); keyL.position.set(-3, 9, 8); scene.add(keyL);
const rimL = new THREE.DirectionalLight("#E0A84B", 1.4); rimL.position.set(4, 4, -6); scene.add(rimL);
const glowL = new THREE.PointLight("#E0A84B", 0, 6, 1.5); glowL.position.set(0, 0.8, 0.6); scene.add(glowL);

// ---------- keyboard: 29 white keys, C2..C6 (MIDI 36..84)
const NW = 29, KW = 0.235, KL = 1.5, X0 = -((NW - 1) * KW) / 2, HIT = 0.16, NZ = -0.86, V = 5.2;
const DEG = { 0: 0, 2: 1, 4: 2, 5: 3, 7: 4, 9: 5, 11: 6 };
const isWhite = (m) => DEG[(m - 36) % 12] !== undefined;
const wIdx = (m) => Math.floor((m - 36) / 12) * 7 + DEG[(m - 36) % 12];
const laneX = (m) => (isWhite(m) ? X0 + wIdx(m) * KW : X0 + wIdx(m - 1) * KW + KW / 2);
const keys = {};
for (let m = 36; m <= 84; m++) {
  const w = isWhite(m), mat = new THREE.MeshStandardMaterial({ color: w ? "#F1E9D6" : "#15100C", roughness: w ? 0.28 : 0.22, metalness: w ? 0 : 0.15, emissive: "#E0A84B", emissiveIntensity: 0 });
  const k = new THREE.Mesh(new THREE.BoxGeometry(w ? KW - 0.014 : 0.135, 0.12, w ? KL : 0.95), mat); k.position.set(laneX(m), w ? 0.06 : 0.17, w ? 0 : -0.275); scene.add(k); keys[m] = { k, y0: k.position.y };
}
const W = NW * KW + 0.6;
const body = new THREE.Mesh(new THREE.BoxGeometry(W, 0.5, 2.4), new THREE.MeshStandardMaterial({ color: "#241C15", roughness: 0.45, metalness: 0.2 })); body.position.set(0, -0.25, -0.3); scene.add(body);
const hitM = new THREE.MeshStandardMaterial({ color: "#E0A84B", emissive: "#F2B84B", emissiveIntensity: 1, metalness: 0.5, roughness: 0.3 });
const hitLine = new THREE.Mesh(new THREE.BoxGeometry(W - 0.2, 0.035, 0.035), hitM); hitLine.position.set(0, HIT, NZ + 0.07); scene.add(hitLine);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: "#0B0907", roughness: 0.95 })); floor.rotation.x = -Math.PI / 2; floor.position.y = -0.5; scene.add(floor);
{ // runway backdrop with octave guide lines
  const c = document.createElement("canvas"); c.width = 1024; c.height = 2048; const g = c.getContext("2d");
  const gr = g.createLinearGradient(0, 0, 0, 2048); gr.addColorStop(0, "rgba(30,24,18,0)"); gr.addColorStop(0.5, "rgba(30,24,18,.75)"); gr.addColorStop(1, "rgba(36,28,20,1)"); g.fillStyle = gr; g.fillRect(0, 0, 1024, 2048);
  for (let m = 36; m <= 84; m += 12) { const x = ((laneX(m) - KW / 2 + W / 2) / W) * 1024; const lg = g.createLinearGradient(0, 0, 0, 2048); lg.addColorStop(0, "rgba(224,168,75,0)"); lg.addColorStop(1, "rgba(224,168,75,.22)"); g.fillStyle = lg; g.fillRect(x - 1.5, 0, 3, 2048); }
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace;
  const p = new THREE.Mesh(new THREE.PlaneGeometry(W, 14), new THREE.MeshBasicMaterial({ map: tx, transparent: true, depthWrite: false })); p.position.set(0, 7, NZ - 0.25); scene.add(p);
}
// ---------- notes (R gold, L violet, X red = wrong note)
const COL = { R: new THREE.Color("#F2B84B"), L: new THREE.Color("#A99BFF"), X: new THREE.Color("#FF3B3B") };
const clip = new THREE.Plane(new THREE.Vector3(0, 1, 0), -HIT), geoCache = {};
const noteObjs = NOTES.map((n) => {
  const w = isWhite(n.m) ? 0.2 : 0.13, len = Math.max(0.12, n.d * V - 0.04), key = `${w}|${len.toFixed(3)}`;
  geoCache[key] = geoCache[key] || new RoundedBoxGeometry(w, len, 0.12, 2, Math.min(0.045, len / 2 - 0.005));
  const mesh = new THREE.Mesh(geoCache[key], new THREE.MeshStandardMaterial({ color: COL[n.h], emissive: COL[n.h], emissiveIntensity: 0.45, roughness: 0.35, clippingPlanes: [clip] }));
  mesh.visible = false; scene.add(mesh); return { n, mesh, len, x: laneX(n.m), z: NZ + (isWhite(n.m) ? 0 : 0.04) };
});
const active = (n, t) => { const s = SEC[n.sec]; return s && t >= s.start && t < s.end; };
// ---------- particles
const dotTex = (() => { const c = document.createElement("canvas"); c.width = c.height = 64; const g = c.getContext("2d"); const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, "rgba(255,255,255,1)"); gr.addColorStop(0.3, "rgba(255,255,255,.55)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c); })();
function pool(n, size) { const pos = new Float32Array(n * 3), col = new Float32Array(n * 3), geo = new THREE.BufferGeometry(); geo.setAttribute("position", new THREE.BufferAttribute(pos, 3)); geo.setAttribute("color", new THREE.BufferAttribute(col, 3)); const pts = new THREE.Points(geo, new THREE.PointsMaterial({ map: dotTex, size, vertexColors: true, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending })); pts.frustumCulled = false; scene.add(pts); return { pos, col, geo }; }
const SPK = 10, sparks = pool(NOTES.length * SPK, 0.09), glows = pool(NOTES.length, 1.25);
const sparkSeed = NOTES.map(() => Array.from({ length: SPK }, () => [(rnd() - 0.5) * 1.6, 1.4 + rnd() * 2.6, rnd() * 0.9, 0.35 + rnd() * 0.5]));
const NP = 260, dustP = new Float32Array(NP * 3), dustS = Array.from({ length: NP }, () => [(rnd() - 0.5) * 12, rnd() * 13, (rnd() - 0.5) * 10 - 1, 0.05 + rnd() * 0.12, rnd() * 6.28]);
const dustG = new THREE.BufferGeometry(); dustG.setAttribute("position", new THREE.BufferAttribute(dustP, 3));
scene.add(new THREE.Points(dustG, new THREE.PointsMaterial({ map: dotTex, size: 0.06, transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending, color: "#FFE2A8" })));
const halo = new THREE.Sprite(new THREE.SpriteMaterial({ map: dotTex, color: "#FFB54A", transparent: true, opacity: 0.55, depthWrite: false, blending: THREE.AdditiveBlending })); halo.scale.set(16, 12, 1); halo.position.set(0.4, 3.2, -4); scene.add(halo);
const SN = 420, snowP = new Float32Array(SN * 3), snowS = Array.from({ length: SN }, () => [(rnd() - 0.5) * 12, rnd() * 14, 0.5 + rnd() * 8, 0.35 + rnd() * 0.5, rnd() * 6.28]);
const snowG = new THREE.BufferGeometry(); snowG.setAttribute("position", new THREE.BufferAttribute(snowP, 3));
const snowPts = new THREE.Points(snowG, new THREE.PointsMaterial({ map: dotTex, size: 0.2, transparent: true, opacity: 0.95, depthWrite: false, color: "#FFFFFF", fog: false })); snowPts.frustumCulled = false; scene.add(snowPts);

// ---------- camera: hook close-up, gentle moves per section, push on Grade 8, pull back on the chord
function cam(t) {
  const CX = 0.45, id = secAt(t), S = SEC[id], k = clamp((t - S.start) / ((id === "d" ? CHORD : S.end) - S.start));
  let p = v3(CX, 5.0, 10.0), l = v3(CX, 2.3, -0.6);
  if (id === "a") { const e = easeIO(clamp(t / 2.4)); p = v3(CX + lerp(1.3, 0.3, e), lerp(3.3, 4.8, e), lerp(7.0, 9.6, e)); l = v3(CX + lerp(0.7, 0.1, e), lerp(1.7, 2.2, e), -0.6); }
  else if (id === "b") { p.x -= 0.7 * Math.sin(k * 2.0); p.z -= 0.7 * k; }
  else if (id === "c") { p.x += 0.7 * Math.sin(k * 2.2); p.z -= 1.1 * k; p.y -= 0.4 * k; }
  else { const kk = easeIO(k); p = v3(CX + 1.0 * Math.sin(kk * 3.3), lerp(4.3, 3.6, kk), lerp(8.8, 7.2, kk)); l = v3(CX + 0.3 * Math.sin(kk * 3.3), lerp(1.9, 1.6, kk), -0.6); const pb = easeIO((t - CHORD) / 1.6); p.lerp(v3(CX, 5.4, 10.8), pb); l.lerp(v3(CX, 2.3, -0.6), pb); }
  for (const [c, a0] of [[SEC.b.start, 0.05], [SEC.c.start, 0.06], [SEC.d.start, 0.08], [CHORD, 0.15]]) if (t > c && t < c + 0.6) { const a = a0 * Math.exp(-(t - c) * 8); p.x += a * Math.sin(t * 95); p.y += a * Math.cos(t * 81); }
  camera.position.copy(p); camera.lookAt(l);
}
// ---------- HTML overlay
const meter = [...document.querySelectorAll("#meter i")];
const rows = [...document.querySelectorAll("#reveal .row")];
function ui(t) {
  const endK = ease((t - CHORD - 0.08) / 0.18), id = secAt(t), S = SEC[id], k = t - S.start;
  const ti = $("title"); ti.style.opacity = (1 - endK).toFixed(3); ti.style.transform = `scale(${lerp(1.12, 1, ease(t / 0.35)).toFixed(3)})`;
  const bd = $("badge"); bd.style.opacity = (clamp(t / 0.12) * (1 - endK)).toFixed(3);
  const Lt = $("let"), up = id.toUpperCase(); if (Lt.textContent !== up) Lt.textContent = up;
  Lt.style.transform = `scale(${lerp(id === "d" ? 2.0 : 1.55, 1, ease(k / 0.28)).toFixed(3)})`; Lt.className = id === "d" ? "hot" : "";
  $("chip").style.transform = `scale(${(1 + 0.04 * Math.sin(t * 8)).toFixed(3)})`;
  const w = $("wait"); w.style.opacity = id === "d" ? 0 : clamp((k - 0.35) / 0.2).toFixed(3);
  rows.forEach((r, i) => { const rk = ease((t - CHORD - 0.25 - i * 0.3) / 0.15); r.style.opacity = rk.toFixed(3); r.style.transform = `scale(${lerp(1.35, 1, rk).toFixed(3)})`; });
  const ek = ease((t - CHORD - 1.55) / 0.25); $("endq").style.opacity = ek.toFixed(3); $("endq").style.transform = `scale(${lerp(0.85, 1, ek).toFixed(3)})`;
  const e2 = ease((t - CHORD - 1.95) / 0.3); $("end2").style.opacity = e2.toFixed(3); $("end2").style.transform = `translateY(${lerp(24, 0, e2).toFixed(1)}px)`;
  const uk = ease((t - URL) / 0.35), big = ease((t - CHORD - 1.95) / 0.3), lt = $("lt"); lt.style.opacity = uk.toFixed(3);
  lt.style.transform = `translateY(${lerp(50, 0, uk).toFixed(1)}px) scale(${(lerp(1, 1.1, big) * (t > URL + 0.4 ? 1 + 0.03 * Math.max(0, Math.sin((t - URL) * 4)) : 1)).toFixed(3)})`;
  let fl = 0.38 * Math.max(0, 1 - t / 0.25);
  for (const c of [SEC.b.start, SEC.c.start, SEC.d.start]) if (t >= c && t < c + 0.2) fl = Math.max(fl, 0.3 * (1 - (t - c) / 0.2));
  if (t >= CHORD && t < CHORD + 0.3) fl = Math.max(fl, 0.3 * (1 - (t - CHORD) / 0.3));
  if (t > DUR - 0.25) fl = Math.max(fl, 0.38 * (t - (DUR - 0.25)) / 0.25);
  $("flash").style.opacity = fl.toFixed(3); $("dim").style.opacity = ease((t - CHORD - 0.1) / 0.4).toFixed(3);
}
// ---------- per-frame
window.render = function (t) {
  cam(t);
  const keyLv = {}, keyCol = {}; let si = 0, gi = 0, best = 0, bestX = 0;
  for (let i = 0; i < noteObjs.length; i++) {
    const o = noteObjs[i], n = o.n, on = active(n, t), bottom = HIT + (n.t - t) * V;
    o.mesh.visible = on && bottom < 14 && bottom + o.len > HIT;
    if (o.mesh.visible) { o.mesh.position.set(o.x, bottom + o.len / 2, o.z); o.mesh.material.emissiveIntensity = t >= n.t && t < n.t + n.d ? 1.35 : 0.45; }
    const a = t - n.t;
    if (on && a >= 0) {
      const lv = a < n.d ? 1 : Math.exp(-(a - n.d) / 0.18);
      if (lv > (keyLv[n.m] || 0)) { keyLv[n.m] = lv; keyCol[n.m] = n.h; }
      if (lv > best) { best = lv; bestX = o.x; }
      const gl = lv * (a < 0.12 ? 1.5 - a * 4 : 1) * 0.85 * (0.6 + 0.4 * n.v);
      if (gl > 0.02) { glows.pos.set([o.x, HIT + 0.08, o.z + 0.12], gi * 3); const c = COL[n.h]; glows.col.set([c.r * gl, c.g * gl, c.b * gl], gi * 3); gi++; }
      if (a < 0.9) for (const [vx, vy, vz, life] of sparkSeed[i]) { if (a > life) continue; const f = (1 - a / life) * (0.5 + 0.5 * n.v), c = COL[n.h]; sparks.pos.set([o.x + vx * a, HIT + vy * a - 4.2 * a * a, o.z + 0.1 + vz * a], si * 3); sparks.col.set([c.r * f + 0.25 * f, c.g * f + 0.2 * f, c.b * f + 0.1 * f], si * 3); si++; }
    }
  }
  for (const [pl, cnt] of [[sparks, si], [glows, gi]]) { pl.geo.setDrawRange(0, cnt); pl.geo.attributes.position.needsUpdate = true; pl.geo.attributes.color.needsUpdate = true; }
  for (const m in keys) { const { k, y0 } = keys[m], lv = keyLv[m] || 0; k.material.emissive.copy(COL[keyCol[m] || "R"]); k.material.emissiveIntensity = 0.9 * lv; k.position.y = y0 - 0.04 * lv; }
  glowL.intensity = 10 * best; glowL.position.x = bestX; hitM.emissiveIntensity = 0.9 + 0.8 * best;
  for (let i = 0; i < NP; i++) { const [x0, y0, z0, sp, ph] = dustS[i]; dustP[i * 3] = x0 + 0.2 * Math.sin(t * 0.5 + ph); dustP[i * 3 + 1] = (y0 + sp * t) % 13; dustP[i * 3 + 2] = z0; }
  dustG.attributes.position.needsUpdate = true;
  for (let i = 0; i < SN; i++) { const [x0, y0, z0, sp, ph] = snowS[i]; snowP[i * 3] = x0 + 0.4 * Math.sin(t * 0.7 + ph); snowP[i * 3 + 1] = 14 - ((14 - y0 + sp * t) % 14); snowP[i * 3 + 2] = z0 - 4; }
  snowG.attributes.position.needsUpdate = true; halo.material.opacity = 0.45 + 0.35 * best;
  renderer.render(scene, camera); ui(t);
};
window.__ready = (async () => { $("piece").textContent = UI.piece; rows.forEach((r, i) => { r.innerHTML = `${"ABCD"[i]} <span class="eq">=</span> <b>Grade ${UI.grades[i]}</b>${i === 3 ? " 🔥" : ""}`; }); window.render(0); return true; })();
