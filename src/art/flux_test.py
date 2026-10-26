"""Side-by-side test: draw the three Phase 2 scenes with Cloudflare Workers AI FLUX models.

Reads CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN from the project's .env
file (which git ignores). The token is never printed or written anywhere else.

Run from the project folder:
    python3 src/art/flux_test.py

Images land in prototypes/flux/. Images that already exist are skipped, so
re-running never spends the free allowance twice. A budget guard stops before
the estimated total would pass 9,000 of the 10,000 free daily "neurons".
"""

import base64
import json
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "prototypes" / "flux"
BUDGET = 9000  # estimated neurons; Cloudflare's free allowance is 10,000/day
WIDTH, HEIGHT = 1024, 768  # 4:3, matches the gallery frames
SEED = 42

STYLE = (
    "Editorial illustration for a magazine cover, painterly digital art with bold simplified shapes, "
    "rich saturated colour, visible gouache-like brush texture, strong single focal point, cinematic "
    "lighting, clearly an illustration and not a photograph. No text, no letters, no logos, no watermark."
)

SCENES = {
    "un": (
        "The United Nations Headquarters in New York at dusk, seen from across the East River: the tall, "
        "slender glass Secretariat tower with many lit office windows, beside it the low white General "
        "Assembly building with its curved, swooping roof and small shallow dome, the Chrysler Building's "
        "spire in the Midtown skyline behind, a small ferry on the river, sunset sky turning violet."
    ),
    "launch": (
        "A crewed rocket lifting off at twilight from a coastal launch pad in Florida, beside a red steel "
        "launch tower, a bright flame and a huge billowing exhaust cloud lit orange from below, the flame "
        "reflected in a lagoon, small silhouetted spectators on a beach in the foreground watching, some "
        "holding up phones. Generic white rocket with no flags or markings."
    ),
    "hurricane": (
        "A large hurricane seen from orbit at night: a clear eye and a dense, bright central cloud mass "
        "spiralling counter-clockwise, ragged rain bands reaching a coastline traced by golden city lights, "
        "lightning flickering inside the clouds, the thin blue glow of Earth's atmosphere along the curved "
        "horizon, stars above."
    ),
}

# (short name, Cloudflare model id, request kind, extra fields, estimated neurons per image)
# Estimates come from Cloudflare's pricing page, assuming ~4 tiles of 512x512 per image.
MODELS = [
    ("schnell", "@cf/black-forest-labs/flux-1-schnell", "json", {"steps": 8}, 100),
    ("klein-4b", "@cf/black-forest-labs/flux-2-klein-4b", "multipart", {}, 110),
    ("klein-9b", "@cf/black-forest-labs/flux-2-klein-9b", "multipart", {}, 1370),
]
# FLUX.2 [dev] is expensive (~3,000 neurons at 20 steps), so it draws one scene only.
DEV = ("dev", "@cf/black-forest-labs/flux-2-dev", "multipart", {"steps": 20}, 3000)
DEV_SCENES = ["un"]


def load_env():
    env = {}
    path = ROOT / ".env"
    if not path.is_file():
        sys.exit("No .env file found. Follow the setup steps first.")
    for line in path.read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip().strip('"').strip("'")
    for key in ("CLOUDFLARE_ACCOUNT_ID", "CLOUDFLARE_API_TOKEN"):
        if not env.get(key):
            sys.exit(f".env is missing {key}.")
    return env


def multipart(fields):
    boundary = uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n')
    parts.append(f"--{boundary}--\r\n")
    return "".join(parts).encode(), f"multipart/form-data; boundary={boundary}"


def generate(env, model_id, kind, prompt, extra):
    url = f"https://api.cloudflare.com/client/v4/accounts/{env['CLOUDFLARE_ACCOUNT_ID']}/ai/run/{model_id}"
    if kind == "json":
        body = json.dumps({"prompt": prompt, "seed": SEED, **extra}).encode()
        ctype = "application/json"
    else:
        body, ctype = multipart({"prompt": prompt, "width": WIDTH, "height": HEIGHT, "seed": SEED, **extra})
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": f"Bearer {env['CLOUDFLARE_API_TOKEN']}", "Content-Type": ctype})
    with urllib.request.urlopen(req, timeout=180) as resp:
        data = json.loads(resp.read())
    return base64.b64decode(data["result"]["image"])


def extension(img):
    if img[:3] == b"\xff\xd8\xff":
        return "jpg"
    if img[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if img[:4] == b"RIFF" and img[8:12] == b"WEBP":
        return "webp"
    return "bin"


def main():
    env = load_env()
    OUT.mkdir(parents=True, exist_ok=True)
    results_path = OUT / "results.json"
    results = json.loads(results_path.read_text()) if results_path.exists() else []
    spent = 0
    jobs = [(m, s) for m in MODELS for s in SCENES] + [(DEV, s) for s in DEV_SCENES]

    for (name, model_id, kind, extra, est), scene in jobs:
        if list(OUT.glob(f"{scene}-{name}.*")):
            print(f"skip   {scene}-{name} (already exists)")
            continue
        if spent + est > BUDGET:
            print(f"stop   {scene}-{name}: would pass the {BUDGET}-neuron budget (spent ~{spent})")
            continue
        prompt = f"{SCENES[scene]} {STYLE}"
        start = time.time()
        try:
            img = generate(env, model_id, kind, prompt, extra)
        except urllib.error.HTTPError as err:
            detail = err.read().decode(errors="replace")[:300]
            print(f"error  {scene}-{name}: HTTP {err.code} {detail}")
            if err.code in (401, 403):
                sys.exit("The token was rejected. Check that it has Workers AI permission and the account ID is right.")
            if err.code == 429:
                sys.exit("Rate limit or free allowance reached; try again after 00:00 UTC.")
            continue
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError) as err:
            print(f"error  {scene}-{name}: {type(err).__name__}: {err}")
            continue
        seconds = round(time.time() - start, 1)
        path = OUT / f"{scene}-{name}.{extension(img)}"
        path.write_bytes(img)
        spent += est
        results.append({"scene": scene, "model": name, "model_id": model_id, "file": path.name,
                        "seconds": seconds, "bytes": len(img), "est_neurons": est,
                        "seed": SEED, "prompt": prompt, "extra": extra,
                        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z")})
        results_path.write_text(json.dumps(results, indent=2) + "\n")
        print(f"saved  {path.name}  {seconds}s  {len(img) // 1024} KB  (~{est} neurons)")
    print(f"Done. Estimated neurons used this run: ~{spent}")


if __name__ == "__main__":
    main()
