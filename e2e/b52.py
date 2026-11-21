# build 52: the forecourt's stains are one lit mesh of atlas stains; outside is drawn at 0.9 of the workshop's exposure
# with the glow starting at 0.93, and the workshop gets its own exposure and 0.8 back when you go in again
# usage: python3 b52.py PAGE
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 6000; s.money = 20000"); await t.close(3)
        await t.pg.wait_for_timeout(1500)
        t.out['ws'] = await t.ev("__out52()")
        await t.act('yard'); await t.pg.wait_for_timeout(5000)
        t.out['yard'] = y = await t.ev("__out52()")
        if not y['stain'] or not y['stain']['lit'] or y['stain']['verts'] < 36: t.bad.append('no lit stain mesh on the forecourt: %s' % y['stain'])
        if abs(y['expo'] - 0.9 * y['ws']) > 0.01: t.bad.append('outside exposure %s, expected 0.9 × %s' % (y['expo'], y['ws']))
        if y['thr'] != 0.93: t.bad.append('outside glow threshold %s' % y['thr'])
        await t.ev("(() => { const b = document.querySelector('[data-dv=yback]'); if (b) b.click(); return !!b; })()")
        await t.pg.wait_for_timeout(3000)
        t.out['back'] = b = await t.ev("({ o: __out52(), drv: !!(window.__drv && __drv()) })")
        if not b['drv'] and (abs(b['o']['expo'] - b['o']['ws']) > 0.01 or b['o']['thr'] != 0.8): t.bad.append('the workshop kept the outside look: %s' % b['o'])
        if b['drv']: t.bad.append('could not leave the yard')
        t.done()
asyncio.run(main())
