# build 53: faceX (where the nose or tail surface is at a height, used to place the lamps before they're seated) still
# assumed the old elliptical ends; since build 51 the ends close in a superellipse, so it now inverts that one
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("const x0 = front ? x0F : x0R, e = front ? eF : eR, mid = front ? midF : midR, hh = mid - 0.26, r = Math.min(1, Math.abs(y - mid) / hh), q = Math.sqrt(1 - r * r);",
    "const x0 = front ? x0F : x0R, e = front ? eF : eR, mid = front ? midF : midR, hh = mid - 0.26, r = Math.min(1, Math.abs(y - mid) / hh), q = Math.pow(1 - Math.pow(r, EP51), 1 / EP51);")
f.save()
print('p53c ok')
