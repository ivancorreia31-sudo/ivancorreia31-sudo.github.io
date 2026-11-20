import asyncio, sys, json, subprocess
sys.path.insert(0, '/home/claude/bu/e2e')
from h import T
OUT = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/bu/fx/van'
async def main():
    import os; os.makedirs(OUT, exist_ok=True)
    async with T('gl3d_dbg.html', 520, 400, init="window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;", mobile=False) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1200)
        await t.ev("(() => { const s = document.createElement('style'); s.textContent = '.ov,.nav,.stage-ui,.mk,.step,.drawer,.hud,.tabbar,#toast{visibility:hidden!important} .ws3d{height:100vh!important}'; document.head.appendChild(s); })()")
        shots = []
        for mode in ['hero', 'lite']:
            if mode == 'hero': await t.ev("__car32({ style: 'van', model: 'Bramble Service Van 2.0', make: 'bramble', paint: '#F2B705', metallic: false, dirt: 0 })"); await t.pg.wait_for_timeout(2000)
            else: print(await t.ev("__dbg.liteShow('van')")); await t.pg.wait_for_timeout(800)
            p = await t.ev("__dbg.carPos()")
            for k, (yaw, pitch, px) in enumerate([(1.5708, 0.08, -0.1), (2.5, 0.15, -1.2), (-2.5, 0.15, -1.2), (0.7, 0.15, 0.8)]):
                await t.ev("o => __camTo(o, true)", {'yaw': yaw, 'pitch': pitch, 'dist': 4.6, 'px': px, 'py': p[1] + 0.9, 'pz': 0}); await t.pg.wait_for_timeout(1000)
                f = '%s/%s_%d.png' % (OUT, mode, k); await t.pg.screenshot(path=f); shots.append(f)
        subprocess.run(['montage'] + shots + ['-tile', '4x2', '-geometry', '360x277+2+2', OUT + '/sheet.png'])
asyncio.run(main())
