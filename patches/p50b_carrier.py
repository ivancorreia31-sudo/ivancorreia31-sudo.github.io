# build 50 (b): the black front-end carrier inside the nose (the slam panel across the top, its two posts, the boxes
# behind the headlamps and the crossmember at the bottom) was built to one size for every car. The nose curves back at
# the corners, so the ends poked out through the paint by up to 6 cm: from under a raised car they showed as a black
# L round the headlamps. Each piece is now fitted inside the nose, with a 1.5 cm gap, using the nose's real shape.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("""    K.add('carrier', gT(rbx(0.09, 0.05, 1.40, 0.012), 1.995, 0.39, 0));
    K.add('carrier', gT(rbx(0.06, 0.035, 1.48, 0.01, { crown: 0.004 }), 2.045, 0.775, 0));
    for (const s of [-1, 1]) K.add('carrier', gT(rbx(0.06, 0.40, 0.05, 0.01), 2.0, 0.58, s * 0.71));""",
    """    /* the crossmember: as wide as the nose allows at its height */
    { let hw = 0.70; while (hw > 0.5 && nose50(0.365, 0.415, hw - 0.05, hw) - GAP50 < 2.04) hw -= 0.02; K.add('carrier', gT(rbx(0.09, 0.05, hw * 2, 0.012), 1.995, 0.39, 0)); }
    /* the slam panel across the top: a full-depth middle and stepped ends that follow the nose round */
    { const segs = [[0, 0.45]]; for (let z = 0.45; z < 0.735; z += 0.07) segs.push([z, Math.min(0.74, z + 0.07)]);
      for (const [z0, z1] of segs) {
        const x = fitX50(2.045, 0.06, 0.7575, 0.7925, z0, z1, 1.0); if (x < 1.96) continue;
        if (z0 === 0) K.add('carrier', gT(rbx(0.06, 0.035, z1 * 2, 0.01, { crown: 0.004 }), x, 0.775, 0));
        else for (const s of [-1, 1]) K.add('carrier', gT(rbx(0.06, 0.035, z1 - z0 + 0.004, 0.006), x, 0.775, s * (z0 + z1) / 2));
      } }
    /* its two posts, in from the corners and back inside the nose */
    for (const s of [-1, 1]) K.add('carrier', gT(rbx(0.06, 0.38, 0.05, 0.01), fitX50(2.0, 0.06, 0.38, 0.76, 0.635, 0.685, 1.90), 0.57, s * 0.66));""")
rep("""    for (const s of [-1, 1]) K.add('carrier', gT(rbx(0.12, 0.10, 0.30, 0.02), 2.03, 0.66, s * 0.55));""",
    """    for (const s of [-1, 1]) K.add('carrier', gT(rbx(0.07, 0.10, 0.24, 0.02), fitX50(2.03, 0.07, 0.61, 0.71, 0.42, 0.66, 1.93), 0.66, s * 0.54));""")
# the nose helpers go at the top of the bay, and the inner wing walls stop short of the nose too
rep("""  function bayShell21(L) {
    const K = kit21(), E = L.E;""", """  function bayShell21(L) {
    const K = kit21(), E = L.E;
    /* build 50: where the nose is (the foremost paint) over a patch of height and width, so the carrier fits inside */
    const nose50 = (y0, y1, z0, z1) => { let m = 9; for (let i = 0; i <= 4; i++) for (let j = 0; j <= 4; j++) { let v = NaN; try { v = SK24 && SK24.fx ? SK24.fx(true, y0 + (y1 - y0) * i / 4, z0 + (z1 - z0) * j / 4) : NaN; } catch (e) { v = NaN; } if (v === v) m = Math.min(m, v); } return m; };
    const GAP50 = 0.015, fitX50 = (x, d, y0, y1, z0, z1, xMin) => { const n = nose50(y0, y1, z0, z1); return n < 9 ? Math.max(xMin, Math.min(x, n - GAP50 - d / 2)) : x; };
""")
rep("""      K.add('paint', gT(rbx(1.08, 0.30, 0.02, 0.006), 1.46, 0.53, s * 0.80));""",
    """      { const xf = Math.max(1.6, Math.min(2.0, nose50(0.38, 0.68, 0.79, 0.81) - GAP50)); K.add('paint', gT(rbx(xf - 0.92, 0.30, 0.02, 0.006), (0.92 + xf) / 2, 0.53, s * 0.80)); }""")
# tests: everything in the engine bay that sits ahead of the nose's paint (should be nothing)
rep("window.__probe32 = (x, y, z) =>", """window.__bayNose50 = () => { if (!car || !SK24) return null; car.updateMatrixWorld(true); const inv = new T.Matrix4().copy(car.matrixWorld).invert(), v = new T.Vector3(), out = {};
    car.traverse(o => { if (!o.isMesh || !o.userData.role || !o.visible) return; for (let q = o.parent; q && q !== car; q = q.parent) if (!q.visible) return; const P = o.geometry.attributes.position, key = o.userData.role + (o.parent && o.parent.userData.part ? '@' + o.parent.userData.part : '');
      for (let i = 0; i < P.count; i += 2) { v.fromBufferAttribute(P, i).applyMatrix4(o.matrixWorld).applyMatrix4(inv); if (v.x < 1.8 || v.y < 0.25) continue; const nx = SK24.fx(true, v.y, v.z); if (nx !== nx) continue; const d = v.x - nx; if (!out[key] || d > out[key][0]) out[key] = [+d.toFixed(3), +v.x.toFixed(2), +v.y.toFixed(2), +v.z.toFixed(2)]; } });
    return Object.entries(out).filter(e => e[1][0] > -0.005).sort((a, b) => b[1][0] - a[1][0]); };
window.__probe32 = (x, y, z) =>""")
f.save()
print('p50b ok')
