# the outside as a player on foot sees it, at phone size: a few fixed eye-height views round the yard and the road
# usage: python3 outlook.py OUT [PAGE]
import asyncio, os, subprocess, sys
from h import T
OUT = sys.argv[1]; PAGE = sys.argv[2] if len(sys.argv) > 2 else 'gl3d_dbg.html'
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
VIEWS = [(0.0, -14.0, 1.2, -0.12), (4.5, -12.5, 2.6, -0.08), (2.0, -8.0, -1.57, -0.05), (10.0, -14.0, 0.3, -0.1), (-6.0, -6.0, -2.4, -0.06), (6.0, 2.0, 1.57, -0.04)]
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(PAGE, 390, 844, init=INIT, mobile=False) as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 6000; s.money = 20000; s.clock = 13 * 60")
        await t.close(3)
        await t.act('yard'); await t.pg.wait_for_timeout(5000)
        await t.ev("(() => { const s = document.createElement('style'); s.textContent = '#drive .yd-card,.dv-hint{visibility:hidden!important}'; document.head.appendChild(s); })()")
        if os.environ.get('JS'): print('js', await t.ev("s => __dbg.run(s)", os.environ['JS'])); await t.pg.wait_for_timeout(500)
        shots = []
        for k, (x, z, yaw, pitch) in enumerate(VIEWS):
            await t.ev("a => __dbg.walkTo(a[0], a[1], a[2], a[3], true)", [x, z, yaw, pitch]); await t.pg.wait_for_timeout(2500)
            f = '%s/o%d.png' % (OUT, k); await t.pg.screenshot(path=f); shots.append(f)
        subprocess.run(['montage'] + shots + ['-tile', '3x2', '-geometry', '390x844+2+2', OUT + '/sheet.png'], check=False)
        print(t.errs[:3])
asyncio.run(main())
