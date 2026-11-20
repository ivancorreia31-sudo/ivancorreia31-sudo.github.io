# build 51: the cars reflect where they are. The workshop and the yard each take a picture of themselves all the way
# round (a cube from where a car stands, the car left out) and use it, blurred to suit each surface, as their reflections
# and ambient light, instead of a stock photo of somewhere else. Paint, glass, chrome and wet tarmac now show the real
# roller door, walls, shops and sky. Taken again when the garage's look changes (lights, floor, walls) and when the
# light outside does.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("  const ENVS = { in: null, out: null };",
"""  const ENVS = { in: null, out: null };
  /* build 51: reflection probes. sc: the scene, (x, y, z): where the cube is taken from, hide: what to leave out of it,
     ibl: the lighting to use while taking it (the photo, so a probe never lights the next one). The capture is
     tone-mapped and stored like the screen (sRGB), so no shader needs building for it; the blurred result is kept in
     RGBE like the photos' (PMREM keeps an 8-bit input's encoding, and blurring in 8-bit sRGB left the paint banded). */
  const PR51 = { pm: null, ws: true, wsRT: null };
  function probe51(sc, x, y, z, hide, ibl, k) {
    if (!T.CubeCamera || !T.WebGLCubeRenderTarget || !T.PMREMGenerator) return null;
    let out = null; const rt = new T.WebGLCubeRenderTarget(256, { generateMipmaps: false }); rt.texture.encoding = T.sRGBEncoding;
    const cc = new T.CubeCamera(0.15, 700, rt); cc.position.set(x, y, z); sc.add(cc); cc.updateMatrixWorld(true);
    const hid = hide.filter(o => o && o.visible), sm = renderer.shadowMap.needsUpdate, e0 = sc.environment, prev = renderer.getRenderTarget(), s49 = lastS49, c49 = lastC49;
    const ex0 = renderer.toneMappingExposure; hid.forEach(o => { o.visible = false; }); renderer.shadowMap.needsUpdate = false; if (ibl) sc.environment = ibl; if (k) renderer.toneMappingExposure = ex0 * k;
    try { cc.update(renderer, sc); if (!PR51.pm) PR51.pm = new T.PMREMGenerator(renderer); const ty = rt.texture.type; rt.texture.type = T.HalfFloatType; try { out = PR51.pm.fromCubemap(rt.texture); } finally { rt.texture.type = ty; } }
    catch (e) { out = null; }
    finally { renderer.toneMappingExposure = ex0; hid.forEach(o => { o.visible = true; }); renderer.shadowMap.needsUpdate = sm; sc.environment = e0; sc.remove(cc); renderer.setRenderTarget(prev); rt.dispose(); lastS49 = s49; lastC49 = c49; }
    return out;
  }""")
rep("ENVS.in = t; scene.environment = t;", "ENVS.in = t; scene.environment = t; PR51.ws = true;")
rep("ENVS.out = t; try { if (dW) { dW.scene.environment = t; } }", "ENVS.out = t; try { if (dW) { dW.scene.environment = t; dW.probe51 = true; } }")
rep("    decorSig = sig;", "    decorSig = sig; PR51.ws = true;")
rep("    W.wet = wet;\n  }", "    W.wet = wet; W.probe51 = true;\n  }")
rep("""    if (canvas.isConnected && canvas.clientWidth) {
      renderer.render(scene, camera);
      placeMarkers();""", """    if (canvas.isConnected && canvas.clientWidth) {
      if (PR51.ws && !booth) {
        PR51.ws = false; const c = car && car.position, rt = probe51(scene, c ? c.x - 0.1 : 0, 1.25, c ? c.z : 0, [car], ENVS.in);
        if (rt) { if (PR51.wsRT) PR51.wsRT.dispose(); PR51.wsRT = rt; scene.environment = rt.texture; }
      }
      renderer.render(scene, camera);
      placeMarkers();""")
rep("""    paintTick22(now);
    if (canvas.isConnected && canvas.clientWidth) { renderer.shadowMap.needsUpdate = true; renderer.render(dW.scene, camera);""",
"""    paintTick22(now);
    if (dW.probe51 && canvas.isConnected) {
      dW.probe51 = false; const rt = probe51(dW.scene, 5.5, 1.3, -9.5, [dW.ride, van33G, d.walk && d.walk.me, dW.rain], ENVS.out, 0.45);
      if (rt) { if (dW.probeRT51) dW.probeRT51.dispose(); dW.probeRT51 = rt; dW.scene.environment = rt.texture; }
    }
    if (canvas.isConnected && canvas.clientWidth) { renderer.shadowMap.needsUpdate = true; renderer.render(dW.scene, camera);""")
rep("  api.envState = () => ({ in: !!ENVS.in, out: !!ENVS.out });",
    "  api.envState = () => ({ in: !!ENVS.in, out: !!ENVS.out });\n"
    "  window.__probe51 = () => ({ ws: !!(PR51.wsRT && scene.environment === PR51.wsRT.texture), out: !!(dW && dW.probeRT51 && dW.scene.environment === dW.probeRT51.texture) });")
f.save()
print('p51c ok')
