# the service van in the yard (and with CARS=1 a project car for sale) seen as a player on foot: eye height, from four
# sides; one sheet. usage: python3 carlook.py OUT [PAGE] [W H]
import asyncio, math, os, subprocess, sys
from h import T
OUT = sys.argv[1]; PAGE = sys.argv[2] if len(sys.argv) > 2 else 'gl3d_dbg.html'
W, H = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (600, 600)
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(PAGE, W, H, init=INIT, mobile=False) as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 6000; s.money = 20000; s.clock = 13 * 60")
        await t.close(3)
        await t.act('yard'); await t.pg.wait_for_timeout(5000)
        await t.ev("(() => { const s = document.createElement('style'); s.textContent = '.ov,.nav,.stage-ui,.mk,.step,.drawer,.hud,.tabbar,#toast,.yw-top,.yw-hint,.drv-ui,header,.topbar,#drive .yd-card,.dv-hint{visibility:hidden!important}'; document.head.appendChild(s); })()")
        if os.environ.get('JS'): print('js', await t.ev("s => __dbg.run(s)", os.environ['JS'])); await t.pg.wait_for_timeout(500)
        cx, cz, r = 9.2, -4.7, float(os.environ.get('R', '4.6')); shots = []
        for k, a in enumerate([int(v) for v in os.environ.get('ANG', '-60,-120,35,180').split(',')]):
            ar = math.radians(a); px, pz = cx + r * math.cos(ar), cz + r * math.sin(ar)
            yaw = math.atan2(-(cz - pz), -(cx - px)); pitch = math.atan2(0.85 - 1.64, r)
            await t.ev("a => __dbg.walkTo(a[0], a[1], a[2], a[3], true)", [px, pz, yaw, pitch]); await t.pg.wait_for_timeout(2500)
            f = '%s/v%d.png' % (OUT, k); await t.pg.screenshot(path=f); shots.append(f)
        subprocess.run(['montage'] + shots + ['-tile', '2x2', '-geometry', '%dx%d+2+2' % (W, H), OUT + '/sheet.png'], check=False)
        print(t.errs[:3])
asyncio.run(main())
