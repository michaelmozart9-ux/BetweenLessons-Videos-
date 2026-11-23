// Shared HTML phone overlay showing the Between Lessons "today's session" plan screen.
// import { planPhone } from "../plan.js"; const plan = planPhone(cfg); then call plan(t) every frame (pure function of t).
// cfg: { at, top=560, scale=1, piece, sub, day, chips:[..], mins:[5,10,5], tempo, bpm, milestone, tag:"Example plan", dark:true }
const CSS = `
#pp { position:absolute; left:50%; width:600px; height:880px; margin-left:-300px; opacity:0; z-index:30; font-family:"Inter"; color:#F5EEDC; transform-origin:50% 100%; }
#pp .ph { position:absolute; inset:0; border-radius:70px; background:#0E0B09; box-shadow:0 40px 90px rgba(0,0,0,.65), inset 0 0 0 10px #2A2420, inset 0 0 0 13px #4A3E33; }
#pp .sc { position:absolute; left:24px; right:24px; top:24px; bottom:24px; border-radius:50px; background:#15110E; overflow:hidden; padding:66px 30px 26px; }
#pp .notch { position:absolute; top:16px; left:50%; width:140px; height:32px; margin-left:-70px; border-radius:18px; background:#000; }
#pp .brand { display:flex; justify-content:space-between; align-items:center; font-weight:800; font-size:26px; color:#E0A84B; margin-bottom:14px; }
#pp .tag { font-size:20px; font-weight:700; color:#B9A78E; border:2px solid #4A3E33; border-radius:999px; padding:4px 12px; }
#pp .day { font-weight:800; font-size:26px; color:#B9A78E; }
#pp .h { font-weight:900; font-size:42px; line-height:1.08; margin:6px 0 4px; }
#pp .sub { font-weight:700; font-size:26px; color:#B9A78E; margin-bottom:16px; }
#pp .chips { display:flex; flex-wrap:wrap; gap:8px; margin-bottom:18px; }
#pp .chips span { padding:8px 16px; border-radius:999px; background:#221C17; font-weight:800; font-size:24px; }
#pp .sess { display:flex; align-items:center; gap:16px; background:#221C17; border-radius:18px; padding:16px 20px; margin-bottom:10px; font-weight:800; font-size:30px; }
#pp .sess i { width:12px; height:42px; border-radius:6px; display:block; flex:none; }
#pp .sess em { margin-left:auto; font-style:normal; color:#B9A78E; font-size:26px; }
#pp .sess b { width:40px; height:40px; border-radius:50%; background:#3CB8A3; color:#08201B; display:flex; align-items:center; justify-content:center; font-size:24px; flex:none; }
#pp .tempo { margin:16px 0 14px; padding:16px; border-radius:20px; background:#2A2213; border:3px solid #E0A84B; text-align:center; font-weight:900; font-size:44px; color:#E0A84B; }
#pp .tempo small { display:block; font-size:24px; color:#D8C7A8; font-weight:700; margin-top:2px; }
#pp .ms { padding:14px 18px; border-radius:18px; background:#1C2B27; border:2px solid #3CB8A3; font-weight:800; font-size:24px; line-height:1.25; }
#pp .ms small { display:block; color:#7FD9C8; font-size:20px; font-weight:800; letter-spacing:.06em; }
`;
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x)), ease = (k) => 1 - Math.pow(1 - clamp(k), 3);
const back = (k) => { k = clamp(k); const c = 1.7; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
export function planPhone(c) {
  const st = document.createElement("style"); st.textContent = CSS; document.head.appendChild(st);
  const el = document.createElement("div"); el.id = "pp"; el.style.top = (c.top ?? 560) + "px";
  const mins = c.mins || [5, 10, 5], cols = ["#E0A84B", "#3CB8A3", "#F08A4B"], names = ["Warm-up", "Main work", "Run-through"];
  el.innerHTML = `<div class="ph"></div><div class="notch"></div><div class="sc">
    <div class="brand"><span>Between Lessons</span><span class="tag">${c.tag || "Example plan"}</span></div>
    <div class="day">${c.day}</div><div class="h">${c.piece}</div><div class="sub">${c.sub || ""}</div>
    <div class="chips">${(c.chips || []).map((x) => `<span>${x}</span>`).join("")}</div>
    ${names.map((n, i) => `<div class="sess r"><i style="background:${cols[i]}"></i>${n}<em>${mins[i]} min</em></div>`).join("")}
    <div class="tempo">Tempo target: ${c.tempo}%<small>${c.bpm} BPM today</small></div>
    <div class="ms"><small>THIS WEEK'S MILESTONE</small>${c.milestone}</div></div>`;
  (c.parent || document.getElementById("stage")).appendChild(el);
  const rows = [...el.querySelectorAll(".sess")], tempo = el.querySelector(".tempo"), ms = el.querySelector(".ms"), sc = c.scale || 1;
  return (t) => {
    const a = t - c.at; if (a < 0 || (c.out && t > c.out)) { el.style.opacity = 0; return; }
    const k = back(a / 0.55); el.style.opacity = clamp(a / 0.15).toFixed(3);
    el.style.transform = `translateX(${c.dx || 0}px) translateY(${((1 - k) * 900).toFixed(1)}px) rotate(${((1 - ease(a / 0.6)) * -6).toFixed(2)}deg) scale(${sc})`;
    rows.forEach((r, i) => { const rk = ease((a - 0.45 - i * 0.2) / 0.2); r.style.opacity = (0.25 + 0.75 * rk).toFixed(3); r.style.transform = `translateX(${((1 - rk) * 40).toFixed(1)}px)`; });
    const tk = clamp((a - 1.15) / 0.25); tempo.style.transform = `scale(${(0.9 + 0.1 * back(tk)).toFixed(3)})`; tempo.style.opacity = (0.3 + 0.7 * tk).toFixed(3);
    ms.style.opacity = (0.3 + 0.7 * ease((a - 1.5) / 0.25)).toFixed(3);
  };
}
