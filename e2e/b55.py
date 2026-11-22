# build 55: the Rowan has two amber side repeaters and a darker band of skin along the tops of its side windows
# usage: python3 b55.py PAGE
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("__car32({ model: 'Hartwell Rowan 1.6' })"); await t.pg.wait_for_timeout(600)
        t.out['b55'] = r = await t.ev("__b55()")
        if r['rep'] != 2: t.bad.append('%d side repeaters, expected 2' % r['rep'])
        t.done()
asyncio.run(main())
