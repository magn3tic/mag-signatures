"""Inline SVG icons and the clipboard script shared by every generated page."""

def icon(paths, w=1.8):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (w, paths))

COPY  = icon('<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>')
DOWN  = icon('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/>')
LINK  = icon('<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>')
OPEN  = icon('<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>')
BACK  = icon('<path d="M19 12H5"/><path d="m12 19-7-7 7-7"/>')
SUN   = icon('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>')
MOON  = icon('<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9"/>')
ALERT = icon('<path d="m21.7 18-8-14a2 2 0 0 0-3.4 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.7-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>')
SEARCH= icon('<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>')
X     = icon('<path d="M18 6 6 18M6 6l12 12"/>', 2)
LIGHT = icon('<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2"/>')
DARKI = icon('<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9"/>')

# The two icons the script swaps in are built here so the escaping is done once.
CHECK_JS = icon('<path d="M20 6 9 17l-5-5"/>', 2.2).replace('"', '\\"')
ALERT_JS = ALERT.replace('"', '\\"')

CLIPBOARD_JS = """
var ICON_CHECK = "%s";
var ICON_ALERT = "%s";
/*
 * Rich-HTML copy. navigator.clipboard.write is the correct path but it needs a
 * secure context, so a selection-based execCommand("copy") stands behind it --
 * that one also works from file://, which is how these pages sometimes get
 * opened.
 */
async function copyRichHtml(html){
  try{
    if(navigator.clipboard && window.ClipboardItem && window.isSecureContext){
      await navigator.clipboard.write([new ClipboardItem({
        "text/html": new Blob([html], {type:"text/html"}),
        "text/plain": new Blob([htmlToText(html)], {type:"text/plain"})
      })]);
      return true;
    }
  }catch(e){ /* fall through to the selection path */ }

  var host = document.createElement("div");
  host.setAttribute("contenteditable", "true");
  host.style.cssText = "position:fixed;left:-9999px;top:0;white-space:normal;";
  host.innerHTML = html;
  document.body.appendChild(host);
  try{
    var range = document.createRange();
    range.selectNodeContents(host);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    var ok = document.execCommand("copy");
    sel.removeAllRanges();
    return ok;
  }catch(e){ return false; }
  finally{ document.body.removeChild(host); }
}

function htmlToText(html){
  var d = document.createElement("div");
  d.innerHTML = html;
  return (d.innerText || d.textContent || "").replace(/\\n{3,}/g, "\\n\\n").trim();
}

/* Button feedback in place of an alert(): the label carries the result and an
   aria-live region announces it, so nothing has to be dismissed. */
function flashButton(btn, ok, okLabel){
  if(btn.dataset.busy === "1") return;
  var original = btn.innerHTML;
  btn.dataset.busy = "1";
  btn.classList.add(ok ? "is-done" : "is-failed");
  btn.innerHTML = (ok ? ICON_CHECK : ICON_ALERT) +
    "<span>" + (ok ? (okLabel || "Copied") : "Copy failed") + "</span>";
  announce(ok ? (okLabel || "Signature") + " copied to the clipboard."
              : "Copy failed. Select the signature and copy it by hand.");
  setTimeout(function(){
    btn.innerHTML = original;
    btn.classList.remove("is-done", "is-failed");
    btn.dataset.busy = "0";
  }, 2200);
}

function announce(msg){
  var live = document.getElementById("live");
  if(live) live.textContent = msg;
}

function downloadHtm(html, filename){
  var doc = '<!DOCTYPE html><html><head><meta charset="utf-8">' +
            '<meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>' +
            '<body style="margin:0;">' + html + '</body></html>';
  var url = URL.createObjectURL(new Blob([doc], {type:"text/html"}));
  var a = document.createElement("a");
  a.href = url; a.download = filename; a.click();
  URL.revokeObjectURL(url);
}

async function copyText(text){
  try{
    if(navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext){
      await navigator.clipboard.writeText(text);
      return true;
    }
  }catch(e){ /* fall through */ }
  var ta = document.createElement("textarea");
  ta.value = text;
  ta.style.cssText = "position:fixed;left:-9999px;top:0;";
  document.body.appendChild(ta);
  ta.select();
  try{ return document.execCommand("copy"); }
  catch(e){ return false; }
  finally{ document.body.removeChild(ta); }
}

/* data-copy / data-download carry the id of the wrapper holding the signature.
   Image URLs are already absolute, so the markup ships as-is. */
document.addEventListener("click", function(ev){
  var btn = ev.target.closest("[data-copy]");
  if(btn){
    var src = document.getElementById(btn.getAttribute("data-copy"));
    if(src) copyRichHtml(src.innerHTML).then(function(ok){ flashButton(btn, ok); });
    return;
  }
  var dl = ev.target.closest("[data-download]");
  if(dl){
    var node = document.getElementById(dl.getAttribute("data-download"));
    if(node) downloadHtm(node.innerHTML, dl.getAttribute("data-filename"));
    return;
  }
  var lk = ev.target.closest("[data-link]");
  if(lk) copyText(lk.getAttribute("data-link")).then(function(ok){ flashButton(lk, ok, "Link copied"); });
});
""" % (CHECK_JS, ALERT_JS)
