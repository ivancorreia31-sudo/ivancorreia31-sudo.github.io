# build 54: the grey trim on the inside of each windscreen pillar was centred on the windscreen's own line, so half of it
# stood out through the glass: a pale strip up the outside of the A-pillar on many cars. It now sits just behind the
# glass and inside the pillar, on every model (the body's inner face is found by casting a ray across the cabin).
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("""        const tum = S.tum != null ? S.tum : van ? 0.1 : 0.42, pz = 0.7, pt = 0.7 - tum * 0.25;
        put('liner', beam3([gx0 - 0.03, G[0][1] + 0.03, s * pz], [G[1][0] + 0.02, G[1][1] - 0.02, s * pt], 0.055, M.dash));""",
"""        const tum = S.tum != null ? S.tum : van ? 0.1 : 0.42, pz = 0.7, pt = 0.7 - tum * 0.25;
        /* build 54: moved back off the windscreen by its own half-thickness and a little, and in from the body's side */
        const a0 = [gx0 - 0.03, G[0][1] + 0.03], a1 = [G[1][0] + 0.02, G[1][1] - 0.02], ddx = a1[0] - a0[0], ddy = a1[1] - a0[1], dl = Math.hypot(ddx, ddy) || 1, nx = -ddy / dl, ny = ddx / dl, k = 0.045;
        const b0 = [a0[0] + nx * k, a0[1] + ny * k], b1 = [a1[0] + nx * k, a1[1] + ny * k];
        const zAt = b => Math.min(zIn54(b[0], b[1], s), zIn54(b[0] - 0.04, b[1] + 0.03, s), zIn54(b[0], b[1] + 0.02, s)) - 0.04, z0 = Math.min(pz, zAt(b0)), z1 = Math.min(pt, zAt(b1));
        /* then each end is pulled further in until all eight corners are inside the cabin, seen from its middle */
        let e0 = [b0[0], b0[1], z0], e1 = [b1[0], b1[1], z1], bm = null;
        for (let it = 0; it < 10; it++) {
          if (bm) bm.geometry.dispose();
          bm = beam3([e0[0], e0[1], s * e0[2]], [e1[0], e1[1], s * e1[2]], 0.055, M.dash); bm.updateMatrix();
          const q = bm.geometry.attributes.position, v = new T.Vector3(); let p0 = false, p1 = false;
          for (let i = 0; i < q.count; i++) { v.fromBufferAttribute(q, i).applyMatrix4(bm.matrix); if (!inside54(v)) { if (v.y > (e0[1] + e1[1]) / 2) p1 = true; else p0 = true; } }
          if (!p0 && !p1) break;
          if (p0) e0 = [e0[0] + nx * 0.012, e0[1] + ny * 0.012, e0[2] - 0.012]; if (p1) e1 = [e1[0] + nx * 0.012, e1[1] + ny * 0.012, e1[2] - 0.012];
        }
        put('liner', bm);""")
rep("  function interior32() {",
"""  /* build 54: how far out the body (paint or glass) is from the centre line at (x, y) on side s, by casting a ray across */
  let ray54 = null;
  function zIn54(x, y, s) {
    const sk = SK24; if (!sk) return 9;
    if (!ray54 || ray54.sk !== sk) { const mat = new T.MeshBasicMaterial({ side: T.DoubleSide }); ray54 = { sk, rc: new T.Raycaster(), ms: [sk.paint, sk.glass, sk.dark].filter(Boolean).map(g => new T.Mesh(g, mat)) }; }
    ray54.rc.set(new T.Vector3(x, y, 0), new T.Vector3(0, 0, s > 0 ? 1 : -1)); ray54.rc.far = 2;
    const h = ray54.rc.intersectObjects(ray54.ms, false); return h.length ? h[0].distance : 9;
  }
  /* a point is inside the cabin when a ray from the middle of it (x -0.1, y 1.05) reaches the point before the body or glass */
  function inside54(v) {
    if (!SK24) return true; zIn54(0, 1, 1);
    const o = new T.Vector3(-0.1, 1.05, 0), d = v.clone().sub(o), L = d.length(); ray54.rc.set(o, d.normalize()); ray54.rc.far = L;
    const h = ray54.rc.intersectObjects(ray54.ms, false); return !(h.length && h[0].distance < L - 0.004);
  }
  function interior32() {""")
# for the tests: interior lining vertices that stand outside the body or the glass, seen from the cabin (x 0.8 - 0.9, y 1.05)
rep("  window.__probe51 = () =>", "  window.__pillar54 = () => { if (!car || !SK24) return null; zIn54(0, 1, 1); const rc = ray54.rc, o = new T.Vector3(-0.1, 1.05, 0), v = new T.Vector3(), d = new T.Vector3(); let n = 0, out = 0; car.traverse(m => { if (!m.isMesh || m.userData.int32 !== 'liner') return; const q = m.geometry.attributes.position; for (let i = 0; i < q.count; i += 3) { v.fromBufferAttribute(q, i).applyMatrix4(m.matrix); d.copy(v).sub(o); const L = d.length(); rc.set(o, d.normalize()); rc.far = L; n++; const h = rc.intersectObjects(ray54.ms, false); if (h.length && h[0].distance < L - 0.004) out++; } }); return { n, out }; };\n  window.__probe51 = () =>")
# the sun visors: their outer front corners went through the glass where the cabin narrows under the roof
rep("      for (const s of [-1, 1]) BX('liner', 0.2, 0.012, 0.34, G[1][0] - 0.1, ly - 0.025, s * 0.32);",
    "      for (const s of [-1, 1]) BX('liner', 0.2, 0.012, 0.29, G[1][0] - 0.15, ly - 0.03, s * 0.27);")
# the roof lining: as wide as the roof is at its height, front, middle and back (it went through the rounded roof edge)
rep("      if (lx1 > lx0) BX('liner', lx1 - lx0, 0.02, 1.16, (lx0 + lx1) / 2, ly, 0);",
    "      if (lx1 > lx0) { let hz = Math.min(0.58, ...[lx0, (lx0 + lx1) / 2, lx1].map(x => zIn54(x, ly + 0.012, 1) - 0.02)), y = ly, a = lx0, b = lx1; const ok = () => [a, b].every(x => inside54(new T.Vector3(x, y + 0.011, hz)) && inside54(new T.Vector3(x, y + 0.011, -hz)));\n"
    "        for (let it = 0; it < 24 && !ok(); it++) { if (it % 3 === 0) y -= 0.008; else if (it % 3 === 1) { a += 0.02; b -= 0.02; } else hz -= 0.015; }\n"
    "        BX('liner', b - a, 0.02, 2 * hz, (a + b) / 2, y, 0); }")
f.save()
print('p54a ok')
