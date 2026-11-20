# patch helper: R(path).rep(old, new, count) replaces text that must occur exactly `count` times; save() writes it back
import sys
class R:
    def __init__(s, path): s.p = path; s.s = open(path, encoding='utf-8').read()
    def rep(s, a, b, cnt=1):
        n = s.s.count(a)
        if n != cnt: raise SystemExit(f'MISMATCH {n}!={cnt}: {a[:120]!r}')
        s.s = s.s.replace(a, b)
    def first(s, a, b, cnt=2):
        n = s.s.count(a)
        if n != cnt: raise SystemExit(f'MISMATCH {n}!={cnt}: {a[:120]!r}')
        s.s = s.s.replace(a, b, 1)
    def save(s): open(s.p, 'w', encoding='utf-8').write(s.s)
