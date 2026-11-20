# build 48 (b): a later-game tool that takes the chore out of the parts shop - the parts catalogue tablet ticks every
# box that fits the car, so after hundreds of jobs you only choose the quality
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("""  { id: 'diag', cat: 'tools', name: 'Diagnostic laptop', desc: 'Live data rules out a wrong answer on every fault, not just the ones with a code.', price: 1100, lvl: 3 },""",
    """  { id: 'diag', cat: 'tools', name: 'Diagnostic laptop', desc: 'Live data rules out a wrong answer on every fault, not just the ones with a code.', price: 1100, lvl: 3 },
  { id: 'catalogue', cat: 'tools', name: 'Parts catalogue tablet', desc: 'The trade catalogue on a tablet. In the parts shop every box that fits the car gets a green tick, so you only have to choose the quality.', price: 1500, lvl: 6 },""")
rep("""    return `<button class="box${o.bad ? ' bad' : ''}" data-a="shop-pick" data-i="${i}"${o.bad ? ' disabled' : ''}>""",
    """    const fit48 = own('catalogue') && o.fits;
    return `<button class="box${o.bad ? ' bad' : ''}${fit48 ? ' fit48' : ''}" data-a="shop-pick" data-i="${i}"${o.bad ? ' disabled' : ''}>""")
rep("""<span class="box-tags"><span class="box-tag t-${o.q}">${T.label}</span>""",
    """<span class="box-tags">${fit48 ? '<span class="box-tag fit48t">✓ Fits</span>' : ''}<span class="box-tag t-${o.q}">${T.label}</span>""")
rep("""    <p class="muted">Pick a box with ${how}. ${tip}</p>""",
    """    <p class="muted">${own('catalogue') ? 'Your parts catalogue has ticked every box that fits. Choose the quality.' : `Pick a box with ${how}.`} ${tip}</p>""")
rep("""    <div class="boxes">${sh.opts.map(boxHtml).join('')}</div>""", """    <div class="boxes${own('catalogue') ? ' cat48' : ''}">${sh.opts.map(boxHtml).join('')}</div>""")
rep(".box.bad{opacity:.4;border-style:dashed;animation:shake .25s;cursor:default}",
    ".box.bad{opacity:.4;border-style:dashed;animation:shake .25s;cursor:default}\n.box.fit48{border-color:var(--good)}\n.box-tag.fit48t{background:var(--good);color:var(--on-sem,#fff)}\n.boxes.cat48 .box:not(.fit48):not(.bad){opacity:.5}")
# tests: open the parts shop for a part of the car on the ramp, and read which boxes fit
rep("function openShop(id, up) {", "window.__shop48 = { open: (id) => { const j = cur(); if (!j) return null; id = id || Object.keys(j.parts).find(k => CAT[k] && j.parts[k].state === 'fitted'); openShop(id, false); return id; }, fits: () => (UI.shop ? UI.shop.opts.map(o => !!o.fits) : null) };\nfunction openShop(id, up) {")
f.save()
print('p48b ok')
