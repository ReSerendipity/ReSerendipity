from pathlib import Path


readme = Path("README.md").read_text(encoding="utf-8")
required = (
    '<b style="font-size:17px;">TTS-MultiModel</b>',
    'href="https://github.com/ReSerendipity/TTS-MultiModel"',
    '<b style="font-size:17px;">SeedVR2-Lite</b>',
    'href="https://github.com/ReSerendipity/SeedVR2-Lite"',
    'href="https://reserendipity.github.io/SeedVR2-Lite/docs/"',
)
for text in required:
    if text not in readme:
        raise SystemExit(f"README.md is missing expected featured-project content: {text}")

if readme.count(" · Apache-2.0</p>") != 2:
    raise SystemExit("README.md must state Apache-2.0 separately for both featured repositories")

for stale in (
    "github.com/ReSerendipity/TTS_MultiModel",
    "github.com/ReSerendipity/SeedVR2-lite",
    "open%20source-Apache--2.0",
):
    if stale in readme:
        raise SystemExit(f"README.md contains stale or misleading content: {stale}")

print("README featured-project names, links, and license scope OK")
