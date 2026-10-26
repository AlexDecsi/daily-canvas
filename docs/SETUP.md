# Setting up GitHub and Claude for automatic daily publishing

Plan you approved on 2026-10-25: **GitHub Pages** hosts the public website, and a **Claude Code scheduled task** (formerly "routine") runs in Anthropic's cloud each evening to research, draw and publish.

Nothing below has been done yet. Steps marked **(you)** need your accounts; I can't do them for you. **Never paste passwords, tokens or keys into the chat.**

---

## Step 1: Check your Claude plan allows this (you, ~5 min)

The docs say scheduled tasks and cloud sessions work on Pro, Max, Team and Enterprise plans. **University or education seats aren't mentioned, so we have to test.** What I already verified from this session: your account can reach the scheduled-tasks API (it lists zero tasks), so the feature isn't completely blocked.

1. Go to **https://claude.ai/code** and sign in with your Northeastern account.
2. If you see a page where you can start a cloud session on a GitHub repository, cloud sessions are allowed. If you see a message that the feature isn't available or is disabled by your organization, stop and tell me. That message means a Northeastern admin turned it off, and we'd need a different plan (options below).
3. Optional: look under **Settings** for your plan name and usage limits, and tell me what it says.

**How usage works:** each daily run uses your normal Claude subscription allowance, the same as chatting with Claude Code. Without extra "usage credits" enabled, there should be no extra charge. Busy days could leave you less room for your own Claude use. I'll measure one run's usage before turning on the daily schedule.

## Step 2: Create a GitHub account (you, ~5 min, free)

1. Go to **https://github.com/signup** and create an account. Your Northeastern email is fine.
2. Choose a username you're happy to have in the website address: the site will live at `https://<username>.github.io/<repo-name>/`.
3. Turn on two-factor authentication when GitHub offers it.

**Why public:** GitHub Pages is free for **public** repositories on a free account. Everything in the repo will be visible, including the code and the daily logs. That's fine because nothing secret goes in it (see CLAUDE.md §2.6).

## Step 3: Create the repository (you, ~2 min)

1. On GitHub, click **+ → New repository**.
2. Name it, for example `daily-canvas`. Set it to **Public**. **Don't** add a README, .gitignore or license, because we already have them.
3. Click **Create repository** and send me the repository's web address (e.g. `https://github.com/<username>/daily-canvas`). The address isn't secret.

After that, I'll connect this folder to the repository and upload the code. I'll ask before the first upload, since that makes the project public.

## Step 4: Connect GitHub to Claude (you, ~5 min)

1. Go to **https://claude.ai/code**.
2. Follow the prompt to **connect GitHub**. It installs the "Claude" GitHub App.
3. When GitHub asks which repositories to allow, choose **Only select repositories** and pick `daily-canvas`. This limits Claude to just this project.
4. If you see a message that an organization **Owner** has to enable the GitHub connector first, your university controls that setting. Tell me.

**Good to know:** commits made by the daily task will show up under your GitHub name. If the GitHub connection lapses for about 3 days, scheduled runs stop until you reconnect.

## Step 5: Cloud environment (I'll guide you; ~5 min)

The cloud workspace by default can only reach a short list of sites (GitHub, Python package sites, and so on). **News websites aren't on it.** We'll need to either:
- add a list of specific news domains (safer, so this is my recommendation), or
- allow full internet access.

I'll prepare the exact domain list from the news sources we choose in Phase 3. The cloud image already includes Python 3 and git, which is all our code needs.

## Step 6: Turn on GitHub Pages (me, with your OK, ~2 min)

In the repository: **Settings → Pages → Source: "Deploy from a branch"**, then choose the branch and the `/public` folder. Pages only offers `/` (root) or `/docs` as the folder. I'll arrange the files to fit when we get there. Updates take up to ~10 minutes to appear.

## Step 7: Create the 9 p.m. schedule (me, with your OK)

- Schedule: `CRON_TZ=America/New_York 7 21 * * *`, which is 9:07 p.m. Boston time all year. Daylight saving ends on Nov 1, 2026, and this setting handles it. The docs suggest a few minutes past the hour because on-the-hour runs can start late.
- Before relying on it, we do one **"Run now"** test while you watch. Unattended runs can stall if Claude hits a permission question with nobody there to answer, and the test shows whether that happens.

---

## If your plan doesn't allow scheduled cloud tasks

| Option | Cost | Mac can be off? | Notes |
|---|---|---|---|
| Ask Northeastern IT to enable Claude Code scheduled tasks for your seat | Free | Yes | Best if they agree |
| Personal Claude Pro subscription | Monthly fee | Yes | Same setup as above |
| GitHub Actions + Anthropic API key | Pay per use; needs billing | Yes | I'd estimate cost from Phase 4 dry runs first |
| Scheduled task on your Mac | Free | **No** | Fine for testing only. Doesn't meet the project rules. |

I won't set up or spend money on any of these without your explicit OK.

---

*Sources: Claude Code docs on scheduled tasks (code.claude.com/docs/en/routines), cloud environments and the web quickstart; GitHub Pages docs. Checked 2026-10-25. Plan eligibility for education seats is **unverified** until Step 1.*
