# build 48 (c): tidier pages for a long game - the Legacy card says plainly how far you are from selling up, the fault
# book shows what you've found and sums up what's left by area instead of a wall of "Not found yet", and the Items
# page shows what you own first, with the items still to find as small tiles
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
# the Legacy card: "Level 10 of 8" read oddly; now the need and a tick
rep("""    <div class="lg47-r"><span class="sm">Level ${L} of 8</span><div class="gauge" role="img" aria-label="Level ${L} of 8"><i class="good" style="width:${Math.round(lv * 100)}%"></i></div></div>
    <div class="lg47-r"><span class="sm">${money(Math.max(0, v))}</span><div class="gauge" role="img" aria-label="Business worth ${money(Math.max(0, v))} of ${money(250000)}"><i class="good" style="width:${Math.round(vv * 100)}%"></i></div></div>""",
    """    <div class="lg47-r"><span class="sm">Level</span><b class="sm${L >= 8 ? ' ok48' : ''}">${L >= 8 ? `${L} ✓` : `${L} of 8`}</b><div class="gauge" role="img" aria-label="Level ${L}, level 8 needed"><i class="good" style="width:${Math.round(lv * 100)}%"></i></div></div>
    <div class="lg47-r"><span class="sm">Business worth</span><b class="sm${v >= 250000 ? ' ok48' : ''}">${money(Math.max(0, v))}${v >= 250000 ? ' ✓' : ` of ${money(250000)}`}</b><div class="gauge" role="img" aria-label="Business worth ${money(Math.max(0, v))} of ${money(250000)}"><i class="good" style="width:${Math.round(vv * 100)}%"></i></div></div>""")
rep(".lg47-r{display:grid;grid-template-columns:7.5em 1fr;align-items:center;gap:10px}",
    ".lg47-r{display:grid;grid-template-columns:1fr auto;align-items:center;gap:3px 10px}\n.lg47-r .gauge{grid-column:1 / -1}\n.lg47-r b.ok48{color:var(--good)}")
# the fault book: found faults as cards, the rest summed up by where they are on the car
rep("""    <div class="b38-grid">${order.map(x => { const e = B[x.k]; let say = ''; try { say = HINT[x.k](x.corner); } catch (er) { say = ''; }
      return e ? `<div class="b38-c"><b>${esc(x.name)}</b><p>“${esc(say)}”</p><small>Fixed ${e.n} time${e.n > 1 ? 's' : ''} · first on day ${e.d}</small></div>`
        : `<div class="b38-c off"><b>Not found yet</b><p>${where(x.zone)}</p></div>`; }).join('')}</div></section>`;""",
    """    ${got ? `<div class="b38-grid">${order.filter(x => B[x.k]).map(x => { const e = B[x.k]; let say = ''; try { say = HINT[x.k](x.corner); } catch (er) { say = ''; }
      return `<div class="b38-c"><b>${esc(x.name)}</b><p>“${esc(say)}”</p><small>Fixed ${e.n} time${e.n > 1 ? 's' : ''} · first on day ${e.d}</small></div>`; }).join('')}</div>` : '<p class="muted sm">Every fault you find and fix on a customer’s car goes in here, with what the customer said about it.</p>'}
    ${got < BOOK38.length ? (() => { const left = {}; BOOK38.filter(x => !B[x.k]).forEach(x => { const w = where(x.zone); left[w] = (left[w] || 0) + 1; });
      return `<div class="b38-left"><b>Still to find</b>${Object.keys(left).map(w => `<span class="b38-c off"><b>${left[w]}</b> ${esc(w.toLowerCase())}</span>`).join('')}</div>`; })() : ''}</section>`;""")
rep(".b38-c.off b{color:var(--muted)}",
    ".b38-c.off b{color:var(--muted)}\n.b38-left{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin-top:10px}\n.b38-left > b{width:100%;font-size:13px;color:var(--muted)}\n.b38-left .b38-c{padding:6px 10px;font-size:13px}\n.b38-left .b38-c b{display:inline;font-size:13px;color:var(--ink)}")
# Items: what you own first, then what's left as small tiles (the same buttons, so a tap still says what it is)
rep("""    <div class="itgrid">${list.map(id => `<button class="itbtn" data-b="item" data-id="${id}">${itemCard(id)}</button>`).join('')}</div>`;""",
    """    ${(() => { const got = list.filter(id => S.inv.seen[id]), left = list.filter(id => !S.inv.seen[id]), btn = id => `<button class="itbtn" data-b="item" data-id="${id}">${itemCard(id)}</button>`;
      return (got.length ? `<div class="itgrid">${got.map(btn).join('')}</div>` : '')
        + (left.length ? `<h4 class="lk48-h">Still to find · ${left.length}</h4><div class="itgrid lk48">${left.map(btn).join('')}</div>` : ''); })()}`;""")
rep(".itc-q{font-family:var(--font-display);font-weight:900;font-size:34px;color:var(--muted);line-height:1}",
    ".itc-q{font-family:var(--font-display);font-weight:900;font-size:34px;color:var(--muted);line-height:1}\n.lk48-h{margin:14px 0 6px;font-size:13px;color:var(--muted);letter-spacing:.04em;text-transform:uppercase}\n.itgrid.lk48{grid-template-columns:repeat(auto-fill,minmax(46px,1fr));gap:6px}\n.itgrid.lk48 .itc{min-height:46px;padding:4px;border-width:1.5px;align-content:center}\n.itgrid.lk48 .itc small{display:none}\n.itgrid.lk48 .itc-q{font-size:18px}")
f.save()
print('p48c ok')
