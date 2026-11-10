"""Build index.html = YCE homepage snapshot + logged-in header + IAP popup.

    python3 src/build.py
"""
import pathlib
import re

SRC = pathlib.Path(__file__).parent
ROOT = SRC.parent
snapshot = (SRC / 'yce-home-snapshot.html').read_text(encoding='utf-8')

HEAD = '''
<!-- ════════ PROTOTYPE additions ════════ -->
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
<style>
  /* Site fonts served locally (the CDN blocks cross-origin font loads from other hosts) */
  @font-face{font-family:icomoon;src:url(assets/icomoon.2f460d1c.ttf) format("truetype"),url(assets/icomoon.0fe901ea.woff) format("woff");font-weight:400;font-style:normal;font-display:block}
  @font-face{font-family:Roboto-Asterisk;font-style:normal;font-weight:400;src:url(assets/Roboto-Asterisk.df2a51a3.ttf) format("truetype")}

  /* Logged-in header, built from the site's own CSS-module classes */
  .proto-dt-header { display:none !important; }
  .proto-header .general-pricing_pricing__ph_6z { gap:0; }
  .proto-avatar { position:relative; display:flex; align-items:center; cursor:pointer; }
  .proto-avatar .color-button_redDot__6SryS { top:-2px; right:-6px; }
  @media (max-width: 768px) { .proto-header .general-pricing_productText__IKebq { display:none; } }
</style>
'''

A = 'https://yce.perfectcorp.com/assets/images'
HEADER = (
    '<div class="headers_container__LC81Q proto-header">'
    f'<button class="headers_menuIcon__DJuXY" style="background-image: url(&quot;{A}/header/icon_menu.svg&quot;);" aria-label="Menu"></button>'
    f'<a draggable="false" class="logo_logoContainer__oDp91" href="https://yce.perfectcorp.com/"><img class="logo_symbol__7aD8E" src="{A}/logo/logo_symbol.svg" alt="YCE Icon" draggable="false">'
    f'<picture><source media="(max-width: 768px)" srcset="{A}/logo/logo_YC_OnlineEditor_d_ENU_mb.svg"><img class="logo_logo__IAh9T" src="{A}/logo/logo_YC_OnlineEditor_d_ENU_dt.svg" alt="YCE Logo" draggable="false"></picture></a>'
    '<div class="headers_buttonsContainer__1E__h">'
    f'<div class="general-pricing_pricing__ph_6z proto-subscribe-trigger" role="button" tabindex="0" aria-label="Subscribe"><img class="general-pricing_productIcon__DNoNJ" src="{A}/header/icon_pricing_mb.svg" alt=""><span class="general-pricing_productText__IKebq">Subscribe</span></div>'
    f'<div class="proto-avatar" aria-label="Account"><img class="color-button_iconProfile__x86o_" src="{A}/header/icon_profile.svg" alt=""><span class="color-button_redDot__6SryS"></span></div>'
    '</div></div>'
)

TRIGGER = '''
<script>
  document.querySelectorAll('.proto-subscribe-trigger').forEach(function (el) {
    el.addEventListener('click', function (e) { e.preventDefault(); openIAP(); });
    el.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openIAP(); } });
  });
  // Prototype opens straight into the popup; closing it and tapping Subscribe brings it back
  openIAP();
</script>
'''

# Holiday theme switcher (bottom-right) for reviewing the holiday UIs.
# Hidden by default: the page always shows the default popup. Add ?review=1 to the URL to get the switcher and the
# holiday themes (?review=1&holiday=christmas opens a theme directly). Sets data-holiday on #iapOverlay ("" = default).
HOLIDAYS = [('', 'Default'), ('christmas', 'Christmas'), ('year-end', 'Year End'), ('halloween', 'Halloween'), ('black-friday', 'Black Friday'), ('golden-week', 'Golden Week')]
HOLIDAY_SWITCH = (
    '<style>'
    '.proto-holiday{display:none}html.proto-review .proto-holiday{position:fixed;right:16px;bottom:16px;z-index:2147483600;display:flex;gap:2px;padding:3px;max-width:calc(100vw - 32px);overflow-x:auto;scrollbar-width:none;'
    'border-radius:20px;background:rgba(21,23,31,.82);font:600 13px/1 Roboto,system-ui,sans-serif;box-shadow:0 4px 12px rgba(0,0,0,.2)}'
    '.proto-holiday::-webkit-scrollbar{display:none}'
    '.proto-holiday button{flex-shrink:0;padding:6px 12px;border:0;border-radius:16px;background:none;color:#fff;font:inherit;opacity:.7;cursor:pointer;white-space:nowrap}'
    '.proto-holiday button:hover{opacity:1}'
    '.proto-holiday button[aria-pressed=true]{background:#fff;color:#15171F;opacity:1}'
    # Phone: the sheet fills the screen, so lift its bottom edge to make room for the switcher instead of covering Buy Credits
    '@media (max-width:599px){.proto-holiday{right:8px;bottom:calc(8px + env(safe-area-inset-bottom));max-width:calc(100vw - 16px);font-size:12px}.proto-holiday button{padding:5px 9px}'
    'html.proto-review #iapOverlay{padding-bottom:calc(48px + env(safe-area-inset-bottom)) !important}}'
    '</style>'
    '<nav class="proto-holiday" aria-label="Holiday theme">'
    + ''.join(f'<button type="button" data-holiday="{k}" aria-pressed="false">{label}</button>' for k, label in HOLIDAYS) +
    '</nav>'
    '<script>(function () {'
    '  var q = new URLSearchParams(location.search);'
    '  if (q.get("review") !== "1") return;'   # not in review mode: no switcher, no holiday theme
    '  document.documentElement.classList.add("proto-review");'
    '  var overlay = document.getElementById("iapOverlay"), btns = document.querySelectorAll(".proto-holiday button");'
    '  function apply(h) {'
    '    if (h) overlay.setAttribute("data-holiday", h); else overlay.removeAttribute("data-holiday");'
    '    btns.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.holiday === h); });'
    '    var url = new URL(location.href); if (h) url.searchParams.set("holiday", h); else url.searchParams.delete("holiday"); history.replaceState(null, "", url);'
    '  }'
    '  btns.forEach(function (b) { b.addEventListener("click", function () { apply(b.dataset.holiday); }); });'
    '  var start = q.get("holiday") || "";'
    '  apply([].some.call(btns, function (b) { return b.dataset.holiday === start; }) ? start : "");'
    '})();</script>'
)

# Version switcher (bottom-right, always visible; sits above the holiday switcher in review mode): A = all blue (blue Pro card, blue → green slider),
# B = orange Pro card and orange slider. ?variant=b opens B directly; the URL follows the choice.
VARIANT_SWITCH = (
    '<style>'
    '.proto-variant{position:fixed;right:16px;bottom:16px;z-index:2147483600;display:flex;align-items:center;gap:2px;padding:3px 3px 3px 12px;'
    'border-radius:20px;background:rgba(21,23,31,.82);color:rgba(255,255,255,.6);font:600 13px/1 Roboto,system-ui,sans-serif;box-shadow:0 4px 12px rgba(0,0,0,.2)}'
    '.proto-variant span{margin-right:6px}'
    '.proto-variant button{width:30px;height:26px;border:0;border-radius:14px;background:none;color:#fff;font:inherit;opacity:.7;cursor:pointer}'
    '.proto-variant button:hover{opacity:1}'
    '.proto-variant button[aria-pressed=true]{background:#fff;color:#15171F;opacity:1}'
    'html.proto-review .proto-variant{bottom:56px}'
    '@media (max-width:599px){.proto-variant{right:8px;bottom:calc(8px + env(safe-area-inset-bottom));font-size:12px}'
    'html.proto-review .proto-variant{bottom:calc(46px + env(safe-area-inset-bottom))}'
    'html.proto-variant-on #iapOverlay{padding-bottom:calc(48px + env(safe-area-inset-bottom)) !important}'
    'html.proto-review.proto-variant-on #iapOverlay{padding-bottom:calc(86px + env(safe-area-inset-bottom)) !important}}'
    '</style>'
    '<nav class="proto-variant" aria-label="Design version"><span>Version</span>'
    '<button type="button" data-variant="a" aria-pressed="true">A</button>'
    '<button type="button" data-variant="b" aria-pressed="false">B</button></nav>'
    '<script>(function () {'
    '  document.documentElement.classList.add("proto-variant-on");'
    '  var overlay = document.getElementById("iapOverlay"), btns = document.querySelectorAll(".proto-variant button");'
    '  function apply(v) {'
    '    overlay.setAttribute("data-variant", v);'
    '    btns.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.variant === v); });'
    '    var url = new URL(location.href); if (v === "b") url.searchParams.set("variant", "b"); else url.searchParams.delete("variant"); history.replaceState(null, "", url);'
    '  }'
    '  btns.forEach(function (b) { b.addEventListener("click", function () { apply(b.dataset.variant); }); });'
    '  apply(new URLSearchParams(location.search).get("variant") === "b" ? "b" : "a");'
    '})();</script>'
)

def once(s, a, b):
    assert s.count(a) >= 1, a[:60]
    return s.replace(a, b, 1)

popup = (SRC / 'iap-popup.html').read_text(encoding='utf-8')
out = snapshot
out = once(out, '<title>', '<title>[Prototype] IAP Popup · ')
out = once(out, '</head>', HEAD + '</head>')
out = once(out, '<div class="headers_container__LC81Q">', HEADER + '<div class="headers_container__LC81Q proto-dt-header">')
out = once(out, '</body>', popup + TRIGGER + HOLIDAY_SWITCH + VARIANT_SWITCH + '</body>')

# No link leads to the live sites: every <a> pointing at a production domain opens the
# pricing page prototype in a new tab instead.
PROTOTYPE_URL = 'https://pricing-page-optimization.vercel.app/?discount=off'
LIVE = re.compile(r'https?://(?:[\w-]+\.)*(?:perfectcorp\.com|youcamapps\.com|makeupar\.com)\b[^"]*')
def to_prototype(m):
    tag = m.group(0)
    if not LIVE.search(tag):
        return tag
    tag = re.sub(r'\s(?:target|rel)="[^"]*"', '', tag)
    tag = re.sub(r'href="[^"]*"', f'href="{PROTOTYPE_URL}"', tag)
    return tag[:-1] + ' target="_blank" rel="noopener">'
out = re.sub(r'<a\b[^>]*\bhref="[^"]*"[^>]*>', to_prototype, out)
assert not re.search(r'<a\b[^>]*href="' + LIVE.pattern, out), 'live link left in index.html'
(ROOT / 'index.html').write_text(out, encoding='utf-8')
print('built index.html', len(out))

# Old version links (c.html from version C, d.html from version D) forward to the root page
for old in ('c.html', 'd.html'):
    (ROOT / old).write_text(
        '<!doctype html><meta charset="utf-8"><title>IAP Popup prototype</title>'
        '<meta http-equiv="refresh" content="0; url=./"><script>location.replace("./"+location.search)</script>',
        encoding='utf-8')
    print(f'built {old} (redirect to index.html)')
