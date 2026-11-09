"""Build index.html = YCE homepage snapshot + logged-in header + IAP popup.

    python3 src/build.py
"""
import pathlib

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

def once(s, a, b):
    assert s.count(a) >= 1, a[:60]
    return s.replace(a, b, 1)

popup = (SRC / 'iap-popup.html').read_text(encoding='utf-8')
out = snapshot
out = once(out, '<title>', '<title>[Prototype] IAP Popup · ')
out = once(out, '</head>', HEAD + '</head>')
out = once(out, '<div class="headers_container__LC81Q">', HEADER + '<div class="headers_container__LC81Q proto-dt-header">')
out = once(out, '</body>', popup + TRIGGER + '</body>')
(ROOT / 'index.html').write_text(out, encoding='utf-8')
print('built index.html', len(out))

# Old version links (c.html from version C, d.html from version D) forward to the root page
for old in ('c.html', 'd.html'):
    (ROOT / old).write_text(
        '<!doctype html><meta charset="utf-8"><title>IAP Popup prototype</title>'
        '<meta http-equiv="refresh" content="0; url=./"><script>location.replace("./"+location.search)</script>',
        encoding='utf-8')
    print(f'built {old} (redirect to index.html)')
