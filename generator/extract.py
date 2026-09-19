"""Reads the 63 legacy pages and pulls out the one thing that matters: the
signature markup, plus the handful of fields the new pages label it with."""
import json, os, re, html

PAGES = "pages"

def field(pat, s, flags=re.S):
    m = re.search(pat, s, flags)
    return html.unescape(m.group(1)).strip() if m else ""


def content_div(s):
    """The signature sits in <div id="content">, and it contains nested divs of
       its own, so the closing tag has to be found by counting rather than by a
       lazy regex. The generated pages wrap it one level deeper than the pages
       this was first written against, which a regex got wrong."""
    open_tag = '<div id="content">'
    i = s.find(open_tag)
    if i == -1:
        return ""
    start = i + len(open_tag)
    depth, j = 1, start
    for m in re.finditer(r'<div\b[^>]*>|</div\s*>', s[start:]):
        depth += 1 if m.group(0).startswith("<div") else -1
        if depth == 0:
            j = start + m.start()
            break
    else:
        return ""
    return s[start:j]

def person_name(s):
    """Titles have read two ways over the life of these pages -- the original
       "Name - Signature" and the current "Name - MAG email signature" with an
       em dash. Both are the name up to the first dash separator."""
    title = field(r"<title>(.*?)</title>", s)
    return re.split(r"\s+[\u2013\u2014-]\s+", title)[0].strip()


def extract(path):
    s = open(path, encoding="utf-8").read()
    sig = content_div(s)
    if not sig:
        raise ValueError(f"{path}: no #content")
    return {
        "file":   os.path.basename(path),
        "name":   person_name(s),
        "role":   field(r'<span style="color: #b59756;">(.*?)</span>', sig),
        "email":  field(r'href="mailto:([^"]+)"', sig),
        "phone":  field(r'href="tel:([^"]+)"', sig),
        "site":   field(r'href="(https://magneticcreative\.com/?)"', sig),
        "photo":  field(r'<img src="([^"]+)" alt=', sig),
        "sig":    sig.strip(),
    }

# index.html is generated from these, not one of them.
rows = [extract(os.path.join(PAGES, f)) for f in sorted(os.listdir(PAGES))
        if f.endswith(".html") and f != "index.html"]
for r in rows:
    p = r["photo"]
    r["region"] = "United States" if "/headshots/us/" in p else "South Africa"
    r["slug"] = "us" if r["region"] == "United States" else "south-africa"

json.dump(rows, open("generator/people.json", "w"), indent=2, ensure_ascii=False)
print(f"{len(rows)} paginas leidas")
missing = {k: [r["name"] for r in rows if not r[k]] for k in ("name","role","email","phone","photo")}
for k, v in missing.items():
    print(f"  sin {k}: {len(v)}" + (f"  -> {v}" if v and len(v) <= 6 else ""))
from collections import Counter
print(" ", Counter(r["region"] for r in rows))
