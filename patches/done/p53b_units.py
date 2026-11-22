# build 53: the buildings across the road and the farm barn were plain painted boxes. Their walls are now profiled steel
# cladding like the workshop's own (a rib every 250 mm that catches the light, a line of fixings, faint streaks), in
# each building's colour, standing on a dark blockwork plinth; the painted shop fronts are drawn at twice the detail
# with the same ribs, a plinth and dirt splashed up from the ground.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
# the material, and a box whose faces are mapped at the workshop cladding's scale (2 m × 1 m a tile)
rep("    B.mat('plainWall', std('#FFFFFF', { roughness: 0.88, vertexColors: true }), { cast: true });",
    "    B.mat('plainWall', std('#FFFFFF', { roughness: 0.88, vertexColors: true }), { cast: true });\n"
    "    B.mat('cladWall', pbr('#FFFFFF', { map: TX.clad, bumpMap: TX.cladB, bumpScale: 0.025, roughness: 0.55, metalness: 0.25, vertexColors: true }), { cast: true });")
rep("  function mergeCol(list) {",
    "  /* build 53: a box for cladding: each face's texture coordinates in metres over the cladding tile (2 m along, 1 m up) */\n"
    "  function cladBox53(w, h, d) {\n"
    "    const g = new T.BoxGeometry(w, h, d), u = g.attributes.uv, span = [[d, h], [d, h], [w, d], [w, d], [w, h], [w, h]];\n"
    "    for (let fc = 0; fc < 6; fc++) for (let k = 0; k < 4; k++) { const i = fc * 4 + k; u.setXY(i, u.getX(i) * span[fc][0] / 2.0, u.getY(i) * span[fc][1] / 1.0); }\n"
    "    return g;\n"
    "  }\n"
    "  function mergeCol(list) {")
# the units across the road: cladding on every wall, a plinth round the sides and back
rep("""        B.add('plainWall', new T.BoxGeometry(w, hh, d - RD), at4(cx, hh / 2, zf + RD + (d - RD) / 2), wallC);
        B.add('plainWall', new T.BoxGeometry(rx0 - x0, hh, RD), at4((x0 + rx0) / 2, hh / 2, zf + RD / 2), wallC);
        B.add('plainWall', new T.BoxGeometry(x1 - rx1, hh, RD), at4((rx1 + x1) / 2, hh / 2, zf + RD / 2), wallC);
        B.add('plainWall', new T.BoxGeometry(rx1 - rx0, hh - CH, RD), at4((rx0 + rx1) / 2, CH + (hh - CH) / 2, zf + RD / 2), wallC);""",
"""        B.add('cladWall', cladBox53(w, hh, d - RD), at4(cx, hh / 2, zf + RD + (d - RD) / 2), wallC);
        B.add('cladWall', cladBox53(rx0 - x0, hh, RD), at4((x0 + rx0) / 2, hh / 2, zf + RD / 2), wallC);
        B.add('cladWall', cladBox53(x1 - rx1, hh, RD), at4((rx1 + x1) / 2, hh / 2, zf + RD / 2), wallC);
        B.add('cladWall', cladBox53(rx1 - rx0, hh - CH, RD), at4((rx0 + rx1) / 2, CH + (hh - CH) / 2, zf + RD / 2), wallC);
        for (const xx of [x0 - 0.03, x1 + 0.03]) B.add('plainWall', new T.BoxGeometry(0.06, 0.55, d), at4(xx, 0.275, zf + d / 2), '#5F5D58');
        B.add('plainWall', new T.BoxGeometry(w + 0.12, 0.55, 0.06), at4(cx, 0.275, zf + d + 0.03), '#5F5D58');""")
# the front picture: twice the pixels, proper ribs, a plinth and dirt
old = "        const f = signTex(512, 256, (c, cw, ch) => {\n          c.fillStyle = wallC; c.fillRect(0, 0, cw, ch); c.strokeStyle = 'rgba(0,0,0,.12)'; c.lineWidth = 2; for (let xx = 0; xx < cw; xx += 10) { c.beginPath(); c.moveTo(xx, 50); c.lineTo(xx, ch); c.stroke(); }"
assert f.s.count(old) == 1, f.s.count(old)
new = """        const f = signTex(1024, 512, (c, cw2, ch2) => {
          c.scale(2, 2); const cw = cw2 / 2, ch = ch2 / 2;
          /* build 53: profiled cladding, a rib every 250 mm (pan, a lit rising flank, the crown, a shaded falling flank) */
          c.fillStyle = wallC; c.fillRect(0, 0, cw, ch);
          { const pitch = cw * 0.25 / w; for (let xx = 0; xx < cw; xx += pitch) { c.fillStyle = 'rgba(255,255,255,.16)'; c.fillRect(xx + pitch * 0.62, 0, pitch * 0.08, ch); c.fillStyle = 'rgba(255,255,255,.07)'; c.fillRect(xx + pitch * 0.70, 0, pitch * 0.16, ch); c.fillStyle = 'rgba(0,0,0,.2)'; c.fillRect(xx + pitch * 0.86, 0, pitch * 0.08, ch); } }
          { const gr = c.createLinearGradient(0, ch - py(0) + py(1.4), 0, ch); gr.addColorStop(0, 'rgba(60,52,40,0)'); gr.addColorStop(1, 'rgba(60,52,40,.35)'); c.fillStyle = gr; c.fillRect(0, py(1.4), cw, ch - py(1.4)); }
          c.fillStyle = '#5F5D58'; c.fillRect(0, py(0.55), cw, ch - py(0.55)); c.fillStyle = 'rgba(0,0,0,.25)'; c.fillRect(0, py(0.55), cw, 1.5);
          for (let xx = 0; xx < cw; xx += cw * 0.44 / w) { c.fillStyle = 'rgba(0,0,0,.16)'; c.fillRect(xx, py(0.55), 1, ch - py(0.55)); }
          c.fillStyle = 'rgba(0,0,0,.16)'; c.fillRect(0, (py(0.55) + ch) / 2, cw, 1);"""
f.s = f.s.replace(old, new)
# the barn on the farm
rep("        P(0, 3, 0, 14, 6, 9, 'plainWall', '#8E2A22');", "        B.add('cladWall', cladBox53(14, 6, 9), FM.clone().multiply(M4w(0, 3, 0)), '#8E2A22');")
f.save()
print('p53b ok')
