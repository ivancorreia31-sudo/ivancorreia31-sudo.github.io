# build 48: the build number and the what's-new sheet
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const BUILD = 47;", "const BUILD = 48;")
rep("""<span class="build-tag">Build 47</span>""", """<span class="build-tag">Build 48</span>""")
rep("seen46: true, seen47: true, eco28: 1,", "seen46: true, seen47: true, seen48: true, eco28: 1,")
rep("S.seen46 = true; S.seen47 = true; save(); setTimeout(() => showWhatsNew23(), 900); }",
    "S.seen46 = true; S.seen47 = true; S.seen48 = true; save(); setTimeout(() => showWhatsNew23(), 900); }")
rep("S.seen46 = true; S.seen47 = true; save(); setTimeout(() => showWhatsNew47(had46), 900); }",
    "S.seen46 = true; S.seen47 = true; S.seen48 = true; save(); setTimeout(() => showWhatsNew48(had47), 900); }")
rep("  else if (!S.seen47) { const had46 = !!S.seen46;", "  else if (!S.seen48) { const had47 = !!S.seen47;")
a = f.s.index("function start(data) {")
f.s = f.s[:a] + """/* build 48: what's new */
function showWhatsNew48(had47) {
  showModal(`<div><span class="label">Build 48</span><h2 class="sheet-title">What’s new</h2></div>
    <ul class="news">
      <li><b>Days that make sense.</b> No more heatwaves in the rain: the day’s event suits the season and the weather. Winter brings cold snaps (battery and starting jobs pay 50% more), and it rains more in autumn and winter.</li>
      <li><b>Parts catalogue.</b> A new tool from level 6. In the parts shop it ticks every box that fits the car, so you only choose the quality.</li>
      <li><b>Tidier collection.</b> The fault book and the Items page show what you’ve found first, and sum up what’s left instead of pages of question marks.</li>
      ${had47 ? '' : '<li><b>Your legacy.</b> From level 5, Daily shows how close you are to selling up for a legacy star. Selling up keeps your Gold Bolts and your whole collection.</li>'}
    </ul>
    <button class="btn primary wide" data-a="close-modal">Let’s go</button>`);
}
""" + f.s[a:]
f.save()
print('build 48 ui ok')
