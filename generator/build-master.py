"""Writes the master list of who has a signature, as .xlsx and .csv.

This is the sheet to work from when someone leaves: set Status to Remove,
then run generator/remove.py to delete their page and rebuild the index.
"""
import csv, json, collections, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

BASE = "https://magn3tic.github.io/mag-signatures/pages/"
XLSX = "MAG-signatures-master.xlsx"

def previous_status():
    """A rebuild must not wipe the column people actually fill in, so whatever
       is already in the sheet is read back and re-applied by page name."""
    if not os.path.exists(XLSX):
        return {}
    from openpyxl import load_workbook
    ws = load_workbook(XLSX, data_only=True)["Signatures"]
    head = [c.value for c in ws[1]]
    i_st, i_pg = head.index("Status"), head.index("Page")
    return {r[i_pg]: (r[i_st] or "") for r in ws.iter_rows(min_row=2, values_only=True) if r[i_pg]}

KEPT = previous_status()
people = sorted(json.load(open("generator/people.json")), key=lambda p: (p["region"], p["name"]))

# Same address twice means one person with two spellings of their name, not two
# people -- worth saying out loud on the row, since one of the pair has to go.
by_mail = collections.defaultdict(list)
for p in people:
    by_mail[p["email"].lower()].append(p)

def notes(p):
    out = []
    twins = [q for q in by_mail[p["email"].lower()] if q is not p]
    if twins:
        out.append("Same address and headshot as " + ", ".join(t["name"] for t in twins)
                   + " - one of these pages should go")
    if not p["phone"]:
        out.append("Phone row links to an empty tel: - fill it in or drop the row")
    return "; ".join(out)

HEAD = ["Status", "Name", "Role", "Email", "Phone", "Region",
        "Page", "Page URL", "Headshot", "Notes"]

rows = [[
    KEPT.get(p["file"], ""), p["name"], p["role"], p["email"], p["phone"] or "", p["region"],
    p["file"], BASE + p["file"], p["photo"].rsplit("/", 1)[-1], notes(p),
] for p in people]

# ---- csv -----------------------------------------------------------------
with open("MAG-signatures-master.csv", "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh)
    w.writerow(HEAD)
    w.writerows(rows)

# ---- xlsx ----------------------------------------------------------------
DARK  = "FF232323"
GOLD  = "FFB59756"
LIGHT = "FFF2F2F2"

wb = Workbook()
ws = wb.active
ws.title = "Signatures"

ws.append(HEAD)
for r in rows:
    ws.append(r)

hdr_fill = PatternFill("solid", fgColor=DARK)
hdr_font = Font(bold=True, color="FFFFFFFF", size=11)
thin = Side(style="thin", color="FFD9D9D9")
for c in ws[1]:
    c.fill, c.font = hdr_fill, hdr_font
    c.alignment = Alignment(vertical="center")
ws.row_dimensions[1].height = 24

widths = {"Status": 11, "Name": 26, "Role": 32, "Email": 26, "Phone": 18,
          "Region": 15, "Page": 30, "Page URL": 46, "Headshot": 40, "Notes": 72}
for i, h in enumerate(HEAD, 1):
    ws.column_dimensions[get_column_letter(i)].width = widths[h]

note_col = HEAD.index("Notes") + 1
url_col  = HEAD.index("Page URL") + 1
for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
    for c in row:
        c.border = Border(bottom=thin)
        c.alignment = Alignment(vertical="top", wrap_text=(c.column == note_col))
    row[note_col - 1].font = Font(color="FF8A6D2F", size=10)
    if row[note_col - 1].value:
        for c in row:
            c.fill = PatternFill("solid", fgColor="FFFDF8EC")
    u = row[url_col - 1]
    u.hyperlink, u.style = u.value, "Hyperlink"

# Status is the column people actually fill in, so it gets a dropdown rather
# than free text -- remove.py matches on the exact word.
dv = DataValidation(type="list", formula1='"Keep,Remove"', allow_blank=True,
                    showDropDown=False, promptTitle="Status",
                    prompt="Leave blank or Keep to publish. Remove deletes the page on the next build.")
ws.add_data_validation(dv)
dv.add("A2:A%d" % ws.max_row)
for r in range(2, ws.max_row + 1):
    ws.cell(r, 1).alignment = Alignment(horizontal="center", vertical="top")

ws.freeze_panes = "B2"
ws.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(HEAD)), ws.max_row)

# ---- a short readme tab, so the file explains itself --------------------
doc = wb.create_sheet("How to use")
doc.column_dimensions["A"].width = 100
lines = [
    ("MAG email signatures - master list", True),
    ("", False),
    ("Every person who currently has a signature page. %d rows." % len(rows), False),
    ("", False),
    ("Someone left the company", True),
    ("Set their Status to Remove, save the file, and run:", False),
    ("    python3 generator/remove.py", False),
    ("That deletes pages/<their file>.html and rebuilds index.html. Their headshot", False),
    ("is left in images/ on purpose - old emails already sent still load it.", False),
    ("", False),
    ("Someone's details changed", True),
    ("Editing this sheet does not change a signature. The signature markup lives in", False),
    ("the page itself. Change it there, or send the new details to whoever rebuilds.", False),
    ("", False),
    ("The highlighted rows", True),
    ("Rows tinted cream have something in Notes worth resolving - a duplicate page,", False),
    ("or a phone row that links nowhere.", False),
    ("", False),
    ("This file is generated", True),
    ("python3 generator/build-master.py overwrites it. Statuses you have typed are", False),
    ("read first and carried over, so a rebuild does not lose your work.", False),
]
for i, (text, bold) in enumerate(lines, 1):
    c = doc.cell(i, 1, text)
    c.font = Font(bold=bold, size=12 if bold else 11,
                  color=DARK if bold else "FF444444")

wb.save("MAG-signatures-master.xlsx")

flagged = sum(1 for r in rows if r[-1])
carried = sum(1 for r in rows if r[0])
print("MAG-signatures-master.xlsx + .csv: %d filas, %d con notas, %d Status conservados"
      % (len(rows), flagged, carried))
