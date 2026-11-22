# build 53: the build number and the what's-new sheet
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const BUILD = 52;", "const BUILD = 53;")
rep("""<span class="build-tag">Build 52</span>""", """<span class="build-tag">Build 53</span>""")
rep("seen51: true, seen52: true, eco28: 1,", "seen51: true, seen52: true, seen53: true, eco28: 1,")
rep("S.seen51 = true; S.seen52 = true; save(); setTimeout(() => showWhatsNew23(), 900); }",
    "S.seen51 = true; S.seen52 = true; S.seen53 = true; save(); setTimeout(() => showWhatsNew23(), 900); }")
rep("S.seen51 = true; S.seen52 = true; save(); setTimeout(() => showWhatsNew52(had51), 900); }",
    "S.seen51 = true; S.seen52 = true; S.seen53 = true; save(); setTimeout(() => showWhatsNew53(had52), 900); }")
rep("  else if (!S.seen52) { const had51 = !!S.seen51;", "  else if (!S.seen53) { const had52 = !!S.seen52;")
a = f.s.index("function start(data) {")
f.s = f.s[:a] + """/* build 53: what's new */
function showWhatsNew53(had52) {
  showModal(`<div><span class="label">Build 53</span><h2 class="sheet-title">What’s new</h2></div>
    <ul class="news">
      <li><b>Lights in the workshop.</b> The lights over your ramp really light it now: highlights move over the paint as you go round a car, and the sealed concrete floor catches the light.</li>
      <li><b>Under the bonnet.</b> Open a bonnet and you’ll see a quilted sound-deadening pad instead of a black slab.</li>
      <li><b>Proper buildings over the road.</b> The units and the farm barn are clad in ribbed steel on a blockwork base, with dirt splashed up from the ground.</li>
      ${had52 ? '' : '<li><b>A cleaner forecourt.</b> The dark blobs outside the garage door are proper oil drips and tyre marks now, and daylight is no longer washed out.</li>'}
    </ul>
    <button class="btn primary wide" data-a="close-modal">Let’s go</button>`);
}
""" + f.s[a:]
f.save()
print('build 53 ui ok')
