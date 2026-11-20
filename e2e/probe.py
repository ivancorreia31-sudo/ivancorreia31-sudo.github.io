# evaluate JS expressions in the debug page (game open, workshop shown) and print the results
# usage: python3 probe.py "expr1" "expr2" ...
import asyncio, json, os, sys
from h import T
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
async def main():
    async with T(os.environ.get('PAGE', 'gl3d_dbg.html'), 480, 640, init=INIT, mobile=False) as t:
        await t.open(fresh=True); await t.close(2)
        for e in sys.argv[1:]: print(e[:60], '=>', json.dumps(await t.ev(e)))
        print(t.errs[:3])
asyncio.run(main())
