# the same car and camera drawn with the static merge on, then off: the pictures should match
# usage: python3 b57same.py OUT PAGE MODEL
import asyncio, os, subprocess, sys
from h import T
OUT, PAGE, MODEL = sys.argv[1], sys.argv[2], sys.argv[3]
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
VIEWS = [(0.65, 0.12, 5.2, -0.1, 0.65, 0), (2.5, 0.14, 5.2, -0.1, 0.65, 0), (1.2, 0.0, 1.5, 1.35, 0.32, 0.8), (-0.6, 0.35, 3.4, -0.1, 0.65, 0)]
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(PAGE, 800, 560, init=INIT, mobile=False) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1000)
        await t.ev("(() => { const s = document.createElement('style'); s.textContent = '.ov,.nav,.stage-ui,.mk,.step,.drawer,.hud,.tabbar,#toast,.ws3d .stage-hint{visibility:hidden!important} .ws3d{height:100vh!important}'; document.head.appendChild(s); })()")
        await t.ev("m => __car32({ model: m, paint: '#7A1F24', metallic: true, dirt: 0 })", MODEL); await t.pg.wait_for_timeout(3000)
        await t.ev("o => __camTo(o, true)", {'yaw': 0.65, 'pitch': 0.12, 'dist': 5.2, 'px': -0.1, 'py': 1.0, 'pz': 0}); await t.pg.wait_for_timeout(2500)
        p = await t.ev("__dbg.carPos()")
        for mode in ['on', 'off']:
            await t.ev("v => { window.__nob57 = v; }", mode == 'off')
            for k, (yaw, pitch, dist, px, py, pz) in enumerate(VIEWS):
                await t.ev("o => __camTo(o, true)", {'yaw': yaw, 'pitch': pitch, 'dist': dist, 'px': px, 'py': p[1] + py, 'pz': pz}); await t.pg.wait_for_timeout(1500)
                await t.pg.screenshot(path='%s/%s%d.png' % (OUT, mode, k))
        print(await t.ev("__batch57()"), t.errs[:3])
    for k in range(len(VIEWS)):
        r = subprocess.run(['compare', '-metric', 'AE', '-fuzz', '4%', '%s/on%d.png' % (OUT, k), '%s/off%d.png' % (OUT, k), '%s/diff%d.png' % (OUT, k)], capture_output=True, text=True)
        print('view', k, 'pixels differing:', r.stderr.strip())
asyncio.run(main())
