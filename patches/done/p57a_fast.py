# build 57: smoother. (1) The three workshop roof lights from build 53 are gone: the workshop and the yard share their
# materials, so the yard had to carry three dummy lights to match, and every lit pixel outside paid for them (the yard
# drew a third slower than in build 50). (2) The car on the ramp (~450 pieces) and the workshop room (~360) are drawn as a
# few dozen each: pieces
# that share a material and stay still are merged into one mesh per material, kept up to date when something is shown,
# hidden, moved or repainted (a piece that moves is left out from then on). The originals stay where they were for taps.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
# (1) no roof lights
rep("  const LT53 = [[0, 0], [-7, 0], [7, 0]].map(([x, z]) => { const p = new T.PointLight(0xfff4e6, 0.95, 16, 2); p.position.set(x, 5.05, z); scene.add(p); return p; });",
    "  const LT53 = [];   /* build 57: removed (the yard had to carry matching dummy lights) */")
rep("  const sun = new T.DirectionalLight(0xfff1dc, 0.9); sun.position.set(2.5, 9, 3.5); sun.castShadow = true;",
    "  const sun = new T.DirectionalLight(0xfff1dc, 1.1); sun.position.set(2.5, 9, 3.5); sun.castShadow = true;")
# (2) the batcher
rep("  const ENVS = { in: null, out: null };", r"""  const ENVS = { in: null, out: null };
  /* build 57: static batching. Originals move to layer 5 (not drawn, still hit by every raycaster), and per material a
     merged copy is drawn on their old layers. */
  const L57 = 1 << 5;
  { const P = T.Raycaster.prototype, io = P.intersectObject, ios = P.intersectObjects;
    P.intersectObject = function (o, r, t) { const m = this.layers.mask; this.layers.mask = m | L57; try { return io.call(this, o, r, t); } finally { this.layers.mask = m; } };
    P.intersectObjects = function (o, r, t) { const m = this.layers.mask; this.layers.mask = m | L57; try { return ios.call(this, o, r, t); } finally { this.layers.mask = m; } }; }
  function batcher57(root, scene0) {
    /* merged meshes are baked in the root's own space and drawn in a group that follows it */
    const host = new T.Group(); host.matrixAutoUpdate = false; host.userData.batch57 = true; scene0.add(host);
    const B = { root, host, items: [], groups: new Map(), dyn: new Set(), n: -1, rebuilds: 0, on: true, ms: 0 };
    const inv = new T.Matrix4(), rel = new T.Matrix4();
    const relOf = o => { o.updateWorldMatrix(true, false); return rel.multiplyMatrices(inv, o.matrixWorld); };
    const eff = o => { for (let p = o; p; p = p.parent) { if (!p.visible) return false; if (p === root) return !!root.parent; } return false; };
    const ok = o => o.isMesh && !o.isInstancedMesh && !o.isSkinnedMesh && !Array.isArray(o.material) && o.material && !o.material.transparent && !Object.prototype.hasOwnProperty.call(o, 'onBeforeRender');   /* see-through things keep their own draw order */
    const okGeo = g => g && g.isBufferGeometry && g.attributes.position && g.attributes.normal && !g.morphAttributes.position && g.drawRange.count === Infinity;   /* a single material draws all of a geometry, whatever its groups */
    const keyOf = it => { const o = it.o, g = o.geometry; return [o.material.uuid, it.mask, o.castShadow ? 1 : 0, o.receiveShadow ? 1 : 0, o.renderOrder, g.attributes.uv ? 1 : 0, g.attributes.color ? 1 : 0].join('|'); };
    const release = it => { it.o.layers.mask = it.mask; };
    const bake = (key, list) => {
      const old = B.groups.get(key); if (old) { host.remove(old); old.geometry.dispose(); B.groups.delete(key); }
      const vis = list.filter(it => eff(it.o)); if (!vis.length) return;
      const o0 = vis[0].o, hasUv = !!o0.geometry.attributes.uv, hasCol = !!o0.geometry.attributes.color;
      let n = 0; for (const it of vis) { const g = it.o.geometry; n += g.index ? g.index.count : g.attributes.position.count; }
      const P = new Float32Array(n * 3), N = new Float32Array(n * 3), U = hasUv ? new Float32Array(n * 2) : null, C = hasCol ? new Float32Array(n * 3) : null;
      const v = new T.Vector3(), nm = new T.Matrix3(); let w = 0;
      for (const it of vis) {
        const o = it.o, g = o.geometry, pa = g.attributes.position, na = g.attributes.normal, ua = g.attributes.uv, ca = g.attributes.color, ix = g.index, cnt = ix ? ix.count : pa.count;
        const mw = relOf(o); nm.getNormalMatrix(mw); const flip = mw.determinant() < 0;
        for (let k = 0; k < cnt; k++) {
          const kk = flip ? (k % 3 === 1 ? k + 1 : k % 3 === 2 ? k - 1 : k) : k, i = ix ? ix.getX(kk) : kk;
          v.fromBufferAttribute(pa, i).applyMatrix4(mw); P[w * 3] = v.x; P[w * 3 + 1] = v.y; P[w * 3 + 2] = v.z;
          v.fromBufferAttribute(na, i).applyMatrix3(nm).normalize(); N[w * 3] = v.x; N[w * 3 + 1] = v.y; N[w * 3 + 2] = v.z;
          if (U) { U[w * 2] = ua.getX(i); U[w * 2 + 1] = ua.getY(i); }
          if (C) { C[w * 3] = ca.getX(i); C[w * 3 + 1] = ca.getY(i); C[w * 3 + 2] = ca.getZ(i); }
          w++;
        }
      }
      const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(P, 3)); g.setAttribute('normal', new T.BufferAttribute(N, 3));
      if (U) g.setAttribute('uv', new T.BufferAttribute(U, 2)); if (C) g.setAttribute('color', new T.BufferAttribute(C, 3));
      g.computeBoundingSphere();
      const m = new T.Mesh(g, o0.material); m.castShadow = o0.castShadow; m.receiveShadow = o0.receiveShadow; m.renderOrder = o0.renderOrder; m.layers.mask = vis[0].mask;
      m.matrixAutoUpdate = false; m.userData.batch57 = true; host.add(m); B.groups.set(key, m); B.rebuilds++;
    };
    /* sync: find the meshes under the root now; new ones join their material's batch, gone ones leave it */
    B.by = new Map(); B.scans = 0;
    const sync = full => {
      const t0 = performance.now(); B.scans++;
      const seen = new Set(), dirty = new Set(); let n = 0;
      root.traverse(o => { if (o.isMesh) { n++; seen.add(o); } });
      for (const it of B.items) if (!seen.has(it.o)) { it.gone = true; dirty.add(it.key); }
      const have = new Set(B.items.map(it => it.o)), fresh = [];
      for (const o of seen) { if (have.has(o) || B.dyn.has(o) || o.layers.mask === L57 || !ok(o) || !okGeo(o.geometry)) continue; const it = { o, mask: o.layers.mask, mat: o.material, vis: eff(o), mw: relOf(o).elements.slice(), ch: 0 }; it.key = keyOf(it); fresh.push(it); }
      for (const it of fresh) { if (!B.by.has(it.key)) B.by.set(it.key, []); B.by.get(it.key).push(it); dirty.add(it.key); }
      for (const k of dirty) {
        const list = (B.by.get(k) || []).filter(it => !it.gone);
        if (list.length < 2) { list.forEach(release); B.by.delete(k); const old = B.groups.get(k); if (old) { host.remove(old); old.geometry.dispose(); B.groups.delete(k); } continue; }
        for (const it of list) it.o.layers.mask = L57; B.by.set(k, list); bake(k, list);
      }
      B.items = [].concat(...B.by.values()); B.n = n; B.ms = Math.round(performance.now() - t0);
    };
    const scan = () => sync(true);
    B.max = 0; B.slow = 0;
    B.tick = () => { const t0 = performance.now(); tick0(); const ms = performance.now() - t0; if (ms > B.max) B.max = ms; if (ms > 8) B.slow++; const A = ALL57[root === roomG ? 'room' : 'car']; A.ticks++; if (ms > A.max) A.max = Math.round(ms); if (ms > 8) A.slow++; if (ms > 30) A.over30++; };
    const tick0 = () => {
      if (!B.on || !root.parent) { host.visible = false; return; }
      root.updateWorldMatrix(true, false); inv.copy(root.matrixWorld).invert(); host.matrix.copy(root.matrixWorld); host.matrixWorldNeedsUpdate = true; host.visible = true;
      let n = 0; root.traverse(o => { if (o.isMesh) n++; });
      if (n !== B.n) { sync(false); return; }
      const dirty = new Set();
      for (const it of B.items) {
        const o = it.o, vis = eff(o); let moved = false;
        if (vis) { const e = relOf(o).elements; for (let i = 0; i < 16; i++) if (Math.abs(e[i] - it.mw[i]) > 1e-5) { moved = true; break; } }
        if (moved || o.material !== it.mat || o.layers.mask !== L57) {
          /* moving, repainted or re-layered by the game: draw it on its own from now on */
          if (o.layers.mask !== L57) it.mask = o.layers.mask;
          B.dyn.add(o); release(it); dirty.add(it.key); it.gone = true; continue;
        }
        if (vis !== it.vis) { it.vis = vis; dirty.add(it.key); if (++it.ch > 6) { B.dyn.add(o); release(it); it.gone = true; } }
      }
      if (dirty.size) {
        for (const k of dirty) {
          const list = (B.by.get(k) || []).filter(it => !it.gone);
          if (list.length < 2) { list.forEach(release); B.by.delete(k); const old = B.groups.get(k); if (old) { host.remove(old); old.geometry.dispose(); B.groups.delete(k); } continue; }
          B.by.set(k, list); bake(k, list);
        }
        B.items = [].concat(...B.by.values());
      }
    };
    B.off = () => { B.on = false; for (const it of B.items) release(it); for (const m of B.groups.values()) { host.remove(m); m.geometry.dispose(); } B.groups.clear(); B.items = []; B.n = -1; if (host.parent) host.parent.remove(host); };
    return B;
  }
  let RB57 = null, CB57 = null; const ALL57 = { room: { ticks: 0, max: 0, slow: 0, over30: 0 }, car: { ticks: 0, max: 0, slow: 0, over30: 0 } };
  const batchRoom57 = () => {
    if (window.__nob57) { if (RB57) RB57.off(); if (CB57) CB57.off(); RB57 = CB57 = null; return; }
    if (roomG) { if (!RB57 || RB57.root !== roomG) { if (RB57) RB57.off(); RB57 = batcher57(roomG, scene); } RB57.tick(); }
    if (car) { if (!CB57 || CB57.root !== car) { if (CB57) CB57.off(); CB57 = batcher57(car, scene); } CB57.tick(); } else if (CB57) { CB57.off(); CB57 = null; }
  };
  const st57 = B => B ? { items: B.items.length, batches: B.groups.size, dyn: B.dyn.size, rebuilds: B.rebuilds, scans: B.scans, lastMs: B.ms, maxMs: Math.round(B.max), slow: B.slow } : null;
  window.__batch57 = () => ({ room: st57(RB57), car: st57(CB57), all: ALL57 });
  window.__pick57 = () => { const grid = () => { const r = canvas.getBoundingClientRect(), out = []; for (let i = 1; i < 30; i++) for (let j = 1; j < 30; j++) { const h = pick(r.left + r.width * i / 30, r.top + r.height * j / 30); out.push(h.part || (h.door ? 'door' : '')); } return out; }; const a = grid(); const merged = !!(CB57 && CB57.items.length); if (RB57) RB57.off(); if (CB57) CB57.off(); RB57 = CB57 = null; const b = grid(); kick(); let same = 0; for (let i = 0; i < a.length; i++) if (a[i] === b[i]) same++; return { merged, n: a.length, same, parts: a.filter(Boolean).length }; };""")
rep("""      POST.thr = 0.8; renderer.toneMappingExposure = expoWs52;
      if (PR51.ws && !booth) {""", """      POST.thr = 0.8; renderer.toneMappingExposure = expoWs52; batchRoom57();
      if (PR51.ws && !booth) {""")
rep("    if (canvas.isConnected && canvas.clientWidth) { renderer.shadowMap.needsUpdate = true; POST.thr = 0.8; renderer.toneMappingExposure = expoWs52; renderer.render(scene, camera); adaptDpr(dt); }",
    "    if (canvas.isConnected && canvas.clientWidth) { renderer.shadowMap.needsUpdate = true; POST.thr = 0.8; renderer.toneMappingExposure = expoWs52; batchRoom57(); renderer.render(scene, camera); adaptDpr(dt); }")
# (3) a last resort on slow phones: under 30 frames a second with the glow already off, draw at 0.85 of a screen pixel
rep("    else if (dprAvg > 1 / 40 && PREF34.gfx !== 'save') { try { if (POST.auto) POST.auto = false; } catch (e) { /* no glow pass */ } }",
    "    else if (dprAvg > 1 / 40 && PREF34.gfx !== 'save' && POST.auto !== false) { try { POST.auto = false; } catch (e) { /* no glow pass */ } }\n"
    "    else if (dprAvg > 1 / 30 && dprNow > 0.85) next = 0.85;")
f.save()
print('p57a ok')
