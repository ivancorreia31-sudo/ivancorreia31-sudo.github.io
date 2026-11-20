#!/bin/bash
# the regression suite against the current e2e/flat.html and e2e/gl3d.html; one log per test in results/, a .done marker
# per finished test (so a rerun after a restart carries on), then a summary of anything bad or erroring.
# usage: tools/regress.sh [BUILD ITEMS]   (BUILD/ITEMS: the build number and its what's-new count, for wn.py)
cd "$(dirname "$0")/../e2e"
B=${1:-48}; N=${2:-3}
mkdir -p ../results s24
run() { local name=$1; shift; [ -f ../results/$name.done ] && return; echo "== $name: $*"; timeout ${TMO:-1200} python3 "$@" > ../results/$name.log 2>&1; echo "exit $?" >> ../results/$name.log; touch ../results/$name.done; }
run smoke_gl_phone smoke.py gl3d.html 390 844
run smoke_flat_phone smoke.py flat.html 390 844
run smoke_gl_small smoke.py gl3d.html 360 740
run smoke_gl_desktop smoke.py gl3d.html 1280 720
run smoke_gl_landscape smoke.py gl3d.html 844 390
run smoke_flat_tablet smoke.py flat.html 768 1024
run wn wn.py flat.html $B $N
run save_flat save.py flat.html
run save_gl save.py gl3d.html
run feat_flat feat.py flat.html
run feat_gl feat.py gl3d.html
run job_gl job.py gl3d.html 2
run b48_flat b48.py flat.html 24
run b48_gl b48.py gl3d.html 8
run b49_gl b49.py gl3d.html
run b50_flat b50.py flat.html
run carrier_gl carrier.py gl3d.html
run share48_gl share48.py gl3d.html
run breadth_gl breadth.py gl3d.html
run project_gl project.py gl3d.html
run long_flat long.py flat.html 30
(cd .. && python3 tools/build_app.py out/bonnet-up.html > /dev/null)
run itch itch.py ../dist/bonnet-up-itch.zip
cd ../results && python3 - <<'PY'
import glob, json, re
bad = 0
for f in sorted(glob.glob('*.log')):
    t = open(f).read(); last = [l for l in t.strip().split('\n') if l.startswith('{')]
    ex = re.findall(r'exit (\d+)', t)
    try: d = json.loads(last[-1]) if last else None
    except Exception: d = None
    ok = d is not None and not d.get('bad') and not d.get('errors') and ex and ex[-1] == '0'
    if not ok: bad += 1
    print('%-20s %s %s' % (f[:-4], 'ok ' if ok else 'BAD', '' if ok else ((d or {}).get('bad'), (d or {}).get('errors'), t[-300:] if d is None else '')))
print('ALL OK' if not bad else '%d BAD' % bad)
PY
