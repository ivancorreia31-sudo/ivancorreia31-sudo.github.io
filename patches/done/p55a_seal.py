# build 55: window rubbers. The side windows ran straight up into the painted roof rail; real ones sit in a black
# rubber seal. The fine body skin (the car on the ramp and every car close up outside) now has a seal along the top of
# the side windows as well as the one along the bottom, about 2.5 cm deep.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("    const fc = lod > 1 ? [0, 0.07, 1] : lod ? [0, 0.07, 0.55, 1] : [0, 0.07, 0.3, 0.53, 0.77, 1];",
    "    const fc = lod > 1 ? [0, 0.07, 1] : lod ? [0, 0.07, 0.55, 1] : [0, 0.07, 0.3, 0.53, 0.77, 0.935, 1];")
rep("        return uLo < 0.01 ? 'dark' : 'glass';", "        return uLo < 0.01 || uLo > 0.93 ? 'dark' : 'glass';")
# side repeaters: a small amber indicator on each front wing, between the wheel arch and the door
rep("  M.well.metalness = 0; M.well.envMapIntensity = 0.3;", "  M.well.metalness = 0; M.well.envMapIntensity = 0.3;\n  M.amber = std('#F2A33A', { emissive: col('#4a2a06'), roughness: 0.2 });")
rep("      /* the fuel flap, on the rear quarter of the right-hand side */",
    "      /* build 55: the side repeater on the front wing */\n"
    "      if (!sty.open || sty.cabrio) { const rx0 = Math.max(Math.max.apply(null, seams) + 0.12, 0.88); if (rx0 < 1.0) fixed(rbox(0.05, 0.02, 0.012, 0.008, M.amber, rx0, 0.735, s * 0.906), 'auto', true); }\n"
    "      /* the fuel flap, on the rear quarter of the right-hand side */")
rep("  window.__probe51 = () =>", "  window.__b55 = () => { let rep = 0; if (car) car.traverse(m => { if (m.isMesh && m.material === M.amber) rep++; }); return { rep }; };\n  window.__probe51 = () =>")
f.save()
print('p55a ok')
