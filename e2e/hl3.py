# debug: silver car on the lift, view from under the front right; find the dark pixels round the headlamp and ask the
# debug copy what each of them is
# usage: python3 hl3.py OUT MODEL YAW PITCH
import asyncio, json, os, sys
from collections import Counter
from PIL import Image
from h import T
OUT, MODEL, YAW, PITCH = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
async def main():
    os.makedirs(OUT, exist_ok=True)
    async with T(os.environ.get('PAGE', 'gl3d_dbg.html'), 390, 844, init=INIT) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(1500)
        await t.ev("m => __car32({ model: m, paint: '#B9BEC2', metallic: true, dirt: 0 })", MODEL); await t.pg.wait_for_timeout(2500)
        await t.ev("__liftTo(1.6)")
        for _ in range(60):
            await t.pg.wait_for_timeout(500)
            p = await t.ev("__dbg.carPos()")
            if p and p[1] > 1.5: break
        await t.pg.wait_for_timeout(1000)
        box = await t.ev("__dbg.partBox('headlamp_FR')")
        c = [(box[0][i] + box[1][i]) / 2 for i in range(3)]
        await t.ev("o => __camTo(o, true)", {'yaw': YAW, 'pitch': PITCH, 'dist': 2.0, 'px': c[0], 'py': c[1], 'pz': c[2]}); await t.pg.wait_for_timeout(2500)
        await t.ev("(() => { const s = document.createElement('style'); s.textContent = '.ov,.nav,.stage-ui,.mk,.step,.drawer{visibility:hidden!important}'; document.head.appendChild(s); })()"); await t.pg.wait_for_timeout(800)
        f = '%s/view.png' % OUT; await t.pg.screenshot(path=f)
        im = Image.open(f).convert('RGB'); W, H = im.size
        cv = await t.ev("(() => { const r = document.querySelector('canvas.stage-canvas').getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; })()")
        if os.environ.get('HIDE'):
            print('hid', await t.ev("r => __dbg.hideRole(r)", os.environ['HIDE'])); await t.pg.wait_for_timeout(1500)
            await t.pg.screenshot(path='%s/view_hidden.png' % OUT)
            return
        for pt in [[126, 300], [128, 340], [150, 252], [180, 252], [118, 300], [200, 330]]:
            h = await t.ev("p => __dbg.pickAll(p[0], p[1])", pt); print("PT", pt, json.dumps(h))
        return
        hits = Counter(); samples = {}
        for y in range(int(cv[1]) + 4, int(cv[3]) - 4, 6):
            for x in range(int(cv[0]) + 4, int(cv[2]) - 4, 6):
                r, g, b = im.getpixel((x, y))
                if r + g + b < 75:
                    h = await t.ev("p => { const h = __dbg.pick(p[0], p[1])[0]; return h ? [h.path, h.col, h.verts, h.box] : null; }", [x, y])
                    if h:
                        k = '%s %s %d' % (h[0], h[1], h[2]); hits[k] += 1; samples.setdefault(k, []).append((x, y))
        for k, n in hits.most_common(12): print(n, k, samples[k][:4])
asyncio.run(main())
