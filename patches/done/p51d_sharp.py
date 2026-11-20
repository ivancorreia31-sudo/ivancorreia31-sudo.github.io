# build 51: sharper on phones. When a phone couldn't keep 40 frames a second the picture's resolution was lowered in
# steps down to three quarters of a screen pixel, so the yard and the drive went soft (and in battery saver, capped at 30
# frames a second, it always went there). It now stops at one screen pixel, and the glow pass is dropped before that.
# The workshop's still picture also respects the battery-saver resolution.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("    if (dprAvg > 1 / 40 && dprNow > 0.75) next = Math.max(0.75, dprNow - 0.25);",
    "    const lo51 = Math.min(1, DPR_MAX);\n"
    "    if (dprAvg > 1 / 40 && dprNow > lo51) next = Math.max(lo51, dprNow - 0.25);\n"
    "    else if (dprAvg > 1 / 40 && PREF34.gfx !== 'save') { try { if (POST.auto) POST.auto = false; } catch (e) { /* no glow pass */ } }")
rep("else if (!booth && dprNow < DPR_MAX) { clearTimeout(dprIdle22); dprIdle22 = setTimeout(() => { if (!raf && !drv && !fp && !ext && !booth) { setDpr22(DPR_MAX); kick(); } }, 450); }",
    "else if (!booth && dprNow < Math.min(DPR_MAX, PREF34.cap)) { clearTimeout(dprIdle22); dprIdle22 = setTimeout(() => { if (!raf && !drv && !fp && !ext && !booth) { setDpr22(Math.min(DPR_MAX, PREF34.cap)); kick(); } }, 450); }")
f.save()
print('p51d ok')
