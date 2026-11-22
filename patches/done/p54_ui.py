# build 54: the build number and the what's-new sheet
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const BUILD = 53;", "const BUILD = 54;")
rep("""<span class="build-tag">Build 53</span>""", """<span class="build-tag">Build 54</span>""")
rep("seen52: true, seen53: true, eco28: 1,", "seen52: true, seen53: true, seen54: true, eco28: 1,")
rep("S.seen52 = true; S.seen53 = true; save(); setTimeout(() => showWhatsNew23(), 900); }",
    "S.seen52 = true; S.seen53 = true; S.seen54 = true; save(); setTimeout(() => showWhatsNew23(), 900); }")
rep("S.seen52 = true; S.seen53 = true; save(); setTimeout(() => showWhatsNew53(had52), 900); }",
    "S.seen52 = true; S.seen53 = true; S.seen54 = true; save(); setTimeout(() => showWhatsNew54(had53), 900); }")
rep("  else if (!S.seen53) { const had52 = !!S.seen52;", "  else if (!S.seen54) { const had53 = !!S.seen53;")
a = f.s.index("function start(data) {")
f.s = f.s[:a] + """/* build 54: what's new */
function showWhatsNew54(had53) {
  showModal(`<div><span class="label">Build 54</span><h2 class="sheet-title">What’s new</h2></div>
    <ul class="news">
      <li><b>Cars up close.</b> Doors have fine shut lines all round, there’s a fuel flap, the boot is outlined above the bumper, and the model and engine size are in chrome letters on the back.</li>
      <li><b>Tidier details.</b> No more pale strip up the windscreen pillars or grey corners sticking out of the mirrors; mirrors have a proper black frame round the glass, and the wheel-arch liners are matt.</li>
      ${had53 ? '' : '<li><b>Lights and buildings.</b> The lights over your ramp now light the car, an open bonnet shows a quilted pad, and the buildings over the road are clad in ribbed steel.</li>'}
    </ul>
    <button class="btn primary wide" data-a="close-modal">Let’s go</button>`);
}
""" + f.s[a:]
f.save()
print('build 54 ui ok')
