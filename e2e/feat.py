# the features around the jobs, each opened and closed as a player would: a test drive on the first job, walking round
# the garage, the phone and its tabs, a crate, the lucky wheel, an auction, and the showroom walk-round
# usage: python3 feat.py PAGE   (gl3d.html for the 3D parts; on flat.html the 3D-only ones are skipped)
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
GL = 'gl3d' in PAGE
async def main():
    async with T(PAGE, init="window.__allSubs = false; window.__locks28 = true; window.__noTitle34 = true; window.__noDriveIn37 = true;") as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(500)
        # 1. a test drive on the first job, and back
        if GL:
            await t.act('g-drive'); await t.pg.wait_for_timeout(4000)
            drv = await t.ev("!!(window.__drv && __drv())")
            t.out['drive'] = drv
            if drv:
                await t.ev("(() => { const b = document.querySelector('[data-dv=end]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(2500); await t.close(2)
                t.out['drive_back'] = await t.ev("!(window.__drv && __drv())")
                if not t.out['drive_back']: t.bad.append('could not end the test drive')
            else: t.bad.append('the test drive did not start')
        # a mid-game garage for the rest
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 9000; s.money = 40000; s.gold = 999; s.owned = Object.assign(s.owned || {}, { showroom: 1, bay2: true })")
        await t.close(3)
        # 2. walk round the garage
        if GL:
            await t.act('fp-walk'); await t.pg.wait_for_timeout(2500)
            t.out['walk'] = await t.ev("!!(window.__fp && __fp())")
            await t.ev("(() => { const b = document.querySelector('[data-fp=exit]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1500)
            t.out['walk_back'] = await t.ev("!(window.__fp && __fp())")
            if not t.out['walk'] or not t.out['walk_back']: t.bad.append('walking round: %s %s' % (t.out['walk'], t.out['walk_back']))
        # 3. the phone and each of its tabs
        await t.ev("(() => { const b = document.querySelector('[data-b=phone35]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(700)
        tabs = await t.ev("[...document.querySelectorAll('[data-b=ph36tab]')].map(b => b.dataset.v || b.innerText.trim())")
        seen = {}
        for v in tabs:
            await t.ev("v => { const b = [...document.querySelectorAll('[data-b=ph36tab]')].find(x => (x.dataset.v || x.innerText.trim()) === v); if (b) b.click(); }", v); await t.pg.wait_for_timeout(500)
            seen[v] = await t.ev("(() => { const m = document.getElementById('modal'); return m.hidden ? 0 : m.innerText.trim().length; })()")
        t.out['phone'] = seen
        if len(tabs) < 3 or any(n < 30 for n in seen.values()): t.bad.append('phone tabs %s' % seen)
        await t.close(3)
        # 4. a crate
        await t.tab('daily', 'crates')
        n0 = len(((await t.S()).get('inv') or {}).get('seen') or {})
        opened = await t.ev("(() => { const b = document.querySelector('[data-b=crate][data-k=style]:not([data-how])') || document.querySelector('[data-b=crate]'); if (!b) return false; b.click(); return true; })()"); await t.pg.wait_for_timeout(2500)
        t.out['crate_scene'] = await t.ev("!!document.getElementById('crate22')")
        for sel in ['#crate22 [data-b=cr-skip]', '[data-b=cr-close]']:
            await t.ev("s => { const b = document.querySelector(s); if (b) b.click(); }", sel); await t.pg.wait_for_timeout(1200)
        await t.close(2)
        n1 = len(((await t.S()).get('inv') or {}).get('seen') or {})
        t.out['crate'] = [opened, n0, n1]
        if not opened or not t.out['crate_scene'] or n1 <= n0: t.bad.append('crate %s scene %s' % (t.out['crate'], t.out['crate_scene']))
        # 5. the lucky wheel
        await t.tab('daily', 'today')
        await t.ev("(() => { const b = document.querySelector('[data-b=wh-open]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(700)
        sp = await t.ev("(() => { const b = document.querySelector('[data-b=wh-spin]'); if (!b || b.disabled) return false; b.click(); return true; })()"); await t.pg.wait_for_timeout(6500)
        t.out['wheel'] = [sp, await t.ev("(() => { const m = document.getElementById('modal'); return m.hidden ? null : m.innerText.replace(/\\s+/g, ' ').slice(0, 80); })()")]
        await t.close(3)
        # 6. an auction (lots come in overnight): start, bid once, walk away
        await t.tab('workshop'); await t.skip_day(); await t.close(3)
        await t.tab('jobs', 'auctions')
        t.out['lots'] = await t.ev("[document.querySelectorAll('[data-a=auction]').length, document.querySelectorAll('[data-a=auction]:not([disabled])').length, ((document.getElementById('view-jobs') || {}).innerText || '').replace(/\\s+/g, ' ').slice(0, 200)]")
        st = await t.ev("(() => { const b = document.querySelector('[data-a=auction]:not([disabled])'); if (!b) return false; b.click(); return true; })()"); await t.pg.wait_for_timeout(1200)
        bid = await t.ev("(() => { const b = document.querySelector('[data-a=auc-bid]:not([disabled])'); if (!b) return false; b.click(); return true; })()"); await t.pg.wait_for_timeout(800)
        t.out['auction'] = [st, bid, await t.ev("(() => { const a = document.querySelector('#sheet .auction'); return a ? a.innerText.replace(/\\s+/g, ' ').slice(0, 80) : null; })()")]
        await t.ev("(() => { const b = document.querySelector('[data-a=auc-walk]') || document.querySelector('[data-a=auc-close]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(800); await t.close(2)
        if not st or not t.out['auction'][2]: t.bad.append('auction %s' % t.out['auction'])
        # 7. the showroom walk-round
        if GL:
            await t.act('sh-walk', b='sh-walk'); await t.pg.wait_for_timeout(2500)
            t.out['showroom_walk'] = await t.ev("!!document.getElementById('shw22')")
            await t.ev("(() => { const c = document.querySelector('#shw22 [data-b=shw-close]'); if (c) c.click(); })()"); await t.pg.wait_for_timeout(800)
            if not t.out['showroom_walk']: t.bad.append('showroom walk-round did not open')
        t.done()
asyncio.run(main())
