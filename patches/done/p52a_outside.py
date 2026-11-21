# build 52: the forecourt's oil stains were soft round dark blobs drawn without light, so they read as shadows of nothing
# beside the player. They're now the workshop floor's stains (oil drips, tyre scuffs, a dried puddle ring), lit and a
# little glossy, so they sit in the sun and the shade like the concrete round them. Outside, only real highlights glow:
# the glow pass starts at 93% brightness instead of 80% (sunlit concrete was blooming into a haze).
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
a = f.s.index("      const stainTex = canvasTex(128, 128, (c, w, h) => { c.clearRect(0, 0, w, h); for (let k = 0; k < 5; k++)")
b = f.s.index("sc.add(m); }", a) + len("sc.add(m); }")
assert b - a < 1200, b - a
f.s = f.s[:a] + """      { const spots = [[-4, -10, 2.0, 0], [5, -12.5, 1.6, 1], [1, -7, 1.3, 2], [24, -14, 1.8, 3], [33, -18, 1.5, 0], [-30, -9, 1.6, 1], [0.4, -13.6, 2.6, 4], [-2.6, -8.2, 1.2, 5], [6.4, -9.2, 1.0, 6]];
        const geos = {}, list = [];
        for (const [x, z, s, k] of spots) {
          if (!geos[k]) { const gg = new T.PlaneGeometry(1, 1), u = gg.attributes.uv; for (let i = 0; i < u.count; i++) u.setXY(i, ((k % 4) + u.getX(i)) / 4, 1 - (Math.floor(k / 4) + 1 - u.getY(i)) / 2); gg.rotateX(-PI / 2); geos[k] = gg; }
          list.push([geos[k], new T.Matrix4().compose(new T.Vector3(x, 0.026, z), new T.Quaternion().setFromEuler(new T.Euler(0, rnd20() * 6.28, 0)), new T.Vector3(s, 1, s))]);
        }
        const sm = new T.Mesh(mergeGeo(list), M.stain); sm.renderOrder = 1; sm.receiveShadow = true; sm.userData.stain52 = true; sc.add(sm); Object.values(geos).forEach(g => g.dispose()); }""" + f.s[b:]
# the glow threshold: outside 0.93, everywhere else 0.8
rep("    paintTick22(now);\n    if (dW.probe51 && canvas.isConnected) {", "    paintTick22(now); POST.thr = 0.93;\n    if (dW.probe51 && canvas.isConnected) {")
rep("""    if (canvas.isConnected && canvas.clientWidth) {
      if (PR51.ws && !booth) {""", """    if (canvas.isConnected && canvas.clientWidth) {
      POST.thr = 0.8;
      if (PR51.ws && !booth) {""")
rep("      renderer.render(ext.scene, ext.camera);", "      POST.thr = 0.8; renderer.render(ext.scene, ext.camera);")
# and outside is drawn a touch darker (exposure ×0.9): sunlit pavement was close to white
rep("  let HEMI0 = 0.1, EXPO0 = 1.0;", "  let HEMI0 = 0.1, EXPO0 = 1.0, expoWs52 = 1.0;")
rep("    renderer.toneMappingExposure = EXPO0 * (lv('lights') ? 1.12 : 1.0);", "    expoWs52 = EXPO0 * (lv('lights') ? 1.12 : 1.0); renderer.toneMappingExposure = expoWs52;")
rep("    paintTick22(now); POST.thr = 0.93;", "    paintTick22(now); POST.thr = 0.93; renderer.toneMappingExposure = expoWs52 * 0.9;")
rep("      POST.thr = 0.8;\n      if (PR51.ws && !booth) {", "      POST.thr = 0.8; renderer.toneMappingExposure = expoWs52;\n      if (PR51.ws && !booth) {")
rep("      POST.thr = 0.8; renderer.render(ext.scene, ext.camera);", "      POST.thr = 0.8; renderer.toneMappingExposure = expoWs52; renderer.render(ext.scene, ext.camera);")
rep("    if (canvas.isConnected && canvas.clientWidth) { renderer.shadowMap.needsUpdate = true; renderer.render(scene, camera); adaptDpr(dt); }",
    "    if (canvas.isConnected && canvas.clientWidth) { renderer.shadowMap.needsUpdate = true; POST.thr = 0.8; renderer.toneMappingExposure = expoWs52; renderer.render(scene, camera); adaptDpr(dt); }")
# for the tests
rep("  window.__probe51 = () =>", "  window.__out52 = () => { let st = null; if (dW) dW.scene.traverse(o => { if (o.userData.stain52) st = { lit: !!(o.material && o.material.isMeshStandardMaterial), verts: o.geometry.attributes.position.count }; }); return { stain: st, expo: +renderer.toneMappingExposure.toFixed(3), ws: +expoWs52.toFixed(3), thr: POST.thr }; };\n  window.__probe51 = () =>")
f.save()
print('p52a ok')
