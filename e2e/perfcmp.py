# how much work a frame is: draw calls, triangles, shader programs, and the time of N synchronous renders (the game's own
# render with its glow pass, then a 1-pixel read so the GPU (SwiftShader here) has finished) in the workshop, the yard on
# foot, and on the road. SwiftShader runs the shaders on the CPU, so its times track shader cost × pixels.
# usage: python3 perfcmp.py PAGE [N]   (debug pages only: needs __dbg.run)
import asyncio, json, os, sys
from h import T
PAGE = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 6
INIT = "window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true; window.__fixedDpr = true;"
MEASURE = """(n => { const S = window.__S || {}; const sc = S.sc(), cam = S.cam(); const gl = renderer.getContext(), px = new Uint8Array(4);
  renderer.info.autoReset = false; renderer.info.reset(); renderer.render(sc, cam); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px);
  const calls = renderer.info.render.calls, tris = renderer.info.render.triangles; renderer.info.autoReset = true;
  const t0 = performance.now(); for (let i = 0; i < n; i++) { renderer.shadowMap.needsUpdate = true; renderer.render(sc, cam); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, px); }
  const ms = (performance.now() - t0) / n; let lights = 0; sc.traverse(o => { if (o.isLight && o.visible && !o.isAmbientLight && !o.isHemisphereLight) lights++; });
  return { ms: +ms.toFixed(1), calls, tris, programs: renderer.info.programs.length, lights, dpr: renderer.getPixelRatio(), size: [renderer.domElement.width, renderer.domElement.height] }; })"""
async def main():
    res = {}
    async with T(PAGE, 390, 844, init=INIT, mobile=False) as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 6000; s.money = 20000; s.clock = 13 * 60")
        await t.close(3); await t.pg.wait_for_timeout(3000)
        await t.ev("__dbg.run(\"window.__S = { sc: () => scene, cam: () => camera }; 1\")")
        res['workshop'] = await t.ev("n => __dbg.run('(' + %s + ')(' + n + ')')" % json.dumps(MEASURE), N)
        await t.act('yard'); await t.pg.wait_for_timeout(6000)
        await t.ev("__dbg.run(\"window.__S = { sc: () => dW.scene, cam: () => camera }; 1\")")
        await t.ev("a => __dbg.walkTo(a[0], a[1], a[2], a[3], true)", [2.0, -8.0, -1.57, -0.05]); await t.pg.wait_for_timeout(2500)
        if os.environ.get('YJS'): print('yjs', await t.ev("s => __dbg.run(s)", os.environ['YJS']))
        res['yard'] = await t.ev("n => __dbg.run('(' + %s + ')(' + n + ')')" % json.dumps(MEASURE), N)
        if os.environ.get('NODRIVE'): print(json.dumps(res)); return
        b = await t.ev("(() => { const b = document.querySelector('[data-dv=yvan]'); if (b) b.click(); return !!b; })()")
        await t.pg.wait_for_timeout(9000)
        if b: res['drive'] = await t.ev("n => __dbg.run('(' + %s + ')(' + n + ')')" % json.dumps(MEASURE), N)
        res['errs'] = t.errs[:3]
    print(json.dumps(res))
asyncio.run(main())
