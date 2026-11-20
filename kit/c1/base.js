// Cartoon 3D explainer. window.render(t) is a pure function of t.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
await Promise.all(["900 80px Inter", "800 40px Inter", "700 30px Inter"].map((f) => document.fonts.load(f)));
const T = window.__TIMING__, B = T.beats, DUR = T.duration;
const $ = (id) => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), lerp = (a, b, k) => a + (b - a) * k, ease = (k) => 1 - Math.pow(1 - clamp(k), 3);
const easeIO = (k) => { k = clamp(k); return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; };
const back = (k) => { k = clamp(k); const c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
const pop = (t, t0, d = 0.35) => (t < t0 ? 0 : back((t - t0) / d));
const v3 = (x, y, z) => new THREE.Vector3(x, y, z);
let seed = 7; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
// ---------- renderer
const renderer = new THREE.WebGLRenderer({ canvas: $("gl"), antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(720, 1280, false);
renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.15; renderer.outputColorSpace = THREE.SRGBColorSpace;
const scene = new THREE.Scene(); scene.background = new THREE.Color("#F2E6D4");
const camera = new THREE.PerspectiveCamera(46, 1080 / 1920, 0.05, 200);
scene.add(new THREE.HemisphereLight("#FFF6E8", "#B89A7A", 1.6));
const sun = new THREE.DirectionalLight("#FFFFFF", 2.2); sun.position.set(-6, 12, 9); scene.add(sun);
const fill = new THREE.DirectionalLight("#CFE3FF", 0.7); fill.position.set(8, 5, -4); scene.add(fill);
const M = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.75, metalness: 0, flatShading: true, ...o });
const box = (w, h, d, c, r = 0.06) => new THREE.Mesh(r ? new RoundedBoxGeometry(w, h, d, 2, r) : new THREE.BoxGeometry(w, h, d), typeof c === "string" ? M(c) : c);
const add = (o, x, y, z, parent = scene) => { o.position.set(x, y, z); parent.add(o); return o; };
function textTex(txt, { w = 256, h = 128, font = "800 64px Inter", fg = "#3B2F25", bg = null } = {}) {
  const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d");
  if (bg) { g.fillStyle = bg; g.fillRect(0, 0, w, h); }
  g.fillStyle = fg; g.font = font; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(txt, w / 2, h / 2 + 4);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
const label = (txt, w, h, opts) => new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: textTex(txt, opts), transparent: true, depthWrite: false }));
const shadow = (r) => { const m = new THREE.Mesh(new THREE.CircleGeometry(r, 24), new THREE.MeshBasicMaterial({ color: "#000", transparent: true, opacity: 0.16, depthWrite: false })); m.rotation.x = -Math.PI / 2; return m; };

// ---------- character
function person(shirt = "#3E8E6E", skin = "#E0A47A", hair = "#2B211B", s = 1) {
  const g = new THREE.Group();
  const legs = add(box(0.62, 0.7, 0.36, "#3B4A6B"), 0, 0.35, 0, g);
  const body = add(box(0.8, 0.85, 0.5, shirt), 0, 1.12, 0, g);
  const head = add(box(0.82, 0.78, 0.74, skin, 0.1), 0, 1.98, 0, g);
  add(box(0.88, 0.26, 0.8, hair, 0.08), 0, 0.32, -0.02, head);
  for (const x of [-0.17, 0.17]) add(box(0.09, 0.13, 0.04, "#1C1410", 0.02), x, 0.02, 0.38, head);
  const mouth = add(box(0.22, 0.05, 0.04, "#7A3B2A", 0.01), 0, -0.18, 0.38, head);
  const aL = add(box(0.22, 0.72, 0.26, shirt), -0.52, 1.1, 0, g), aR = add(box(0.22, 0.72, 0.26, shirt), 0.52, 1.1, 0, g);
  add(shadow(0.6), 0, 0.01, 0, g); g.scale.setScalar(s);
  g.userData = { head, body, aL, aR, mouth }; return g;
}

function phoneTex() {
  const c = document.createElement("canvas"); c.width = 540; c.height = 1080; const g = c.getContext("2d");
  g.fillStyle = "#14110E"; g.fillRect(0, 0, 540, 1080);
  g.fillStyle = "#E0A84B"; g.font = "800 34px Inter"; g.textAlign = "center"; g.fillText("Between Lessons", 270, 90);
  g.fillStyle = "#F5EEDC"; g.font = "900 52px Inter"; g.fillText("Your 6-week plan", 270, 170);
  const days = ["M", "T", "W", "T", "F", "S", "S"], on = [1, 1, 1, 1, 1, 1, 0];
  days.forEach((d, i) => { const x = 60 + i * 70; g.fillStyle = on[i] ? "#3CB8A3" : "#2B2520"; g.beginPath(); g.arc(x, 260, 28, 0, 7); g.fill(); g.fillStyle = "#FFF"; g.font = "800 28px Inter"; g.fillText(d, x, 270); });
  g.fillStyle = "#B9A78E"; g.font = "700 26px Inter"; g.fillText("you pick the days", 270, 330);
  const rows = [["Warm-up", "#E0A84B"], ["Main work", "#3CB8A3"], ["Run-through", "#F08A4B"]];
  g.fillStyle = "#F5EEDC"; g.font = "800 34px Inter"; g.textAlign = "left"; g.fillText("Day 1 · 20 min", 50, 420);
  rows.forEach(([r, col], i) => { const y = 460 + i * 120; g.fillStyle = "#221C17"; g.beginPath(); g.roundRect(40, y, 460, 96, 22); g.fill(); g.fillStyle = col; g.fillRect(40, y, 12, 96); g.fillStyle = "#F5EEDC"; g.font = "800 36px Inter"; g.fillText(r, 76, y + 60); });
  g.fillStyle = "#E0A84B"; g.font = "900 40px Inter"; g.textAlign = "center"; g.fillText("Tempo target: 40%", 270, 880);
  g.fillStyle = "#B9A78E"; g.font = "700 26px Inter"; g.fillText("one milestone every week", 270, 940);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
// ---------- world
add(new THREE.Mesh(new THREE.PlaneGeometry(400, 80), M("#E3C9A6")), 60, 0, 0).rotation.x = -Math.PI / 2;
for (const [x, c] of [[0, "#CFE0F5"], [20, "#D5EDD8"], [120, "#DCE8E0"]]) add(box(14, 10, 0.3, c, 0), x, 5, -4);
function piano(x, z) {
  const g = new THREE.Group(); add(box(2.6, 1.6, 0.7, "#3A2418", 0.05), 0, 0.8, 0, g); add(box(2.7, 0.08, 0.8, "#2A1A12", 0.02), 0, 1.62, 0, g);
  add(box(2.6, 0.14, 0.55, "#2A1A12", 0.02), 0, 0.86, 0.6, g); const keys = [];
  for (let i = 0; i < 15; i++) keys.push({ m: add(box(0.155, 0.06, 0.42, "#F7F3EA", 0.015), -1.12 + i * 0.16, 0.95, 0.66, g), black: false });
  for (let i = 0; i < 14; i++) if (![2, 6, 9, 13].includes(i)) keys.push({ m: add(box(0.09, 0.07, 0.26, "#151110", 0.01), -1.04 + i * 0.16, 1.0, 0.56, g), black: true });
  for (const xx of [-1.2, 1.2]) add(box(0.12, 0.86, 0.12, "#2A1A12", 0), xx, 0.43, 0.75, g);
  add(box(1.4, 0.5, 0.5, "#5A3A28", 0.05), 0, 0.25, 1.55, g); add(shadow(1.8), 0, 0.01, 0.4, g); add(g, x, 0, z); return keys;
}
const keysMax = piano(0, -1.2), keysZoe = piano(20, -1.2);
const maxK = add(person("#E2533A", "#E0A47A", "#3A2A1C"), 0, 0.25, 0.4); maxK.rotation.y = Math.PI;
const zoeK = add(person("#3CB8A3", "#C68A5E", "#1C1410"), 20, 0.25, 0.4); zoeK.rotation.y = Math.PI;
add(label("ZOE", 1.6, 0.6, { w: 256, h: 96, font: "900 80px Inter", fg: "#2F9C8A" }), 17.8, 3.3, -3.7);
const xs = Array.from({ length: 6 }, () => add(label("❌", 0.7, 0.7, { w: 128, h: 128, font: "100px sans-serif" }), 0, -5, 0));
const turtle = add(label("🐢", 0.9, 0.9, { w: 128, h: 128, font: "100px sans-serif" }), 20.9, 2.9, 0.2);
const ticks = Array.from({ length: 3 }, (_, i) => add(label("✅", 0.6, 0.6, { w: 128, h: 128, font: "100px sans-serif" }), 19 + i * 0.7, 3.3, 0));
const sweat = add(new THREE.Mesh(new THREE.SphereGeometry(0.08, 10, 8), M("#7EC8FF", { emissive: "#3AA0FF", emissiveIntensity: 0.4 })), 0, -5, 0);
// ---------- stage at x=40
add(box(12, 0.6, 5, "#7A4A2C", 0.05), 40, 0.3, -1.4); add(box(14, 9, 0.3, "#7A1E2A", 0), 40, 4.5, -4);
for (let i = 0; i < 7; i++) add(box(0.5, 9, 0.5, "#8E2433", 0.2), 34 + i * 2, 4.5, -3.7);
const stageKeys = piano(40, -1.8); scene.children[scene.children.length - 1].position.y = 0.6;
const maxS = add(person("#E2533A", "#E0A47A", "#3A2A1C"), 40, 0.85, 0.0); maxS.rotation.y = Math.PI;
const zoeS = add(person("#3CB8A3", "#C68A5E", "#1C1410"), 40, 0.85, 0.0); zoeS.rotation.y = Math.PI;
const spotMat = new THREE.MeshBasicMaterial({ color: "#FFF1C4", transparent: true, opacity: 0.18, depthWrite: false, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
const spot = add(new THREE.Mesh(new THREE.ConeGeometry(2.2, 7, 32, 1, true), spotMat), 40, 4.1, -0.9);
const crowd = []; let ci = 0;
for (let r = 0; r < 4; r++) for (let c = 0; c < 9; c++, ci++) {
  const cols = ["#E2733A", "#3E8E6E", "#4E6EC4", "#C4508A", "#D9A43B", "#7A5CC4"];
  const p = add(person(cols[ci % 6], ["#E0A47A", "#C68A5E", "#8D5A3B", "#F1C9A5"][ci % 4], "#2B211B", 0.62), 40 - 4.4 + c * 1.1 + (r % 2) * 0.5, 0, 2.4 + r * 1.2); p.rotation.y = Math.PI; crowd.push(p);
}
const confetti = Array.from({ length: 60 }, (_, i) => { const m = add(box(0.12, 0.22, 0.02, ["#F08A4B", "#3CB8A3", "#E0A84B", "#C4508A", "#4E6EC4"][i % 5], 0), 40, -5, 0); m.userData = { x: (rnd() - 0.5) * 9, z: (rnd() - 0.5) * 4, y: 6 + rnd() * 4, sp: 1 + rnd() * 1.5, r: rnd() * 6 }; return m; });
// ---------- phone at x=120
const phone = new THREE.Group(); add(box(2.3, 4.6, 0.26, "#1E1B19", 0.22), 0, 0, 0, phone);
add(new THREE.Mesh(new THREE.PlaneGeometry(2.1, 4.2), new THREE.MeshBasicMaterial({ map: phoneTex(), toneMapped: false })), 0, 0, 0.14, phone);
add(phone, 120, 2.9, 0); phone.scale.setScalar(0.8);

