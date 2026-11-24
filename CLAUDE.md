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

## Promotion rules (Michael: "lots of views but they don't promote it well")
- The product must be PART of the payoff, not just an end card. Every video shows the Between Lessons phone UI (plan screen: today's session, Warm-up / Main work / Run-through, tempo target %/BPM, weekly milestone) for at least 2-3 s BEFORE the final second, tied to the video's topic (e.g. after "Grade 8 version" show "Your plan for this piece: Week 1, 40% tempo"; cartoon: the character who wins is shown using the plan).
- 1 of the 3 daily videos is product-led: a real practice problem (stuck bar, no time, missed day, don't know where to start) solved on screen by a real feature.
- Pitch = a specific reason, not generic: "Want to play this? Type the piece in, get a free Day 1 plan" instead of "check out Between Lessons".
- Caption first line is the hook; second line is the offer with "Day 1 free, no card"; keep #ad.
- Aim the hook at people who play or are learning piano (problems, grades, practice), not only general music fans. They are the buyers.

## Daily run (fires 7:31pm Europe/Dublin)
1. Read history.md. Make 3 NEW videos for TOMORROW, each a different format, none repeating the last 2 days' formats or pieces. Mix (from YouTube data 24 Nov): NO cartoons (last 6 cartoons got 0-24 views each), NO nursery/kids songs (Twinkle 24, Deck 49, Mary 45), NO talking/explainer videos (8-16 views). Use the formats that get 1-4k views: "Grade 1 vs Grade 8 <famous classical/Christmas piece>", "Guess the grade", "<famous piece> but it gets EPIC", "Guess the song: Easy to Impossible". Famous pieces only (Carol of the Bells, Beethoven 5th, Mountain King, Turkish March, Canon, Moonlight, Für Elise, Happy Birthday...). Grade formats are preferred: they attract learners and tie to the product ("Which grade are you? Get a plan for your grade"). Hook in first second, payoff before 15 s, short Between Lessons pitch at the end.
2. Render, check sheets, encode.
3. Upload (releases are blocked for this session type; use the orphan `media` branch, replaced each day so the repo stays small): `rm -rf /tmp/media && mkdir /tmp/media && cd /tmp/media && git init -q -b media && cp <kit>/out/*.mp4 . && git add . && git -c user.name=claude -c user.email=noreply@anthropic.com commit -q -m "media YYYY-MM-DD" && git remote add origin https://github.com/michaelmozart9-ux/BetweenLessons-Videos-.git && git push -q -f origin media`. Then vidiq_video_upload with url `https://raw.githubusercontent.com/michaelmozart9-ux/BetweenLessons-Videos-/media/<file>.mp4` (tested, works) and use the returned uploadId as the draft's video media.
4. One vidiq_social_post_draft_create per video, all 3 platforms, publishAt tomorrow 16:00 / 19:00 / 22:00 Europe/Dublin. YouTube needs title. IMPORTANT: put publishAt AND privacyStatus "public" inside the YOUTUBE destination itself (past runs left YouTube with no time, which would post it instantly). vidiq_social_post_draft_create DROPS the YouTube time (happened 3 days in a row), so ALWAYS follow each create with vidiq_social_post_draft_update setting the YOUTUBE destination publishAt + privacyStatus "public", then vidiq_social_post_draft_get to confirm all 3 destinations show scheduledFor. If publishing asks for YouTube verification, send Michael the link and retry after he says done.
5. Add rows to history.md, commit kit changes + history, push to main.
6. SendUserMessage + SendUserFile the 3 MP4s to Michael with titles, captions and times, ending: "Reply **go** to schedule all 3." Only when he replies go: vidiq_social_post_publish each draft.
