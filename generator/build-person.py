"""Rebuilds every person page in the MAG design system.

Each page shows the signature light and dark, gives two ways to take it away
(copy it, or share the link), and walks through installing it in Gmail with the
illustrations in assets/gmail/ (made by build-shots.py).
"""
import json, os, struct, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme, ui

BASE = "https://magn3tic.github.io/mag-signatures/pages/"
OUT  = "pages"

PAGE_CSS = """
.wrap{max-width:1180px;}
.hero{padding:var(--sp-12) 0 var(--sp-8);}
.hero h1{font-family:Fragment,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  font-size:clamp(34px,6vw,56px); font-weight:400; letter-spacing:-.01em;}
.hero .role{margin:var(--sp-3) 0 0; font-size:13px; letter-spacing:.12em; text-transform:uppercase; color:var(--text-dim);}
.hero .mailto{margin:var(--sp-2) 0 0; font-size:15px; color:var(--warm);}

/* The signature is a fixed 504px artifact, so the two previews only sit side
   by side once each half can actually hold one. */
.panes{display:grid; gap:var(--sp-4); grid-template-columns:1fr;}
@media (min-width:1160px){ .panes{grid-template-columns:1fr 1fr;} }

.actions{
  display:flex; flex-wrap:wrap; gap:var(--sp-3); align-items:center;
  margin:var(--sp-8) 0; padding:var(--sp-4);
  border:1px solid var(--border); border-radius:var(--r-lg); background:var(--dark-alt);
}
.actions .label{font-size:12px; letter-spacing:.11em; text-transform:uppercase;
  color:var(--text-dim); margin-right:var(--sp-2);}

/* Instruction card: light surface, because it is the part people read. */
.steps{
  background:var(--light); color:var(--dark); border-radius:var(--r-lg);
  padding:var(--sp-8); margin-bottom:var(--sp-12); line-height:1.65; max-width:900px;
}
.steps > h2{
  font-size:17px; letter-spacing:.01em; margin:var(--sp-12) 0 var(--sp-4);
  padding-bottom:var(--sp-2); border-bottom:1px solid var(--gray-light);
}
.steps > h2:first-child{margin-top:0;}
.steps p{margin:0 0 var(--sp-6); font-size:15px; color:#555;}
.steps b{font-weight:700;}
.steps kbd{
  font-family:inherit; font-size:12px; font-weight:700; line-height:1;
  display:inline-block; padding:4px 7px; border-radius:4px;
  background:var(--light-alt); border:1px solid var(--gray-light); border-bottom-width:2px;
}
.steps code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:13px;
  background:var(--light-alt); border:1px solid var(--gray-light); padding:1px 6px;
  border-radius:3px; word-break:break-all;}

/* Numbered walk-through. The rail is drawn on the <ol> so it runs behind the
   markers and stops at the last one. */
.walk{list-style:none; margin:0; padding:0; position:relative;}
.walk::before{content:""; position:absolute; left:15px; top:14px; bottom:14px; width:2px; background:var(--gray-light);}
.walk > li{position:relative; padding:0 0 var(--sp-8) 48px; counter-increment:walk;}
.walk > li:last-child{padding-bottom:0;}
.walk > li::before{
  content:counter(walk); position:absolute; left:0; top:-2px;
  width:32px; height:32px; border-radius:50%;
  display:flex; align-items:center; justify-content:center;
  background:var(--dark); color:var(--light);
  font-size:14px; font-weight:700; font-variant-numeric:tabular-nums;
}
.walk{counter-reset:walk;}
.walk .t{font-size:15px;}
.walk figure{margin:var(--sp-4) 0 0;}
.walk img{
  display:block; width:100%; height:auto; border-radius:var(--r);
  border:1px solid var(--gray-light);
}
@media (max-width:560px){ .steps{padding:var(--sp-6) var(--sp-4);} .walk > li{padding-left:42px;} }
"""

def esc(s): return html.escape(s or "", quote=True)

def png_size(path):
    """The screenshots range from 504px to 1330px wide. Their real size goes on
       the <img> so the browser reserves the right box, and caps the display
       width so the small ones are never upscaled into a blur."""
    with open(path, "rb") as fh:
        head = fh.read(24)
    return struct.unpack(">II", head[16:24])

SHOTS = "assets/gmail"
SHOT_SIZE = {f: png_size(os.path.join(SHOTS, f)) for f in os.listdir(SHOTS) if f.endswith(".png")}

def gmail_steps(name):
    """Step 1 happens on this page; the illustrations cover the rest, one action each."""
    return [
        ('Click <b>Copy signature</b> above. The whole signature, artwork included, '
         'is now on your clipboard.', None),
        ('Open <a href="https://mail.google.com/mail" target="_blank" rel="noopener">Gmail</a> '
         'and click the <b>settings</b> gear at the top right.', "step-2.png"),
        ('Click <b>See all settings</b>.', "step-3.png"),
        ('On the <b>General</b> tab, scroll down to <b>Signature</b> and click <b>Create new</b>. '
         'If you already have a signature there, still click <b>Create new</b>: add a new one '
         'instead of editing the old one.', "step-4.png"),
        ('Name it <code>MAG</code> and click <b>Create</b>. If that name is taken by your old '
         'signature, use <code>MAG 2026</code>.', "step-5.png"),
        ('Click into the signature box and paste with <kbd>Cmd</kbd> + <kbd>V</kbd> on a Mac '
         'or <kbd>Ctrl</kbd> + <kbd>V</kbd> on Windows.', "step-6.png"),
        ('Under <b>Signature defaults</b>, choose the new signature for both '
         '<b>For new emails use</b> and <b>On reply/forward use</b>. If your old one is still '
         'selected there, switch both to the new one. You can then delete the old one with the '
         'bin icon next to it.', "step-7.png"),
        ('Scroll to the very bottom of the page and click <b>Save Changes</b>. '
         'Open a new email to check it.', "step-8.png"),
    ]

def render(p):
    name, slug = p["name"], p["file"][:-5]
    walk = []
    for text, shot in gmail_steps(name):
        if shot:
            w, h = SHOT_SIZE[shot]
            fig = ('\n      <figure style="max-width:%dpx"><img src="../%s/%s" alt="" '
                   'loading="lazy" width="%d" height="%d"></figure>'
                   % (w // 2, SHOTS, shot, w, h))
        else:
            fig = ""
        walk.append('    <li><span class="t">%s</span>%s</li>' % (text, fig))

    pane = lambda kind, label, icn: (
        '    <div class="pane pane-%s">\n'
        '      <div class="pane-head">%s<span>%s</span></div>\n'
        '      <div class="pane-body">%s</div>\n'
        '    </div>' % (kind, icn, label,
                        ('<div id="content">%s</div>' % p["sig"]) if kind == "light"
                        else ('<div>%s</div>' % p["sig"])))

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} &mdash; MAG email signature</title>
<meta name="robots" content="noindex">
<style>{fonts}{base}{css}</style>
</head>
<body>
<header class="topbar">
  <div class="wrap">
    <a class="mark" href="https://magneticcreative.com" target="_blank" rel="noopener">Mag<b>.</b></a>
    <span class="sep" aria-hidden="true"></span>
    <span class="ctx">{region} &middot; Email signature</span>
    <span class="grow"></span>
    <a class="btn btn-sm" href="index.html">{back}<span>All signatures</span></a>
  </div>
</header>

<main class="wrap">
  <div class="hero">
    <span class="eyebrow">Your signature</span>
    <h1>{name}</h1>
    <p class="role">{role}</p>
    <p class="mailto"><a href="mailto:{email}">{email}</a></p>
  </div>

  <div class="panes">
{light}
{dark}
  </div>
  <p class="note">In dark mode Gmail turns the black type white and leaves the artwork and the
     gold job title alone.</p>

  <div class="actions">
    <span class="label">Install</span>
    <button class="btn btn-primary" data-copy="content">{copy}<span>Copy signature</span></button>
    <button class="btn" data-link="{url}" title="{url}">{link}<span>Copy link to this page</span></button>
  </div>

  <div class="steps">
    <h2>Install it in Gmail</h2>
    <p>Eight steps, about two minutes. Use Gmail on a computer: the mobile app cannot
       paste a formatted signature. Once it is saved, it shows up on your phone too.</p>
    <p><b>Already have a signature in Gmail?</b> Don't edit it. Add this one as a new
       signature (step 4) and select it as the default (step 7).</p>
    <ol class="walk">
{walk}
    </ol>
  </div>
</main>

<footer class="wrap">
  <p>This page lives at <a href="{url}"><code>{url}</code></a> &mdash; yours to keep, and safe to re-open any time.</p>
  <p>Artwork loads from <code>{cdn}</code>, so what you see here is exactly what gets pasted.</p>
</footer>

<div id="live" class="sr-only" role="status" aria-live="polite"></div>
<script>{js}</script>
</body>
</html>
""".format(
        name=esc(name), role=esc(p["role"]), email=esc(p["email"]),
        region=esc(p["region"]), slug=esc(slug), url=BASE + slug + ".html",
        fonts=theme.FONTS, base=theme.BASE, css=PAGE_CSS, js=ui.CLIPBOARD_JS, cdn=theme.CDN.split("//", 1)[1],
        light=pane("light", "Light background", ui.LIGHT),
        dark=pane("dark", "Dark mode", ui.DARKI),
        copy=ui.COPY, link=ui.LINK, back=ui.BACK,
        walk="\n".join(walk),
    )

people = json.load(open("generator/people.json"))
for p in people:
    open(os.path.join(OUT, p["file"]), "w", encoding="utf-8").write(render(p))
print(f"{len(people)} paginas reconstruidas")
