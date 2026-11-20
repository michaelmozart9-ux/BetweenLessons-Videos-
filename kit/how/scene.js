// Product ad: animated phone UI (HTML) over a 3D piano background. window.render(t) is a pure function of t.
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
await Promise.all(["900 80px Inter", "800 40px Inter", "700 30px Inter"].map((f) => document.fonts.load(f)));
const T = window.__TIMING__, B = T.beats, TP = T.taps, DUR = T.duration, $ = (id) => document.getElementById(id);
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
// ---------- screens
const SCR = ["s0", "s1", "s2", "s3", "s3b", "s4", "s5", "s6"];
const screenAt = (t) => t < B.s1 ? "s0" : t < B.s2 ? "s1" : t < B.s3 ? "s2" : t < B.card ? "s3" : t < B.s4 ? "s3b" : t < B.s5 ? "s4" : t < B.s6 ? "s5" : "s6";
const startOf = { s0: 0, s1: B.s1, s2: B.s2, s3: B.s3, s3b: B.card, s4: B.s4, s5: B.s5, s6: B.s6 };
$("grades").innerHTML = [1, 2, 3, 4, 5, 6, 7, 8].map((g) => `<div class="pill" id="g${g}">${g}</div>`).join("");
$("days").innerHTML = ["M", "T", "W", "T", "F", "S", "S"].map((d, i) => `<div class="day" id="d${i}">${d}</div>`).join("");
$("lens").innerHTML = [20, 30, 45, 60].map((m) => `<div class="pill" id="l${m}">${m} min</div>`).join("");
const WK = [[40, 50], [45, 60], [50, 70], [40, 65], [40, 70], [70, 80]];
$("weeks").innerHTML = WK.map(([a, b], i) => `<div class="wk"><span>W${i + 1}</span><div class="bar" id="w${i}" style="width:0px"></div><span class="rng">${a}–${b}%${i === 3 ? " · new section" : ""}</span></div>`).join("");
const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]; $("cal").innerHTML = DAYS.map((d, i) => `<div id="c${i}">${d}<small>${i === 1 ? "✕" : i === 2 ? "▶" : "✓"}</small></div>`).join("");
const CHIP = { s0: "<b>STUCK</b> ON A PIECE? 😩", s1: "STEP 1 · <b>YOUR PIECE</b>", s2: "STEP 2 · <b>YOUR SCHEDULE</b>", s3: "STEP 3 · <b>YOUR 6-WEEK PLAN</b>", s3b: "STEP 3 · <b>EVERY SESSION</b>", s4: "STEP 4 · <b>RATE IT</b>", s5: "<b>NO GUILT</b> 🙌", s6: "<b>TRY IT FREE</b>" };
const CAP = [[0, "Stuck on a piece? 😩"], [1.25, "Here's how <span class='hl'>Between Lessons</span> works 👇"], [B.s1, "Pick your piece and your grade"], [B.s2, "Pick your days and session length"],
  [B.s3, "Get a <span class='hl'>6-week plan</span>, day by day"], [B.card, "Warm-up, main work, run-through + a <span class='hl'>tempo target</span>"],
  [B.s4, "Too easy? Next session is <span class='hl'>5% faster</span>"], [B.s5, "Missed a day? It just waits. One milestone every week 🏁"], [B.s6, "Try Day 1 <span class='hl'>free</span> 👇"]];
let lastS = "", lastChip = "", lastCap = -1;
function finger(t, t0, el) { const f = $("finger"), a = t - t0; if (a < -0.35 || a > 0.35 || !el) return false; const r = el.getBoundingClientRect(), s = $("screen").getBoundingClientRect(); f.style.left = `${r.left - s.left + r.width * 0.7}px`; f.style.top = `${r.top - s.top + r.height * 0.6}px`; f.style.opacity = (a < 0 ? 1 + a / 0.35 : 1 - a / 0.35).toFixed(2); f.style.transform = `scale(${a > 0 ? lerp(0.8, 1.3, a / 0.35) : 1})`; return true; }
function ui(t) {
  const s = screenAt(t); if (s !== lastS) { SCR.forEach((id) => ($(id).style.opacity = 0)); lastS = s; }
  const k = ease((t - startOf[s]) / 0.3), el = $(s); el.style.opacity = 1; el.style.transform = `translateX(${lerp(80, 0, k).toFixed(1)}px)`;
  const ck = s === "s3b" ? "s3b" : s; if (ck !== lastChip) { $("chip").innerHTML = CHIP[ck]; lastChip = ck; }
  $("chip").style.transform = `translateX(-50%) scale(${lerp(0.75, 1, ease((t - startOf[s]) / 0.25)).toFixed(3)})`;
  let ci = 0; CAP.forEach(([ct], i) => { if (t >= ct) ci = i; }); if (ci !== lastCap) { $("cap").innerHTML = CAP[ci][1]; lastCap = ci; }
  $("cap").style.transform = `scale(${lerp(1.12, 1, ease((t - CAP[ci][0]) / 0.15)).toFixed(3)})`;
  // s0: red crosses
  [...document.querySelectorAll("#s0 .x")].forEach((x, i) => { const a = t - (0.35 + i * 0.4); x.style.opacity = a > 0 ? 1 : 0; x.style.transform = `scale(${lerp(1.4, 1, ease(a / 0.15)).toFixed(3)})`; });
  // s1: typing + select piece + grade
  const typed = "Clair de Lune".slice(0, Math.max(0, Math.floor((t - B.s1 - 0.3) / 0.06))); $("q").innerHTML = `🔍 ${typed}<span class="cur"></span>`;
  $("pc").className = t >= TP.piece ? "card sel" : "card"; $("pc").style.opacity = t > B.s1 + 0.9 ? 1 : 0;
  for (let g = 1; g <= 8; g++) $(`g${g}`).className = g === 6 && t >= TP.grade ? "pill on" : "pill";
  // s2: days + length
  TP.days.forEach((dt, i) => { const d = $(`d${i}`); d.className = t >= dt ? "day on" : "day"; d.style.transform = `scale(${t >= dt ? lerp(1.3, 1, ease((t - dt) / 0.15)) : 1})`; });
  [20, 30, 45, 60].forEach((m) => ($(`l${m}`).className = m === 30 && t >= TP.len ? "pill on" : "pill"));
  // s3: week bars grow
  WK.forEach(([a, b], i) => { const kk = ease((t - B.s3 - 0.3 - i * 0.2) / 0.3); $(`w${i}`).style.width = `${(b * 2.6 * kk).toFixed(0)}px`; });
  // s3b: session rows pop
  [...document.querySelectorAll("#s3b .sess")].forEach((x, i) => { const a = t - (B.card + 0.2 + i * 0.25); x.style.opacity = a > 0 ? 1 : 0; x.style.transform = `translateX(${lerp(60, 0, ease(a / 0.2)).toFixed(0)}px)`; });
  document.querySelector("#s3b .tempo").style.opacity = t > B.card + 1.0 ? 1 : 0;
  // s4: tap too easy -> toast + tempo counter
  $("be").className = t >= TP.easy ? "btn hit" : "btn"; const tk = ease((t - TP.easy - 0.3) / 0.25); $("toast").style.opacity = tk; $("toast").style.transform = `scale(${lerp(0.8, 1, tk).toFixed(3)})`;
  $("tn").textContent = `${Math.round(lerp(40, 45, ease((t - TP.easy - 0.6) / 0.6)))}% tempo`;
  // s5: calendar skip shifts + milestone
  for (let i = 0; i < 5; i++) { const c = $(`c${i}`); c.className = i === 1 ? "skip" : i === 2 && t > B.s5 + 0.8 ? "next" : ""; }
  const bk = t - B.s5 - 1.6; $("badge").style.opacity = bk > 0 ? 1 : 0; $("badge").style.transform = `scale(${bk > 0 ? back(bk / 0.3).toFixed(3) : 1})`;
  // s6: checks
  [...document.querySelectorAll("#s6 .check")].forEach((x, i) => { const a = t - (B.s6 + 0.5 + i * 0.35); x.style.opacity = a > 0 ? 1 : 0; x.style.transform = `scale(${a > 0 ? back(a / 0.25).toFixed(3) : 1})`; });
  const ctk = t - B.s6 - 1.6; $("cta").style.opacity = ctk > 0 ? 1 : 0; $("cta").style.transform = `translateX(-50%) scale(${(ctk > 0 ? back(ctk / 0.3) * (1 + 0.03 * Math.sin(t * 6)) : 1).toFixed(3)})`;
  // finger taps
  const taps = [[TP.piece, $("pc")], [TP.grade, $("g6")], ...TP.days.map((d, i) => [d, $(`d${i}`)]), [TP.len, $("l30")], [TP.easy, $("be")]];
  if (!taps.some(([tt, e]) => finger(t, tt, e))) $("finger").style.opacity = 0;
  // phone motion
  const sw = startOf[s], pk = ease((t - sw) / 0.35);
  $("phone").style.transform = `rotateY(${(lerp(s === "s0" ? 0 : -14, 0, pk) + 3 * Math.sin(t * 0.8)).toFixed(2)}deg) rotateX(${(2 * Math.sin(t * 0.6)).toFixed(2)}deg) translateY(${(8 * Math.sin(t * 1.1)).toFixed(1)}px)`;
  $("phoneWrap").style.transform = `scale(${t < 0.4 ? lerp(1.12, 1, ease(t / 0.4)).toFixed(3) : 1})`;
  let fl = 0; for (const b of ["s1", "s2", "s3", "s4", "s5", "s6"]) if (t >= B[b] && t < B[b] + 0.14) fl = Math.max(fl, 0.35 * (1 - (t - B[b]) / 0.14));
  if (t > DUR - 0.3) fl = Math.max(fl, (t - (DUR - 0.3)) / 0.3);
  $("flash").style.opacity = fl.toFixed(3);
  let red = 0; for (const b of [0.35, 0.75, 1.15]) if (t > b && t < b + 0.15) red = 0.15; $("red").style.opacity = red;
}
window.render = (t) => {
  camera.position.set(Math.sin(t * 0.25) * 1.2, 3.2 + 0.2 * Math.sin(t * 0.4), 7.5); camera.lookAt(0, 2.2, -2);
  const play = Math.floor(t * 4), hot = t < B.s1 ? -1 : [12, 16, 19, 24, 19, 16, 7, 11, 14, 19][play % 10] + 12 * (Math.floor(play / 10) % 2);
  keys.forEach((kk, i) => { const on = i === hot; kk.m.material.emissive.set(on ? "#E0A84B" : "#000000"); kk.m.material.emissiveIntensity = on ? 0.9 : 0; kk.m.position.y = (kk.b ? 0.12 : 0) - (on ? 0.05 : 0); });
  motes.forEach((m) => { const u = m.userData; m.position.set(u.x + 0.3 * Math.sin(t * 0.5 + u.z), ((u.y + t * u.sp) % 10), u.z); m.scale.setScalar(u.s); });
  nts.forEach((n) => { const u = n.userData; n.position.set(u.x + 0.4 * Math.sin(t + u.ph), 1 + ((u.y + t * u.sp) % 8), u.z); n.scale.setScalar(0.5); n.material.opacity = 0.55; });
  renderer.render(scene, camera); ui(t);
};
window.__ready = (async () => { window.render(0.5); return true; })();
