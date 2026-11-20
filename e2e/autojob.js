/* in-page auto player for the job on the ramp: follows the step card like a player would (bolts, seized nuts, torque,
   the parts shop by reading the car and the boxes, mini-games, quizzes) and stops at the invoice. Returns its log.
   window.__AJ = { limit ms, stopAtShop: bool } can change how it runs. */
(async () => {
  const log = [], wait = ms => new Promise(r => setTimeout(r, ms));
  const vis = e => e && e.offsetWidth > 0;
  const opt = window.__AJ || {}, LIMIT = opt.limit || 150000;
  const T0 = performance.now(); let seizedTries = 0, idle = 0;
  for (let i = 0; i < 400 && performance.now() - T0 < LIMIT; i++) {
    const m = document.getElementById('modal');
    if (m && !m.hidden) {
      const t = m.innerText.replace(/\s+/g, ' ').slice(0, 70); if (log[log.length - 1] !== 'sheet: ' + t) log.push('sheet: ' + t);
      if (/invoice/i.test(t) && /£/.test(m.innerText)) { log.push('STOP at invoice'); break; }
      if (m.querySelector('[data-a=shop-pick]')) {
        if (opt.stopAtShop) { log.push('STOP at shop'); break; }
        const car = ((m.querySelector('.shop-car b') || {}).innerText || ''), yr = +((car.match(/\b(19|20)\d\d\b/) || [0])[0]), mk = car.split(' ')[0];
        const side = (car.match(/(left|right|front|rear) (side|axle)/) || [''])[0], size = (car.match(/\d{3}\/\d\d ?R\d\d/) || [''])[0];
        const sc = b => { const f = (b.querySelector('.box-fit') || {}).innerText || '', y = f.match(/(\d{4})\D+(\d{4})/), ax = (b.querySelector('.box-axle') || {}).innerText || '', sz = (b.querySelector('.box-size') || {}).innerText || ''; let v = 0;
          if (!f.includes(mk)) v -= 100; if (y && (yr < +y[1] || yr > +y[2])) v -= 100; if (side && ax && ax.toLowerCase() !== side) v -= 100; if (size && sz && sz.replace(/\s/g, '') !== size.replace(/\s/g, '')) v -= 100;
          if (/cheap|copy|lookalike/i.test(b.innerText)) v -= 5; if (/genuine/i.test(b.innerText)) v += 3; return v; };
        const bs = [...m.querySelectorAll('[data-a=shop-pick]:not([disabled])')].sort((a, b) => sc(b) - sc(a));
        if (bs[0]) { log.push('shop pick ' + sc(bs[0]) + ' ' + bs[0].innerText.replace(/\s+/g, ' ').slice(0, 50)); bs[0].click(); }
        await wait(700); continue;
      }
      const p = m.querySelector('.btn.primary:not(:disabled)'); if (p) { log.push('sheet press: ' + p.innerText.replace(/\s+/g, ' ').slice(0, 30)); p.click(); await wait(700); continue; }
      const c = m.querySelector('[data-a=close-modal]'); if (c) { c.click(); await wait(500); continue; }
    }
    const h = (document.querySelector('.step h3') || {}).innerText || '';
    if (log[log.length - 1] !== 'step: ' + h) log.push('step: ' + h);
    if (window.__mg && __mg() && !__mg().ended) { await wait(400); __mgWin(90); await wait(800); continue; }
    if (window.__mg && __mg() && __mg().ended) { const d = document.querySelector('[data-mg=done]'); if (d) { log.push('mini-game done'); d.click(); await wait(900); continue; } }
    const tq = document.querySelector('.tq-wrap');
    if (tq) { const lo = +tq.dataset.lo, hi = +tq.dataset.hi, mm = (hi - lo) * 0.25; for (let k = 0; k < 400; k++) { await new Promise(r => requestAnimationFrame(r)); const f = +tq.dataset.f; if (f > lo + mm && f < hi - mm) { tq.click(); break; } } await wait(500); continue; }
    if (document.querySelector('.bolt.seized')) {
      seizedTries++; const oil = document.querySelector('.step [data-a=oil], [data-a=oil]');
      if (seizedTries > 3 && oil) { log.push('oil the seized nuts'); oil.click(); seizedTries = 0; await wait(1500); continue; }
      for (let k = 0; k < 8; k++) { const sz = document.querySelector('.bolt.seized'); if (!sz) break; sz.click(); await wait(90); }
      await wait(300); continue;
    }
    const hold = document.querySelector('[data-hold=air]');
    if (hold && vis(hold)) {
      const tgt = +((((document.querySelector('.cap-txt b') || {}).innerText || '').match(/(\d+) psi/) || [0, 0])[1]);
      const read = () => +(((document.getElementById('air-read') || {}).textContent || '0').replace(/\D/g, ''));
      const ev = (el, ty) => el && el.dispatchEvent(new PointerEvent(ty, { bubbles: true, cancelable: true, pointerId: 7, isPrimary: true }));
      const t1 = performance.now();
      if (read() < tgt) { ev(hold, 'pointerdown'); while (read() < tgt && performance.now() - t1 < 90000) await wait(25); ev(hold, 'pointerup'); }
      else if (read() > tgt) { const de = document.querySelector('[data-hold=deflate]'); ev(de, 'pointerdown'); while (read() > tgt && performance.now() - t1 < 90000) await wait(25); ev(de, 'pointerup'); }
      log.push('pumped to ' + read() + ' of ' + tgt); await wait(700); continue;
    }
    const tnRun = document.querySelector('[data-a=tn-run]');
    if (tnRun && vis(tnRun)) {
      const save = document.querySelector('[data-a=tn-save]:not([disabled])');
      if (save && vis(save)) { log.push('tune: save'); save.click(); window.__tn = 0; await wait(900); continue; }
      window.__tn = (window.__tn || 0) + 1;
      const hint = document.querySelector('[data-a=tn-hint]');
      if (window.__tn <= 3 && hint && vis(hint) && !/best map/i.test((document.getElementById('toast') || {}).textContent || '')) { hint.click(); await wait(500); continue; }
      log.push('tune: dyno run'); tnRun.click(); window.__tn = 0; await wait(3500); continue;
    }
    const capw = document.querySelector('.capw'), hold0 = [...document.querySelectorAll('[data-hold]')].find(b => vis(b) && !['air', 'deflate'].includes(b.dataset.hold));
    if ((capw && vis(capw)) || hold0) {
      const ev = (el, ty) => el && el.dispatchEvent(new PointerEvent(ty, { bubbles: true, cancelable: true, pointerId: 8, isPrimary: true }));
      const hb = [...document.querySelectorAll('[data-hold]')].find(b => vis(b) && !['air', 'deflate'].includes(b.dataset.hold));
      let held = false;
      if (hb) {
        ev(hb, 'pointerdown'); await wait(250);
        if (hb.classList.contains('down')) {
          held = true; const k = hb.dataset.hold, t1 = performance.now();
          while (performance.now() - t1 < 90000) {
            const r = ((document.querySelector('.fluidw .fw-read') || {}).textContent || '');
            if (!hb.classList.contains('down')) break;
            if (k !== 'drain' && /Between/.test(r)) { await wait(200); break; }
            await wait(25);
          }
          log.push('held ' + k + ': ' + ((document.querySelector('.fluidw .fw-read') || {}).textContent || ''));
        }
        ev(hb, 'pointerup'); ev(document.body, 'pointerup');
      }
      if (!held) { const dial = document.querySelector('.cap-dial'); if (dial && vis(dial)) { dial.click(); await wait(420); continue; } }
      else { await wait(700); continue; }
    }
    const bolt = document.querySelector('.bolt.next') || document.querySelector('.bolt:not(.done)');
    if (bolt && vis(bolt)) { bolt.click(); await wait(420); continue; }
    const btns = [...document.querySelectorAll('.step button')].filter(b => vis(b) && !b.disabled && !/^(Job card|Less|More)$/.test(b.innerText.trim()) && !['oil', 'drawer', 'stepmin', 'g-drive'].includes(b.dataset.a || b.dataset.b));
    const pref = ['handback', 'g-fit', 'g-shop', 'g-remove', 'mini-go', 'g-go', 'g-ok', 'g-lift'];
    let b = null; for (const a of pref) { b = btns.find(x => x.dataset.a === a); if (b) break; }
    b = b || btns[0];
    if (b) { idle = 0; log.push('press: ' + (b.dataset.a || b.dataset.b) + ' ' + b.innerText.replace(/\s+/g, ' ').slice(0, 30)); b.click(); await wait(800); continue; }
    if (++idle > 40) { log.push('STUCK: nothing to press'); break; }
    await wait(500);
  }
  return log;
})()
