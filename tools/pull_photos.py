"""Save photos the store page handed over (ArtifactData list of "sitephotos" with out_dir).

usage: python3 tools/pull_photos.py DOWNLOAD_DIR [REPO_DIR]
Reads DOWNLOAD_DIR/sitephotos/<asset id>.json ({type, data: base64}) and writes
images/<asset id>.webp. Prints the ids saved, one per line.
"""
import base64, glob, io, json, os, re, sys

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(os.path.join(out, 'images'), exist_ok=True)
for f in sorted(glob.glob(os.path.join(src, 'sitephotos', '*.json'))):
    i = os.path.basename(f)[:-5]
    if not re.fullmatch(r'[0-9a-f]{32}', i):
        continue
    try:
        doc = json.load(open(f))
        raw = base64.b64decode(doc['data'])
        dst = os.path.join(out, 'images', i + '.webp')
        if doc.get('type') == 'image/webp':
            open(dst, 'wb').write(raw)
        else:
            from PIL import Image
            Image.open(io.BytesIO(raw)).convert('RGB').save(dst, 'WEBP', quality=85)
        print(i)
    except Exception as e:
        print('skip', i, e, file=sys.stderr)
