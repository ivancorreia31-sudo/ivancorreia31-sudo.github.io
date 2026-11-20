# build 49: the build number and the what's-new sheet
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const BUILD = 48;", "const BUILD = 49;")
rep("""<span class="build-tag">Build 48</span>""", """<span class="build-tag">Build 49</span>""")
rep("seen47: true, seen48: true, eco28: 1,", "seen47: true, seen48: true, seen49: true, eco28: 1,")
rep("S.seen47 = true; S.seen48 = true; save(); setTimeout(() => showWhatsNew23(), 900); }",
    "S.seen47 = true; S.seen48 = true; S.seen49 = true; save(); setTimeout(() => showWhatsNew23(), 900); }")
rep("S.seen47 = true; S.seen48 = true; save(); setTimeout(() => showWhatsNew48(had47), 900); }",
    "S.seen47 = true; S.seen48 = true; S.seen49 = true; save(); setTimeout(() => showWhatsNew49(had48), 900); }")
rep("  else if (!S.seen48) { const had47 = !!S.seen47;", "  else if (!S.seen49) { const had48 = !!S.seen48;")
a = f.s.index("function start(data) {")
f.s = f.s[:a] + """/* build 49: what's new */
function showWhatsNew49(had48) {
  showModal(`<div><span class="label">Build 49</span><h2 class="sheet-title">What’s new</h2></div>
    <ul class="news">
      <li><b>No more black flicker.</b> On slower phones the 3D garage could flash black for a moment while it adjusted its sharpness to keep things smooth. It doesn’t any more.</li>
      ${had48 ? '' : '<li><b>Share your work, and days that make sense.</b> A Share button for your photos and before & afters, a parts catalogue from level 6, and events that suit the season and the weather.</li>'}
    </ul>
    <button class="btn primary wide" data-a="close-modal">Let’s go</button>`);
}
""" + f.s[a:]
f.save()
print('build 49 ui ok')
