# Between Lessons daily video run

Michael runs Between Lessons (betweenlessons.org): an AI 6-week piano practice plan. Day 1 free, no card; full plan €17 once ($ for US visitors); 7-day money-back guarantee. Start every reply to Michael with "Michael,". Short, honest, tables/bullets, no filler.

## Hard rules
- Only real product facts. No fake reviews, testimonials, user counts, stats or results. Any made-up chart is labelled "Illustration".
- Public-domain music only (classical, traditional). Never copyrighted songs.
- Every caption includes #ad and points to betweenlessons.org or "Google 'Between Lessons piano'".
- Never publish without Michael's explicit "go" in the chat. Drafts only until then.
- TikTok settings (Michael chose these): privacyLevel PUBLIC_TO_EVERYONE, allowComment true, musicUsageConfirmed true. YouTube privacyStatus public, categoryId 10.
- vidIQ account IDs: YouTube UCVbn57YlW5KuBiJRZB5ed-g (@betweenlessons1), TikTok _0008wIIcn99gBeG2_5bVfQiefProRJ8F9be, Instagram 30099240289662399 (@between_lessons_piano). Re-check with vidiq_social_account_list.

## Real product facts usable in videos
6-week plan, day-by-day sessions: Warm-up / Main work / Run-through. Tempo target (% and BPM) every session, one milestone per week. Pick days/week and 20/30/45/60-min sessions. Missed day just waits. "Too easy" = next session 5% faster, "Too hard" = 5% slower. Hands separate supported. Timer, metronome, PDF download. Example: Clair de Lune, Grade 6, 5 days, 30 min; W1 D1 opening theme left hand 40% / 36 BPM.

## Kit (kit/)
- Setup: `cd kit && npm i && npx playwright install chromium` (or use CHROME_PATH=/opt/pw-browsers/chromium if present). Python needs numpy, soundfile, scipy; ffmpeg.
- Load the `piano-shorts-video` skill if it is listed.
- Each video is a folder (copy the closest existing one): build.py writes audio.wav + timing.json; index.html + scene.js draw it.
  - lv.py `make(HERE, levels, final_beat, ui, ...)`: "X but it gets harder" (levels a–d). Examples: ml2.
  - gtg.py `make(HERE, piece, levels, final_beat, grades)`: "Guess the grade". Example: fe.
  - Cartoon family (k3, p2, p3, c1, c2): low-poly characters, captions from timing.json. c1/base.js is shared.
  - Others: gc/g3 guess the song, cb/ml "but epic", xv wrong vs right, how/ad* phone-UI ads.
- Render: start server in the SAME command: `(python3 -m http.server 8791 --bind 127.0.0.1 >/dev/null 2>&1 &) ; sleep 1; env PORT=8791 GL=swiftshader node render.mjs <dir> test|full|sheet` (START/END env for frame ranges; run 2 workers in parallel). Keyboard range is MIDI 36–84. Check test frames/sheet visually before full render.
- Encode: `python3 encode.py <dir> out/<name>.mp4` (8–20 s, 1080x1920).

## Daily run (fires 7:31pm Europe/Dublin)
1. Read history.md. Make 3 NEW videos for TOMORROW, each a different format, none repeating the last 2 days' formats or pieces. Mix: 1 cartoon (series "3 types of piano students PART N" or a new relatable cartoon), 2 piano formats. Hook in first second, payoff before 15 s, short Between Lessons pitch at the end.
2. Render, check sheets, encode.
3. Upload: `gh release create day-YYYY-MM-DD out/*.mp4 -R michaelmozart9-ux/BetweenLessons-Videos- --title ... --notes ...`; then vidiq_video_upload with url `https://github.com/michaelmozart9-ux/BetweenLessons-Videos-/releases/download/day-YYYY-MM-DD/<file>.mp4`.
4. One vidiq_social_post_draft_create per video, all 3 platforms, publishAt tomorrow 16:00 / 19:00 / 22:00 Europe/Dublin (cartoon first). YouTube needs title.
5. Add rows to history.md, commit kit changes + history, push to main.
6. SendUserMessage + SendUserFile the 3 MP4s to Michael with titles, captions and times, ending: "Reply **go** to schedule all 3." Only when he replies go: vidiq_social_post_publish each draft.
