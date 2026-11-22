# build 53: three roof fittings light the workshop (off in battery saver), the bonnet's pad uses the quilted felt, and
# the units over the road are clad
# usage: python3 b53.py PAGE
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 6000; s.money = 20000"); await t.close(3)
        await t.pg.wait_for_timeout(2000)
        t.out['ws'] = w = await t.ev("__b53()")
        if w['pad'] < 1: t.bad.append('the bonnet has no felt pad')
        if w['lights'] != 3: t.bad.append('%d roof lights on, expected 3' % w['lights'])
        t.out['save'] = s = await t.ev("(() => { __gfx53('save'); const a = __b53().lights; __gfx53('auto'); return [a, __b53().lights]; })()")
        if s != [0, 3]: t.bad.append('battery saver should turn the roof lights off and back on: %s' % s)
        await t.act('yard'); await t.pg.wait_for_timeout(5000)
        t.out['yard'] = y = await t.ev("__b53()")
        if y['clad'] < 100: t.bad.append('no cladding on the units over the road')
        t.done()
asyncio.run(main())
