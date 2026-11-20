# debug: the car on the lift at 1.6 m, the camera pivoting on the front-right headlamp from below at 8 headings;
# writes screenshots and lists what's under a grid of points round the lamp
# usage: python3 hl2.py OUTDIR MODEL [PITCH]
import asyncio, json, os, sys
from h import T
OUT, MODEL = sys.argv[1], sys.argv[2]
PITCH = float(sys.argv[3]) if len(sys.argv) > 3 else -0.3
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T('gl3d_dbg.html', 390, 844, init=INIT) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1500)
        print(await t.ev("m => __car32({ model: m })", MODEL)); await t.pg.wait_for_timeout(2500)
        await t.ev("__liftTo(1.6)")
        for _ in range(60):
            await t.pg.wait_for_timeout(500)
            p = await t.ev("__dbg.carPos()")
            if p and p[1] > 1.5: break
        await t.pg.wait_for_timeout(1000)
        box = await t.ev("__dbg.partBox('headlamp_FR')"); print('lamp', box, 'car', await t.ev("__dbg.carPos()"))
        if not box: return
        c = [(box[0][i] + box[1][i]) / 2 for i in range(3)]
        for k in [int(x) for x in os.environ.get("KS", "0,1,2,3,4,5,6,7").split(",")]:
            yaw = -3.1416 + k * 0.785
            await t.ev("o => __camTo(o, true)", {'yaw': yaw, 'pitch': PITCH, 'dist': 2.4, 'px': c[0], 'py': c[1], 'pz': c[2]}); await t.pg.wait_for_timeout(1800)
            await t.pg.screenshot(path='%s/y%d.png' % (OUT, k))
            for pt in json.loads(os.environ.get('PICK', '[]')):
                print(k, pt, json.dumps(await t.ev("p => __dbg.pick(p[0], p[1])", pt))[:300])
            if os.environ.get('ISO'):
                pt = json.loads(os.environ['ISO']); print('iso', await t.ev("p => __dbg.isolate(p[0], p[1])", pt)); await t.pg.wait_for_timeout(1500)
                await t.pg.screenshot(path='%s/iso%d.png' % (OUT, k))
                for j, (yw, pc) in enumerate([(-0.785, -0.3), (0, 0.4), (-1.57, 0.1)]):
                    await t.ev("o => __camTo(o, true)", {'yaw': yw, 'pitch': pc, 'dist': 3.0, 'px': c[0], 'py': c[1], 'pz': c[2]}); await t.pg.wait_for_timeout(1500)
                    await t.pg.screenshot(path='%s/iso%d_%d.png' % (OUT, k, j))
        print(t.errs)
asyncio.run(main())
