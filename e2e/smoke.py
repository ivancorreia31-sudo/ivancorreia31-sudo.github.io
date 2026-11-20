# a fresh game at one screen size: the welcome card, the first car on the ramp, then every tab and every sub-tab (with a
# mid-game save so all of them are open), checking for page errors, sideways overflow and blank pages
# usage: python3 smoke.py PAGE [W H]
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
W, H = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (390, 844)
WIDE = """(() => { const out = []; for (const e of document.querySelectorAll('main *, .hud *, .tabbar *')) { const r = e.getBoundingClientRect(); if (r.width > 0 && r.right > innerWidth + 2 && !e.closest('.subtabs, .stabs, .chips2, [class*=scroll], .ptypes, .tabs35') && getComputedStyle(e).position !== 'fixed') out.push(e.tagName + '.' + String(e.className).slice(0, 24) + ' ' + Math.round(r.right)); } return out.slice(0, 4); })()"""
async def main():
    async with T(PAGE, W, H, init="window.__allSubs = false; window.__noDriveIn37 = true;") as t:
        await t.open(fresh=True)
        first = await t.ev("(() => { const m = document.getElementById('modal'); const o = document.querySelector('.ov-card'); return { modal: m.hidden ? null : m.innerText.slice(0, 80), card: o ? o.innerText.replace(/\\s+/g, ' ').slice(0, 80) : null, step: ((document.querySelector('.step h3') || {}).innerText || null), bays: JSON.parse(localStorage.getItem('bonnet-up.v1') || '{}').bays }; })()")
        t.out['first'] = {k: first[k] for k in ['modal', 'card', 'step']}
        t.out['first_car'] = bool(first['bays'] and first['bays'][0])
        if not t.out['first_car']: t.bad.append('no car on the ramp at the start')
        if not (first['card'] or first['modal']): t.bad.append('no welcome')
        await t.close(2)
        t.out['wide_start'] = await t.ev(WIDE)
        # a mid-game garage: every area open
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 9000; s.money = 40000; s.gold = 300; s.owned = Object.assign(s.owned || {}, { showroom: 1, bay2: true, recept: true })")
        await t.close(3)
        pages = {}
        for tab in ['workshop', 'jobs', 'daily', 'collection', 'garage']:
            await t.tab(tab)
            subs = await t.ev("n => [...document.querySelectorAll('#view-' + n + ' [data-b=sub]')].map(b => b.dataset.v)", tab) or [None]
            for v in subs:
                if v: await t.tab(tab, v)
                info = await t.ev("n => { const m = document.querySelector('main'); const v = document.getElementById('view-' + n) || m; return { h: m.scrollHeight, text: (v.innerText || '').trim().length }; }", tab)
                wide = await t.ev(WIDE)
                pages[tab + ('/' + v if v else '')] = info['h']
                if info['text'] < 20 and tab != 'workshop': t.bad.append('blank page %s/%s' % (tab, v))
                if wide: t.bad.append('sideways overflow on %s/%s: %s' % (tab, v, wide))
                await t.close(2)
        t.out['pages'] = pages
        t.out['build'] = await t.ev("(document.querySelector('.build') || {}).innerText || null")
        t.done()
asyncio.run(main())
