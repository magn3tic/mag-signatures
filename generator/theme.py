"""The MAG design system, shared by the index and the 63 person pages.

Same tokens as the SleepOver signature pages -- Aeonik and Fragment off
magneticcreative.com, the #d53703 primary and the #b59756 gold that the
signatures themselves use for the job title.
"""

FONTS = """
@font-face{font-family:Aeonik;font-style:normal;font-weight:400;font-display:swap;
  src:url(https://magneticcreative.com/hubfs/2023-web/fonts/Aeonik-Regular.woff2) format("woff2"),url(https://magneticcreative.com/hubfs/2023-web/fonts/Aeonik-Regular.woff) format("woff");}
@font-face{font-family:Aeonik;font-style:normal;font-weight:700;font-display:swap;
  src:url(https://magneticcreative.com/hubfs/2023-web/fonts/Aeonik-Bold.woff2) format("woff2"),url(https://magneticcreative.com/hubfs/2023-web/fonts/Aeonik-Bold.woff) format("woff");}
@font-face{font-family:Fragment;font-style:normal;font-weight:400;font-display:swap;
  src:url(https://magneticcreative.com/hubfs/2023-web/fonts/PPFragment-GlareRegular.woff2) format("woff2"),url(https://magneticcreative.com/hubfs/2023-web/fonts/PPFragment-GlareRegular.woff) format("woff");}
"""

BASE = """
:root{
  --dark:#232323; --dark-alt:#323232; --primary:#d53703;
  --secondary:#b59756; --warm:#bab8ac; --light:#ffffff;
  --light-alt:#f2f2f2; --gray-light:#d9d9d9;
  --surface:#2b2b2b; --border:rgba(186,184,172,.22); --border-strong:rgba(186,184,172,.38);
  --text:#f4f2ee; --text-dim:#a8a5a0;
  --r:4px; --r-lg:8px;
  --sp-1:4px; --sp-2:8px; --sp-3:12px; --sp-4:16px; --sp-6:24px; --sp-8:32px; --sp-12:48px;
}
*,*::before,*::after{box-sizing:border-box;}
html{-webkit-text-size-adjust:100%;}
body{
  margin:0; background:var(--dark); color:var(--text);
  font-family:Aeonik,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  font-size:16px; line-height:1.55; -webkit-font-smoothing:antialiased;
}
a{color:inherit;}
h1,h2,h3{margin:0; font-weight:700; line-height:1.15;}
:focus-visible{outline:2px solid var(--primary); outline-offset:3px; border-radius:2px;}

.wrap{max-width:1080px; margin:0 auto; padding:0 var(--sp-6);}
.topbar{border-bottom:1px solid var(--border); background:var(--dark); position:sticky; top:0; z-index:40;}
.topbar .wrap{display:flex; align-items:center; gap:var(--sp-4); min-height:64px;}
.mark{
  font-family:Fragment,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  font-size:19px; letter-spacing:.14em; text-transform:uppercase; text-decoration:none; white-space:nowrap;
}
.mark b{color:var(--primary); font-weight:400;}
.topbar .sep{width:1px; align-self:stretch; margin:14px 0; background:var(--border);}
.topbar .ctx{font-size:12px; letter-spacing:.1em; text-transform:uppercase; color:var(--text-dim);
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap;}
.topbar .grow{margin-left:auto;}
.topbar .btn{white-space:nowrap;}
@media (max-width:560px){ .topbar .ctx,.topbar .sep{display:none;} }

.btn{
  display:inline-flex; align-items:center; justify-content:center; gap:var(--sp-2);
  min-height:44px; padding:0 var(--sp-4);
  font-family:inherit; font-size:14px; font-weight:700; letter-spacing:.02em;
  border:1px solid var(--border-strong); border-radius:var(--r);
  background:transparent; color:var(--text); text-decoration:none;
  cursor:pointer; transition:background 180ms ease,color 180ms ease,border-color 180ms ease;
}
.btn svg{width:17px; height:17px; flex:none;}
.btn:hover{background:rgba(186,184,172,.12);}
.btn:active{transform:translateY(1px);}
.btn-primary{background:var(--primary); border-color:var(--primary); color:#fff;}
.btn-primary:hover{background:#ef4109; border-color:#ef4109;}
.btn-sm{min-height:38px; padding:0 var(--sp-3); font-size:13px;}
.btn-sm svg{width:15px; height:15px;}
.btn.is-done{background:var(--secondary); border-color:var(--secondary); color:var(--dark);}
.btn.is-done:hover{background:var(--secondary);}
.btn.is-failed{background:transparent; border-color:var(--primary); color:var(--primary);}

.pane{border:1px solid var(--border); border-radius:var(--r-lg); overflow:hidden; background:var(--surface);}
.pane-head{
  display:flex; align-items:center; gap:var(--sp-2);
  padding:var(--sp-2) var(--sp-3); border-bottom:1px solid var(--border);
  font-size:11px; letter-spacing:.11em; text-transform:uppercase; color:var(--text-dim);
}
.pane-head svg{width:14px; height:14px; flex:none;}
.pane-body{overflow-x:auto; padding:var(--sp-4) var(--sp-2); background:#fff;}
.pane-body > div{width:max-content; margin:0 auto;}
/* Imitates the client-side inversion: black type comes back near-white, the
   gold job title survives, images are left alone. Preview only -- these rules
   live in the page, never in the copied markup. */
.pane-dark .pane-body{background:#121212;}
.pane-dark .pane-body span[style*="color: black"],
.pane-dark .pane-body a[style*="#333333"]{color:#f4f2ee !important;}
.note{margin:var(--sp-3) 0 0; font-size:13px; line-height:1.5; color:var(--text-dim); max-width:76ch;}

.eyebrow{display:inline-block; margin-bottom:var(--sp-3); font-size:11px;
  letter-spacing:.16em; text-transform:uppercase; color:var(--secondary);}

.flags{border:1px solid var(--border); border-left:3px solid var(--secondary);
  border-radius:var(--r); background:rgba(181,151,86,.07); margin:var(--sp-6) 0;}
.flags summary{display:flex; align-items:center; gap:var(--sp-2); cursor:pointer;
  padding:var(--sp-3) var(--sp-4); font-size:14px; font-weight:700; list-style:none;}
.flags summary::-webkit-details-marker{display:none;}
.flags summary svg{width:16px; height:16px; color:var(--secondary); flex:none;}
.flags ul{margin:0; padding:0 var(--sp-6) var(--sp-4) 40px; font-size:14px; line-height:1.6;}
.flags li{margin-bottom:var(--sp-4);}
.flags li:last-child{margin-bottom:0;}
.flags b{color:var(--secondary);}
.flags .why{display:block; margin-top:2px; font-size:13px; color:var(--text-dim); max-width:76ch;}

footer{border-top:1px solid var(--border); padding:var(--sp-8) 0 var(--sp-12);
  color:var(--text-dim); font-size:13px;}
footer p{margin:0 0 var(--sp-2); max-width:76ch;}
footer code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; font-size:12px; color:var(--warm);}

.sr-only{position:absolute; width:1px; height:1px; padding:0; margin:-1px;
  overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; border:0;}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{transition-duration:.01ms !important; animation-duration:.01ms !important;}
}
"""
