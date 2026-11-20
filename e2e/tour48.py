# build 48: a look round a saved garage - every main tab and its sub-tabs, scrolled top to bottom, as phone screenshots,
# plus a strip per tab (montage) so a whole tab can be read in one picture. Prints errors and anything that overflows sideways.
# usage: python3 tour48.py PAGE STATE.json OUTDIR [tabs]
import asyncio, json, os, subprocess, sys
from playwright.async_api import async_playwright
PAGE, STATE, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
TABS = sys.argv[4].split(',') if len(sys.argv) > 4 else ['workshop', 'jobs', 'daily', 'collection', 'garage']
W, H = int(os.environ.get('W', 390)), int(os.environ.get('H', 844))
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = await b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=True, is_mobile=W < 700)
        await ctx.add_init_script("window.__noTitle34 = true; window.__allSubs = false; window.__noDriveIn37 = true;")
        page = await ctx.new_page(); errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:300]))
        await page.goto('file://' + os.path.abspath(PAGE))
        await page.evaluate("d => { localStorage.clear(); for (const k in d) localStorage.setItem(k, d[k]); }", json.load(open(STATE))); await page.reload()
        await page.wait_for_timeout(4500 if 'gl3d' in PAGE else 2500)
        await page.evaluate("(() => { const m = document.getElementById('modal'); if (m && !m.hidden) { const c = m.querySelector('[data-a=close-modal]') || m.querySelector('.btn.primary'); if (c) c.click(); } })()")
        report = {}
        for t in TABS:
            await page.click('#tab-' + t); await page.wait_for_timeout(900)
            subs = await page.evaluate("[...document.querySelectorAll('main [data-b=sub]')].filter(b => b.offsetWidth).map(b => b.dataset.v || b.innerText.trim())")
            subs = subs or [None]
            for si, sv in enumerate(subs):
                if sv is not None:
                    await page.evaluate("v => { const b = [...document.querySelectorAll('main [data-b=sub]')].find(x => (x.dataset.v || x.innerText.trim()) === v); if (b) b.click(); }", sv); await page.wait_for_timeout(700)
                h = await page.evaluate("(() => { const m = document.querySelector('main'); m.scrollTop = 0; return [m.scrollHeight, m.clientHeight]; })()")
                files = []; y = 0; k = 0
                while True:
                    await page.evaluate("y => { document.querySelector('main').scrollTop = y; }", y); await page.wait_for_timeout(250)
                    f = '%s/%s_%d_%d.png' % (OUT, t, si, k); await page.screenshot(path=f); files.append(f); k += 1
                    if y + h[1] >= h[0] or k >= 8: break
                    y += h[1] - 60
                wide = await page.evaluate("[...document.querySelectorAll('main *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && r.right > innerWidth + 2 && getComputedStyle(e).position !== 'fixed'; }).slice(0, 4).map(e => e.tagName + '.' + String(e.className).slice(0, 30) + ' ' + Math.round(e.getBoundingClientRect().right))")
                key = t + ('/' + str(sv) if sv is not None else '')
                report[key] = {'height': h[0], 'shots': len(files), 'wide': wide}
                strip = '%s/strip_%s_%d.png' % (OUT, t, si)
                subprocess.run(['montage'] + files + ['-tile', '%dx1' % len(files), '-geometry', '+4+0', '-resize', '%dx' % (W * 3 // 4), strip], check=False)
        report['errors'] = errs[:6]
        print(json.dumps(report, indent=0))
        json.dump(await page.evaluate("Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))"), open(OUT + '/after.json', 'w'))
        await b.close()
asyncio.run(main())
