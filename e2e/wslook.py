# the workshop as a player sees it at phone size: the normal view, a close orbit of the car, a low view, and the room
# in first person. usage: python3 wslook.py OUT [PAGE]
import asyncio, os, subprocess, sys
from h import T
OUT = sys.argv[1]; PAGE = sys.argv[2] if len(sys.argv) > 2 else 'gl3d_dbg.html'
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(PAGE, 390, 844, init=INIT, mobile=False) as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 6000; s.money = 20000")
        await t.close(3); await t.pg.wait_for_timeout(1500)
        await t.ev("a => __car32({ model: a[0], paint: a[1], metallic: true, dirt: 0.2 })", [os.environ.get('MODEL', 'Hartwell Rowan 1.6'), os.environ.get('PAINT', '#2D4C78')]); await t.pg.wait_for_timeout(2500)
        if os.environ.get('JS'): print('js', await t.ev("s => __dbg.run(s)", os.environ['JS'])); await t.pg.wait_for_timeout(800)
        shots = []
        f = OUT + '/w0.png'; await t.pg.screenshot(path=f); shots.append(f)
        p = await t.ev("__dbg.carPos()")
        for k, (yaw, pitch, dist) in enumerate([(0.7, 0.18, 4.6), (2.6, 0.05, 4.2), (-1.2, 0.45, 6.5)]):
            await t.ev("o => __camTo(o, true)", {'yaw': yaw, 'pitch': pitch, 'dist': dist, 'px': p[0], 'py': p[1] + 0.6, 'pz': p[2]}); await t.pg.wait_for_timeout(1800)
            f = '%s/w%d.png' % (OUT, k + 1); await t.pg.screenshot(path=f); shots.append(f)
        await t.act('fp-walk'); await t.pg.wait_for_timeout(3500)
        f = OUT + '/w4.png'; await t.pg.screenshot(path=f); shots.append(f)
        subprocess.run(['montage'] + shots + ['-tile', '5x1', '-geometry', '390x844+2+2', OUT + '/sheet.png'], check=False)
        print(t.errs[:3])
asyncio.run(main())
