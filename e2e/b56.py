# build 56: on every model the chin under the nose and tail stays inside the body; the Rowan's tail lamps have clear
# reversing sections and its headlamps projectors and indicators
# usage: python3 b56.py PAGE
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True); await t.close(2)
        r = await t.ev("__models32().map(m => m.name || m.model || m).map(m => { __car32({ model: m }); return [m, __skirt56()]; })")
        t.out['models'] = len(r)
        for m, o in r:
            if not o or o[0] or o[1]: t.bad.append('%s: chin points outside the body %s' % (m, o))
        await t.ev("__car32({ model: 'Hartwell Rowan 1.6' })"); await t.pg.wait_for_timeout(600)
        t.out['lamps'] = l = await t.ev("__lamps56()")
        if l['rev'] < 2 or l['amber'] < 4 or l['proj'] < 2: t.bad.append('lamp sections missing: %s' % l)
        t.done()
asyncio.run(main())
