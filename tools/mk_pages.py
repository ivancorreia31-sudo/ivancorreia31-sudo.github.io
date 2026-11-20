# test pages beside the tests in e2e/: flat.html (no three.js, the 2D fallback) and gl3d.html (three.js from e2e/three.min.js)
import shutil, sys
src = open(sys.argv[1] if len(sys.argv) > 1 else 'out/bonnet-up.html', encoding='utf-8').read()
cdn = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
assert src.count(cdn) == 1
pre = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>\n'
end = '\n</body></html>\n'
sfx = sys.argv[2] if len(sys.argv) > 2 else ''
open('e2e/flat%s.html' % sfx, 'w', encoding='utf-8').write(pre + src.replace(cdn, '') + end)
open('e2e/gl3d%s.html' % sfx, 'w', encoding='utf-8').write(pre + src.replace(cdn, '<script src="three.min.js"></script>') + end)
shutil.copy('static/three.min.js', 'e2e/three.min.js')
