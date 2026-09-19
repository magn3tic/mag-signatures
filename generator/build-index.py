"""Builds pages/index.html -- every signature on one page, grouped by region,
searchable, with a copy button on each card."""
import json, os, sys, html, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme, ui

BASE = "https://magn3tic.github.io/mag-signatures/pages/"

INDEX_CSS = """
.wrap{max-width:1240px;}
.hero{padding:var(--sp-12) 0 var(--sp-6);}
.hero h1{font-family:Fragment,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  font-size:clamp(32px,5.5vw,52px); font-weight:400; letter-spacing:-.01em;}
.hero p{margin:var(--sp-4) 0 0; max-width:62ch; color:var(--text-dim); font-size:15px;}

.toolbar{position:sticky; top:64px; z-index:30; background:var(--dark);
  border-bottom:1px solid var(--border); padding:var(--sp-3) 0;}
.toolbar .wrap{display:flex; align-items:center; gap:var(--sp-2); flex-wrap:wrap;}
.chip{display:inline-flex; align-items:center; gap:var(--sp-2);
  min-height:38px; padding:0 var(--sp-3);
  border:1px solid var(--border); border-radius:var(--r);
  font-size:13px; font-weight:700; text-decoration:none; color:var(--text);
  transition:border-color 180ms ease,background 180ms ease;}
.chip span{font-size:11px; font-weight:400; color:var(--dark);
  background:var(--warm); border-radius:9px; padding:1px 7px;}
.chip:hover{background:rgba(186,184,172,.12); border-color:var(--border-strong);}
.chip[data-empty]{opacity:.35;}
.switch{margin-left:auto;}

.search{position:relative; display:flex; align-items:center; margin-right:var(--sp-2);}
.search > svg{position:absolute; left:11px; width:16px; height:16px; color:var(--text-dim); pointer-events:none;}
.search input{width:240px; height:38px; padding:0 38px 0 34px;
  font-family:inherit; font-size:14px; color:var(--text);
  background:var(--dark-alt); border:1px solid var(--border);
  border-radius:var(--r); transition:border-color 180ms ease;}
.search input::placeholder{color:var(--text-dim);}
.search input:hover{border-color:var(--border-strong);}
.search input:focus{outline:none; border-color:var(--primary);}
.search input:focus-visible{outline:none;}
.search input::-webkit-search-cancel-button{-webkit-appearance:none; appearance:none;}
.search .clear{position:absolute; right:2px; display:flex; align-items:center; justify-content:center;
  width:34px; height:34px; padding:0; background:none; border:0; border-radius:var(--r);
  color:var(--text-dim); cursor:pointer;}
.search .clear svg{width:15px; height:15px;}
.search .clear:hover{color:var(--text); background:rgba(186,184,172,.12);}
@media (max-width:700px){ .search{width:100%; margin-right:0;} .search input{width:100%;} }

.empty{margin:var(--sp-12) 0; padding:var(--sp-8);
  border:1px dashed var(--border-strong); border-radius:var(--r-lg);
  text-align:center; color:var(--text-dim); font-size:15px;}
.empty b{color:var(--text);}
.linkish{font:inherit; color:var(--primary); background:none; border:0; padding:0;
  text-decoration:underline; cursor:pointer;}

/* While a search is running the intro and the notes are about the whole set,
   not the handful on screen, so they get out of the way. */
body.is-filtering .hero,
body.is-filtering .flags{display:none;}
body.is-filtering .region:first-of-type{margin-top:var(--sp-8);}

.region{margin:var(--sp-12) 0;}
.region-head{display:flex; align-items:baseline; gap:var(--sp-4);
  padding-bottom:var(--sp-3); margin-bottom:var(--sp-6);
  border-bottom:1px solid var(--border-strong);}
.region-head h2{font-size:22px; letter-spacing:-.01em;}
.region-head .count{font-size:12px; letter-spacing:.1em; text-transform:uppercase; color:var(--text-dim);}

.card{border:1px solid var(--border); border-radius:var(--r-lg);
  background:var(--surface); overflow:hidden; margin-bottom:var(--sp-4);}
.card-head{display:flex; align-items:flex-start; gap:var(--sp-4); flex-wrap:wrap;
  padding:var(--sp-4); border-bottom:1px solid var(--border);}
.who{min-width:0;}
.who h3{font-size:17px;}
.who .role{margin:var(--sp-1) 0 0; font-size:11px; letter-spacing:.11em;
  text-transform:uppercase; color:var(--secondary);}
.who .mail{margin:var(--sp-1) 0 0; font-size:13px; color:var(--text-dim);}
.who .mail a{text-decoration:none;}
.who .mail a:hover{text-decoration:underline;}
.card-actions{margin-left:auto; display:flex; gap:var(--sp-2); flex-wrap:wrap;}

/* One switch flips every preview, so all 63 can be scanned in either mode. */
body.dark-preview .card .pane-body{background:#121212;}
body.dark-preview .card .pane-body span[style*="color: black"],
body.dark-preview .card .pane-body a[style*="#333333"]{color:#f4f2ee !important;}

@media (max-width:560px){ .toolbar{position:static;} .card-actions{margin-left:0; width:100%;} }
"""

INDEX_JS = """
/* ---------------------------- name search --------------------------------
   63 cards is far more than fits on a screen, so the toolbar filters them in
   place. Every token in the query has to match somewhere in the card's
   data-search string, which means "van niek" finds Gerrie van Niekerk without
   the words having to be adjacent. */
var q = document.getElementById("q");
var qClear = document.getElementById("q-clear");
var cards = Array.prototype.slice.call(document.querySelectorAll(".card[data-search]"));
var sections = Array.prototype.slice.call(document.querySelectorAll(".region[data-region]"));
var chips = Array.prototype.slice.call(document.querySelectorAll("[data-chip]"));
var empty = document.getElementById("empty");
var emptyQ = document.getElementById("empty-q");

function applyFilter(){
  var terms = q.value.toLowerCase().split(/\\s+/).filter(Boolean);
  var total = 0;
  document.body.classList.toggle("is-filtering", terms.length > 0);

  cards.forEach(function(card){
    var hay = card.getAttribute("data-search");
    var hit = terms.every(function(t){ return hay.indexOf(t) !== -1; });
    card.hidden = !hit;
    if(hit) total++;
  });

  // A region with nothing left disappears, and its heading count and nav chip
  // report what is actually showing.
  sections.forEach(function(section){
    var shown = section.querySelectorAll(".card:not([hidden])").length;
    section.hidden = shown === 0;
    var count = section.querySelector("[data-count]");
    var all = Number(count.getAttribute("data-total"));
    count.textContent = terms.length && shown !== all
      ? shown + " of " + all
      : all + (all === 1 ? " signature" : " signatures");
    var chip = chips.filter(function(c){ return c.getAttribute("data-chip") === section.getAttribute("data-region"); })[0];
    if(chip){
      chip.querySelector("[data-chip-count]").textContent = shown;
      if(shown === 0) chip.setAttribute("data-empty", "");
      else chip.removeAttribute("data-empty");
    }
  });

  empty.hidden = total !== 0;
  emptyQ.textContent = q.value.trim();
  qClear.hidden = q.value === "";
  announce(terms.length
    ? total + (total === 1 ? " signature matches " : " signatures match ") + q.value.trim()
    : "Showing all " + total + " signatures.");
}

function clearSearch(){ q.value = ""; applyFilter(); q.focus(); }
q.addEventListener("input", applyFilter);
q.addEventListener("keydown", function(ev){
  if(ev.key === "Escape" && q.value !== ""){ ev.preventDefault(); clearSearch(); }
});
qClear.addEventListener("click", clearSearch);
document.getElementById("empty-clear").addEventListener("click", clearSearch);

/* "/" jumps to the field, the way it does in most list UIs. */
document.addEventListener("keydown", function(ev){
  if(ev.key !== "/" || ev.metaKey || ev.ctrlKey || ev.altKey) return;
  var el = document.activeElement;
  if(el && /^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName)) return;
  ev.preventDefault(); q.focus(); q.select();
});

var toggle = document.getElementById("theme-toggle");
var ICON_SUN = "%SUN%";
var ICON_MOON = "%MOON%";
toggle.addEventListener("click", function(){
  var dark = document.body.classList.toggle("dark-preview");
  toggle.setAttribute("aria-pressed", String(dark));
  toggle.innerHTML = (dark ? ICON_SUN : ICON_MOON) +
    "<span>" + (dark ? "Light" : "Dark") + " preview</span>";
  announce("Previews switched to " + (dark ? "dark" : "light") + " mode.");
});
""".replace("%SUN%", ui.SUN.replace('"', '\\"')).replace("%MOON%", ui.MOON.replace('"', '\\"'))


def esc(s): return html.escape(s or "", quote=True)

people = json.load(open("generator/people.json"))

# --- the notes worth reading before this goes out -------------------------
by_mail = collections.defaultdict(list)
for p in people:
    by_mail[p["email"].lower()].append(p)
twins = {k: v for k, v in by_mail.items() if len(v) > 1}
no_phone = [p for p in people if not p["phone"]]

flags = []
if twins:
    pairs = "; ".join("%s &amp; %s" % (esc(v[0]["name"]), esc(v[1]["name"])) for v in twins.values())
    flags.append((
        "Five people have two pages each &mdash; %d of the 63" % sum(len(v) for v in twins.values()),
        "%s. Each pair shares one address and one headshot, so they are name variants, not "
        "different people. Send each person the one spelling they actually use, and delete the "
        "other page once that is settled." % pairs))
if no_phone:
    flags.append((
        "Empty phone link &mdash; %s" % ", ".join(esc(p["name"]) for p in no_phone),
        "the signature carries a phone row whose link is <code>tel:</code> with nothing after it, "
        "so it renders as a clickable icon that dials nothing. Either fill the number in or drop "
        "the row."))
flags.append((
    "One stale copy was left behind",
    "the old repo kept a second set of 56 pages under <code>signature-generator/signatures/</code>. "
    "It was not carried over: it had a broken <code>src=\"undefined\"</code> on Owen Korinek and "
    "still showed Mia Pitino's previous headshot."))

# --- regions ---------------------------------------------------------------
order = ["United States", "South Africa"]
groups = collections.OrderedDict((r, []) for r in order)
for p in sorted(people, key=lambda x: x["name"]):
    groups[p["region"]].append(p)

chips, sections = [], []
for region, members in groups.items():
    rid = "us" if region == "United States" else "south-africa"
    chips.append('      <a class="chip" href="#%s" data-chip="%s">%s<span data-chip-count>%d</span></a>'
                 % (rid, rid, esc(region), len(members)))
    cards = []
    for p in members:
        slug = p["file"][:-5]
        hay = " ".join([p["name"], p["role"], p["email"], region]).lower()
        cards.append("""    <article class="card" data-search="{hay}">
      <div class="card-head">
        <div class="who">
          <h3>{name}</h3>
          <p class="role">{role}</p>
          <p class="mail"><a href="mailto:{email}">{email}</a></p>
        </div>
        <div class="card-actions">
          <button class="btn btn-primary btn-sm" data-copy="sig-{slug}">{copy}<span>Copy</span></button>
          <button class="btn btn-sm" data-link="{url}" title="{url}">{link}<span>Link</span></button>
          <a class="btn btn-sm" href="{file}">{open}<span>Page</span></a>
        </div>
      </div>
      <div class="pane-body">
<div id="sig-{slug}">{sig}</div>
      </div>
    </article>""".format(hay=esc(hay), name=esc(p["name"]), role=esc(p["role"]),
                         email=esc(p["email"]), slug=esc(slug), file=esc(p["file"]),
                         url=BASE + slug + ".html", sig=p["sig"],
                         copy=ui.COPY, link=ui.LINK, open=ui.OPEN))
    sections.append("""  <section class="region" id="{rid}" data-region="{rid}">
    <div class="region-head">
      <h2>MAG {region}</h2>
      <span class="count" data-count data-total="{n}">{n} signatures</span>
    </div>
{cards}
  </section>""".format(rid=rid, region=esc(region), n=len(members), cards="\n".join(cards)))

flag_items = "\n".join(
    '      <li><b>%s</b><span class="why">%s</span></li>' % (t, w) for t, w in flags)

doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MAG Email Signatures</title>
<meta name="robots" content="noindex">
<style>{fonts}{css}</style>
</head>
<body>
<header class="topbar">
  <div class="wrap">
    <a class="mark" href="https://magneticcreative.com" target="_blank" rel="noopener">Mag<b>.</b></a>
    <span class="sep" aria-hidden="true"></span>
    <span class="ctx">Email signatures &middot; Master</span>
    <span class="grow"></span>
  </div>
</header>

<div class="toolbar">
  <div class="wrap">
      <div class="search">
        {search}
        <label class="sr-only" for="q">Search signatures by name</label>
        <input id="q" type="search" autocomplete="off" spellcheck="false"
               placeholder="Search by name&hellip;" aria-describedby="q-hint">
        <button type="button" class="clear" id="q-clear" hidden aria-label="Clear search">{x}</button>
      </div>
      <p id="q-hint" class="sr-only">Also matches job title, email address and region. Press slash to focus, Escape to clear.</p>
{chips}
      <button class="btn btn-sm switch" id="theme-toggle" aria-pressed="false">{moon}<span>Dark preview</span></button>
  </div>
</div>

<main class="wrap">
  <div class="hero">
    <span class="eyebrow">Master list</span>
    <h1>MAG email signatures</h1>
    <p>All {total} signatures, rendered from the exact markup each person's page copies.
       Flip the preview to dark to check the inversion, hit <b>Copy</b> on any card to put
       that one on the clipboard, or send someone <b>Link</b> and let them follow the
       Gmail walk-through on their own page.</p>
  </div>

  <details class="flags" open>
    <summary>{alert}<span>{nflags} things to look at before sign-off</span></summary>
    <ul>
{flag_items}
    </ul>
  </details>

{sections}

  <p class="empty" id="empty" hidden>No signature matches <b id="empty-q"></b>.
     Check the spelling, or <button type="button" class="linkish" id="empty-clear">clear the search</button>.</p>
</main>

<footer class="wrap">
  <p>Published at <a href="{base}"><code>{base}</code></a> &mdash; each person's link is that
     plus their file name, e.g. <code>Gabriel_Arias.html</code>.</p>
  <p>Rebuild with <code>python3 generator/extract.py &amp;&amp; python3 generator/build-person.py &amp;&amp; python3 generator/build-index.py</code>.</p>
  <p>Images load from <code>cdn.jsdelivr.net/gh/magn3tic/mag-signatures@v1.0.0</code>, pinned to the
     tag, so this page renders exactly what gets pasted.</p>
</footer>

<div id="live" class="sr-only" role="status" aria-live="polite"></div>
<script>{js}{indexjs}</script>
</body>
</html>
""".format(fonts=theme.FONTS, base=BASE, css=theme.BASE + INDEX_CSS,
           js=ui.CLIPBOARD_JS, indexjs=INDEX_JS, total=len(people),
           search=ui.SEARCH, x=ui.X, moon=ui.MOON, alert=ui.ALERT,
           nflags=len(flags), flag_items=flag_items,
           chips="\n".join(chips), sections="\n\n".join(sections))

open("pages/index.html", "w", encoding="utf-8").write(doc)
print("index.html: %d cards, %d regiones, %d avisos, %.0f KB"
      % (len(people), len(groups), len(flags), len(doc) / 1024))
