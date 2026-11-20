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
const bars = T.notes.map((n) => { const k = keyOf(n.m), len = Math.max(0.15, n.d * SPEED); const mesh = new THREE.Mesh(new RoundedBoxGeometry(k.b ? 0.18 : 0.28, len, 0.18, 2, 0.06), new THREE.MeshStandardMaterial({ color: COL[n.h], emissive: COL[n.h], emissiveIntensity: 0.6 }));
  mesh.position.set(k.X, -10, k.b ? -0.4 : 0.15); scene.add(mesh); return { n, k, mesh, len }; });
const CAP = [[0, "You practise every day… so why aren't you getting <span class='hl'>better?</span> 😩"], [B.fail2, "No plan. Same speed. Same mistakes."],
  [B.plan, "Between Lessons gives you a <span class='hl'>day-by-day plan</span> for YOUR piece"], [B.rate, "It speeds up only when <span class='hl'>you're ready</span>"],
  [B.full, "Then… full speed 🔥"], [T.chord, "That could be <span class='hl'>you</span> 😳"], [B.offer, "Nothing to lose. Try Day 1 <span class='hl'>free</span> 👇"]];
let lastCap = -1, lastS = "";
const tempoAt = (t) => t < B.plan ? ["100% ❌", "bad"] : t < 10.3 ? ["40%", ""] : t < 12.1 ? ["60%", ""] : t < B.full ? ["80%", ""] : ["100% ✅", "good"];
function ui(t) {
  let ci = 0; CAP.forEach(([ct], i) => { if (t >= ct) ci = i; }); if (ci !== lastCap) { $("cap").innerHTML = CAP[ci][1]; lastCap = ci; }
  $("cap").style.transform = `scale(${lerp(1.12, 1, ease((t - CAP[ci][0]) / 0.15)).toFixed(3)})`;
  $("cap").style.top = t >= T.chord && t < B.offer ? "760px" : "1420px"; $("cap").style.fontSize = t >= T.chord && t < B.offer ? "100px" : "66px";
  $("chip").innerHTML = t < B.plan ? "<b style='color:#FF8A7A'>STUCK</b> ON A PIECE? 😩" : "<b>BETWEEN LESSONS</b>";
  const [tv, tc] = tempoAt(t), te = $("tempo"); if (te.textContent !== tv) { te.textContent = tv; te.className = tc; } te.style.opacity = t >= B.offer ? 0 : 1;
  const lastChange = [0, B.plan, 10.3, 12.1, B.full].filter((x) => x <= t).pop(); te.style.transform = `scale(${lerp(1.35, 1, ease((t - lastChange) / 0.2)).toFixed(3)})`;
  const phase = t < B.plan ? 0 : t < B.full ? 1 : t < B.offer ? 2 : 3;
  let y = 900, op = 0;
  if (phase === 1) { y = lerp(900, 0, ease((t - B.plan) / 0.45)); op = 1; }
  if (phase === 2) { const o = ease((t - B.full) / 0.4); y = 900 * o; op = 1 - o; }
  if (phase === 3) { y = lerp(900, 0, ease((t - B.offer) / 0.45)); op = 1; }
  $("phoneWrap").style.opacity = op.toFixed(3); $("phoneWrap").style.transform = `translateY(${y.toFixed(0)}px)`;
  const s = t < B.rate ? "s3b" : t < B.offer ? "s4" : "s6"; if (s !== lastS) { ["s3b", "s4", "s6"].forEach((id) => ($(id).style.opacity = 0)); lastS = s; }
  const sk = ease((t - (s === "s3b" ? B.plan : s === "s4" ? B.rate : B.offer)) / 0.3); $(s).style.opacity = 1; $(s).style.transform = `translateX(${lerp(80, 0, sk).toFixed(1)}px)`;
  [...document.querySelectorAll("#s3b .sess")].forEach((x, i) => { const a = t - (B.plan + 0.6 + i * 0.25); x.style.opacity = a > 0 ? 1 : 0; x.style.transform = `translateX(${lerp(60, 0, ease(a / 0.2)).toFixed(0)}px)`; });
  document.querySelector("#s3b .tempo").style.opacity = t > B.plan + 1.4 ? 1 : 0;
  $("be").className = t >= T.tap ? "btn hit" : "btn"; const tk = ease((t - T.tap - 0.3) / 0.25); $("toast").style.opacity = tk; $("toast").style.transform = `scale(${lerp(0.8, 1, tk).toFixed(3)})`;
  [...document.querySelectorAll("#s6 .check")].forEach((x, i) => { const a = t - (B.offer + 0.5 + i * 0.4); x.style.opacity = a > 0 ? 1 : 0; x.style.transform = `scale(${a > 0 ? back(a / 0.25).toFixed(3) : 1})`; });
  const ch = document.querySelector("#s6 .cheap"), ca = t - (B.offer + 1.7); ch.style.opacity = ca > 0 ? 1 : 0; ch.style.transform = `scale(${ca > 0 ? back(ca / 0.3).toFixed(3) : 1})`;
  const f = $("finger"), a = t - T.tap; if (a > -0.35 && a < 0.35) { const r = $("be").getBoundingClientRect(), sc = $("screen").getBoundingClientRect(); f.style.left = `${r.left - sc.left + r.width * 0.7}px`; f.style.top = `${r.top - sc.top + r.height * 0.6}px`; f.style.opacity = (a < 0 ? 1 + a / 0.35 : 1 - a / 0.35).toFixed(2); } else f.style.opacity = 0;
  const ctk = t - B.offer - 2.3; $("cta").style.opacity = ctk > 0 ? 1 : 0; $("cta").style.transform = `translateX(-50%) scale(${(ctk > 0 ? back(ctk / 0.3) * (1 + 0.04 * Math.sin(t * 6)) : 1).toFixed(3)})`;
  let fl = 0.3 * Math.max(0, 1 - t / 0.2); for (const b of [B.plan, B.rate, B.full, T.chord, B.offer]) if (t >= b && t < b + 0.15) fl = Math.max(fl, 0.4 * (1 - (t - b) / 0.15));
  if (t >= T.chord && t < T.chord + 0.35) fl = Math.max(fl, 0.6 * (1 - (t - T.chord) / 0.35));
  if (t > DUR - 0.3) fl = Math.max(fl, (t - (DUR - 0.3)) / 0.3); $("flash").style.opacity = fl.toFixed(3);
  let red = 0; for (const c of T.crashes) if (t > c && t < c + 0.4) red = 0.4 * (1 - (t - c) / 0.4); $("red").style.opacity = red.toFixed(3);
}
window.render = (t) => {
  let shake = 0; for (const c of T.crashes) if (t > c && t < c + 0.5) shake = 0.12 * Math.exp(-(t - c) * 7);
  const pull = (t >= B.plan && t < B.full + 0.3) || t >= B.offer ? 1 : 0;
  camera.position.set(1.8 + Math.sin(t * 0.3) * 0.3 + shake * Math.sin(t * 90), lerp(2.0, 2.8, pull) + shake * Math.cos(t * 80), lerp(12.0, 13.0, pull)); camera.lookAt(1.8, lerp(3.9, 4.1, pull), 0);
  keys.forEach((kk) => { kk.m.material.emissive.set("#000000"); kk.m.material.emissiveIntensity = 0; kk.m.position.y = kk.b ? 0.12 : 0; });
  bars.forEach(({ n, k, mesh, len }) => {
    const y = HIT + (n.t - t) * SPEED; const vis = y < 9 && y + len > HIT - 0.01 && t < n.t + n.d + 0.05; mesh.visible = vis;
    if (vis) { const bottom = Math.max(HIT, y); const top = y + len; const L = Math.max(0.01, top - bottom); mesh.scale.y = L / len; mesh.position.y = bottom + L / 2; }
    if (t >= n.t && t < n.t + Math.max(0.12, n.d)) { k.m.material.emissive.set(COL[n.h]); k.m.material.emissiveIntensity = 0.9; k.m.position.y = (k.b ? 0.12 : 0) - 0.05; }
  });
  motes.forEach((m) => { const u = m.userData; m.position.set(u.x + 0.3 * Math.sin(t * 0.5 + u.z), ((u.y + t * u.sp) % 10), u.z); m.scale.setScalar(u.s); });
  nts.forEach((nn) => (nn.visible = false));
  renderer.render(scene, camera); ui(t);
};
window.__ready = (async () => { window.render(0.5); return true; })();
