# build 57: the build number and the what's-new sheet
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const BUILD = 56;", "const BUILD = 57;")
rep("""<span class="build-tag">Build 56</span>""", """<span class="build-tag">Build 57</span>""")
rep("seen55: true, seen56: true, eco28: 1,", "seen55: true, seen56: true, seen57: true, eco28: 1,")
rep("S.seen55 = true; S.seen56 = true; save(); setTimeout(() => showWhatsNew23(), 900); }",
    "S.seen55 = true; S.seen56 = true; S.seen57 = true; save(); setTimeout(() => showWhatsNew23(), 900); }")
rep("S.seen55 = true; S.seen56 = true; save(); setTimeout(() => showWhatsNew56(had55), 900); }",
    "S.seen55 = true; S.seen56 = true; S.seen57 = true; save(); setTimeout(() => showWhatsNew57(had56), 900); }")
rep("  else if (!S.seen56) { const had55 = !!S.seen55;", "  else if (!S.seen57) { const had56 = !!S.seen56;")
a = f.s.index("function start(data) {")
f.s = f.s[:a] + """/* build 57: what's new */
function showWhatsNew57(had56) {
  showModal(`<div><span class="label">Build 57</span><h2 class="sheet-title">What’s new</h2></div>
    <ul class="news">
      <li><b>Smoother.</b> The workshop now draws the car and the room in about half the work it took before, and the yard is back to its old speed. Phones that struggle step down more gracefully.</li>
      ${had56 ? '' : '<li><b>Proper lights.</b> Tail lights in sections (red, amber, clear reversing light), projector headlights, and no more spike under the bumper corners.</li>'}
    </ul>
    <button class="btn primary wide" data-a="close-modal">Let’s go</button>`);
}
""" + f.s[a:]
f.save()
print('build 57 ui ok')
