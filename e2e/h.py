# shared test helpers: open a page with a fresh or given save, close sheets, read the save, collect page errors
import asyncio, json, os
from playwright.async_api import async_playwright
KEY = 'bonnet-up.v1'
ARGS = ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-precise-memory-info']
INIT = "window.__allSubs = false; window.__locks28 = true; window.__noTitle34 = true; window.__noDriveIn37 = true;"
CLOSE = "(() => { const m = document.getElementById('modal'); const t = m.hidden ? '' : m.innerText.replace(/\\s+/g, ' '); if (!m.hidden) { const c = m.querySelector('[data-a=close-modal]') || m.querySelector('.btn.primary'); if (c) c.click(); else m.hidden = true; } return t; })()"

class T:
    """one browser page for a test: T(page, w, h, init=INIT); await t.open(fresh=True, save=None, patch=None)"""
    def __init__(s, page_file, w=390, h=844, init=INIT, mobile=None):
        s.file, s.w, s.h, s.init = page_file, w, h, init
        s.mobile = (w < 700) if mobile is None else mobile
        s.errs, s.bad, s.out = [], [], {}
    async def __aenter__(s):
        s.p = await async_playwright().start()
        s.b = await s.p.chromium.launch(args=ARGS)
        s.ctx = await s.b.new_context(viewport={'width': s.w, 'height': s.h}, device_scale_factor=1, has_touch=s.mobile, is_mobile=s.mobile)
        if s.init: await s.ctx.add_init_script(s.init)
        s.pg = await s.ctx.new_page()
        s.pg.on('pageerror', lambda e: s.errs.append(str(e)[:300]))
        return s
    async def __aexit__(s, *a):
        try: await s.b.close()
        finally: await s.p.stop()
    async def open(s, fresh=True, save=None, patch=None, boot=None):
        """fresh: clear storage; save: dict of localStorage to load; patch: JS run on the parsed save S (as s) before reloading"""
        await s.pg.goto('file://' + os.path.abspath(s.file))
        if save is not None:
            await s.pg.evaluate("d => { localStorage.clear(); for (const k in d) localStorage.setItem(k, d[k]); }", save); await s.pg.reload()
        elif fresh:
            await s.pg.evaluate("localStorage.clear()"); await s.pg.reload()
        await s.pg.wait_for_timeout(boot or (3500 if 'gl3d' in s.file else 1800))
        if patch:
            await s.pg.evaluate("""(() => { const s = JSON.parse(localStorage.getItem('%s')); %s; localStorage.setItem('%s', JSON.stringify(s)); })()""" % (KEY, patch, KEY))
            await s.pg.reload(); await s.pg.wait_for_timeout(boot or (3500 if 'gl3d' in s.file else 1800))
    async def close(s, n=1):
        out = []
        for _ in range(n):
            t = await s.pg.evaluate(CLOSE)
            if not t: break
            out.append(t[:90]); await s.pg.wait_for_timeout(250)
        return out
    async def S(s): return await s.pg.evaluate("JSON.parse(localStorage.getItem('%s'))" % KEY)
    async def ev(s, js, arg=None): return await (s.pg.evaluate(js, arg) if arg is not None else s.pg.evaluate(js))
    async def tab(s, name, sub=None):
        await s.pg.evaluate("n => document.getElementById('tab-' + n).click()", name); await s.pg.wait_for_timeout(500)
        if sub: await s.pg.evaluate("a => { const b = [...document.querySelectorAll('#view-' + a[0] + ' [data-b=sub]')].find(x => x.dataset.v === a[1]); if (b) b.click(); }", [name, sub]); await s.pg.wait_for_timeout(400)
    async def act(s, a, **data):
        """click a hidden button with data-a (or data-b if b=True) so the game's own click handler runs"""
        attrs = {'a': a}; attrs.update({k: str(v) for k, v in data.items()})
        await s.pg.evaluate("""d => { const b = document.createElement('button'); for (const k in d) b.dataset[k] = d[k]; b.hidden = true; document.body.appendChild(b); b.click(); b.remove(); }""", attrs)
        await s.pg.wait_for_timeout(400)
    async def skip_day(s):
        """skip to closing and through the night; returns the summary text"""
        s0 = await s.S(); day = s0['day']; summ = ''
        for k in range(50):
            await s.pg.evaluate("(() => { if (!document.getElementById('modal').hidden || document.body.classList.contains('skipping23')) return; __skip('close') || __skip('m120') || __skip('m60'); })()"); await s.pg.wait_for_timeout(120)
            t = await s.pg.evaluate(CLOSE)
            if 'closed' in t.lower() and not summ: summ = t
            if (await s.S())['day'] != day: break
        for _ in range(10):
            await s.pg.wait_for_timeout(150); t = await s.pg.evaluate(CLOSE)
            if 'closed' in t.lower() and not summ: summ = t
        return summ
    def done(s, **extra):
        s.out.update(extra); s.out['bad'] = s.bad; s.out['errors'] = s.errs[:6]
        print(json.dumps(s.out))
        return s.out
