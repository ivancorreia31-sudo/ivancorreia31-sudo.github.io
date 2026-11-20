# debug: a car on the lift at 1.6 m, looked at from under the front right corner and from above, for each given model
# usage: python3 hl.py OUTDIR "Model 1" "Model 2" ...
import asyncio, json, os, sys
from h import T
OUT = sys.argv[1]; MODELS = sys.argv[2:]
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T('gl3d.html', 390, 844, init=INIT) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1500)
        for i, m in enumerate(MODELS):
            ok = await t.ev("m => __car32({ model: m })", m); await t.pg.wait_for_timeout(2500)
            await t.ev("__liftTo(1.6)"); await t.pg.wait_for_timeout(2500)
            look = await t.ev("__look40('headlamp_FR')"); await t.pg.wait_for_timeout(2000)
            cam = await t.ev("__camDir()")
            print(m, ok, json.dumps(look)[:200], cam[:6] if cam else None)
            await t.pg.screenshot(path='%s/%02d_look.png' % (OUT, i))
            for name, pitch in [('under', -0.32), ('above', 0.45)]:
                await t.ev("p => { const r = window.__camR49 || null; return r; }", 0)
                await t.ev("p => __camTo({ pitch: p, dist: 2.6 }, false)", pitch); await t.pg.wait_for_timeout(2500)
                await t.pg.screenshot(path='%s/%02d_%s.png' % (OUT, i, name))
        print(t.errs)
asyncio.run(main())
