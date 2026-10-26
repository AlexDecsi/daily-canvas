# Daily run: instructions for Claude

These are the steps for one daily run. The scheduled task on the owner's Mac (~9:07 p.m. Boston time; prompt in `ops/scheduled-task-prompt.md`) follows this file. It runs on the Mac because Northeastern hasn't enabled GitHub for Claude cloud sessions (see `logs/changes.md`). Read `CLAUDE.md` and `config/editorial-style.md` (the approved style and news focus) first.

**Hard rules:**
- Accuracy over output: if something can't be verified, publish nothing and record why.
- Stay within the limits in `config/pipeline.json`.
- Never overwrite a published entry.
- Never put secrets in files.

## 0. Status and backfill
```bash
python3 src/pipeline/daily.py status
```
- If the project window has ended, stop.
- If there are missed days, do up to `backfill_dates_per_run` of them **after** today's entry, oldest first, each with steps 1–6 (prepare uses the backfill path automatically).

## 1. Prepare
```bash
python3 src/pipeline/daily.py prepare            # today (Boston); or give a past date for backfill
```
- Exit 2 = already published: stop. Exit 4 = another run holds the lock: stop.
- Live: read `logs/research/<date>/candidates.json`. Backfill: read `wiki_events.json`.

## 2. Choose and verify → `logs/research/<date>/brief.json`
- Follow the **news focus**: top US national stories first, then significant Boston/New England news. International stories only when US outlets lead with them or they directly affect the US.
- Pick **one focal story**, plus 0–2 supporting stories only if they fit one coherent picture.
- Read the actual articles: at most `article_reads` reads and `web_searches` searches. Respect paywalls and robots; never bypass them.
- For past dates, confirm each source's time with `src/news/article_meta.py`.
- Write facts in your own words. Keep quotes very short. Record every source with its publisher, title, url and published_at; also record `wire` ("AP", "AFP", "Reuters") when the piece is a wire story.
- For each public figure, write the exact `verified_action` to be drawn.
- Check the brief:
  ```bash
  python3 src/news/brief.py <date>
  ```
  It must print OK. If it can't pass, choose another story or record a failure (step 7).

## 3. Draw → `src/art/daily/<date>.py` writes `public/artwork/<date>.svg`
- Use the people kit (`src/art/people.py`) and helpers (`src/art/svg.py`); look at `src/art/prototypes/poster_*.py` for patterns.
- Approved style: literal, colorful graphic poster; people doing the reported action; no invented text, signs, quotes, crowds or casualties.
- Set the `<title>` and `<desc>` honestly. Don't add the "ART STUDY" tag.
- Loop at most `art_render_rounds` times:
  ```bash
  python3 src/art/daily/<date>.py
  python3 src/art/check_art.py public/artwork/<date>.svg
  python3 src/art/render_png.py public/artwork/<date>.svg   # then LOOK at cache/previews/<date>-1200.png and -360.png
  ```
- Review it against the style guide checklist. Fix the biggest problem each round.
- If it still fails after the last round, don't publish: record a failure (step 7).

## 4. Caption draft → `cache/drafts/<date>.entry.json`
```json
{
  "title": "Short, factual title",
  "caption": "First the events shown, then one or two sentences of context. No more than 75 words.",
  "alt": "What the picture shows and which story it represents, without overstating.",
  "stories_shown": ["<story name exactly as in the brief>"],
  "art_reviewed": true,
  "art": {"revision": "r<number of render rounds used>"},
  "usage": {"article_reads": 0, "web_searches": 0, "render_rounds": 0, "minutes": 0},
  "backfill_reason": "only for past dates: why it was made late"
}
```
- `stories_shown` lists only stories actually drawn. A supporting story that didn't fit the picture stays in the brief but not in the entry.

## 5. Finalize
```bash
python3 src/pipeline/daily.py finalize <date>
```
It runs these checks:
- the brief
- the artwork
- caption length
- `art_reviewed`
- every source link
- the entry schema

Then it publishes atomically, rolling back on error, and releases the lock. If it reports BLOCKED, fix the problem (within the limits) or go to step 7.

## 6. Afterwards
- Run the tests, then commit (`Daily entry <date>`) and push to `main`. GitHub Actions republishes `public/` to https://alexdecsi.github.io/daily-canvas/.
- Confirm the live `entries.json` contains the new date.

## 7. If the day can't be done
```bash
python3 src/pipeline/daily.py fail <date> "short reason"
```
- The date stays flagged and is retried as a backfill.
- Never publish weak or unverified work just to fill a day.
