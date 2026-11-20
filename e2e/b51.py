# build 51: the simple outside cars are built like the workshop car (fine skin close up, coarse far off) and their lamps
# sit on the flat of the nose and tail on every body style (the yard van's tail lamps used to wrap round its corners);
# the workshop and the yard each use a reflection probe of themselves
# usage: python3 b51.py PAGE
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True); await t.close(2)
        r = await t.ev("__lite51('hatch').styles.map(k => { const n = __lite51(k), f = __lite51(k, true); return [k, n.reachT, n.reachH, n.tris, f.tris]; })")
        t.out['styles'] = len(r); t.out['worst_tail'] = max(r, key=lambda e: e[1]); t.out['worst_head'] = max(r, key=lambda e: e[2])
        for k, rt, rh, near, far in r:
            if rt > 0.22: t.bad.append('%s: tail lamp reaches %.2f m round from the tail' % (k, rt))
            if rh > 0.22: t.bad.append('%s: headlamp reaches %.2f m round from the nose' % (k, rh))
            if near <= far * 2: t.bad.append('%s: close-up car not finer than the far one (%d vs %d triangles)' % (k, near, far))
        if len(r) < 60: t.bad.append('only %d styles' % len(r))
        await t.pg.wait_for_timeout(3000)
        t.out['ws'] = await t.ev("__probe51()")
        if not t.out['ws']['ws']: t.bad.append('the workshop has no reflection probe')
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 6000; s.money = 20000"); await t.close(3)
        await t.act('yard'); await t.pg.wait_for_timeout(6000)
        t.out['yard'] = await t.ev("__probe51()")
        if not t.out['yard']['out']: t.bad.append('the yard has no reflection probe')
        t.done()
asyncio.run(main())
