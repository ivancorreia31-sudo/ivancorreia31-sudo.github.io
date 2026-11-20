# saves: progress survives a reload; a save code copied from one garage loads into a fresh one (cash, level, Gold Bolts,
# legacy stars, kit); a broken code is refused without losing the garage; the save stays small
# usage: python3 save.py PAGE
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'flat.html'
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 7000; s.money = 12345; s.gold = 321; s.legacy = 2; s.owned = Object.assign(s.owned || {}, { heater: true, bay2: true })")
        await t.close(3)
        s1 = await t.S()
        await t.pg.reload(); await t.pg.wait_for_timeout(2500); await t.close(3)
        s2 = await t.S()
        t.out['reload'] = [s2['money'], s2['xp'], s2['gold'], s2.get('legacy')]
        if [s2['money'], s2['xp'], s2['gold']] != [s1['money'], s1['xp'], s1['gold']]: t.bad.append('reload changed the save %s' % t.out['reload'])
        code = await t.ev("__lg47.code()")
        t.out['code_len'] = len(code or '')
        if not code or len(code) < 50: t.bad.append('no save code')
        # a fresh garage, then load the code
        await t.open(fresh=True); await t.close(2)
        fresh = await t.S(); t.out['fresh'] = [fresh['money'], fresh['xp'], fresh['gold']]
        await t.ev("__lg47.paste()"); await t.pg.wait_for_timeout(400)
        await t.pg.fill('#save-in', 'BONNETUP-this-is-not-a-code'); await t.act('save-load'); await t.pg.wait_for_timeout(500)
        err = await t.ev("(() => { const e = document.getElementById('save-err'); return e && !e.hidden ? e.textContent : null; })()")
        t.out['bad_code'] = err
        if not err: t.bad.append('a broken code was not refused')
        if (await t.S())['money'] != fresh['money']: t.bad.append('a broken code changed the garage')
        await t.pg.fill('#save-in', code); await t.act('save-load')
        try: await t.pg.wait_for_function("JSON.parse(localStorage.getItem('bonnet-up.v1')).gold === 321", timeout=15000)
        except Exception: pass
        await t.pg.wait_for_timeout(600); await t.close(3)
        s3 = await t.S()
        t.out['loaded'] = [s3['money'], s3['xp'], s3['gold'], s3.get('legacy'), bool((s3.get('owned') or {}).get('heater'))]
        if [s3['money'], s3['xp'], s3['gold']] != [s1['money'], s1['xp'], s1['gold']] or not (s3.get('owned') or {}).get('heater'): t.bad.append('the save code did not bring the garage over %s' % t.out['loaded'])
        if (s3.get('legacy') or 0) < 2 or await t.ev("__lg47.stars()") < 2: t.bad.append('legacy stars lost')
        t.out['kb'] = round(len(await t.ev("localStorage.getItem('bonnet-up.v1')")) / 1024, 1)
        if t.out['kb'] > 120: t.bad.append('save is %s KB at the start' % t.out['kb'])
        t.done()
asyncio.run(main())
