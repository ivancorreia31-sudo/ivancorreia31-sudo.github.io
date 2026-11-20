# the yard outside the garage, as a player walking out sees it: a few views at phone size
import asyncio, os, sys
from h import T
OUT = sys.argv[1]; PAGE = sys.argv[2] if len(sys.argv) > 2 else 'gl3d.html'
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(PAGE, 390, 844, init="window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;") as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 6000; s.money = 20000")
        await t.close(3)
        await t.act('yard'); await t.pg.wait_for_timeout(6000)
        await t.pg.screenshot(path=OUT + '/y0.png')
        # turn to look along the yard: drag on the right half
        for k in range(1, 4):
            await t.pg.mouse.move(300, 500); await t.pg.mouse.down(); await t.pg.mouse.move(220, 500, steps=8); await t.pg.mouse.up(); await t.pg.wait_for_timeout(2500)
            await t.pg.screenshot(path='%s/y%d.png' % (OUT, k))
        print(t.errs[:3])
asyncio.run(main())
