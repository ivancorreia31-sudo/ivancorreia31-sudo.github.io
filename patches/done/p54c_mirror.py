# build 54: door mirrors and wheel arches up close. The mirror glass was a flat card behind a housing whose back was
# fully rounded, so its corners stuck out above and below as grey triangles. The housing is now rounded at the front
# and closed at the back by a black frame the glass sits in. The black wheel-arch liners caught a pale sheen at their
# edges from the reflections; they're matt now.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("      fixed(rbox(0.12, 0.08, 0.16, 0.03, M.paint, 0.66, sty.van ? 1.08 : 1.0, s * 0.97), 'block', true);",
    "      fixed(rbox(0.10, 0.08, 0.16, 0.03, M.paint, 0.67, sty.van ? 1.08 : 1.0, s * 0.97), 'block', true);\n"
    "      fixed(rbox(0.02, 0.076, 0.156, 0.006, M.trim, 0.611, sty.van ? 1.08 : 1.0, s * 0.97), 'block', true);")
rep("      { const mg = new T.Mesh(new T.PlaneGeometry(0.11, 0.06), M.chrome); mg.rotation.y = -PI / 2; fixed(at(mg, 0.598, sty.van ? 1.08 : 1.0, s * 0.97), 'block', true); }",
    "      { const mg = new T.Mesh(new T.PlaneGeometry(0.136, 0.05), M.chrome); mg.rotation.y = -PI / 2; fixed(at(mg, 0.6005, sty.van ? 1.08 : 1.0, s * 0.97), 'block', true); }")
rep("  const XRAY = [M.paint, M.glass, M.trim, M.well];", "  const XRAY = [M.paint, M.glass, M.trim, M.well];\n  M.well.metalness = 0; M.well.envMapIntensity = 0.3;")
f.save()
print('p54c ok')
