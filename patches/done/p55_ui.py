# build 55: the build number and the what's-new sheet
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const BUILD = 54;", "const BUILD = 55;")
rep("""<span class="build-tag">Build 54</span>""", """<span class="build-tag">Build 55</span>""")
rep("seen53: true, seen54: true, eco28: 1,", "seen53: true, seen54: true, seen55: true, eco28: 1,")
rep("S.seen53 = true; S.seen54 = true; save(); setTimeout(() => showWhatsNew23(), 900); }",
    "S.seen53 = true; S.seen54 = true; S.seen55 = true; save(); setTimeout(() => showWhatsNew23(), 900); }")
rep("S.seen53 = true; S.seen54 = true; save(); setTimeout(() => showWhatsNew54(had53), 900); }",
    "S.seen53 = true; S.seen54 = true; S.seen55 = true; save(); setTimeout(() => showWhatsNew55(had54), 900); }")
rep("  else if (!S.seen54) { const had53 = !!S.seen53;", "  else if (!S.seen55) { const had54 = !!S.seen54;")
a = f.s.index("function start(data) {")
f.s = f.s[:a] + """/* build 55: what's new */
function showWhatsNew55(had54) {
  showModal(`<div><span class="label">Build 55</span><h2 class="sheet-title">What’s new</h2></div>
    <ul class="news">
      <li><b>Window rubbers.</b> The side windows sit in black seals along the top as well as the bottom, on the car on your ramp and every car outside.</li>
      <li><b>Side repeaters.</b> Each front wing has its amber indicator.</li>
      ${had54 ? '' : '<li><b>Cars up close.</b> Fine shut lines round every door, a fuel flap, the boot outlined with the model and engine in chrome letters, and no more pale strip up the windscreen pillars.</li>'}
    </ul>
    <button class="btn primary wide" data-a="close-modal">Let’s go</button>`);
}
""" + f.s[a:]
f.save()
print('build 55 ui ok')
