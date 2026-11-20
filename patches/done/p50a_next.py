# build 50 (a): the level sheet always says what's next. From level 8 it shows the road to your next legacy star
# (business worth against £250,000), and once every level reward is in, that's what it points to instead of a dead end.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("""    ${rows.length ? `<span class="label">Coming up</span><ul class="lv41">${rows.join('')}</ul>` : '<p>Everything’s open, and customers pay the most they will for your labour.</p>'}
    <button class="btn primary wide" data-a="close-modal">Back to work</button>`;""",
    """    ${rows.length ? `<span class="label">Coming up</span><ul class="lv41">${rows.join('')}</ul>` : '<p>Everything’s open, and customers pay the most they will for your labour.</p>'}
    ${(() => { try { return next50(L); } catch (e) { return ''; } })()}
    <button class="btn primary wide" data-a="close-modal">Back to work</button>`;""")
rep("function level41Html() {", """/* build 50: from level 8, the next big goal is a legacy star */
function next50(L) {
  const st = legacy21(); if (L < 8 || st >= 5) return '';
  const v = Math.max(0, netWorth21()), ready = canSellUp(), pct = Math.round(Math.min(1, v / 250000) * 100);
  return `<div class="nx50"><span class="label">What’s next: legacy star ${st + 1}</span>
    <p class="sm">${ready ? 'You can sell up now and start a new garage. Every legacy star makes labour pay 8% more in every garage you ever run.' : `Grow the business to ${money(250000)}, then sell up and start again with labour paying 8% more for good.`}</p>
    <div class="lg47-r"><span class="sm">Business worth</span><b class="sm${ready ? ' ok48' : ''}">${money(v)}${v >= 250000 ? ' ✓' : ` of ${money(250000)}`}</b><div class="gauge" role="img" aria-label="Business worth ${money(v)} of ${money(250000)}"><i class="good" style="width:${pct}%"></i></div></div>
    ${ready ? '<button class="btn wide" data-b="nx50">See the Legacy card on Daily</button>' : ''}</div>`;
}
function level41Html() {""")
rep(".lg47-r b.ok48{color:var(--good)}", ".lg47-r b.ok48{color:var(--good)}\n.nx50{display:grid;gap:6px;margin:4px 0 10px;padding:10px 12px;border-radius:12px;background:var(--panel-2)}")
rep("act22('ba-save', b => baSave22(+b.dataset.no));", "act22('ba-save', b => baSave22(+b.dataset.no));\nact22('nx50', () => { closeModal(); S.sub = S.sub || {}; S.sub.daily = 'today'; S.view = 'daily'; render(); toTop(); });")
f.save()
print('p50a ok')
