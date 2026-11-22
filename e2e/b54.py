# build 54: on every model the interior lining (A-pillar trims, roof lining) stays inside the glass and the body, seen
# from the cabin; the Rowan carries ROWAN and 1.6 lettering on the boot
# usage: python3 b54.py PAGE
import asyncio, os, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True); await t.close(2)
        models = await t.ev("__models32().map(m => m.name || m.model || m)")
        if os.environ.get("ONLY"): models = [m for m in models if m in os.environ["ONLY"].split(";")]
        bad = []
        for m in models:
            await t.ev("m => __car32({ model: m })", m); await t.pg.wait_for_timeout(250)
            r = await t.ev("__pillar54()")
            if r and r['out'] > 0: bad.append([m, r])
        t.out['models'] = len(models); t.out['poking'] = bad
        if len(models) < 60 and not os.environ.get("ONLY"): t.bad.append('only %d models' % len(models))
        for m, r in bad: t.bad.append('%s: %d of %d lining points outside the body' % (m, r['out'], r['n']))
        await t.ev("__car32({ model: 'Hartwell Rowan 1.6' })"); await t.pg.wait_for_timeout(400)
        t.out['badges'] = b = await t.ev("__badges54()")
        if sorted(b) != ['1.6', 'ROWAN']: t.bad.append('boot lettering: %s' % b)
        t.done()
asyncio.run(main())
