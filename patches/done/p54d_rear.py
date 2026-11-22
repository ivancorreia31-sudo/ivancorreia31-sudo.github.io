# build 54: the back and the front of the car up close. The rear was one blank painted face with lamps, a plate and a
# badge on it. It now has the boot lid's shut lines (down each side beside the lamps and across above the bumper), the
# bumper's top line running round to the corners, red reflectors in the bumper, and the model's name and engine size
# in chrome letters on the boot. The front gets the bumper's top line too, broken round the grille.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("    conformLamps24();\n  }", """    conformLamps24();
    trim54();
  }
  /* build 54: shut lines, reflectors and boot lettering on the nose and tail (not vans, open cars or chrome-bumpered classics) */
  let BADGE54 = {};
  function trim54() {
    const SK = SK24; if (!SK || !SK.fx || sty.van || sty.open || sty.classic) return;
    const line = (front, y0, y1, z0, z1, mat) => {
      const h = Math.max(0.0045, y1 - y0), w = Math.max(0.0045, z1 - z0);
      const g = new T.BoxGeometry(0.004, h, w, 1, Math.max(1, Math.round(h / 0.04)), Math.max(1, Math.round(w / 0.04))); g.translate(0, (y0 + y1) / 2, (z0 + z1) / 2);
      const m = new T.Mesh(seatGeo27(SK, g, front, null, -0.0026, false, 0.03), mat || M.trim); m.userData.noShape = true; fixed(m, 'auto'); return m;
    };
    const sideAt = (front, y) => 0.81 * SK.SF(SK.faceX(front, y), y);
    /* the tail: lamp inner edges, the bumper line just under the plate */
    const F = sty.tl && TL32[sty.tl], ty = sty.tailY, lw = F ? (F.round ? F.r + (F.two || 0) / 2 : F.w / 2) : 0.18, lz = F ? F.z : 0.58;
    const lzc = Math.min(lz, sideAt(false, ty) - lw * 0.8), zs = Math.max(0.22, lzc - lw - 0.014), lh = F ? (F.round ? F.r : F.h / 2) : 0.056;
    const yb = Math.max(0.40, sty.plateY - 0.085), yt = ty - lh - 0.012, zw = sideAt(false, yb) - 0.03;
    if (yt - yb > 0.08) { for (const s of [-1, 1]) line(false, yb, yt, s * zs - 0.00225, s * zs + 0.00225); }
    line(false, yb - 0.00225, yb + 0.00225, -zw, zw);
    for (const s of [-1, 1]) { const g = new T.BoxGeometry(0.008, 0.022, 0.085); g.translate(0, yb - 0.07, s * (zw - 0.09)); const m = new T.Mesh(seatGeo27(SK, g, false, null, -0.004, true), M.tail); m.userData.noShape = true; fixed(m, 'auto'); }
    /* chrome letters, 28 mm tall: the model on one side of the boot, the engine on the other */
    const nm = String((car32 && car32.model) || '').replace(new RegExp('^' + String((car32 && car32.make) || '#').replace(/[^A-Za-z]/g, '') + '\\\\s+', 'i'), '').trim().split(/\\s+/);
    const eng = /^\\d\\.\\d/.test(nm[nm.length - 1] || '') ? nm.pop() : '', word = (nm[0] || '').toUpperCase();
    const letters = (txt, w, z) => {
      if (!txt) return;
      const key = txt + '|' + w; let tx = BADGE54[key];
      if (!tx) {
        tx = BADGE54[key] = canvasTex(512, 96, (c, cw, ch) => {
          c.clearRect(0, 0, cw, ch); c.font = '700 80px "Barlow", Arial, sans-serif'; const fw = c.measureText(txt).width; if (fw > cw - 24) c.font = '700 ' + Math.floor(80 * (cw - 24) / fw) + 'px "Barlow", Arial, sans-serif'; c.textAlign = 'center'; c.textBaseline = 'middle';
          const g = c.createLinearGradient(0, 14, 0, 82); g.addColorStop(0, '#FFFFFF'); g.addColorStop(0.45, '#BFC4C8'); g.addColorStop(0.55, '#6E7479'); g.addColorStop(1, '#E3E6E8');
          c.lineWidth = 5; c.strokeStyle = 'rgba(20,22,24,.55)'; c.strokeText(txt, cw / 2, ch / 2 + 2); c.fillStyle = g; c.fillText(txt, cw / 2, ch / 2);
        });
      }
      const y = Math.min(yt - 0.05, yb + 0.21), pg = new T.PlaneGeometry(w * 512 / 96, w, 16, 1); pg.rotateY(-PI / 2); pg.translate(0, y, z);
      const m = new T.Mesh(seatGeo27(SK, pg, false, null, 0.0015, false, 0.02), new T.MeshStandardMaterial({ map: tx, transparent: true, depthWrite: false, alphaTest: 0.04, metalness: 0.6, roughness: 0.3, polygonOffset: true, polygonOffsetFactor: -2 }));
      m.userData.ownMat = true; m.userData.noShape = true; m.userData.badge54 = txt; fixed(m, 'auto');
    };
    if (zs > 0.3) { letters(word, 0.04, -Math.min(zs - 0.13, 0.3)); letters(eng, 0.036, Math.min(zs - 0.08, 0.3)); }
    /* the nose: the bumper's top line, under the lamps, broken round the grille */
    const HF = sty.hl && HL32[sty.hl], hy = HF ? HF.y : 0.635, hh = HF ? (HF.round ? HF.r : HF.h / 2) : 0.058, yf = hy - hh - 0.03;
    const GR = sty.gr && GR32 && GR32[sty.gr], gw = GR ? GR[0] / 2 + 0.03 : 0.42, gy0 = GR ? GR[2] - GR[1] / 2 - 0.02 : 0.5, gy1 = GR ? GR[2] + GR[1] / 2 + 0.02 : 0.68, zf = sideAt(true, yf) - 0.03;
    if (yf > 0.42 && zf > gw + 0.1) { if (yf > gy0 && yf < gy1) { for (const s of [-1, 1]) line(true, yf - 0.00225, yf + 0.00225, s > 0 ? gw : -zf, s > 0 ? zf : -gw); } else line(true, yf - 0.00225, yf + 0.00225, -zf, zf); }
  }""")
rep("  window.__probe51 = () =>", "  window.__badges54 = () => { const o = []; if (car) car.traverse(m => { if (m.isMesh && m.userData.badge54) o.push(m.userData.badge54); }); return o; };\n  window.__probe51 = () =>")
f.save()
print('p54d ok')
