# MAG signature assets

The MAG email signatures and the images they load, hosted here so they no
longer depend on HubSpot Files.

Signature images are hotlinked, never embedded — every time anyone opens one of
these emails, their client re-fetches the image from its URL. That is why the
images live in a repo with stable, versioned URLs instead of in HubSpot.

Public, because nothing here is confidential: the pages and the headshots are
what already goes out on every email MAG sends. This is the difference from
SleepOver, which needed a second private repo for a workbook full of phone
numbers.

## How to reference an image

Always through jsDelivr, always pinned to a tag:

```
https://cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0/images/icons/mail.png
```

A tag is immutable on jsDelivr: once a version has been served it is cached
forever and will never change under a live signature. To ship new artwork, push
it and cut a **new** tag, then update the signatures to that tag. Never
re-point an existing tag.

`@main` also works and picks up pushes, but it is for previewing only — do not
put a `@main` URL into a signature that goes out to people.

## Layout

```
MAG-signatures-master.xlsx  who has a signature -- the sheet to work from
MAG-signatures-master.csv   the same rows, plain text
pages/                      the 63 signature pages, plus index.html
generator/                  the build scripts, and the old SA and US generators
images/icons/               shared chrome: globe, mail, smartphone
images/headshots/us/        US headshots
images/headshots/sa/        SA headshots
images/headshots/sa-2025/   the 2025 SA round
assets/                     the step-by-step install screenshots
migration/url-map.json      every old HubSpot URL and the file it became
```

## The pages

Served by GitHub Pages off `main`:

```
https://magn3tic.github.io/mag-signatures/pages/index.html          the master list
https://magn3tic.github.io/mag-signatures/pages/Gabriel_Arias.html  one person
```

`index.html` is the page to send round: all 63 signatures grouped by region,
searchable, with one switch that flips every preview to dark and a copy button
on each card. Each person's own page shows their signature on white and on
black, gives them the three ways to take it away — copy, a `.htm` for Outlook
desktop, or the link — and walks them through Gmail with screenshots.

The pages are generated. Editing one by hand is overwritten on the next build:

```bash
python3 generator/extract.py        # read the pages -> generator/people.json
python3 generator/build-person.py   # rebuild the 63
python3 generator/build-index.py    # rebuild index.html
```

`extract.py` reads the signature markup back out of the pages themselves, so
the signatures survive a rebuild untouched — the design around them is the only
thing regenerated.

## When someone leaves

`MAG-signatures-master.xlsx` lists all 63 with their role, address, phone,
region, page and page URL. Set their **Status** to `Remove` in the Signatures
tab, save, and run:

```bash
python3 generator/remove.py            # show what would go
python3 generator/remove.py --apply    # delete the pages and rebuild
```

Their headshot stays in `images/` on purpose. Emails they already sent still
hotlink it, and pulling the file breaks their signature in every one of them.

The sheet is generated, but a rebuild reads the Status column back first, so
what you have typed is never lost. Editing any other column changes nothing on
its own — the signature markup lives in the page.

Eleven rows come pre-flagged in **Notes**: five people hold two pages each under
one address, and one phone row links to an empty `tel:`.

Two different jobs in one repo, and the difference matters. The images are
pinned by tag and must never change under a signature already sitting in
someone's mail client. The pages are expected to change, and are served off
`main`. Pushing a page therefore does not touch what `@v1.0.0` serves.

## Where this came from

[gabrielmagcr/Mag-Signatures](https://github.com/gabrielmagcr/Mag-Signatures) is
the old location. It is left exactly as it was, still loading from HubSpot, and
nothing new is published there.

That repo kept two copies of the pages: 63 at the root and 56 stale ones under
`signature-generator/signatures/`. Only the root set came across — the stale
copy had a broken `src="undefined"` on Owen Korinek and was missing Mia
Pitino's newer headshot.

## Adding or changing artwork

```bash
# add the file under images/, then
git add images && git commit -m "new headshot for <name>"
git push
git tag v1.1.0 && git push origin v1.1.0    # a NEW tag, never move v1.0.0
# then update the signatures that use it to @v1.1.0
```

## HubSpot

`migration/url-map.json` maps each old `magneticcreative.com/hubfs/…` URL to
the file that replaced it. Leave the HubSpot files live but unused during the
transition — deleting them breaks the images in every already-sent email, and
HubSpot has no redirect from a deleted file URL.
