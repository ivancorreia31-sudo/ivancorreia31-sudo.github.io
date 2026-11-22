# the workshop room in first person at phone size from several spots (needs the debug page's fpTo)
# usage: python3 roomlook.py OUT [PAGE] [W H]
import asyncio, os, subprocess, sys
from h import T
OUT = sys.argv[1]; PAGE = sys.argv[2] if len(sys.argv) > 2 else 'gl3d_dbg.html'
W, H = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (390, 844)
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
VIEWS = [(0, 5.2, 1.5708, -0.08), (5.2, 0, 0.0, -0.08), (-5.2, 0, 3.1416, -0.08), (0, -4.6, -1.5708, -0.08), (4.8, 4.8, 0.785, -0.1), (-4.8, -4.4, -2.356, -0.1)]
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(PAGE, W, H, init=INIT, mobile=False) as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch=os.environ.get('PATCH', "s.seenIntro = true; s.xp = 6000; s.money = 20000"))
        await t.close(3); await t.pg.wait_for_timeout(1500)
        await t.ev("a => __car32({ model: a[0], paint: a[1], metallic: true, dirt: 0.2 })", [os.environ.get('MODEL', 'Hartwell Rowan 1.6'), os.environ.get('PAINT', '#2D4C78')]); await t.pg.wait_for_timeout(2500)
        await t.act('fp-walk'); await t.pg.wait_for_timeout(3000)
        await t.ev("(() => { const s = document.createElement('style'); s.textContent = '.fp-hint{visibility:hidden!important}'; document.head.appendChild(s); })()")
        if os.environ.get('JS'): print('js', await t.ev("s => __dbg.run(s)", os.environ['JS'])); await t.pg.wait_for_timeout(800)
        shots = []
        for k, (x, z, yaw, pitch) in enumerate(VIEWS):
            print(await t.ev("a => __dbg.fpTo(a[0], a[1], a[2], a[3])", [x, z, yaw, pitch])); await t.pg.wait_for_timeout(2200)
            f = '%s/r%d.png' % (OUT, k); await t.pg.screenshot(path=f); shots.append(f)
        subprocess.run(['montage'] + shots + ['-tile', '3x2', '-geometry', '%dx%d+2+2' % (W, H), OUT + '/sheet.png'], check=False)
        print(t.errs[:3])
asyncio.run(main())
