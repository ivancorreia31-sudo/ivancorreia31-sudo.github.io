# build 53: the workshop lit like a workshop. It was lit by one big light from above (plus the sky), so everything was
# evenly bright and every shadow fell the same way. Three of the roof's light fittings (over the bay and either side) now really give light: pools of it
# on the floor, falling away towards the walls, and highlights moving over the car's paint as you go round it. The
# floor is a little glossier (sealed concrete), so it shows those lights. The overhead light is softer to make room for
# them. Battery saver leaves those lights off.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("  const sun = new T.DirectionalLight(0xfff1dc, 1.3); sun.position.set(2.5, 9, 3.5); sun.castShadow = true;",
    "  const sun = new T.DirectionalLight(0xfff1dc, 0.9); sun.position.set(2.5, 9, 3.5); sun.castShadow = true;")
rep("  const back = new T.DirectionalLight(0xdfe8ff, 0.15); back.position.set(-6, 5, -5); scene.add(back);",
    "  const back = new T.DirectionalLight(0xdfe8ff, 0.15); back.position.set(-6, 5, -5); scene.add(back);\n"
    "  /* build 53: three of the roof fittings give light, the one over the bay and the two beside it (no shadows; off in battery saver) */\n"
    "  const LT53 = [[0, 0], [-7, 0], [7, 0]].map(([x, z]) => { const p = new T.PointLight(0xfff4e6, 0.95, 16, 2); p.position.set(x, 5.05, z); scene.add(p); return p; });")
rep("M.floor.roughnessMap = TX.concreteR; M.floor.roughness = 1; M.floor.envMapIntensity = 0.74;", "M.floor.roughnessMap = TX.concreteR; M.floor.roughness = 0.72; M.floor.envMapIntensity = 0.8;")
rep("M.floor.roughnessMap = f ? null : TX.concreteR; M.floor.roughness = f >= 2 ? 0.3 : f ? 0.22 : 1;", "M.floor.roughnessMap = f ? null : TX.concreteR; M.floor.roughness = f >= 2 ? 0.3 : f ? 0.22 : 0.72;")
rep("    POST.user = PREF34.gfx === 'save' ? false : o.fx !== false; shadowDirty = true; kick();",
    "    POST.user = PREF34.gfx === 'save' ? false : o.fx !== false; shadowDirty = true; LT53.forEach(l => { l.visible = PREF34.gfx !== 'save'; }); PR51.ws = true; kick();")
# for the tests
rep("  window.__probe51 = () =>", "  window.__light53 = () => ({ on: LT53.filter(l => l.visible).length, sun: sun.intensity, floor: M.floor.roughness });\n  window.__gfx53 = g => api.prefs34({ gfx: g });\n  window.__probe51 = () =>")
f.save()
print('p53a ok')
