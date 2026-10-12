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
# 400px shown at 150: the browser's downscale smooths the circle's edge.
SIZE, COLORS, STEPS, STEP_MS = 400, 48, 10, 40
HOLD_PHOTO_MS, HOLD_LOGO_MS = 2600, 1800

ease = lambda t: 4 * t**3 if t < .5 else 1 - (-2 * t + 2)**3 / 2


# GIF transparency is all-or-nothing, so the circle's soft edge is cut at half
# alpha. The pixels kept on that edge keep the circle's own colour rather than
# being mixed with a background, so there is no halo on light or dark inboxes.
CUT = 128


def load(path):
    return Image.open(path).convert("RGBA").resize((SIZE, SIZE), Image.LANCZOS)


def flatten(im):
    return im.convert("RGB")


def same(a, b):
    """True when two RGBA images look identical once composited on grey."""
    grey = Image.new("RGBA", (SIZE, SIZE), (150, 150, 150, 255))
    a, b = Image.alpha_composite(grey, a), Image.alpha_composite(grey, b)
    return ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v >= 16 else 0).getbbox() is None


def save(frames, durations, path):
    """frames are RGBA; palette index COLORS is kept for transparent pixels."""
    out = []
    for f in frames:
        q = flatten(f).quantize(colors=COLORS, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        pal = q.getpalette()[:COLORS * 3] + [0, 0, 0] * (256 - COLORS)
        q.putpalette(pal)
        q.paste(COLORS, mask=f.getchannel("A").point(lambda a: 255 if a < CUT else 0))
        out.append(q)
    out[0].save(path, save_all=True, append_images=out[1:], duration=durations, loop=0,
                transparency=COLORS, disposal=2, optimize=False)


def make(photo_path, out):
    logo = load(LOGO)
    photo = logo if photo_path == LOGO else load(photo_path)
    # Some old headshots are already the logo; there is nothing to fade between.
    if same(photo, logo):
        return save([logo], [0], out)
    fade = lambda a, b: [Image.blend(a, b, ease(i / STEPS)) for i in range(1, STEPS)]
    save([photo, *fade(photo, logo), logo, *fade(logo, photo)],
         [HOLD_PHOTO_MS, *[STEP_MS] * (STEPS - 1), HOLD_LOGO_MS, *[STEP_MS] * (STEPS - 1)], out)


def main():
    people = json.load(open(PEOPLE, encoding="utf-8"))
    sources = json.load(open(SOURCES, encoding="utf-8")) if os.path.exists(SOURCES) else {}
    # macOS file names arrive decomposed (e + combining diaeresis); key everything in NFC.
    nfc = lambda s: unicodedata.normalize("NFC", s)
    sources = {nfc(k): v for k, v in sources.items()}
    os.makedirs(GIFS, exist_ok=True)
    save([load(LOGO)], [0], GIFS + "/mag-logo.gif")

    for p in people:
        page = nfc(p["file"][:-5])
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
