# the web app (GitHub Pages) and the itch.io zip from out/bonnet-up.html: fonts and three.js served from the site instead of
# Google Fonts and the CDN, a proper head/body, and a service-worker cache name tied to the build and the page's hash
import hashlib, os, re, shutil, sys, zipfile
src = open(sys.argv[1] if len(sys.argv) > 1 else 'out/bonnet-up.html', encoding='utf-8').read()
L = src.split('\n')
head, fonts = open('static/app-head.txt', encoding='utf-8').read(), open('static/app-fonts.txt', encoding='utf-8').read()
assert L[0] == '<title>Bonnet Up</title>' and L[1].startswith('<meta name="claude:viewport-fit-sides"') and 'fonts.googleapis.com/css2' in L[4], 'unexpected page head'
L = [L[0], fonts.rstrip('\n')] + L[5:]
i = L.index('</style>'); L = L[:i + 1] + ['</head>', '<body>', ''] + L[i + 1:]
out = '\n'.join(L)
cdn = '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
assert out.count(cdn) == 1; out = out.replace(cdn, '<script src="three.min.js"></script>')
out = head + out.rstrip('\n') + '\n\n</body>\n</html>\n'
build = re.search(r'const BUILD = (\d+);', src).group(1)
os.makedirs('dist/app', exist_ok=True)
open('dist/app/game.html', 'w', encoding='utf-8').write(out)
sha = hashlib.sha1(out.encode('utf-8')).hexdigest()[:8]
sw = open('static/sw.js', encoding='utf-8').read()
sw = re.sub(r"const VERSION = 'bonnet-up-v[^']*';", "const VERSION = 'bonnet-up-v%s-%s';" % (build, sha), sw, count=1)
open('dist/app/sw.js', 'w', encoding='utf-8').write(sw)
for f in ['index.html', 'manifest.webmanifest', 'privacy.html', 'three.min.js', 'three-LICENSE.txt', 'apple-touch-icon.png', 'favicon-48.png', 'icon-192.png', 'icon-512.png', 'icon-maskable-192.png', 'icon-maskable-512.png']:
    shutil.copy('static/' + f, 'dist/app/' + f)
shutil.rmtree('dist/app/fonts', ignore_errors=True); shutil.copytree('static/fonts', 'dist/app/fonts')
# itch.io: the game page is the zip's index.html; it needs three.js and the fonts beside it
z = zipfile.ZipFile('dist/bonnet-up-itch.zip', 'w', zipfile.ZIP_DEFLATED)
z.writestr('index.html', out)
for f in ['three.min.js', 'three-LICENSE.txt']: z.write('static/' + f, f)
for f in sorted(os.listdir('static/fonts')): z.write('static/fonts/' + f, 'fonts/' + f)
z.close()
print('app build', build, 'sw', sha, 'itch zip', os.path.getsize('dist/bonnet-up-itch.zip'))
