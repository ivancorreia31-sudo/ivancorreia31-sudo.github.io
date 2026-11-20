# look for bits poking out of the body: each model on the lift at 1.6 m, seen from below at 8 headings round the car
# and from above at 4, with the buttons hidden; one sheet of pictures per model
# usage: python3 sweep.py OUTDIR "Model 1" "Model 2" ...
import asyncio, json, os, subprocess, sys
from h import T
OUT = sys.argv[1]; MODELS = sys.argv[2:]
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T('gl3d.html', 480, 640, init=INIT, mobile=False) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1000)
        await t.ev("(() => { const s = document.createElement('style'); s.textContent = '.ov,.nav,.stage-ui,.mk,.step,.drawer,.hud,.tabbar,#toast{visibility:hidden!important}'; document.head.appendChild(s); })()")
        for mi, m in enumerate(MODELS):
            await t.ev("m => __car32({ model: m, paint: '#C3C7CB', metallic: true, dirt: 0 })", m); await t.pg.wait_for_timeout(1500)
            await t.ev("__liftTo(1.6)"); await t.pg.wait_for_timeout(9000)
            shots = []
            # close up from below: the four corners and the middle of each side, looking up at the body
            for k, (px, pz, yaw) in enumerate([(1.9, 0.6, 0.0), (1.9, -0.6, 0.0), (-1.7, 0.6, 3.1416), (-1.7, -0.6, 3.1416), (0.2, 0.8, 1.5708), (0.2, -0.8, -1.5708), (1.9, 0.75, 0.785), (-1.7, -0.75, -2.36)]):
                await t.ev("o => __camTo(o, true)", {'yaw': yaw, 'pitch': -0.35, 'dist': 2.3, 'px': px, 'py': 2.2, 'pz': pz}); await t.pg.wait_for_timeout(1400)
                f = '%s/%d_c%d.png' % (OUT, mi, k); await t.pg.screenshot(path=f); shots.append(f)
            subprocess.run(['montage'] + shots + ['-tile', '4x2', '-geometry', '360x480+2+2', '%s/close_%d.png' % (OUT, mi)], check=False)
            await t.ev("__liftTo(0)"); await t.pg.wait_for_timeout(6000)
            print(m, 'done')
        print(t.errs[:3])
asyncio.run(main())
