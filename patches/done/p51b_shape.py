# build 51: crisper bodies. The nose and tail used to close in a plain ellipse, so every car's ends were rounded like a bar
# of soap (the front face bulged 10 cm over its height). They now close in a superellipse: a flatter face with tighter
# edges round the bonnet front, the boot lip and the bumpers, like a pressed panel.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
P = '5'
rep("const nc = [5, 3, 2][lod]; for (let k = 1; k <= nc; k++) { const u = Math.sin(k / nc * PI / 2); must.push(x0R - eR * u, x0F + eF * u); }",
    "const nc = [7, 4, 2][lod]; for (let k = 1; k <= nc; k++) { const u = 1 - Math.pow(1 - k / nc, 2.2); must.push(x0R - eR * u, x0F + eF * u); }")
rep("""      if (x > x0F) { const u = Math.min(1, (x - x0F) / eF), q = Math.sqrt(Math.max(0, 1 - u * u)); y = midF + (y - midF) * q; z *= 0.84 + 0.16 * q; }
      else if (x < x0R) { const u = Math.min(1, (x0R - x) / eR), q = Math.sqrt(Math.max(0, 1 - u * u)); y = midR + (y - midR) * q; z *= 0.84 + 0.16 * q; }""",
    """      if (x > x0F) { const u = Math.min(1, (x - x0F) / eF), q = Math.pow(Math.max(0, 1 - Math.pow(u, EP51)), 1 / EP51); y = midF + (y - midF) * q; z *= 0.84 + 0.16 * q; }
      else if (x < x0R) { const u = Math.min(1, (x0R - x) / eR), q = Math.pow(Math.max(0, 1 - Math.pow(u, EP51)), 1 / EP51); y = midR + (y - midR) * q; z *= 0.84 + 0.16 * q; }""")
rep("const lod = Math.min(2, o.lod | 0), R = s.rear, rx = s.rx, van = !!s.van, bay = !!o.bay, RA = 0.385;",
    "const lod = Math.min(2, o.lod | 0), R = s.rear, rx = s.rx, van = !!s.van, bay = !!o.bay, RA = 0.385, EP51 = %s;" % P)
# and a crisper shoulder: the edge where the side meets the bonnet, waist and boot is tighter (8.5 cm → 5 cm)
if True:
    a, b = '0.05', '0.04'
    rep("const rs = van ? 0.035 : 0.085, rsz = van ? 0.03 : 0.07,", "const rs = van ? 0.035 : %s, rsz = van ? 0.03 : %s," % (a, b))
f.save()
print('p51b ok')
