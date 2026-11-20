# the project-car loop: win a car at auction (keep bidding until the hammer falls), fix it with the auto player, then
# sell it; money and the car's whereabouts are checked at each stage
# usage: python3 project.py PAGE
import asyncio, json, os, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
AJ = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'autojob.js')).read()
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 11000; s.money = 60000; s.bays = [null]")
        await t.close(3)
        await t.skip_day(); await t.close(3)
        await t.open(fresh=False, patch="s.aucDay = s.day; s.bays = (s.bays || []).map(() => null)"); await t.close(3)
        await t.tab('jobs', 'auctions')
        lot = await t.ev("(() => { const b = document.querySelector('[data-a=auction]:not([disabled])'); if (!b) return null; const tx = (b.closest('article, .ticket') || b.parentElement).innerText.replace(/\\s+/g, ' ').slice(0, 90); b.click(); return tx; })()")
        t.out['lot'] = lot
        if not lot: t.bad.append('no lot to bid on'); t.done(); return
        res = None
        for k in range(120):
            await t.pg.wait_for_timeout(500)
            st = await t.ev("(() => { const a = document.querySelector('#sheet .auction'); if (!a) return { gone: true, modal: document.getElementById('modal').hidden ? '' : document.getElementById('modal').innerText.slice(0, 80) }; const lead = (a.querySelector('.auc-lead') || {}).innerText || ''; const b = a.querySelector('[data-a=auc-bid]:not([disabled])'); if (b && !/^You$/i.test(lead.trim())) b.click(); return { lead, going: (a.querySelector('.auc-going') || {}).innerText }; })()")
            if st.get('gone'): res = st; break
        t.out['auction'] = res
        await t.pg.wait_for_timeout(2500); await t.close(3)
        s = await t.S()
        mine = [b for b in (s.get('bays') or []) if b and b.get('project')] + [u for u in (s.get('unit') or []) if u and u.get('project')]
        t.out['won'] = bool(mine)
        if not mine: t.out['note'] = 'outbid this time'; t.done(); return
        on_ramp = any(b and b.get('project') for b in s.get('bays') or [])
        t.out['on_ramp'] = on_ramp
        if not on_ramp: t.bad.append('the car I won is not on a ramp'); t.done(); return
        await t.tab('workshop'); await t.pg.wait_for_timeout(2500)
        m0 = s['money']
        await t.ev("window.__AJ = { limit: 900000 }")
        log = await t.pg.evaluate(AJ)
        t.out['fix'] = log[-6:]
        await t.pg.wait_for_timeout(1500)
        t.out['after_fix'] = await t.ev("(() => { const m = document.getElementById('modal'); return m.hidden ? null : m.innerText.replace(/\\s+/g, ' ').slice(0, 200); })()")
        t.out['step'] = await t.ev("(document.querySelector('.step') || {}).innerText || null")
        t.out['money'] = [m0, (await t.S())['money']]
        if not any(l.startswith('sheet: SOLD') for l in log): t.bad.append('the project car was not sold: %s' % log[-4:])
        elif t.out['money'][1] <= m0: t.bad.append('selling made no money %s' % t.out['money'])
        t.done()
asyncio.run(main())
