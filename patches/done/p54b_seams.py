# build 54: shut lines. Each door had a single 8 mm black bar standing proud of the paint at its front and back, and
# nothing along the bottom, so up close they looked drawn on. They're fine grooves now (4.5 mm), the doors are outlined
# along the bottom too, a rear door's back edge runs down to the wheel arch, and there's a fuel flap on the rear quarter.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("""      const seams = sty.seams || [0.78, -0.35].concat(sty.doors > 1 ? [-1.15] : []);
      seams.forEach((x, i) => {
        const inArch = Math.abs(x - 1.35) < 0.45 || Math.abs(x - sty.rx) < 0.45;
        const y0 = inArch ? 0.66 : 0.35;
        fixed(at(new T.Mesh(new T.BoxGeometry(0.008, 0.885 - y0, 0.008, 1, 10, 1), M.trim), x, (0.885 + y0) / 2, s * 0.905), 'auto', true);
        if (i > 0) fixed(rbox(0.11, 0.025, 0.02, 0.008, M.trim, x + 0.15, 0.82, s * 0.91), 'auto', true);
      });""",
"""      const seams = sty.seams || [0.78, -0.35].concat(sty.doors > 1 ? [-1.15] : []);
      /* build 54: fine grooves, the bottom edge too; a line in an arch's reach starts just above the arch */
      const ZS = 0.9025, yB = 0.375, archTop = x => { const ax = Math.abs(x - 1.35) < Math.abs(x - sty.rx) ? 1.35 : sty.rx, dx = Math.abs(x - ax); return dx < 0.405 ? 0.30 + Math.sqrt(0.405 * 0.405 - dx * dx) + 0.012 : 0; };
      seams.forEach((x, i) => {
        const y0 = Math.max(yB, archTop(x));
        fixed(at(new T.Mesh(new T.BoxGeometry(0.0045, 0.885 - y0, 0.005, 1, 10, 1), M.trim), x, (0.885 + y0) / 2, s * ZS), 'auto', true);
        if (i > 0) fixed(rbox(0.11, 0.025, 0.02, 0.008, M.trim, x + 0.15, 0.82, s * 0.91), 'auto', true);
      });
      { const xa = Math.max(Math.min.apply(null, seams), sty.rx + 0.40), xb = Math.min(Math.max.apply(null, seams), 1.35 - 0.40);
        if (xb - xa > 0.2) fixed(at(new T.Mesh(new T.BoxGeometry(xb - xa, 0.0045, 0.005, 24, 1, 1), M.trim), (xa + xb) / 2, yB, s * ZS), 'auto', true); }
      /* the fuel flap, on the rear quarter of the right-hand side */
      if (s > 0 && !sty.open) {
        const fxp = Math.min(sty.rx - 0.05, Math.min.apply(null, seams) - 0.2), fyp = 0.78;
        if (fxp - 0.09 > R + 0.25) {
          const rr = (sh, w, h, r) => { sh.moveTo(-w / 2 + r, -h / 2); sh.lineTo(w / 2 - r, -h / 2); sh.quadraticCurveTo(w / 2, -h / 2, w / 2, -h / 2 + r); sh.lineTo(w / 2, h / 2 - r); sh.quadraticCurveTo(w / 2, h / 2, w / 2 - r, h / 2); sh.lineTo(-w / 2 + r, h / 2); sh.quadraticCurveTo(-w / 2, h / 2, -w / 2, h / 2 - r); sh.lineTo(-w / 2, -h / 2 + r); sh.quadraticCurveTo(-w / 2, -h / 2, -w / 2 + r, -h / 2); return sh; };
          const ring = rr(new T.Shape(), 0.165, 0.12, 0.03); ring.holes.push(rr(new T.Path(), 0.156, 0.111, 0.026));
          const g = new T.ExtrudeGeometry(ring, { depth: 0.004, bevelEnabled: false, curveSegments: 4 }); g.translate(0, 0, -0.002);
          fixed(at(new T.Mesh(g, M.trim), fxp, fyp, ZS), 'auto', true);
        }
      }""")
f.save()
print('p54b ok')
