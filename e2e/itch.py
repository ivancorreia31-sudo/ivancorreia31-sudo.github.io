# the itch.io zip as itch serves it: unzipped behind a web server, index.html (the shell) loads game.html in a frame;
# the game starts with no errors, the fonts and three.js load from the zip, and on a phone the quarter-turn button is
# there and turns the frame
# usage: python3 itch.py ZIP
import asyncio, http.server, json, os, shutil, socketserver, sys, tempfile, threading, zipfile
from playwright.async_api import async_playwright
ZIP = sys.argv[1] if len(sys.argv) > 1 else '../dist/bonnet-up-itch.zip'
async def main():
    d = tempfile.mkdtemp(); zipfile.ZipFile(ZIP).extractall(d)
    names = sorted(os.listdir(d)); bad = []; out = {'files': names}
    for need in ['index.html', 'game.html', 'three.min.js', 'fonts']:
        if need not in names: bad.append('zip lacks ' + need)
    H = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=d, **k)
    http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
    srv = socketserver.TCPServer(('127.0.0.1', 0), H); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
        pg = await ctx.new_page(); errs = []; failed = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.on('requestfailed', lambda r: failed.append(r.url[-60:]))
        pg.on('response', lambda r: failed.append('%d %s' % (r.status, r.url[-60:])) if r.status >= 400 else None)
        await pg.goto('http://127.0.0.1:%d/index.html' % port); await pg.wait_for_timeout(6000)
        fr = pg.frame_locator('#game')
        g = [f for f in pg.frames if f.url.endswith('game.html')]
        if not g: bad.append('no game frame')
        else:
            gf = g[0]
            gf.on = None
            out['game'] = await gf.evaluate("({ three: typeof THREE !== 'undefined', build: (document.querySelector('.build-tag') || {}).textContent || null, card: !!document.querySelector('.ov-card'), fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family).filter((v, i, a) => a.indexOf(v) === i) })")
            if not out['game']['three']: bad.append('three.js did not load')
            if len(out['game']['fonts']) < 2: bad.append('fonts did not load: %s' % out['game']['fonts'])
            await gf.evaluate("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await pg.wait_for_timeout(800)
            out['turn_button'] = await gf.evaluate("(() => { const b = document.querySelector('[data-a=turn]'); return b ? !b.hidden : null; })()")
            if not out['turn_button']: bad.append('no quarter-turn button on a phone')
            else:
                await gf.evaluate("document.querySelector('[data-a=turn]').click()"); await pg.wait_for_timeout(600)
                out['turned'] = await pg.evaluate("document.getElementById('game').style.transform")
                if 'rotate' not in (out['turned'] or ''): bad.append('the turn did not rotate the frame: %s' % out['turned'])
                await gf.evaluate("document.querySelector('[data-a=turn]').click()"); await gf.evaluate("document.querySelector('[data-a=turn]').click()"); await pg.wait_for_timeout(400)
                out['back'] = await pg.evaluate("document.getElementById('game').style.transform")
        out['failed'] = [f for f in failed if 'fonts.g' not in f][:6]
        if out['failed']: bad.append('requests failed: %s' % out['failed'])
        out['bad'] = bad; out['errors'] = errs[:5]
        print(json.dumps(out)); await b.close()
    srv.shutdown(); shutil.rmtree(d)
asyncio.run(main())
