"""Renders the Gmail walk-through illustrations from generator/gmail-shots.html
into assets/gmail/step-<n>.png with headless Chrome (2x, for sharp screens).

    python3 generator/build-shots.py
"""
import os, pathlib, subprocess

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SRC = pathlib.Path("generator/gmail-shots.html").resolve().as_uri()
OUT = "assets/gmail"
STEPS = range(2, 9)          # step 1 is the copy button on the page itself

os.makedirs(OUT, exist_ok=True)
for n in STEPS:
    out = os.path.abspath(f"{OUT}/step-{n}.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", "--window-size=960,540",
                    "--virtual-time-budget=4000", f"--screenshot={out}", f"{SRC}#{n}"],
                   check=True, capture_output=True)
    print(f"{os.path.getsize(out) // 1024:5d} KB  {OUT}/step-{n}.png")
