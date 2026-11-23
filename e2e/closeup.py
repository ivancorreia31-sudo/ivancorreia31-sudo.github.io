# one model, the workshop car (or the simple car with LITE=1), big, from a few angles: for judging the look
# usage: python3 closeup.py OUT MODEL [PAINT]
import asyncio, json, os, subprocess, sys
from h import T
OUT, MODEL = sys.argv[1], sys.argv[2]; PAINT = sys.argv[3] if len(sys.argv) > 3 else '#2D4C78'
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
VIEWS = [(0.65, 0.12, 5.2), (2.5, 0.14, 5.2), (1.5708, 0.05, 5.6), (0.25, 0.3, 4.6), (0.9, 0.06, 2.6), (2.2, 0.1, 2.6), (1.4, 0.02, 2.4), (-0.6, 0.35, 3.4), (0.3, 0.06, 2.5), (2.8, 0.08, 2.5), (3.1416, 0.05, 1.6), (1.2, 0.0, 1.5)]
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(os.environ.get('PAGE', 'gl3d_dbg.html'), 800, 560, init=INIT, mobile=False) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1200)
        await t.ev("(() => { const s = document.createElement('style'); s.textContent = '.ov,.nav,.stage-ui,.mk,.step,.drawer,.hud,.tabbar,#toast,.ws3d .stage-hint{visibility:hidden!important} .ws3d{height:100vh!important}'; document.head.appendChild(s); })()")
        await t.ev("a => __car32({ model: a[0], paint: a[1], metallic: true, dirt: 0 })", [MODEL, PAINT]); await t.pg.wait_for_timeout(2500)
        if os.environ.get('LITE'): await t.ev("m => __dbg.liteShow(m)", MODEL); await t.pg.wait_for_timeout(800)
        if os.environ.get('JS'): print('js', await t.ev("s => __dbg.run(s)", os.environ['JS'])); await t.pg.wait_for_timeout(800)
        p = await t.ev("__dbg.carPos()"); shots = []
        for k, (yaw, pitch, dist) in [(i, VIEWS[i]) for i in [int(v) for v in os.environ.get('VS', '0,1,2,3').split(',')]]:
            await t.ev("o => __camTo(o, true)", {'yaw': yaw, 'pitch': pitch, 'dist': dist, 'px': (1.6 if k == 8 else -1.6 if k == 9 else -1.9 if k == 10 else 1.35 if k == 11 else -0.1), 'py': p[1] + (0.32 if k == 11 else 0.65), 'pz': (0.8 if k == 11 else 0)}); await t.pg.wait_for_timeout(1500)
            f = '%s/c%d.png' % (OUT, k); await t.pg.screenshot(path=f); shots.append(f)
            for pt in [p2[1:] for p2 in json.loads(os.environ.get('PICK', '[]')) if p2[0] == k]:
                h = await t.ev("p => __dbg.pickAll(p[0], p[1])", pt); print('PICK', k, pt, json.dumps(h)[:600])
        subprocess.run(['montage'] + shots + ['-tile', os.environ.get('TILE', '2x2'), '-geometry', '800x560+2+2', OUT + '/sheet.png'], check=False)
        print(t.errs[:3])
asyncio.run(main())
