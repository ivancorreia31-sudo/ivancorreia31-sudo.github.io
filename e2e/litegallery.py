# a gallery of the simple outside cars (and, with HERO=1, the workshop car) for every model: rear three-quarter, side and
# front three-quarter, on the bay, buttons hidden; one sheet per 6 models
# usage: python3 litegallery.py PAGE OUTDIR [first [count]]
import asyncio, os, subprocess, sys
from h import T
PAGE, OUT = sys.argv[1], sys.argv[2]
FIRST = int(sys.argv[3]) if len(sys.argv) > 3 else 0
COUNT = int(sys.argv[4]) if len(sys.argv) > 4 else 99
HERO = os.environ.get('HERO')
VIEWS = [(2.4, 0.18), (1.5708, 0.12), (0.75, 0.18)]
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(PAGE, 520, 400, init="window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;", mobile=False) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1200)
        await t.ev("(() => { const s = document.createElement('style'); s.textContent = '.ov,.nav,.stage-ui,.mk,.step,.drawer,.hud,.tabbar,#toast,.ws3d .stage-hint{visibility:hidden!important} .ws3d{height:100vh!important}'; document.head.appendChild(s); })()")
        models = (await t.ev("__models32()"))[FIRST:FIRST + COUNT]; shots = []
        for i, m in enumerate(models):
            if HERO: await t.ev("m => __car32({ model: m, paint: '#B8BEC4', metallic: true, dirt: 0 })", m); await t.pg.wait_for_timeout(1500)
            else: await t.ev("m => __dbg.liteShow(m)", m); await t.pg.wait_for_timeout(700)
            p = await t.ev("__dbg.carPos()")
            for k, (yaw, pitch) in enumerate(VIEWS):
                await t.ev("o => __camTo(o, true)", {'yaw': yaw, 'pitch': pitch, 'dist': 5.4, 'px': 0.0, 'py': p[1] + 0.7, 'pz': 0}); await t.pg.wait_for_timeout(900)
                f = '%s/%02d_%d.png' % (OUT, FIRST + i, k); await t.pg.screenshot(path=f); shots.append(f)
        for j in range(0, len(shots), 18):
            subprocess.run(['montage'] + shots[j:j + 18] + ['-tile', '3x6', '-geometry', '300x231+2+2', '%s/sheet_%02d.png' % (OUT, (FIRST * 3 + j) // 18)], check=False)
        print(models, t.errs[:3])
asyncio.run(main())
