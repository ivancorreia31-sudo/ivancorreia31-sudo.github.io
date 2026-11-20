# does everything in the engine bay (the black front-end carrier, the inner wings...) stay inside the nose on every model?
# a vertex is outside when it is ahead of the nose's paint at its height and width (the skin's own front-profile grid)
# usage: python3 carrier.py PAGE [N]   (Build 50 on)
import asyncio, json, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
N = int(sys.argv[2]) if len(sys.argv) > 2 else 999
async def main():
    async with T(PAGE, 390, 844, init="window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true;") as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1000)
        models = (await t.ev("__models32()"))[:N]; bad = []
        for m in models:
            await t.ev("m => __car32({ model: m })", m); await t.pg.wait_for_timeout(900)
            r = await t.ev("__bayNose50()")
            if r is None: print(m, r); continue
            if r: bad.append([m, r[:3]])
        print(json.dumps({'models': len(models), 'with_carrier_outside': len(bad), 'bad': bad, 'errors': t.errs[:3]}))
asyncio.run(main())
