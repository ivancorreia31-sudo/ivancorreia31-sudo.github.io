# build 56: the build number and the what's-new sheet
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const BUILD = 55;", "const BUILD = 56;")
rep("""<span class="build-tag">Build 55</span>""", """<span class="build-tag">Build 56</span>""")
rep("seen54: true, seen55: true, eco28: 1,", "seen54: true, seen55: true, seen56: true, eco28: 1,")
rep("S.seen54 = true; S.seen55 = true; save(); setTimeout(() => showWhatsNew23(), 900); }",
    "S.seen54 = true; S.seen55 = true; S.seen56 = true; save(); setTimeout(() => showWhatsNew23(), 900); }")
rep("S.seen54 = true; S.seen55 = true; save(); setTimeout(() => showWhatsNew55(had54), 900); }",
    "S.seen54 = true; S.seen55 = true; S.seen56 = true; save(); setTimeout(() => showWhatsNew56(had55), 900); }")
rep("  else if (!S.seen55) { const had54 = !!S.seen54;", "  else if (!S.seen56) { const had55 = !!S.seen55;")
a = f.s.index("function start(data) {")
f.s = f.s[:a] + """/* build 56: what's new */
function showWhatsNew56(had55) {
  showModal(`<div><span class="label">Build 56</span><h2 class="sheet-title">What’s new</h2></div>
    <ul class="news">
      <li><b>Proper rear lights.</b> Tail lights are in sections now: red with its LED bar, an amber indicator and a clear reversing light.</li>
      <li><b>Headlights.</b> A projector lens in the inner bowl and an amber indicator at the outer end.</li>
      <li><b>Tidier bumpers.</b> No more blue spike hanging under the bumper corners.</li>
      ${had55 ? '' : '<li><b>Window rubbers and side repeaters.</b> Black seals along the tops of the side windows, and an amber indicator on each front wing.</li>'}
    </ul>
    <button class="btn primary wide" data-a="close-modal">Let’s go</button>`);
}
""" + f.s[a:]
f.save()
print('build 56 ui ok')
