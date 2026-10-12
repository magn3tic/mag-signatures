"""Turns every headshot into a crossfade GIF: photo -> MAG logo -> photo.

    python3 generator/make-gifs.py      # needs Pillow; then rebuild the pages

Writes images/gifs/<us|sa>/<Page>.gif and points each signature in
generator/people.json at it on jsDelivr, pinned to theme.CDN's tag. A person
whose photo is "LOGO" (a new starter with no headshot yet) gets the logo alone.
The headshot each GIF was made from is kept in images/gifs/sources.json, so the
GIFs can be rebuilt after the signatures already point at them.
"""
import json, os, re, sys, unicodedata
from PIL import Image, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import CDN

PEOPLE = "generator/people.json"
GIFS = "images/gifs"
SOURCES = GIFS + "/sources.json"
LOGO = "images/mag-logo.png"
SIZE, COLORS, STEPS, STEP_MS = 240, 64, 14, 30
HOLD_PHOTO_MS, HOLD_LOGO_MS = 2600, 1800

ease = lambda t: 4 * t**3 if t < .5 else 1 - (-2 * t + 2)**3 / 2


def flatten(path):
    im = Image.open(path).convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS)
    bg = Image.new("RGBA", (SIZE, SIZE), "white")
    bg.alpha_composite(im)
    return bg.convert("RGB")


def save(frames, durations, path):
    q = [f.quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for f in frames]
    q[0].save(path, save_all=True, append_images=q[1:], duration=durations, loop=0, optimize=True)


def make(photo_path, out):
    logo = flatten(LOGO)
    photo = logo if photo_path == LOGO else flatten(photo_path)
    # Some old headshots are already the logo; there is nothing to fade between.
    if ImageChops.difference(photo, logo).convert("L").point(lambda v: 255 if v >= 16 else 0).getbbox() is None:
        return save([logo], [0], out)
    fade = lambda a, b: [Image.blend(a, b, ease(i / STEPS)) for i in range(1, STEPS)]
    save([photo, *fade(photo, logo), logo, *fade(logo, photo)],
         [HOLD_PHOTO_MS, *[STEP_MS] * (STEPS - 1), HOLD_LOGO_MS, *[STEP_MS] * (STEPS - 1)], out)


def main():
    people = json.load(open(PEOPLE, encoding="utf-8"))
    sources = json.load(open(SOURCES, encoding="utf-8")) if os.path.exists(SOURCES) else {}
    os.makedirs(GIFS, exist_ok=True)
    save([flatten(LOGO)], [0], GIFS + "/mag-logo.gif")

    for p in people:
        page = p["file"][:-5]
        photo = p["photo"]
        if "/images/headshots/" in photo:
            sources[page] = "images/headshots/" + photo.split("/images/headshots/", 1)[1]
        elif photo == "LOGO":
            sources[page] = LOGO
        source = sources[page]

        region = "us" if source.startswith("images/headshots/us/") else "sa"
        name = unicodedata.normalize("NFKD", page).encode("ascii", "ignore").decode() + ".gif"
        out = f"{GIFS}/{region}/{name}"
        os.makedirs(os.path.dirname(out), exist_ok=True)
        make(source, out)

        url = f"{CDN}/{out}"
        p["sig"] = re.sub(r'(<img src=")[^"]*(" alt=)', lambda m: m.group(1) + url + m.group(2), p["sig"], count=1)
        p["photo"] = url
        print(f"{os.path.getsize(out) // 1024:5d} KB  {out}")

    json.dump(dict(sorted(sources.items())), open(SOURCES, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    json.dump(people, open(PEOPLE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
