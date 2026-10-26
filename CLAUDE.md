# Daily Visual News Gallery — Agent Instructions (`CLAUDE.md`)

> **Status:** Project specification and implementation instructions, not proof that any automation is already running.
> **Project owner:** A Northeastern University student, new to Claude Code and programming.
> **Project window:** From the verified public launch date through **December 18, 2026**, inclusive.
> **Timezone:** `America/New_York` (Boston local time, including daylight-saving changes).
> **Target publication:** Approximately **9:00 p.m. Boston time**, each calendar day.

## 1. Mission and definition of success

Build and operate a **public, shareable, mobile-friendly online art gallery of daily news**. Each day's entry is a single, distinctive, high-quality, colorful **editorial illustration** that visually communicates the day's most important verified developments. The gallery is primarily an **art exhibition**, not a conventional scrolling news feed.

The system should, once genuinely deployed and authorized, work with **minimal daily human involvement**: research, select stories, fact-check, plan artwork, produce and validate artwork, write a concise museum-style caption, cite sources, publish, and record its work. The owner may occasionally provide plain-English feedback through Claude Code. Preserve the evolving visual archive and evidence of the agent's independent decisions for a final class presentation about agentic AI.

**Success criteria:**
- A public HTTPS website with a prominently featured newest artwork and a newest-first archive grid.
- One date-specific, accurate, visually strong entry per day of operation, with accessible source links.
- Each artwork has **one clear focal story** and typically **one or two supporting stories** only when justified; do not force extra stories.
- A short, factual caption first identifies the events actually illustrated, then adds essential context or takeaways. Avoid generic or flowery descriptions.
- Fully automated daily publishing **only after** an actual scheduler, agent execution environment, credentials, and deployment pipeline are configured and verified.
- Missed dates are automatically detected and backfilled with **date-accurate reporting**, with failures and catch-up actions flagged in logs and weekly reports.
- Concise daily operational logs, weekly summaries, and a feedback/change log.
- Low recurring cost and bounded Claude usage, without sacrificing the minimum acceptable visual quality.

## 2. Important operating boundaries

1. **`CLAUDE.md` is context, not a scheduler.** Reading this file does not itself trigger a daily run. Build and test a real unattended execution path before claiming the project is autonomous.
2. **Do not assume a university Claude subscription includes Anthropic API credits, cloud compute, image-generation APIs, or unlimited unattended Claude Code use.** Check actual entitlements, usage restrictions, and any costs before proposing deployment.
3. **Never incur paid usage, enable billing, publish publicly, connect third-party services, expose data, or make irreversible changes without the owner's explicit approval.** Routine daily publication may proceed unattended *after* the owner has approved the deployment and publication policy.
4. Favor free-tier hosting and infrastructure where genuinely sufficient; do not promise that GitHub Actions can run an authenticated Claude agent for free without verifying the execution mechanism and account permissions.
5. The owner is a beginner. Explain prerequisites and major decisions in plain language; perform the coding, testing, and file maintenance yourself when authorized. Ask only for actions requiring their account access, credentials, permission, or aesthetic judgment.
6. Do not place secrets in code, `CLAUDE.md`, artwork, logs, or git history. Use secret managers/environment variables; redact diagnostics.
7. Follow source terms, licenses, image rights, privacy standards, platform usage policies, and applicable rate limits. Do not bypass paywalls or fabricate source access.
8. Avoid running large numbers of parallel agents, repetitive research, or unlimited retries. Make efficiency measurable.

## 3. Experience and visual design

### Homepage
- Present the **most recent completed illustration** prominently at the top, with its date and a concise headline/label.
- Below, show all earlier entries in a clean, responsive **newest-first gallery grid**.
- Clicking an artwork opens an accessible enlarged detail view (or dedicated detail page) showing the full image, the news date, a brief caption, and direct source links.
- Minimal typography and controls; artwork is the focus. The page should resemble a curated exhibition rather than a cluttered news portal.
- Responsive on mobile and desktop; support keyboard navigation, accessible image descriptions, readable contrast, and fast loading.
- Older entries remain published **as originally released**. Changes to style apply prospectively unless the owner expressly requests a correction or specific revision. Factual corrections must be transparently recorded.

### Editorial art direction
- **Detailed, colorful, sophisticated editorial illustration** with a consistent visual identity but variety in subjects, framing, compositions, and palette.
- Real-world subjects should be **recognizable**: buildings, locations, relevant objects, people, or distinctive events, when the sources justify them. Do not rely solely on generic abstract symbols.
- Make the main story immediately legible. Integrate one or two supporting stories only when the composition remains cohesive. Use visual hierarchy, intentional negative space, and strong focal points.
- Avoid crowded collage layouts, tiny unrelated icons, misleading depictions, text-heavy art, generic clip art, and repetitive templates that flatten different events into the same scene.
- Do not falsely depict a staged or invented event as a documentary image. The work is clearly presented as editorial illustration, not photography.
- Avoid false visual claims (e.g., a specific person at a location they were not reported to be, unconfirmed casualties, invented protest signs, or invented quotations).

### Artwork production method and quality/cost balance
- **Start by prototyping SVG artwork generated with code**, using reusable design tokens/components where they genuinely improve consistency and efficiency.
- SVG is the initial method, **not a requirement to accept poor art**. If prototypes fail to produce detailed, compelling, recognizable editorial images, investigate genuinely free or already-entitled alternatives (including rights and automation/API access). Present any cost, permissions, reliability, or quality trade-offs to the owner before switching.
- Do not assume Claude Code can directly call a particular image-generation service. Verify availability and licensing.
- Render and inspect SVGs in a browser or image preview; ensure correct aspect ratio, crisp shapes, legible focal point, reasonable file size, and no malformed markup. Sanitize any untrusted SVG content.
- Prototype at least **three different news scenarios** (e.g., international/political, science/technology, environment/culture) before choosing a production pipeline. Show the owner examples and obtain approval of the **quality bar** before public launch.
- Keep a small reusable style guide, palette, and component library, but don't allow efficiency measures to make every illustration look the same.
- Set explicit per-run limits for model calls, iterations, source fetches, execution time, and retries based on measured usage during prototyping. If the limits cannot support the required quality, report the trade-off rather than silently degrading output.

## 4. News discovery, selection, and verification

- Cover significant developments across world affairs, politics, economics, science, technology, environment, culture, sports, and other fields **without fixed category quotas**.
- Use a practical mix of accessible reputable news feeds, public RSS, original reporting, and established outlets where available. Do not assume all outlets provide free scraping or unrestricted APIs. Respect robots, rate limits, and terms.
- Gather a bounded candidate set; deduplicate overlapping reports about the same event.
- Assess each candidate for **real-world significance, breadth of credible coverage, public relevance, freshness for the target date, and visual storytelling potential**. Visual appeal should not override importance or truth.
- Choose a coherent daily composition: generally **two or three stories total**, with one unmistakable focal event. One story is acceptable if it dominates the news or additional stories would compromise clarity.
- Verify consequential facts with **at least two independent credible sources when reasonably available**; prioritize primary/original reporting. If only one strong source is available, explicitly assess confidence and either avoid the story or disclose the limitation in internal logs. Two articles republishing the same wire report are not independent corroboration.
- For developing news, include **only verified facts known at publication time**. Separate facts from allegations, forecasts, and speculation; do not draw unconfirmed outcomes.
- Keep a direct URL, publisher, title, and publication/update timestamp for each supporting source, plus access/check time when feasible.
- Use a clear editorial cutoff tied to the **target date in Boston time**. A daily entry is a snapshot, not an ever-updating claim about what is true now.
- Avoid fabricated quotes, statistics, events, or sources. If evidence is insufficient, choose another story or mark the date as pending instead of publishing misleading content.

## 5. Captions, metadata, and accessibility

For each entry, store:
- `date`: the **news date** in `YYYY-MM-DD` in `America/New_York`.
- `published_at`: actual publication timestamp with timezone/UTC representation.
- `status`: `published`, `pending`, `failed`, or `backfilled` (or equivalent explicit fields).
- `title`: short and informative.
- `caption`: **brief museum-label style**, starting with the actual stories/events represented; then one or two concise sentences of significance/context if needed. Avoid a long article.
- `stories`: selected story names, concise verified facts, source URLs, and source timestamps.
- `artwork`: local asset path, format, alt text, method, and revision identifier.
- `backfill`: whether the entry was made after its scheduled date and why.

The public detail view should show source links unobtrusively but clearly. Alt text should describe meaningful visual content and the represented stories, without overstating facts. Avoid misleading headline wording and unsupported claims.

## 6. Daily autonomous workflow

Implement an **idempotent**, testable pipeline. Suggested pseudocode:

```text
function daily_run(target_date = today_in_America_New_York):
    load_configuration_and_limits()
    acquire_lock(target_date)
    if published_entry_exists_and_is_valid(target_date):
        log("already published; no duplicate")
        release_lock()
        return SUCCESS

    check_remaining_budget_and_permissions()
    candidates = collect_reputable_news_for(target_date, bounded_sources)
    candidates = deduplicate_and_rank(candidates)
    selected = choose_coherent_stories(candidates, main_story_count=1,
                                       supporting_story_count=0_to_2)
    verified = corroborate_and_record_sources(selected, as_of=target_date)
    if insufficient_verified_material(verified):
        record_pending_or_failure(target_date, reason)
        alert_in_project_logs()
        release_lock()
        return NEEDS_RETRY_OR_REVIEW

    concept = design_single_clear_editorial_scene(verified, style_guide)
    artwork = render_artwork_with_bounded_iterations(concept)
    if not validate_artwork_quality_and_factual_fidelity(artwork, verified):
        record_pending_or_failure(target_date, reason)
        release_lock()
        return NEEDS_RETRY_OR_REVIEW

    entry = create_short_caption_metadata_and_alt_text(verified, artwork)
    validate_links_dates_schema_and_accessibility(entry)
    publish_atomically(entry)  # no half-written public entry
    verify_live_site_contains_entry(target_date)
    log_story_choices_art_method_usage_and_publication_status()
    release_lock()
    return SUCCESS
```

### Daily scheduling
- Aim for **9:00 p.m. `America/New_York`**. Configure DST correctly; UTC-based cron schedules may require adjustment or a timezone-aware wrapper.
- The scheduler must execute in a reliable environment that does **not** depend on the owner's Mac being awake.
- Evaluate a static site on GitHub Pages plus a hosted scheduler/CI workflow as an initial architecture **only if** the AI execution and publishing credentials are technically feasible and within budget. A static hosting service alone cannot research news or create art.
- Verify how Claude Code/agent execution is invoked unattended; if it requires API credentials or paid usage not included in the owner's university plan, **stop and explain**. Offer an alternative architecture and ask approval. Do not misrepresent local Claude Code sessions as cloud automation.
- Use explicit run timeouts, bounded retries with backoff, logging, and success/failure checks.

## 7. Missed days, backfill, and flags

At the start of each scheduled run, inspect the date range from actual launch through the earlier of the current target date and **2026-12-18**. Identify dates without valid published entries.

- **Automatically attempt catch-up** for missing dates, prioritizing oldest missing dates while respecting usage and execution limits.
- For a historical date, research **what was known and reported on that date**. Use dated archives or original publication timestamps; do not incorporate later developments as though they were already known. If trustworthy as-of-date evidence is unavailable, keep the date flagged as unresolved rather than inventing it.
- Mark each recovered entry internally as **backfilled**, retaining both the original news date and actual publication time. Keep public presentation honest about timing if the distinction is relevant.
- **Also flag every missed run**, even after successful catch-up: log the date, detected reason if known, recovery attempt, outcome, and remaining issues. Include it in the next weekly report.
- Never publish duplicate dates or overwrite a previously published illustration as part of backfill.
- Prevent a large backlog from exhausting usage: impose a per-execution backfill cap and resume remaining dates in later runs; flag any unresolved backlog.
- If a scheduler, credentials, service, or account access is unavailable, the agent cannot guarantee self-repair. Record the issue when execution resumes and request user intervention if necessary.
- Stop creating new daily entries after **December 18, 2026**. After that date, allow only explicitly authorized backfill, correction, documentation, or maintenance; do not silently extend the project.

## 8. Project records and weekly reporting

Maintain **concise structured logs** sufficient for course reflection, not exhaustive transcripts:

- `logs/daily/YYYY-MM-DD.json` or `.md`: candidate/selected stories and rationale; verification sources; artwork method; approximate usage if observable; outcome; errors/retries; backfill status.
- `logs/changes.md`: date, owner's feedback, decisions made, files/workflows changed, and observed effect. Record significant agent-initiated changes as well.
- `reports/weekly/YYYY-Www.md` (or dated week-ending files): entries created, editorial/visual highlights, successes, failures, backfills, usage/cost observations, owner feedback, and lessons for the final presentation.
- Keep public gallery content separate from private operational logs; do not expose account identifiers, secrets, or sensitive diagnostics.
- Generate a short weekly summary automatically via a verified weekly scheduled job **or** a date-aware step in the daily workflow; ensure the same week is not repeatedly regenerated unnecessarily.
- Record meaningful limitations honestly. A useful project log should make it possible to explain what the agent did autonomously versus what required human intervention.

## 9. Owner feedback and change policy

- The owner will occasionally speak to Claude Code in **natural language**. Interpret feedback carefully, propose concise adjustments when ambiguous, and implement approved changes.
- Translate recurring feedback into the relevant style guide, workflow settings, tests, or documentation rather than requiring the owner to repeat it.
- Preserve already-published artwork and captions in their original state by default. If a **factual error** is discovered, recommend a transparent correction process that preserves an audit trail; obtain approval for substantive revisions when appropriate.
- Update `logs/changes.md` after meaningful feedback. Do not turn feedback into unlimited retries or uncontrolled usage.

## 10. Proposed repository structure

Adapt the exact framework only after verifying deployment feasibility; prefer a simple static site with minimal dependencies.

```text
project-root/
├── CLAUDE.md                   # This persistent project context
├── README.md                   # Plain-English setup and operation
├── package.json                # Only if framework/tooling requires it
├── src/                        # Site and pipeline source code
│   ├── site/                   # Gallery UI/components/styles
│   ├── news/                   # Discovery, ranking, verification
│   ├── art/                    # SVG renderer, components, style guide
│   └── pipeline/               # Orchestration, validation, publishing
├── content/
│   └── entries/                # Immutable dated entry metadata
├── public/
│   └── artwork/                # Published SVG/other approved assets
├── config/
│   ├── sources.*               # Source registry and constraints
│   └── editorial-style.md      # Approved visual identity/quality bar
├── logs/
│   ├── daily/
│   └── changes.md
├── reports/
│   └── weekly/
├── tests/                      # Pipeline, date, idempotency, content checks
└── .github/workflows/          # Only if approved and verified
```

Treat this as a **suggested** structure, not a mandate to create empty files or unnecessary tooling. Keep the code beginner-maintainable and well documented.

## 11. Phased build and test plan

**Phase 0 — Feasibility and account check**
1. Inspect the local project and this file; summarize the mission in plain English.
2. Determine which Claude Code functions, API entitlements, third-party services, and deployment options are *actually* available. Do not infer API access from an Enterprise/Premium Seat label.
3. Estimate usage/cost and propose a realistic zero-cost or explicitly approved low-cost automation architecture.
4. Identify accounts, credentials, and approvals the owner must supply. Never ask the owner to paste secrets into chat or commit them.
5. Present a short implementation proposal with major trade-offs; obtain approval before any external deployment or billable service.

**Phase 1 — Gallery prototype**
1. Build a working local gallery with **clearly labeled sample data**, featured latest entry, newest-first archive grid, enlarged detail views, and source links.
2. Test mobile layout, keyboard access, image rendering, and missing-data states.
3. Show the owner how to preview it; request aesthetic feedback.

**Phase 2 — Art quality proof**
1. Produce at least three genuinely different sample editorial SVG illustrations and render them for review.
2. Evaluate recognition, detail, hierarchy, composition, factual fidelity, and effort/usage.
3. If SVG quality is insufficient, investigate free/entitled alternatives; do not change service or spend money without approval.
4. Establish and document an approved style guide and objective quality checklist.

**Phase 3 — Research and verification**
1. Implement accessible feed/source ingestion, timestamps, deduplication, ranking, and verification.
2. Test with several **historical dates** to ensure the system does not leak future information into past entries.
3. Record sources and concise editorial selection rationale.

**Phase 4 — End-to-end daily run**
1. Connect research → selection → verified art brief → illustration → caption → validation → dated entry.
2. Add idempotency, atomic publication, source-link checks, limits, retry behavior, and logging.
3. Run several supervised dry runs and fix failures before allowing public autonomous operation.

**Phase 5 — Public deployment and real scheduling**
1. With explicit owner approval, create or connect the hosting repository and publish the website.
2. Configure a genuine cloud-side schedule and authenticated agent execution path, verifying permissions and costs.
3. Test a scheduled invocation **without relying on the owner's Mac** and confirm that the resulting entry appears on the public website.
4. Test timezone handling, duplicate-run protection, secrets management, and rollback.
5. Record the **actual successful launch date**; daily entry obligations begin then, not retroactively from this document's creation.

**Phase 6 — Recovery and ongoing operation**
1. Simulate a missed day and verify date-accurate backfill plus persistent flagging.
2. Verify weekly summary generation and that failed entries are not published as successes.
3. Monitor usage and quality; refine only within approved limits.
4. Continue through **2026-12-18**, then preserve the archive and prepare a concise final project retrospective.

### Checkpoints versus daily autonomy
During initial construction, show the owner meaningful prototypes and pause for necessary decisions (especially visual quality, accounts, paid services, and public deployment). **After launch**, daily editorial selection and publication should not require owner approval. Do not conflate phased setup checkpoints with daily manual operation.

## 12. Tests and acceptance checks

Before claiming production readiness, verify:
- Site renders latest feature + newest-first archive and works on phone and desktop.
- Entries have date, meaningful image, short accurate caption, alt text, and working source links.
- Different illustration subjects remain legible and sufficiently detailed; owner approved representative samples.
- Running the same date twice never duplicates or silently overwrites an entry.
- Missing dates trigger bounded backfill, accurate as-of-date sourcing, and **flags even when recovered**.
- An unverified claim or invalid artwork blocks publication and is logged.
- Weekly summaries are created once per week and reflect real logs.
- Cloud schedule works with the owner's computer off, using genuinely authorized execution and credentials.
- Secrets are absent from repository and logs; deployment costs/usage remain within approved limits.
- Project stops new daily entries after December 18, 2026.

## 13. Working style for Claude Code

- Act as the project's **technical lead, researcher, designer, and implementation agent**. Take initiative within the owner's approved scope.
- Start each session by reading this file, `README.md`, current project status, and recent relevant logs. Do not assume previous steps are complete without inspecting files or tests.
- Before major implementation changes, state briefly what you intend to do and why. Then implement and test rather than giving the owner long instructions to write code themselves.
- Prefer simple, robust code over sophisticated but fragile multi-agent infrastructure.
- Keep changes incremental, testable, and reversible. Use version control where appropriate.
- Report honestly what is **implemented**, **tested**, **deployed**, **scheduled**, and **not yet possible**. Never say “fully automated” based on a local demo alone.
- If stuck, provide the precise blocker and the smallest action required from the owner.
- Respect the owner's priorities in this order: **accuracy and safety; clearly communicative, high-quality art; reliable autonomous publication; sustainable usage/cost; visual consistency and polish**.

## 14. First-session instruction

**On the owner's first Claude Code session in this folder:**
1. Read `CLAUDE.md` in full.
2. Explain the project and phased plan back in a short, beginner-friendly summary.
3. Inspect the local environment and available account/deployment options; clearly distinguish verified capabilities from assumptions.
4. Recommend a minimal architecture and identify any account/permission/cost blockers **before** claiming unattended automation is feasible.
5. Begin Phase 1's local website prototype with sample entries, unless an essential approval or setup action is required first.
6. Tell the owner exactly how to preview the prototype and what feedback would be useful.

**Do not wait for daily user prompts once a working, authorized scheduler is actually deployed.** Until then, be transparent that the project is in setup/testing mode.
