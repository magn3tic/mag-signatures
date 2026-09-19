"""Reads the 63 legacy pages and pulls out the one thing that matters: the
signature markup, plus the handful of fields the new pages label it with."""
import json, os, re, html

PAGES = "pages"

def field(pat, s, flags=re.S):
    m = re.search(pat, s, flags)
    return html.unescape(m.group(1)).strip() if m else ""

def extract(path):
    s = open(path, encoding="utf-8").read()
    sig = field(r'<div id="content">(.*?)\n</div>', s)
    if not sig:
        raise ValueError(f"{path}: no #content")
    return {
        "file":   os.path.basename(path),
        "name":   field(r"<title>(.*?)(?:\s*-\s*Signature)?</title>", s),
        "role":   field(r'<span style="color: #b59756;">(.*?)</span>', sig),
        "email":  field(r'href="mailto:([^"]+)"', sig),
        "phone":  field(r'href="tel:([^"]+)"', sig),
        "site":   field(r'href="(https://magneticcreative\.com/?)"', sig),
        "photo":  field(r'<img src="([^"]+)" alt=', sig),
        "sig":    sig.strip(),
    }

rows = [extract(os.path.join(PAGES, f)) for f in sorted(os.listdir(PAGES)) if f.endswith(".html")]
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
