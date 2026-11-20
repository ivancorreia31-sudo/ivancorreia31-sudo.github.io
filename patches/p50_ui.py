# build 50: the build number and the what's-new sheet
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const BUILD = 49;", "const BUILD = 50;")
rep("""<span class="build-tag">Build 49</span>""", """<span class="build-tag">Build 50</span>""")
rep("seen48: true, seen49: true, eco28: 1,", "seen48: true, seen49: true, seen50: true, eco28: 1,")
rep("S.seen48 = true; S.seen49 = true; save(); setTimeout(() => showWhatsNew23(), 900); }",
    "S.seen48 = true; S.seen49 = true; S.seen50 = true; save(); setTimeout(() => showWhatsNew23(), 900); }")
rep("S.seen48 = true; S.seen49 = true; save(); setTimeout(() => showWhatsNew49(had48), 900); }",
    "S.seen48 = true; S.seen49 = true; S.seen50 = true; save(); setTimeout(() => showWhatsNew50(had49), 900); }")
rep("  else if (!S.seen49) { const had48 = !!S.seen48;", "  else if (!S.seen50) { const had49 = !!S.seen49;")
a = f.s.index("function start(data) {")
f.s = f.s[:a] + """/* build 50: what's new */
function showWhatsNew50(had49) {
  showModal(`<div><span class="label">Build 50</span><h2 class="sheet-title">What’s new</h2></div>
    <ul class="news">
      <li><b>Always something to aim for.</b> From level 8 the level sheet shows the road to your next legacy star, and once every level reward is yours it points you there.</li>
      ${had49 ? '' : '<li><b>Smoother and easier to reach.</b> No more black flicker on slower phones, and on small screens the main buttons stay at the bottom of their card.</li>'}
    </ul>
    <button class="btn primary wide" data-a="close-modal">Let’s go</button>`);
}
""" + f.s[a:]
f.save()
print('build 50 ui ok')
