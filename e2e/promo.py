# screenshots for the itch.io page: the workshop with a car on the ramp, the engine bay up close, a test drive, a busy
# later garage, the showroom walk-round and a crate, at 1280x720 (and a phone shot), resolution fixed so they're sharp
# usage: python3 promo.py PAGE OUTDIR
import asyncio, json, os, sys
from h import T
PAGE, OUT = sys.argv[1], sys.argv[2]
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
async def settle(t, ms=4000): await t.pg.wait_for_timeout(ms)
async def main():
    os.makedirs(OUT, exist_ok=True); got = {}
    async with T(PAGE, 1280, 720, init=INIT, mobile=False) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await settle(t, 5000)
        await t.pg.screenshot(path=OUT + '/01_workshop.png'); got['workshop'] = True
        # the engine bay, bonnet up: tap the engine-bay pin
        await t.ev("(() => { const z = document.querySelector('[data-a=zone][data-z=engine]'); if (z) z.click(); })()"); await settle(t, 5000)
        await t.pg.screenshot(path=OUT + '/02_engine.png')
        # a test drive
        await t.ev("(() => { const z = document.querySelector('[data-a=view-all]'); if (z) z.click(); })()"); await settle(t, 1500)
        await t.act('g-drive'); await settle(t, 3000)
        if await t.ev("!!(window.__drv && __drv())"):
            await t.pg.keyboard.down('ArrowUp'); await settle(t, 6000); await t.pg.keyboard.up('ArrowUp')
            await t.pg.screenshot(path=OUT + '/03_drive.png'); got['drive'] = True
            await t.ev("(() => { const b = document.querySelector('[data-dv=end]'); if (b) b.click(); })()"); await settle(t, 2500); await t.close(2)
        # a later garage: three ramps, staff, showroom
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 14000; s.money = 80000; s.gold = 400; s.owned = Object.assign(s.owned || {}, { bay2: true, bay3: true, showroom: 1, neon: true, lights: true, plants: true, floor: 2, recept: true })")
        await t.close(3); await settle(t, 2000)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()")
        await t.act('view-all'); await settle(t, 4000)
        await t.pg.screenshot(path=OUT + '/04_garage.png')
        await t.act('sh-walk', b='sh-walk'); await settle(t, 6000)
        if await t.ev("!!document.getElementById('shw22')"):
            await t.pg.screenshot(path=OUT + '/05_showroom.png'); got['showroom'] = True
            await t.ev("(() => { const c = document.querySelector('#shw22 [data-b=shw-close]'); if (c) c.click(); })()"); await settle(t, 1500)
        await t.tab('daily', 'crates')
        await t.ev("(() => { const b = document.querySelector('[data-b=crate][data-k=style]:not([data-how])') || document.querySelector('[data-b=crate]'); if (b) b.click(); })()"); await settle(t, 2500)
        await t.pg.screenshot(path=OUT + '/06_crate_open.png')
        await t.ev("(() => { const b = document.querySelector('#crate22 [data-b=cr-skip]'); if (b) b.click(); })()"); await settle(t, 2500)
        await t.pg.screenshot(path=OUT + '/07_crate_prize.png')
        print(json.dumps({'got': got, 'errors': t.errs[:4]}))
    async with T(PAGE, 390, 844, init=INIT) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await settle(t, 5000)
        await t.pg.screenshot(path=OUT + '/08_phone.png')
asyncio.run(main())
