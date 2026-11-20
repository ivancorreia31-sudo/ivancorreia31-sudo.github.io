# a clean picture for the itch.io cover (630x500) and banner: the 3D view alone, no buttons
import asyncio, os, sys, subprocess
from h import T
PAGE, OUT = sys.argv[1], sys.argv[2]
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
HIDE = "(() => { const s = document.createElement('style'); s.textContent = '.hud,.tabbar,.ov,.nav,.stage-ui,.mk,.pins,#toast,.drive > *:not(canvas){display:none!important} body::before{display:none!important}'; document.head.appendChild(s); return true; })()"
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(PAGE, 1400, 1000, init=INIT, mobile=False) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(4000)
        await t.ev("(() => { const z = document.querySelector('[data-a=zone][data-z=engine]'); if (z) z.click(); })()"); await t.pg.wait_for_timeout(5000)
        await t.ev(HIDE); await t.pg.wait_for_timeout(1500)
        bb = await t.ev("(() => { const r = document.querySelector('canvas.stage-canvas').getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height }; })()"); await t.pg.screenshot(path=OUT + '/clean_engine.png', clip=bb)
        await t.ev("document.querySelector('[data-a=view-all]') && document.querySelector('[data-a=view-all]').click()")
        await t.ev("(() => { const s = [...document.styleSheets].pop(); })()")
        await t.pg.wait_for_timeout(4000)
        await t.pg.screenshot(path=OUT + '/clean_workshop.png', clip=bb)
asyncio.run(main())
