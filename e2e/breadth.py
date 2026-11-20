# a wide sweep of the less-travelled corners, each opened, used and closed with no page errors: every mini-game won,
# every garage upgrade bought (and the 3D workshop still drawing with all of it in), the bank loan taken and paid off,
# the story's first chapter, the level sheet, the local paper, the calendar, and every lucky-wheel prize
# usage: python3 breadth.py PAGE
import asyncio, json, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
GL = 'gl3d' in PAGE
MINIS = ['dent', 'chip', 'puncture', 'fuse', 'valet', 'aim', 'align', 'balance', 'jump', 'listen', 'drag']
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True); await t.close(2)
        # the story's first chapter, from the welcome card
        await t.act('story-start'); await t.pg.wait_for_timeout(900)
        t.out['story'] = await t.ev("(() => { const m = document.getElementById('modal'); return m.hidden ? null : m.innerText.replace(/\\s+/g, ' ').slice(0, 80); })()")
        if not t.out['story']: t.bad.append('the story did not open')
        await t.close(4)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(500)
        # every mini-game, won
        minis = {}
        if GL:
            for k in MINIS:
                e0 = len(t.errs)
                await t.ev("k => { try { __miniOpen(k); } catch (e) { window.__mErr = String(e); } }", k); await t.pg.wait_for_timeout(1500)
                st = await t.ev("(() => { const m = window.__mg && __mg(); return m ? { kind: m.kind, ended: m.ended } : null; })()")
                if st:
                    await t.ev("window.__mgWin && __mgWin(90)"); await t.pg.wait_for_timeout(1200)
                    done = await t.ev("(() => { const d = document.querySelector('[data-mg=done]'); if (d) { d.click(); return true; } const q = document.querySelector('[data-mg=quit]'); if (q) { q.click(); return 'quit'; } return false; })()"); await t.pg.wait_for_timeout(900)
                    open_after = await t.ev("!!(window.__mg && __mg())")
                    minis[k] = [st['kind'], done, open_after]
                    if open_after: t.bad.append('mini-game %s did not close' % k)
                else: minis[k] = None
                if len(t.errs) > e0: t.bad.append('errors in mini-game %s: %s' % (k, t.errs[e0:e0 + 2]))
                await t.close(2)
            t.out['minis'] = minis
            if sum(1 for v in minis.values() if v) < len(MINIS) - 2: t.bad.append('mini-games that would not open: %s' % [k for k, v in minis.items() if not v])
        # a rich garage: buy every upgrade there is
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 40000; s.money = 9000000; s.gold = 500")
        await t.close(3)
        await t.tab('garage', 'upgrades')
        bought = 0
        for _ in range(120):
            n = await t.ev("(() => { const b = document.querySelector('#view-garage [data-a=buy]:not([disabled])'); if (!b) return 0; b.click(); return 1; })()")
            if not n: break
            bought += 1; await t.pg.wait_for_timeout(250); await t.close(2)
            await t.tab('garage', 'upgrades')
        s = await t.S()
        t.out['upgrades_bought'] = bought; t.out['owned'] = len(s.get('owned') or {})
        left = await t.ev("[...document.querySelectorAll('#view-garage [data-a=buy]')].map(b => b.dataset.id)")
        if left: t.bad.append('upgrades left unbought: %s' % left[:6])
        if bought < 20: t.bad.append('only %d upgrades bought' % bought)
        await t.tab('workshop'); await t.pg.wait_for_timeout(3000)
        if GL:
            t.out['draws'] = await t.ev("window.__perfProbe ? __perfProbe(2) : null")
        # the bank: borrow, then pay it off
        await t.open(fresh=False, patch="s.money = 3000")
        await t.close(3)
        await t.tab('garage', 'business')
        m0 = (await t.S())['money']
        took = await t.ev("(() => { const b = document.querySelector('[data-a=loan]:not([disabled])'); if (!b) return null; b.click(); return b.innerText; })()"); await t.pg.wait_for_timeout(700); await t.close(2)
        s = await t.S(); t.out['loan'] = [took, m0, s['money'], bool(s.get('loan'))]
        if not took or s['money'] <= m0: t.bad.append('could not borrow: %s' % t.out['loan'])
        await t.tab('garage', 'business')
        off = await t.ev("(() => { const b = document.querySelector('[data-a=loan-off]:not([disabled])'); if (!b) return null; b.click(); return b.innerText; })()"); await t.pg.wait_for_timeout(700); await t.close(2)
        t.out['loan_off'] = [off, bool((await t.S()).get('loan'))]
        # the level sheet, the paper, the calendar
        t.out['level_sheet'] = await t.ev("__lvl41()"); await t.close(2)
        await t.ev("__paper37('make')"); await t.ev("__paper37('open')"); await t.pg.wait_for_timeout(700)
        t.out['paper'] = await t.ev("(() => { const m = document.getElementById('modal'); return m.hidden ? null : m.innerText.replace(/\\s+/g, ' ').slice(0, 60); })()"); await t.close(3)
        t.out['calendar'] = await t.ev("__cal39('open')"); await t.pg.wait_for_timeout(600); await t.close(3)
        if not t.out['paper']: t.bad.append('the paper did not open')
        # every lucky-wheel prize
        prizes = []
        for i in range(8):
            await t.tab('daily', 'today')
            await t.ev("(() => { const b = document.querySelector('[data-b=wh-open]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(400)
            await t.ev("i => __wheelSpin(i)", i); await t.pg.wait_for_timeout(5500)
            prizes.append(await t.ev("(() => { const m = document.getElementById('modal'); return m.hidden ? null : m.innerText.replace(/\\s+/g, ' ').slice(0, 50); })()"))
            await t.close(3)
        t.out['wheel'] = prizes
        t.done()
asyncio.run(main())
