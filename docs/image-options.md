# Image-generation options (researched 2026-10-25)

**Why:** the owner judged the Phase 2 SVG art studies not good enough (2026-10-25). Below are the free or already-included alternatives that a scheduled cloud task could use **unattended**. Nothing has been signed up for, connected or changed.

**Requirements for any option:** it costs $0 within normal use, has an API a cloud task can call with no human present, has terms that allow publishing the images on a public site, and is reliable enough for a daily run.

## Comparison

| Option | Free amount | Automatable? | Rights / terms | Verdict |
|---|---|---|---|---|
| **Cloudflare Workers AI** (FLUX models) | 10,000 "neurons"/day, resets 00:00 UTC; no credit card needed (secondary sources) | Yes: REST API with account ID + API token | FLUX: Black Forest Labs terms. They claim no ownership of outputs; you may use them; no consent-less depiction of identifiable people; outputs must not be passed off as real photos of real events | **Recommended to test** |
| Pollinations.ai (keyless endpoint) | Free, no account | Yes | Unclear official terms; possible watermark; no uptime promise; reportedly about 1 request per 15 s | Backup only |
| Google Gemini API (Flash Image) | Image models appear **paid-only** now (sources conflict; newest say no free tier) | Yes | Google terms | Not free → no |
| Hugging Face Inference Providers | $0.10/month of credit (official docs) | Yes | Per model | Too little credit → no |
| Adobe Firefly / Microsoft Copilot through Northeastern | Possibly included (2023 Northeastern IT post lists Firefly; unverified now) | **No**: web apps only, no student API | Adobe/Microsoft terms | Manual use only; can't run daily unattended |
| Run an open model on free GitHub Actions | Free CPU runners (no GPU) | Technically | Depends on model | Too slow or too low-quality on CPU → no |
| Keep improving code-drawn SVG | Free | Yes | Ours | Keep as the **fallback** when image generation fails |

## Cloudflare models and how many images fit in the free daily amount

Neuron costs are from Cloudflare's pricing page. Image counts are my estimate for one 1024×768 image (≈4 tiles of 512×512):

| Model | Approx. cost per image | Images per free day | Notes |
|---|---|---|---|
| `flux-1-schnell` | ~100 neurons (8 steps) | ~100 | Fast, older (2024), decent |
| `flux-2-klein-4b` | ~105 neurons | ~95 | Newer, small, fast |
| `flux-2-klein-9b` | ~1,365 neurons | ~7 | Newer, bigger. Likely the best quality-per-budget for 1 image + a few retries a day |
| `flux-2-dev` | ~3,000–4,200 neurons (step-dependent) | ~2–3 | Highest quality, leaves no room for retries or backfill |
| `lucid-origin` (Leonardo) | ~2,900 neurons | ~3 | Leonardo's terms on output rights for API use are unclear → avoid until checked |

**Daily need:** 1 image, plus up to 3 retries, plus occasional backfill days. That fits comfortably on klein-4b or schnell, and fits on klein-9b on most days.

## Catches to know about

1. **Storing the API key.**
   - Claude's cloud workspaces can hold a key as a "network secret". Claude can then use the key without ever seeing it, which is the safest way.
   - **On Enterprise plans, only an organization admin can add one.** Without that, the key would go in an environment variable. Anyone using that workspace can read environment variables; for your personal workspace, that's you and the Claude sessions running in it.
   - Mitigation: a Cloudflare token limited to Workers AI only, on a free account with no card attached. The worst case is someone using up the day's free allowance, and you can revoke the token at any time.
2. **Network access.** The cloud workspace must be allowed to reach `api.cloudflare.com`. That's one line in the allowed-domains list.
3. **Accuracy risks of AI images.** These models can distort landmarks, add garbled text, or invent people and crowds. Safeguards:
   - prompts ask for an illustrated (not photographic) style, no text, and no identifiable real people
   - Claude **looks at every image** and rejects it against the quality checklist, with at most 3 tries
   - if no image passes, nothing is published that day
4. **Labeling.** Each entry would say "AI-generated editorial illustration". BFL's terms forbid presenting outputs as real photos of real events, which our project rules already forbid.
5. **Reliability.** If Cloudflare is down or the free allowance is used up, fall back to an SVG or mark the day "pending" and backfill later.
6. **Format change.** Images become JPEG/PNG instead of SVG (roughly 150–400 KB each). The gallery already handles any image format.

## Suggested next step (needs owner OK)

Run a **side-by-side test** of the three Phase 2 scenes (UN at dusk, rocket launch, hurricane from orbit) on 2–3 Cloudflare FLUX models, about 10–15 images in all. That's well within one day's free amount. The owner then compares them with the SVG studies and picks the quality bar.

**Owner's part:** create a free Cloudflare account (no card), then create an API token with only Workers AI permissions. I'll explain each click when we get there; the key is never pasted into chat.

## Sources
- Cloudflare Workers AI pricing: https://developers.cloudflare.com/workers-ai/platform/pricing/
- FLUX.1 schnell model page (REST format): https://developers.cloudflare.com/workers-ai/models/flux-1-schnell/
- Black Forest Labs terms: https://bfl.ai/legal/terms-of-service
- Claude Code cloud environments (network secrets, env vars, allowed domains): https://code.claude.com/docs/en/cloud-environments.md
- Hugging Face credits: https://huggingface.co/docs/inference-providers/pricing
- Gemini free-tier status (forum, conflicting secondary sources): https://discuss.ai.google.dev/t/i-keep-getting-429-on-image-generation-requests/116437
- Northeastern Adobe access (2023): https://its.northeastern.edu/2023/09/05/new-adobe-tools-and-services-for-bringing-your-ideas-to-life-this-school-year
- Pollinations (third-party summary only): https://apiframe.ai/blog/free-ai-image-generation-api-2026
