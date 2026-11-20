# build 49 (a): no black flash when the 3D view changes resolution. To keep the frame rate up the game lowers or raises
# the drawing resolution as it goes; resizing the canvas wipes it, and it stayed blank until the next frame was drawn
# (a black flicker on slower phones, and a black screenshot now and then). Now the last picture is drawn again at once.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("""  if (!renderer || !renderer.getContext()) return api;
  api.ok = true;""", """  if (!renderer || !renderer.getContext()) return api;
  /* build 49: remember what was last drawn, so a resize can draw it again straight away */
  let lastS49 = null, lastC49 = null;
  { const r0 = renderer.render.bind(renderer); renderer.render = (s, c) => { lastS49 = s; lastC49 = c; return r0(s, c); }; }
  const redraw49 = () => { if (lastS49 && lastC49 && canvas.isConnected) { try { renderer.shadowMap.needsUpdate = true; renderer.render(lastS49, lastC49); } catch (e) { /* next frame will do */ } } };
  api.ok = true;""")
rep("""    if (next !== dprNow) { dprNow = next; renderer.setPixelRatio(dprNow); const w = stage.clientWidth, h = stage.clientHeight; if (w && h) renderer.setSize(w, h, false); }""",
    """    if (next !== dprNow) { dprNow = next; renderer.setPixelRatio(dprNow); const w = stage.clientWidth, h = stage.clientHeight; if (w && h) { renderer.setSize(w, h, false); redraw49(); } }""")
# tests: change the resolution the way the frame loop does and read the canvas straight after
rep("  function adaptDpr(dt) {", "  api.dprFlash49 = v => { const w = stage.clientWidth, h = stage.clientHeight; dprNow = v; renderer.setPixelRatio(v); renderer.setSize(w, h, false); redraw49(); const g = renderer.getContext(), px = new Uint8Array(4); g.readPixels(Math.floor(g.drawingBufferWidth / 2), Math.floor(g.drawingBufferHeight / 2), 1, 1, g.RGBA, g.UNSIGNED_BYTE, px); return [...px]; };\n  function adaptDpr(dt) {")
rep("window.__perfProbe = n =>", "window.__dpr49 = v => (Car3D.ok && Car3D.dprFlash49 ? Car3D.dprFlash49(v) : null);\nwindow.__perfProbe = n =>")
f.save()
print('p49a ok')
