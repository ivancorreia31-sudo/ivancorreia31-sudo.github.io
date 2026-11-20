# syntax-check every large inline script of a page with node --check
import os, re, subprocess, sys, tempfile
p = sys.argv[1] if len(sys.argv) > 1 else 'out/bonnet-up.html'
s = open(p, encoding='utf-8').read(); n = 0
for m in re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', s, re.S):
    code = m.group(1)
    if len(code) < 2000: continue
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as t: t.write(code)
    r = subprocess.run(['node', '--check', t.name], capture_output=True, text=True); os.unlink(t.name)
    if r.returncode: print(r.stderr[:2000]); raise SystemExit('SYNTAX ERROR in script %d' % n)
    n += 1
print('syntax OK', n, 'scripts')
