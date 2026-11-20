# build 48: sharing. Without a share sheet (desktop browsers) there's no Share button and Save works as before; on a phone
# that can share pictures (stubbed here), photo mode and the before & after card hand a JPEG, a line about the car and the
# link to the game to the share sheet
# usage: python3 share48.py gl3d.html
import asyncio, os, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
AJ = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'autojob.js')).read()
STUB = "(() => { window.__shared = null; navigator.canShare = () => true; navigator.share = async d => { const f = d.files && d.files[0]; window.__shared = { n: (d.files || []).length, type: f && f.type, size: f && f.size, name: f && f.name, text: d.text }; }; return true; })()"
SHEET = "(() => { const m = document.getElementById('modal'); return m.hidden ? null : [...m.querySelectorAll('button')].map(b => b.dataset.a || b.dataset.b); })()"
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(2500)
        t.out['can_plain'] = await t.ev("__share48.can()")
        await t.act('photo'); await t.pg.wait_for_timeout(1200)
        t.out['photo_plain'] = await t.ev(SHEET)
        if t.out['can_plain'] or 'photo-share48' in (t.out['photo_plain'] or []): t.bad.append('Share shown where the browser cannot share pictures')
        if 'photo-save' not in (t.out['photo_plain'] or []): t.bad.append('no Save in photo mode: %s' % t.out['photo_plain'])
        await t.close(2)
        # a phone that can share
        await t.ev(STUB)
        await t.act('photo'); await t.pg.wait_for_timeout(1200)
        t.out['photo_btns'] = await t.ev(SHEET)
        await t.ev("(() => { const b = document.querySelector('[data-b=photo-share48]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(800)
        t.out['photo_shared'] = await t.ev("window.__shared")
        sh = t.out['photo_shared'] or {}
        if sh.get('n') != 1 or sh.get('type') != 'image/jpeg' or (sh.get('size') or 0) < 5000 or 'github.io' not in (sh.get('text') or ''): t.bad.append('photo share %s' % sh)
        await t.close(2)
        # finish the first job, then share its before & after
        log = await t.pg.evaluate(AJ); await t.close(3); await t.pg.wait_for_timeout(1500); await t.close(2)
        t.out['job'] = log[-1:]
        await t.tab('collection', 'feed')
        opened = await t.ev("(() => { const b = document.querySelector('[data-b=ba-open]'); if (!b) return false; b.click(); return true; })()"); await t.pg.wait_for_timeout(2500)
        t.out['ba_open'] = opened
        if opened:
            await t.ev("window.__shared = null")
            t.out['ba_btns'] = await t.ev(SHEET)
            await t.ev("(() => { const b = document.querySelector('[data-b=ba-share48]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(2500)
            sh = await t.ev("window.__shared") or {}
            t.out['ba_shared'] = sh
            if sh.get('type') != 'image/jpeg' or 'Before and after' not in (sh.get('text') or '') or (sh.get('size') or 0) < 10000: t.bad.append('before & after share %s' % sh)
            t.out['shares'] = (await t.S())['stats'].get('shares48')
            if (t.out['shares'] or 0) < 2: t.bad.append('shares not counted: %s' % t.out['shares'])
        else: t.out['note'] = 'no before & after for this job (not every job gets one)'
        t.done()
asyncio.run(main())
