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
VIS = "s => { const b = document.querySelector(s); if (!b) return null; const r = b.getBoundingClientRect(), bar = (document.querySelector('.tabbar') || {}).getBoundingClientRect ? document.querySelector('.tabbar').getBoundingClientRect().top : innerHeight; const c = b.closest('.ov-card, .step'); const cr = c ? c.getBoundingClientRect() : { top: 0, bottom: innerHeight }; const e = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return { top: Math.round(r.top), bottom: Math.round(r.bottom), bar: Math.round(bar), card: [Math.round(cr.top), Math.round(cr.bottom)], hit: !!(e && (e === b || b.contains(e))) }; }"
async def small(W, H):
    async with T(PAGE, W, H, init="window.__allSubs = false; window.__noDriveIn37 = true;") as t:
        await t.open(fresh=True)
        t.out['size'] = [W, H]
        t.out['letsgo'] = await t.ev(VIS, '[data-a=dismiss-intro]')
        g = t.out['letsgo']
        if not g or not g['hit'] or g['bottom'] > g['bar']: t.bad.append("Let's go not on screen without scrolling: %s" % g)
        await t.ev("document.querySelector('[data-a=dismiss-intro]').click()"); await t.pg.wait_for_timeout(1500)
        t.out['drive'] = await t.ev(VIS, '[data-a=g-drive]')
        g = t.out['drive']
        if not g or not g['hit'] or g['bottom'] > g['bar']: t.bad.append('Test drive not on screen without scrolling: %s' % g)
        await t.pg.screenshot(path='s24/B49_%dx%d.png' % (W, H))
        t.done()
async def all_():
    await main()
    for W, H in [(320, 568), (360, 640), (390, 844)]: await small(W, H)
asyncio.run(all_())
