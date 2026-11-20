# build 51: the simple cars outside (yard, car park, showroom, traffic) close up are made like the workshop car: the same
# fine body skin (so a van's rear door windows and cab windows are the same as in the workshop) and the lamps the same
# size, kept on the flat of the nose and tail the way the workshop lamps are (the yard van's tail lamps were wrapped
# round its rear corners)
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const SKL = skin24(s, { lod: far ? 2 : 1 });", "const SKL = skin24(s, { lod: far ? 2 : 0 });")
rep("seated.push([kind, seatGeo27(SKL, g, front, null, lift, rigid, far ? 0.17 : 0.09)]); };",
    "seated.push([kind, seatGeo27(SKL, g, front, null, lift, rigid, far ? 0.17 : 0.045)]); };\n"
    "    /* build 51: a lamp's centre is kept in from the corner as the workshop car's are (conformLamps24) */\n"
    "    const zL51 = (front, y, z, halfW) => Math.sign(z) * Math.min(Math.abs(z), 0.81 * SKL.SF(SKL.faceX(front, y), y) - halfW * 0.8);")
# headlamps
rep("lp.rotateZ(PI / 2); seatL('lamp', lp, M4(2.168, HF.y, sd * (HF.z + dz)), true, -0.012, true); const ring = new T.TorusGeometry(HF.r + 0.003, 0.009, 6, 20); ring.rotateY(PI / 2); seatL('chrome', ring, M4(2.183, HF.y, sd * (HF.z + dz)), true, 0.008, true); }",
    "lp.rotateZ(PI / 2); const zc = zL51(true, HF.y, sd * HF.z, lampHalf32(HF)) + sd * dz; seatL('lamp', lp, M4(2.168, HF.y, zc), true, -0.012, true); const ring = new T.TorusGeometry(HF.r + 0.003, 0.009, 6, 20); ring.rotateY(PI / 2); seatL('chrome', ring, M4(2.183, HF.y, zc), true, 0.008, true); }")
rep("else if (HF) seatL('lamp', RB(0.05, HF.h, HF.w, Math.min(0.024, HF.h / 2)), M4(2.148, HF.y, sd * HF.z), true, -0.03);",
    "else if (HF) seatL('lamp', RB(0.05, HF.h, HF.w, Math.min(0.024, HF.h / 2)), M4(2.148, HF.y, zL51(true, HF.y, sd * HF.z, lampHalf32(HF))), true, -0.03);")
rep("seatL('lamp', lp, M4(2.168, 0.64, sd * 0.60), true, 0, true); const ring = new T.TorusGeometry(0.058, 0.01, 6, 20); ring.rotateY(PI / 2); seatL('chrome', ring, M4(2.183, 0.64, sd * 0.60), true, 0.02, true); }",
    "const zc = zL51(true, 0.64, sd * 0.60, 0.165); seatL('lamp', lp, M4(2.168, 0.64, zc), true, 0, true); const ring = new T.TorusGeometry(0.058, 0.01, 6, 20); ring.rotateY(PI / 2); seatL('chrome', ring, M4(2.183, 0.64, zc), true, 0.02, true); }")
rep("else { seatL('lamp', RB(0.05, 0.085, 0.33, 0.024), M4(2.148, 0.635, sd * 0.5), true, -0.03); seatL('chrome', RB(0.01, 0.06, 0.08, 0.02), M4(2.165, 0.638, sd * 0.43), true, 0.018, true); }",
    "else { const zc = zL51(true, 0.635, sd * 0.545, 0.165); seatL('lamp', RB(0.05, 0.116, 0.33, 0.024), M4(2.148, 0.635, zc), true, -0.03); for (const dz of [-0.075, 0.065]) { const bw = new T.CylinderGeometry(0.024, 0.024, 0.012, 14); bw.rotateZ(PI / 2); seatL('chrome', bw, M4(2.17, 0.641, zc + dz), true, 0.002, true); } }")
# tail lamps
rep("const ty = s.van ? 1.08 : s.tailY, tx = SKL.faceX(false, ty) + 0.014;",
    "const ty = s.van ? 1.08 : s.tailY, tx = SKL.faceX(false, ty) + 0.014, tz = zL51(false, ty, sd * TF.z, lampHalf32(TF));")
rep("lp.rotateZ(PI / 2); seatL('tail', lp, M4(tx, ty, sd * (TF.z + dz)), false, -0.012, true); }",
    "lp.rotateZ(PI / 2); seatL('tail', lp, M4(tx, ty, tz + sd * dz), false, -0.012, true); }")
rep("else seatL('tail', RB(0.05, TF.h, TF.w, Math.min(0.02, TF.h / 2)), M4(tx, ty, sd * TF.z), false, -0.03);",
    "else seatL('tail', RB(0.05, TF.h, TF.w, Math.min(0.02, TF.h / 2)), M4(tx, ty, tz), false, -0.03);")
rep("} else if (s.van) seatL('tail', RB(0.05, 0.30, 0.12, 0.02), M4(tailX, 1.08, sd * 0.74), false, -0.03); else seatL('tail', RB(0.05, 0.085, 0.36, 0.02), M4(tailX, s.tailY, sd * 0.5), false, -0.03);",
    "} else if (s.van) seatL('tail', RB(0.05, 0.30, 0.12, 0.02), M4(tailX, 1.08, zL51(false, 1.08, sd * 0.74, 0.06)), false, -0.03); else seatL('tail', RB(0.05, 0.112, 0.36, 0.02), M4(tailX, s.tailY, zL51(false, s.tailY, sd * 0.58, 0.18)), false, -0.03);")
# close up: the workshop car's wipers and shark-fin aerial
rep("      if (s.roofSpoiler) add('paint', RB(0.22, 0.03, 1.34, 0.012), M4(x1 - 0.06, ry + 0.015, 0));",
    "      if (s.roofSpoiler) add('paint', RB(0.22, 0.03, 1.34, 0.012), M4(x1 - 0.06, ry + 0.015, 0));\n"
    "      if (!far && s.glass) { add('paint', EX([[x1 + 0.05, ry + 0.02], [x1 + 0.22, ry + 0.02], [x1 + 0.08, ry + 0.075]], 0.04, 0, -0.02));\n"
    "        const gx = s.glass[0][0], gy = s.glass[0][1], sl = (s.glass[1][1] - gy) / (gx - s.glass[1][0]);\n"
    "        for (const [z, len] of [[-0.18, 0.56], [0.33, 0.5]]) add('dark', new T.BoxGeometry(0.014, 0.012, len), M4(gx - 0.06, gy + 0.06 * sl + 0.04 * Math.sqrt(1 + sl * sl) + 0.008, z)); }")
# for the tests: how far each simple car's lamps reach round from the face they sit on (a lamp on the flat of the tail
# reaches back only a few centimetres; the van's used to wrap 40 cm round the corner)
rep("  function miniCar(paint, style) {",
    "  window.__lite51 = (name, far) => { const g = liteGeo(name, !!far), r = { rear: g.rear, reachT: 0, reachH: 0 }; const scan = (k, f) => { const q = g[k] && g[k].attributes.position; if (q) for (let i = 0; i < q.count; i++) f(q.getX(i)); };\n"
    "    scan('tail', x => { if (x < g.rear + 0.6) r.reachT = Math.max(r.reachT, x - g.rear); }); scan('lamp', x => { if (x > 1.5) r.reachH = Math.max(r.reachH, 2.2 - x); }); r.reachT = +r.reachT.toFixed(3); r.reachH = +r.reachH.toFixed(3);\n"
    "    r.tris = Object.keys(g).reduce((n, k) => n + (g[k] && g[k].isBufferGeometry ? g[k].attributes.position.count / 3 : 0), 0) | 0; r.styles = Object.keys(STYLES); return r; };\n"
    "  function miniCar(paint, style) {")
f.save()
print('p51a ok')
