# the inside camera (from the driver's seat) for a few models; usage: python3 insidelook.py OUT PAGE "Model" ...
import asyncio, os, subprocess, sys
from h import T
OUT, PAGE, MODELS = sys.argv[1], sys.argv[2], sys.argv[3:]
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(PAGE, 600, 600, init=INIT, mobile=False) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1000)
        shots = []
        for i, m in enumerate(MODELS):
            await t.ev("m => __car32({ model: m, paint: '#2D4C78' })", m); await t.pg.wait_for_timeout(2000)
            await t.ev("__dbg.run(\"setView('inside'); kick(); 1\")"); await t.pg.wait_for_timeout(2500)
            f = '%s/i%d.png' % (OUT, i); await t.pg.screenshot(path=f); shots.append(f)
            await t.ev("__dbg.run(\"setView('overview'); kick(); 1\")"); await t.pg.wait_for_timeout(800)
        subprocess.run(['montage'] + shots + ['-tile', '%dx1' % len(shots), '-geometry', '600x600+2+2', OUT + '/sheet.png'], check=False)
        print(t.errs[:3])
asyncio.run(main())
