# build 52: the build number and the what's-new sheet
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const BUILD = 51;", "const BUILD = 52;")
rep("""<span class="build-tag">Build 51</span>""", """<span class="build-tag">Build 52</span>""")
rep("seen50: true, seen51: true, eco28: 1,", "seen50: true, seen51: true, seen52: true, eco28: 1,")
rep("S.seen50 = true; S.seen51 = true; save(); setTimeout(() => showWhatsNew23(), 900); }",
    "S.seen50 = true; S.seen51 = true; S.seen52 = true; save(); setTimeout(() => showWhatsNew23(), 900); }")
rep("S.seen50 = true; S.seen51 = true; save(); setTimeout(() => showWhatsNew51(had50), 900); }",
    "S.seen50 = true; S.seen51 = true; S.seen52 = true; save(); setTimeout(() => showWhatsNew52(had51), 900); }")
rep("  else if (!S.seen51) { const had50 = !!S.seen50;", "  else if (!S.seen52) { const had51 = !!S.seen51;")
a = f.s.index("function start(data) {")
f.s = f.s[:a] + """/* build 52: what's new */
function showWhatsNew52(had51) {
  showModal(`<div><span class="label">Build 52</span><h2 class="sheet-title">What’s new</h2></div>
    <ul class="news">
      <li><b>A cleaner forecourt.</b> The dark round blobs outside the garage door were oil stains that looked like shadows. They’re proper oil drips and tyre scuffs now, lit by the sun like the concrete round them.</li>
      <li><b>Clearer daylight.</b> Outside is no longer washed out: sunlit concrete doesn’t glow into a haze, and colours are richer.</li>
      ${had51 ? '' : '<li><b>Better-looking cars everywhere.</b> The cars outside are built like the car on your ramp, your van’s rear lights and windows are fixed, and paint and glass reflect the garage and street round them.</li>'}
    </ul>
    <button class="btn primary wide" data-a="close-modal">Let’s go</button>`);
}
""" + f.s[a:]
f.save()
print('build 52 ui ok')
