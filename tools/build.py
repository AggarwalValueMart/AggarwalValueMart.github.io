"""Sync the website from a saved copy of the live Claude store page.

usage: python3 tools/build.py LIVE_HTML [REPO_DIR]
Each /_blob/<id> photo is served from images/<id>.webp when that file is in the repo.
Photos not in the repo are left out (the product shows its other photo or a
"Photo coming soon" tile) and listed in tools/missing-photos.txt;
their asset ids go to tools/need.json, which the sync hands to the store page so it can send them.
"""
import json, os, re, shutil, sys

SITE = 'https://aggarwalvaluemart.github.io/'
live = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(live).read()
body = html[re.search(r'<body>', html).end():]
body = re.sub(r'</body></html>\s*$', '', body).lstrip()

rx = r'(<script type="application/json" id="store-data">)(.*?)(</script>)'
M = re.search(rx, body, re.S)
d = json.loads(M.group(2))
os.makedirs(os.path.join(out, 'images'), exist_ok=True)
have = set()
need = set()

def local(url):
    """Return the website path for a /_blob/ url, or None if that photo is not in the repo."""
    if not url or not url.startswith('/_blob/'):
        return url or None
    i = url.split('/')[-1]
    if os.path.exists(os.path.join(out, 'images', i + '.webp')):
        have.add(i)
        return 'images/' + i + '.webp'
    need.add(i)
    return None

missing = []
s = d['store']
s['url'] = SITE
s['logo'] = local(s.get('logo')) or ''
for key in ('catImg', 'brandLogo'):
    for k, v in list((s.get(key) or {}).items()):
        nv = local(v)
        if nv: s[key][k] = nv
        else: del s[key][k]; missing.append((key, k))
for p in d['packs']:
    for a, b in (('image', 'full'), ('image2', 'full2')):
        x, y = local(p.get(a)), local(p.get(b))
        x = x or y; y = y or x
        if x: p[a], p[b] = x, y
        else:
            if p.get(a) or p.get(b): missing.append((p['id'], a))
            p.pop(a, None); p.pop(b, None)
    if not p.get('image') and p.get('image2'):
        p['image'], p['full'] = p.pop('image2'), p.pop('full2')

body = body[:M.start(2)] + json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c') + body[M.end(2):]

# Add to Home Screen: use the browser's own install prompt when it offers one (Android Chrome).
a = "case 'a2hs':openSheet('home',null);break;"
assert body.count(a) == 1
body = body.replace(a, "case 'a2hs':if(window.__a2hs){var ev=window.__a2hs;window.__a2hs=null;ev.prompt();ev.userChoice.then(function(r){if(r&&r.outcome==='accepted')toast('Added to your home screen')}).catch(function(){})}else openSheet('home',null);break;")

t = re.search(r'<title>.*?</title>', body).group(0)
body = body.replace(t, '', 1)
body = body.replace('<meta name="claude:viewport-fit-sides" content="cover">', '')
name = s['name']
desc = 'Festive gift packs – sweets, namkeens, chocolates, cookies, dry fruits, perfumes and juices. Order on WhatsApp.'
head = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{name}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#6E1A50">
<meta property="og:type" content="website"><meta property="og:url" content="{SITE}">
<meta property="og:title" content="{name}"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}icon-512.png"><meta property="og:image:width" content="512"><meta property="og:image:height" content="512">
<link rel="icon" href="icon-192.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Aggarwal Mart">
<style>:root{{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0;padding:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
<script>window.addEventListener('beforeinstallprompt',function(e){{e.preventDefault();window.__a2hs=e}});
if('serviceWorker' in navigator)window.addEventListener('load',function(){{navigator.serviceWorker.register('sw.js').catch(function(){{}})}});</script>
'''
open(os.path.join(out, 'index.html'), 'w').write(head + '</head><body>\n' + body + '\n</body></html>\n')

open(os.path.join(out, '.nojekyll'), 'w').write('')
json.dump({'ids': sorted(need)}, open(os.path.join(out, 'tools', 'need.json'), 'w'))
open(os.path.join(out, 'tools', 'missing-photos.txt'), 'w').write('\n'.join('%s %s' % m for m in missing) + '\n')
print(len(d['packs']), 'packs,', len(have), 'photos; missing:', missing)
