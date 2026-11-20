# build 51: the build number and the what's-new sheet
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const BUILD = 50;", "const BUILD = 51;")
rep("""<span class="build-tag">Build 50</span>""", """<span class="build-tag">Build 51</span>""")
rep("seen48: true, seen49: true, seen50: true, eco28: 1,", "seen48: true, seen49: true, seen50: true, seen51: true, eco28: 1,")
rep("S.seen48 = true; S.seen49 = true; S.seen50 = true; save(); setTimeout(() => showWhatsNew23(), 900); }",
    "S.seen48 = true; S.seen49 = true; S.seen50 = true; S.seen51 = true; save(); setTimeout(() => showWhatsNew23(), 900); }")
rep("S.seen48 = true; S.seen49 = true; S.seen50 = true; save(); setTimeout(() => showWhatsNew50(had49), 900); }",
    "S.seen48 = true; S.seen49 = true; S.seen50 = true; S.seen51 = true; save(); setTimeout(() => showWhatsNew51(had50), 900); }")
rep("  else if (!S.seen50) { const had49 = !!S.seen49;", "  else if (!S.seen51) { const had50 = !!S.seen50;")
a = f.s.index("function start(data) {")
f.s = f.s[:a] + """/* build 51: what's new */
function showWhatsNew51(had50) {
  showModal(`<div><span class="label">Build 51</span><h2 class="sheet-title">What’s new</h2></div>
    <ul class="news">
      <li><b>Better-looking cars everywhere.</b> The cars outside (your van, the yard, the showroom, the street) are now built like the car on your ramp: the same body, glass and lights. Your van’s rear lights and windows are fixed.</li>
      <li><b>Real reflections.</b> Paint, glass and chrome now reflect the garage and the street around them, and the bodywork has sharper edges.</li>
      <li><b>Sharper on phones.</b> Walking the yard and driving no longer go blurry when your phone is working hard.</li>
      ${had50 ? '' : '<li><b>A tidier nose.</b> Raise a car on the lift and look up at the front: the black panel inside the nose no longer pokes out round the headlamps.</li>'}
    </ul>
    <button class="btn primary wide" data-a="close-modal">Let’s go</button>`);
}
""" + f.s[a:]
f.save()
print('build 51 ui ok')
