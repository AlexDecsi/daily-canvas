# The Daily Canvas

A gallery of daily news: one editorial illustration per day, with a short museum-style caption and source links. `CLAUDE.md` holds the full project spec.

**Live site:** https://alexdecsi.github.io/daily-canvas/ · **Repository:** https://github.com/AlexDecsi/daily-canvas

## Current status (2026-10-25)

| Piece | Status |
|---|---|
| Local gallery website (Phase 1) | **Built and tested locally**: now shows 2 real pre-launch entries (sample data removed) |
| Art quality proof (Phase 2) | **Done.** Style guide v3 approved (`config/editorial-style.md`); studies in `prototypes/poster/` |
| News research and verification (Phase 3) | **Built and tested**: code in `src/news/`, supervised dry runs in `logs/research/` |
| Daily pipeline (Phase 4) | **Built; 2 supervised dry runs published locally** (runbook: `ops/daily-run.md`) |
| Public website | **Live** at https://alexdecsi.github.io/daily-canvas/ (GitHub Pages; republished automatically when `public/` changes on `main`) |
| Daily schedule | **Scheduled on the owner's Mac** (Claude desktop app): 9:07 p.m. run, backup checks 11:07 p.m. and 8:07 a.m. Runs only while the Mac is awake and the app is open. First automatic entry expected Oct 26. |

## Preview the gallery on your Mac

From this folder, run:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 --directory public
```

Then open http://localhost:8000 in a browser. Press Ctrl+C in the terminal to stop it.
(Opening `public/index.html` directly by double-clicking won't work, because browsers block it from loading `entries.json`.)

## How it fits together

```text
content/entries/YYYY-MM-DD.json   one file per day (the source of truth)
        │
        ▼  python3 src/pipeline/build_site.py   (checks every entry, then writes ↓)
public/entries.json               only "published" and "backfilled" entries
public/artwork/*.svg              the illustrations
public/index.html, styles.css, app.js   the gallery page (no frameworks, no build tools)
```

- **Entries** with status `pending` or `failed` are never shown. The builder stops if any entry is missing alt text or artwork, has a non-https source, has a misnamed file, or is dated after 2026-12-18.
- **Detail links:** each entry has its own address, for example `http://localhost:8000/#/2026-10-24`.
- **Keyboard:** Tab moves through the artworks and Enter opens one. In the enlarged view, ← and → move between days and Esc closes it.

## Preview the art studies

```bash
python3 -m http.server 8001 --bind 127.0.0.1 --directory prototypes/art
```

Then open http://localhost:8001. To redraw a study after changing its script, run, for example, `python3 src/art/prototypes/launch.py`.

## Run a day by hand (Phase 4)

Follow `ops/daily-run.md`. The bookkeeping commands are:

```bash
python3 src/pipeline/daily.py status
python3 src/pipeline/daily.py prepare            # or a past date: prepare 2026-10-24
python3 src/pipeline/daily.py finalize 2026-10-25
```

## Research a news day (Phase 3 tools)

```bash
python3 src/news/feeds.py 2026-10-25        # read feeds (today if no date)
python3 src/news/cluster.py 2026-10-25      # group and rank candidates
python3 src/news/wiki_events.py 2026-10-12  # past dates: discover events as of that day
python3 src/news/brief.py 2026-10-25        # check Claude's story brief before art is made
```

## Checks

```bash
python3 -m unittest discover tests
```

## Folders

- `logs/changes.md`: decisions and owner feedback
- `logs/daily/`: one log per news day · `reports/weekly/`: weekly summaries, written once per week by the daily task (`src/pipeline/weekly.py`)
- `.claude/launch.json`: lets Claude Code open the preview in its browser pane
