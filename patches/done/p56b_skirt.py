# build 56: the chin under the nose and tail ran out to 76 cm either side whatever the car's width there; since the ends
# became crisper (build 51) its last strip stood outside the body at the corners, a blue spike under each bumper
# corner. Its width is now fitted (it stops where its lower edge would leave the body) and it tapers away at the ends.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("""  function skirt27(SK, front, n) {
    const yTop = 0.318, yBot = 0.2, zH = 0.76, sg = front ? 1 : -1, pos = [];
    n = n || 18;""",
"""  /* build 56: the body's half-width at (x, y) on a skin (paint or cladding), by a ray from the centre line (cached per skin) */
  function skinW56(SK, x, y) {
    if (!SK.paint) return 9;
    if (!SK.ray56) { const mt = new T.MeshBasicMaterial({ side: T.DoubleSide }); SK.ray56 = { rc: new T.Raycaster(), ms: [SK.paint, SK.dark].filter(Boolean).map(g => new T.Mesh(g, mt)) }; }
    const r = SK.ray56; r.rc.set(new T.Vector3(x, y, 0), new T.Vector3(0, 0, 1)); r.rc.far = 2;
    const h = r.rc.intersectObjects(r.ms, false); return h.length ? h[0].distance : 9;
  }
  function skirt27(SK, front, n) {
    const yTop = 0.318, yBot = 0.2, sg = front ? 1 : -1, pos = [];
    let zH = 0.76;
    for (; zH > 0.45; zH -= 0.01) { const x = SK.fx(front, yTop, zH); if (zH <= skinW56(SK, x - sg * 0.006, 0.3) && zH * 0.985 <= skinW56(SK, x - sg * 0.04, 0.3) - 0.012 && zH * 0.97 <= skinW56(SK, x - sg * 0.11, 0.3) - 0.012) break; }
    n = n || 18;""")
rep("  window.__probe51 = () =>", "  window.__skirt56 = () => { if (!SK24) return null; const o = []; for (const fr of [true, false]) { const g = skirt27(SK24, fr), q = g.attributes.position; let out = 0; for (let i = 0; i < q.count; i++) { const x = q.getX(i), y = q.getY(i), z = Math.abs(q.getZ(i)); if (z > skinW56(SK24, x, Math.max(0.3, y)) + 0.004) out++; } o.push(out); g.dispose(); } return o; };\n  window.__probe51 = () =>")
# and its ends taper to nothing, so seen from the side there's no triangle of it hanging under the corner
rep("for (let i = 0; i <= n; i++) { const z = -zH + 2 * zH * i / n, x = SK.fx(front, yTop, z); P.push([[x - sg * 0.006, yTop, z], [x - sg * 0.04, yBot, z * 0.985], [x - sg * 0.11, yBot + 0.012, z * 0.97]]); }",
    "for (let i = 0; i <= n; i++) { const z = -zH + 2 * zH * i / n, x = SK.fx(front, yTop, z), u = Math.min(1, (1 - Math.abs(z) / zH) / 0.22), t = u * u * (3 - 2 * u); P.push([[x - sg * 0.006, yTop, z], [x - sg * (0.006 + 0.034 * t), yTop - (yTop - yBot) * t, z * (1 - 0.015 * t)], [x - sg * (0.006 + 0.104 * t), yTop - (yTop - yBot - 0.012) * t, z * (1 - 0.03 * t)]]); }")
f.save()
print('p56b ok')
