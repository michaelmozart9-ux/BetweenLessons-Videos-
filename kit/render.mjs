// Frame renderer. Run from the kit folder while `python -m http.server 8765` is running there.
//   node render.mjs <videoDir> test 0.5 3 8 ...   -> <videoDir>/test-<t>.png
//   node render.mjs <videoDir> full                -> <videoDir>/frames/0000.jpg ...   (env START / END = frame range)
//   node render.mjs <videoDir> sheet               -> <videoDir>/sheet.png (contact sheet of 12 frames from frames/)
// Optional env: PORT (default 8765), CHROME_PATH (use a specific Chromium), GL=swiftshader (force software GL).
import { chromium } from "playwright";
import fs from "node:fs";
const [dir, mode, ...rest] = process.argv.slice(2);
if (!dir || !mode) { console.log("usage: node render.mjs <videoDir> test|full|sheet [times...]"); process.exit(1); }
const port = process.env.PORT || 8765;
const args = ["--ignore-gpu-blocklist", "--enable-webgl"]; if (process.env.GL === "swiftshader") args.push("--use-angle=swiftshader", "--enable-unsafe-swiftshader");
async function launch() {
  const tries = process.env.CHROME_PATH ? [{ executablePath: process.env.CHROME_PATH }] : [{}, { channel: "chrome" }, { channel: "msedge" }];
  for (const o of tries) { try { return await chromium.launch({ args, ...o }); } catch (e) { if (o === tries[tries.length - 1]) throw e; } }
}
const b = await launch();
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
if (mode === "sheet") {
  const files = fs.readdirSync(`${dir}/frames`).filter((f) => f.endsWith(".jpg")).sort(); const pick = Array.from({ length: 12 }, (_, i) => files[Math.min(files.length - 1, Math.floor((i + 0.5) * files.length / 12))]);
  await p.setViewportSize({ width: 1440, height: 1280 });
  await p.setContent(`<body style="margin:0;background:#000;display:grid;grid-template-columns:repeat(6,240px)">${pick.map((f) => `<img src="data:image/jpeg;base64,${fs.readFileSync(`${dir}/frames/${f}`).toString("base64")}" style="width:240px;height:427px;object-fit:cover">`).join("")}</body>`);
  await p.screenshot({ path: `${dir}/sheet.png` }); console.log(`wrote ${dir}/sheet.png`); await b.close(); process.exit(0);
}
const timing = JSON.parse(fs.readFileSync(`${dir}/timing.json`, "utf8"));
const errs = []; p.on("pageerror", (e) => errs.push(e.message)); p.on("console", (m) => { if (m.type() === "error" && !m.text().includes("404")) errs.push(m.text()); });
await p.addInitScript(`window.__TIMING__ = ${JSON.stringify(timing)};`);
await p.goto(`http://127.0.0.1:${port}/${dir.replace(/\\/g, "/")}/index.html`);
await p.waitForFunction(() => window.__ready, null, { timeout: 120000 }); await p.evaluate(() => window.__ready);
const stage = await p.$("#stage");
const shot = async (t, path, type) => { await p.evaluate((t) => window.render(t), t); await stage.screenshot(type === "jpeg" ? { path, type: "jpeg", quality: 93 } : { path }); };
if (mode === "test") { for (const t of rest.map(Number)) await shot(t, `${dir}/test-${t}.png`); console.log(`wrote ${rest.length} test frames`); }
else {
  fs.mkdirSync(`${dir}/frames`, { recursive: true }); const n = Math.ceil(timing.duration * timing.fps); const i0 = +(process.env.START || 0), i1 = Math.min(n, +(process.env.END || n)); const t0 = Date.now();
  for (let i = i0; i < i1; i++) { await shot(i / timing.fps, `${dir}/frames/${String(i).padStart(4, "0")}.jpg`, "jpeg"); if ((i - i0) % 60 === 0) console.log(`frame ${i}/${n}`); }
  console.log(`rendered ${i1 - i0} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
}
console.log("errors", JSON.stringify(errs.slice(0, 5))); await b.close();
