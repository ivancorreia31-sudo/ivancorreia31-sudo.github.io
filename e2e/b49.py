# build 49: changing the 3D view's resolution draws the picture again at once, so the canvas is never left blank
# usage: python3 b49.py gl3d.html
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(2500)
        px = []
        for v in [0.75, 1, 0.75, 1.25]:
            px.append(await t.ev("v => window.__dpr49 ? __dpr49(v) : null", v)); await t.pg.wait_for_timeout(300)
        t.out['pixels'] = px
        if any(p is None for p in px): t.bad.append('no __dpr49 hook')
        elif any(sum(p[:3]) == 0 for p in px): t.bad.append('blank canvas straight after a resolution change: %s' % px)
        t.done()
asyncio.run(main())
