# build 48: play one job in a saved garage with the in-page auto player, taking a phone screenshot every few seconds,
# then a strip of them; prints the auto player's log, the time it took and what the invoice said
# usage: python3 job48.py PAGE STATE.json OUTDIR [big]
import asyncio, json, os, subprocess, sys, time
from playwright.async_api import async_playwright
PAGE, STATE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
BIG = len(sys.argv) > 4 and sys.argv[4] == 'big'
EVERY = float(os.environ.get('EVERY', 6))
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=1, has_touch=True, is_mobile=True)
        await ctx.add_init_script("window.__noTitle34 = true; window.__allSubs = false; window.__noDriveIn37 = true;")
        page = await ctx.new_page(); errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:300]))
        await page.goto('file://' + os.path.abspath(PAGE))
        await page.evaluate("d => { localStorage.clear(); for (const k in d) localStorage.setItem(k, d[k]); }", json.load(open(STATE))); await page.reload()
        await page.wait_for_timeout(4500 if 'gl3d' in PAGE else 2500)
        if BIG: print('big:', await page.evaluate("(() => { for (let i = 0; i < 8; i++) { const j = window.__big46 && __big46(); if (j) return j.title || true; } return null; })()"))
        await page.locator('[data-a=desk-go]').first.click(); await page.wait_for_timeout(1200)
        await page.screenshot(path=OUT + '/a_desk.png')
        await page.locator('[data-b=desk-start44]').first.click(); await page.wait_for_timeout(2500)
        js = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'autojob45.js')).read()
        t0 = time.time(); task = asyncio.ensure_future(page.evaluate(js)); files = []; k = 0
        while not task.done() and time.time() - t0 < 200:
            await asyncio.sleep(EVERY)
            f = '%s/s%02d.png' % (OUT, k); k += 1
            try: await page.screenshot(path=f); files.append(f)
            except Exception as e: print('shot failed', str(e)[:80])
        log = await task if task.done() else ['(still running)']
        await page.wait_for_timeout(800); await page.screenshot(path=OUT + '/z_end.png'); files.append(OUT + '/z_end.png')
        inv = await page.evaluate("(() => { const m = document.getElementById('modal'); return m && !m.hidden ? m.innerText.replace(/\\s+/g, ' ').slice(0, 900) : null; })()")
        print(json.dumps({'secs': round(time.time() - t0), 'steps': len(log), 'log': log[-60:], 'invoice': inv, 'errors': errs[:5]}, indent=0))
        for i in range(0, len(files), 6):
            subprocess.run(['montage'] + files[i:i + 6] + ['-tile', '%dx1' % len(files[i:i + 6]), '-geometry', '292x632+4+0', '%s/strip_%d.png' % (OUT, i // 6)], check=False)
        json.dump(await page.evaluate("Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))"), open(OUT + '/after.json', 'w'))
        await b.close()
asyncio.run(main())
