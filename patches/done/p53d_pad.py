# build 53: the sound-deadening pad under the bonnet was plain black, so an open bonnet showed a black slab in the middle
# of the screen. It's dark grey felt now, pressed in a diamond quilt like the real thing, with a little sheen on the ridges.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("    { const pad = prismS([[0.12, -0.0654], [1.08, -0.1564], [1.08, -0.1644], [0.12, -0.0734]], 1.2, M.dark, 0, 8); pad.geometry.translate(0, 0, -0.6);",
    "    { const pad = prismS([[0.12, -0.0654], [1.08, -0.1564], [1.08, -0.1644], [0.12, -0.0734]], 1.2, padMat53(), 0, 8); pad.geometry.translate(0, 0, -0.6);\n"
    "      { const P = pad.geometry.attributes.position, U = pad.geometry.attributes.uv; for (let i = 0; i < P.count; i++) U.setXY(i, P.getX(i), P.getZ(i)); U.needsUpdate = true; }")
rep("  const prismS = (pts, depth, mat, bevel, steps) =>",
    "  /* build 53: bonnet pad felt, 1 m a tile: speckled dark grey, quilted in diamonds every 125 mm */\n"
    "  let PAD53 = null;\n"
    "  const padMat53 = () => {\n"
    "    if (PAD53) return PAD53;\n"
    "    const tx = canvasTex(256, 256, (c, w, h) => {\n"
    "      speckle(c, w, h, '#3A3D40', 0.09, 7000);\n"
    "      for (const s of [1, -1]) for (let k = -8; k <= 16; k++) { const x0 = k * 32; c.strokeStyle = 'rgba(0,0,0,.34)'; c.lineWidth = 2; c.beginPath(); c.moveTo(x0, s > 0 ? 0 : h); c.lineTo(x0 + w, s > 0 ? h : 0); c.stroke(); c.strokeStyle = 'rgba(255,255,255,.07)'; c.lineWidth = 1.5; c.beginPath(); c.moveTo(x0 + 3, s > 0 ? 0 : h); c.lineTo(x0 + 3 + w, s > 0 ? h : 0); c.stroke(); }\n"
    "    });\n"
    "    tx.wrapS = tx.wrapT = T.RepeatWrapping;\n"
    "    return (PAD53 = std('#FFFFFF', { map: tx, bumpMap: tx, bumpScale: 0.0012, roughness: 0.93 }));\n"
    "  };\n"
    "  const prismS = (pts, depth, mat, bevel, steps) =>")
rep("  window.__probe51 = () =>", "  window.__b53 = () => { let pad = 0, clad = 0; if (car) car.traverse(o => { if (o.isMesh && PAD53 && o.material === PAD53) pad++; }); if (dW) dW.scene.traverse(o => { if (o.isMesh && o.name === 'b19:cladWall') clad += o.geometry.attributes.position.count / 3 | 0; }); return { pad, clad, lights: LT53.filter(l => l.visible).length }; };\n  window.__probe51 = () =>")
f.save()
print('p53d ok')
