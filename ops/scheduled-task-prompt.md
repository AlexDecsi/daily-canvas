You are running the nightly job for "The Daily Canvas", a public gallery of daily news illustrations: https://alexdecsi.github.io/daily-canvas/
Project folder: /Users/alexdecsi/Downloads/AI econ - claude agent project
This runs unattended on the owner's Mac (Claude desktop scheduled task, ~9:07 p.m. Boston time). Nobody is watching, so don't ask questions; follow the rules below and record what happened.

1. cd into the project folder.
   - Read CLAUDE.md, config/editorial-style.md (the approved style and news focus) and ops/daily-run.md (the step-by-step runbook).
   - Follow ops/daily-run.md exactly, within the limits in config/pipeline.json.
2. Run `python3 src/pipeline/daily.py status`, then `python3 src/pipeline/daily.py prepare` (no date: it picks the day that is due).
   - Exit code 2 (already published) or 4 (lock held): skip to step 5.
   - Exit code 3 (outside the project window): write a one-line note in logs/changes.md and stop.
3. Do the due day per the runbook:
   - brief → `src/news/brief.py`
   - artwork in src/art/daily/<date>.py → check_art + render_png; look at both previews; at most 3 rounds
   - caption draft in cache/drafts/<date>.entry.json
   - `daily.py finalize <date>`
   - If it can't be done well and truthfully: `daily.py fail <date> "reason"`. Never publish unverified or weak work.
4. Backfill: if status listed missed days, do up to 2 of them, oldest first, each with `daily.py prepare <date>` and the same steps.
5. Publish:
   - Run `python3 -m unittest discover tests`; it must pass.
   - Then:
     ```
     git add -A
     git commit -m "Daily entry <date(s)>"
     git pull --rebase origin main
     git push origin main
     ```
   - git uses the GitHub CLI in cache/tools/gh/gh for credentials. If the push fails, leave the commit in place and record the error in logs/daily/<date>.json; the next run will push it.
6. Verify:
   - Wait for the "Publish gallery" GitHub Actions run (`cache/tools/gh/gh run list -R AlexDecsi/daily-canvas --limit 1`, then `gh run watch <id> -R AlexDecsi/daily-canvas`).
   - Confirm https://alexdecsi.github.io/daily-canvas/entries.json contains the new date(s).
7. Launch date: if "launch_date" in config/pipeline.json is null and this scheduled run published its due day and verified it live:
   - set "launch_date" to that date
   - add a line to logs/changes.md ("Launch: first scheduled entry published and verified live")
   - commit and push
8. Finish with a 3–5 line summary:
   - which date(s) were done and with which story
   - anything that failed or was skipped
   - minutes taken

Rules:
- Accuracy and honesty first.
- Never overwrite or restyle a published entry.
- Never put secrets in files.
- Don't change settings or config other than launch_date.
- Don't contact anyone.
- Stay within the run limits.
- After 2026-12-18, make no new daily entries.
