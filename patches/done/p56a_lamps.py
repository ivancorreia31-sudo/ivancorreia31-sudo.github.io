# build 56: lamps up close. Tail lamps were one block of red with an LED bar; real ones are in sections. Each is now red
# (with its LED bar), an amber indicator and a clear reversing lamp, the clear one nearest the middle (or lowest on tall
# lamps), and the red lens is glossier. Twin round tail lamps have a clear inner one. Headlamps get an amber indicator at
# their outer end and a projector lens in the inner bowl.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("  M.amber = std('#F2A33A', { emissive: col('#4a2a06'), roughness: 0.2 });",
    "  M.amber = std('#F2A33A', { emissive: col('#4a2a06'), roughness: 0.2 });\n"
    "  M.rev = std('#E6EAEB', { roughness: 0.08, metalness: 0.55 }); M.amberL = M.amber.clone(); M.proj = std('#1E2428', { roughness: 0.04, metalness: 0.5 });")
rep("    tail: std('#A3231C', { emissive: col('#3d0c08'), roughness: 0.3 }),", "    tail: std('#A3231C', { emissive: col('#3d0c08'), roughness: 0.14 }),", 2)
# headlamps
rep("""            g.add(box(0.008, Math.max(0.005, Math.min(0.009, F.h * 0.2)), F.w * 0.86, M.drl, 0.025, -F.h * 0.36, 0));
            g.add(rbox(0.006, F.h + 0.004, F.w + 0.004, Math.min(0.024, F.h / 2), M.lens, 0.028, 0, 0));""",
"""            g.add(box(0.008, Math.max(0.005, Math.min(0.009, F.h * 0.2)), F.w * 0.86, M.drl, 0.025, -F.h * 0.36, 0));
            if (F.w > 0.22) g.add(box(0.004, Math.min(0.045, F.h * 0.55), 0.03, M.amberL, 0.027, 0, s * (F.w / 2 - 0.028)));
            if (nb === 2) { const pj = new T.Mesh(new T.SphereGeometry(br * 0.55, 14, 10), M.proj); pj.scale.set(0.6, 1, 1); g.add(at(pj, 0.03, 0, -s * 0.25 * F.w)); }
            g.add(rbox(0.006, F.h + 0.004, F.w + 0.004, Math.min(0.024, F.h / 2), M.lens, 0.028, 0, 0));""")
rep("""        g.add(box(0.008, 0.009, led ? 0.31 : 0.27, M.drl, 0.025, -0.029, 0));
        g.add(rbox(0.006, 0.084, 0.334, 0.024, M.lens, 0.028, 0, 0));""",
"""        g.add(box(0.008, 0.009, led ? 0.31 : 0.27, M.drl, 0.025, -0.029, 0));
        g.add(box(0.004, 0.05, 0.032, M.amberL, 0.027, 0.004, s * 0.142));
        { const pj = new T.Mesh(new T.SphereGeometry(0.017, 14, 10), M.proj); pj.scale.set(0.6, 1, 1); g.add(at(pj, 0.03, 0.006, s > 0 ? -0.075 : 0.065)); }
        g.add(rbox(0.006, 0.084, 0.334, 0.024, M.lens, 0.028, 0, 0));""")
# tail lamps
rep("""      const tail = led => {
        const g = new T.Group(), lens = led ? M.smoke : M.tail, F = sty.tl && TL32[sty.tl];""",
"""      /* build 56: a tail lamp in sections, each its own solid lens: clear reversing lamp nearest the middle (or lowest), amber, then red with its LED bar */
      const zones56 = (g, w, h, vert, led, lens) => {
        const r = Math.min(0.02, h / 2, w / 2);
        if (!vert) {
          const zi = -s * w / 2, rw = w * 0.28, aw = w * 0.12, red = w - rw - aw, zr = s * (w / 2 - red / 2);
          g.add(rbox(0.05, h, red, r, lens, 0, 0, zr));
          g.add(rbox(0.048, h, aw - 0.004, Math.min(0.006, h / 2), M.amberL, 0.001, 0, zi + s * (rw + aw / 2)));
          g.add(rbox(0.05, h, rw - 0.004, r, M.rev, 0, 0, zi + s * rw / 2));
          g.add(box(0.006, Math.max(0.008, h * 0.18), red * 0.86, M.led, -0.027, h * 0.2, zr));
          if (led) g.add(box(0.006, Math.max(0.008, h * 0.14), red * 0.86, M.led, -0.027, -h * 0.22, zr));
        } else {
          const yb = -h / 2, rh = h * 0.27, ah = h * 0.15, red = h - rh - ah, yr = h / 2 - red / 2;
          g.add(rbox(0.05, red, w, r, lens, 0, yr, 0));
          g.add(rbox(0.048, ah - 0.004, w, Math.min(0.006, ah / 2), M.amberL, 0.001, yb + rh + ah / 2, 0));
          g.add(rbox(0.05, rh - 0.004, w, Math.min(r, rh / 2), M.rev, 0, yb + rh / 2, 0));
          g.add(box(0.006, red * 0.8, Math.max(0.008, w * 0.18), M.led, -0.027, yr, led ? -w * 0.2 : 0));
          if (led) g.add(box(0.006, red * 0.8, Math.max(0.008, w * 0.18), M.led, -0.027, yr, w * 0.2));
        }
      };
      const tail = led => {
        const g = new T.Group(), lens = led ? M.smoke : M.tail, F = sty.tl && TL32[sty.tl];""")
rep("              g.add(cyl(F.r * 0.45, 0.006, M.led, -0.022, 0, dz, 'x', 16));",
    "              g.add(cyl(F.r * 0.45, 0.006, F.two && Math.sign(dz) === -s ? M.rev : M.led, -0.022, 0, dz, 'x', 16));")
rep("""            g.add(rbox(0.05, F.h, F.w, Math.min(0.02, F.h / 2), lens)); g.add(box(0.006, Math.max(0.008, F.h * 0.18), F.w * 0.84, M.led, -0.027, F.h * 0.2, 0));
            if (led) g.add(box(0.006, Math.max(0.008, F.h * 0.14), F.w * 0.84, M.led, -0.027, -F.h * 0.22, 0));""",
"""            zones56(g, F.w, F.h, F.h > F.w * 0.9, led, lens);""")
rep("        if (sty.van) { g.add(rbox(0.05, 0.30, 0.12, 0.02, lens)); g.add(box(0.006, led ? 0.26 : 0.22, 0.02, M.led, -0.027, 0, 0)); return at(g, tailX, 1.08, s * 0.74); }",
    "        if (sty.van) { zones56(g, 0.12, 0.30, true, led, lens); return at(g, tailX, 1.08, s * 0.74); }")
rep("""        g.add(rbox(0.05, 0.08, 0.36, 0.02, lens)); g.add(box(0.006, 0.014, 0.30, M.led, -0.027, 0.016, 0));
        if (led) g.add(box(0.006, 0.01, 0.30, M.led, -0.027, -0.018, 0));""",
"""        zones56(g, 0.34, 0.08, false, led, lens);""")
rep("        return at(g, tailX, sty.tailY, s * 0.58);\n      };", "        return at(g, tailX, sty.tailY, s * 0.555);\n      };")
rep("  window.__probe51 = () =>", "  window.__lamps56 = () => { const o = { rev: 0, amber: 0, proj: 0 }; if (car) car.traverse(m => { if (!m.isMesh || !m.visible) return; let p = m; while (p && !p.userData.part) p = p.parent; const part = p && p.userData.part || ''; if (m.material === M.rev && /taillamp/.test(part)) o.rev++; if (m.material === M.amberL && /lamp/.test(part)) o.amber++; if (m.material === M.proj) o.proj++; }); return o; };\n  window.__probe51 = () =>")
f.save()
print('p56a ok')
