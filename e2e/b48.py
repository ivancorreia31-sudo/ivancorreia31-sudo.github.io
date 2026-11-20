# build 48: the day's event suits the season and the weather (and a month of real nights never breaks that), the parts
# catalogue ticks exactly the boxes that fit, and the tidier Legacy card, fault book and Items page
# usage: python3 b48.py PAGE [DAYS]
import asyncio, json, os, sys
from playwright.async_api import async_playwright
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'flat.html'
DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 24
KEY = 'bonnet-up.v1'
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = await b.new_context(viewport={'width': 390, 'height': 844}, has_touch=True, is_mobile=True)
        await ctx.add_init_script("window.__allSubs = false; window.__locks28 = true; window.__noTitle34 = true; window.__noDriveIn37 = true;")
        pg = await ctx.new_page(); errs = []; bad = []; out = {}
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        await pg.goto('file://' + os.path.abspath(PAGE)); await pg.evaluate("localStorage.clear()"); await pg.reload(); await pg.wait_for_timeout(2000)
        await pg.evaluate("""(() => { const s = JSON.parse(localStorage.getItem('%s')); s.seenIntro = true; s.xp = 6500; s.money = 60000; s.day = 22; s.wx36 = 'dry';
          localStorage.setItem('%s', JSON.stringify(s)); })()""" % (KEY, KEY))
        await pg.reload(); await pg.wait_for_timeout(2500)
        close = "(() => { const m = document.getElementById('modal'); const t = m.hidden ? '' : m.innerText.replace(/\\s+/g, ' '); if (!m.hidden) { const c = m.querySelector('[data-a=close-modal]') || m.querySelector('.btn.primary'); if (c) c.click(); else m.hidden = true; } return t; })()"
        await pg.evaluate(close)
        # 1. which events fit which days
        ev = {k: await pg.evaluate("a => __ev48(a[0], a[1])", v) for k, v in {'summer_dry': [20, 'dry'], 'summer_wet': [20, 'rain'], 'autumn': [35, 'dry'], 'winter_dry': [50, 'dry'], 'winter_wet': [50, 'rain'], 'spring': [5, 'dry']}.items()}
        out['fits'] = {k: v['fits'] for k, v in ev.items()}; out['rain'] = {k: v['rain'] for k, v in ev.items()}
        F = out['fits']
        if 'heatwave' not in F['summer_dry']: bad.append('no heatwave on a dry summer day')
        if any('heatwave' in F[k] for k in ['summer_wet', 'autumn', 'winter_dry', 'spring']): bad.append('heatwave where it should not be')
        if 'coldsnap' not in F['winter_dry'] or 'coldsnap' not in F['winter_wet']: bad.append('no cold snap in winter')
        if any('coldsnap' in F[k] for k in ['summer_dry', 'autumn', 'spring']): bad.append('cold snap outside winter')
        if 'potholes' in F['summer_dry'] or 'potholes' not in F['autumn']: bad.append('pothole season wrong')
        if not (out['rain']['summer_dry'] < out['rain']['spring'] < out['rain']['autumn'] < out['rain']['winter_dry']): bad.append('rain chances %s' % out['rain'])
        # 2. real nights: summer into autumn into winter, the morning's event always suits the day
        S = lambda: pg.evaluate("JSON.parse(localStorage.getItem('%s'))" % KEY)
        mornings = []; s = await S(); d0 = s['day']
        while True:
            s = await S()
            if s['day'] - d0 >= DAYS or s.get('over'): break
            day = s['day']
            for k in range(40):
                await pg.evaluate("(() => { if (!document.getElementById('modal').hidden || document.body.classList.contains('skipping23')) return; __skip('close') || __skip('m120') || __skip('m60'); })()"); await pg.wait_for_timeout(100)
                await pg.evaluate(close); s = await S()
                if s['day'] != day: break
            if s['day'] == day: bad.append('day %d never ended' % day); break
            await pg.wait_for_timeout(300); await pg.evaluate(close); s = await S()
            mornings.append([s['day'], (await pg.evaluate("__ev48()"))["season"], s.get('event'), s.get('weather')])
        out['mornings'] = mornings
        clash = [m for m in mornings if (m[2] == 'heatwave' and (m[1] != 'Summer' or m[3] == 'rain')) or (m[2] == 'coldsnap' and m[1] != 'Winter') or (m[2] == 'potholes' and m[1] == 'Summer')]
        if clash: bad.append('events that do not suit the day: %s' % clash)
        if len(mornings) < DAYS: bad.append('only %d nights' % len(mornings))
        out['seasons'] = sorted(set(m[1] for m in mornings))
        # 3. the parts catalogue: no ticks without it, ticks on exactly the boxes that fit with it
        await pg.evaluate("document.getElementById('tab-jobs').click()"); await pg.wait_for_timeout(600)
        took = await pg.evaluate("(() => { const b = document.querySelector('[data-a=accept]:not([disabled])'); if (!b) return false; b.click(); return true; })()"); await pg.wait_for_timeout(1500)
        await pg.evaluate(close)
        out['took'] = took
        part = await pg.evaluate("__shop48.open()"); await pg.wait_for_timeout(500)
        before = await pg.evaluate("[document.querySelectorAll('#modal .box').length, document.querySelectorAll('#modal .box.fit48').length, (document.querySelector('#modal .muted') || {}).innerText]")
        await pg.evaluate(close)
        bought = await pg.evaluate("(() => { const b = document.createElement('button'); b.dataset.a = 'buy'; b.dataset.id = 'catalogue'; b.hidden = true; document.body.appendChild(b); b.click(); b.remove(); return JSON.parse(localStorage.getItem('%s')).owned.catalogue || null; })()" % KEY)
        await pg.wait_for_timeout(400); await pg.evaluate(close)
        await pg.evaluate("__shop48.open(%s)" % json.dumps(part)); await pg.wait_for_timeout(500)
        after = await pg.evaluate("[document.querySelectorAll('#modal .box').length, [...document.querySelectorAll('#modal .box')].map(b => b.classList.contains('fit48')), __shop48.fits(), (document.querySelector('#modal .muted') || {}).innerText]")
        await pg.screenshot(path='s24/B48_shop.png')
        out['catalogue'] = {'part': part, 'before': before[:2], 'bought': bought, 'boxes': after[0], 'ticked': sum(after[1]), 'fit': sum(after[2] or []), 'text': after[3][:80]}
        if not part: bad.append('no job to open the shop on (took a job: %s)' % took)
        elif before[1] != 0: bad.append('ticks without the catalogue')
        elif not bought: bad.append('could not buy the catalogue')
        elif after[1] != after[2] or not sum(after[1]): bad.append('ticks %s but fits %s' % (after[1], after[2]))
        await pg.evaluate(close)
        # 4. tidier pages: the Legacy card, the fault book, Items
        await pg.evaluate("document.getElementById('tab-daily').click()"); await pg.wait_for_timeout(500)
        await pg.evaluate("(() => { const b = [...document.querySelectorAll('main [data-b=sub]')].find(x => x.dataset.v === 'today'); if (b) b.click(); })()"); await pg.wait_for_timeout(400)
        out['legacy'] = await pg.evaluate("[...document.querySelectorAll('.lg47-r')].map(r => r.innerText.replace(/\\s+/g, ' ').trim())")
        if len(out['legacy']) != 2 or not out['legacy'][0].startswith('Level') or 'Business worth' not in out['legacy'][1] or ' of ' not in out['legacy'][0] + out['legacy'][1]: bad.append('legacy rows %s' % out['legacy'])
        await pg.evaluate("document.getElementById('tab-collection').click()"); await pg.wait_for_timeout(500)
        await pg.evaluate("(() => { const b = [...document.querySelectorAll('main [data-b=sub]')].find(x => x.dataset.v === 'faults'); if (b) b.click(); })()"); await pg.wait_for_timeout(400)
        out['book'] = await pg.evaluate("({ cards: document.querySelectorAll('.book38 .b38-grid .b38-c').length, left: document.querySelectorAll('.b38-left .b38-c').length, leftText: ((document.querySelector('.b38-left') || {}).innerText || '').replace(/\\s+/g, ' '), n: (document.querySelector('.b38-n') || {}).innerText, h: document.querySelector('main').scrollHeight })")
        if not (1 <= out['book']['left'] <= 3): bad.append('fault book summary %s' % out['book'])
        await pg.screenshot(path='s24/B48_book.png')
        await pg.evaluate("(() => { const b = [...document.querySelectorAll('main [data-b=sub]')].find(x => x.dataset.v === 'parts'); if (b) b.click(); })()"); await pg.wait_for_timeout(400)
        out['items'] = await pg.evaluate("({ all: document.querySelectorAll('.itgrid .itbtn').length, small: document.querySelectorAll('.itgrid.lk48 .itbtn').length, lockedBig: document.querySelectorAll('.itgrid:not(.lk48) .itc.locked').length, head: (document.querySelector('.coll-h b') || {}).innerText, h: document.querySelector('main').scrollHeight })")
        tot = int((out['items']['head'] or '0 of 0').split(' of ')[-1])
        if out['items']['all'] != tot or out['items']['lockedBig'] or not out['items']['small']: bad.append('items page %s' % out['items'])
        await pg.screenshot(path='s24/B48_items.png')
        out['bad'] = bad; out['errors'] = errs[:5]
        print(json.dumps(out)); await b.close()
asyncio.run(main())
