# the first minutes of a brand-new game at one screen size, as screenshots: the title/intro as it arrives (with the
# first car driving in), after "Let's go", and through the first job with the auto player, then what the game offers
# next. Writes OUT/<n>.png and a strip; prints what was on screen at each point.
# usage: python3 first.py PAGE W H OUT
import asyncio, json, os, subprocess, sys
from h import T
PAGE, W, H, OUT = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
AJ = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'autojob.js')).read()
SAY = "(() => { const m = document.getElementById('modal'); const o = document.querySelector('.ov-card, .welcome'); const s = document.querySelector('.step'); return { modal: m.hidden ? null : m.innerText.replace(/\\s+/g, ' ').slice(0, 120), card: o ? o.innerText.replace(/\\s+/g, ' ').slice(0, 100) : null, step: s ? s.innerText.replace(/\\s+/g, ' ').slice(0, 120) : null, toast: (document.getElementById('toast') || {}).textContent || null }; })()"
async def main():
    os.makedirs(OUT, exist_ok=True); shots = []
    async with T(PAGE, W, H, init="window.__allSubs = false;") as t:
        async def shot(name, wait=0):
            if wait: await t.pg.wait_for_timeout(wait)
            f = '%s/%s.png' % (OUT, name); await t.pg.screenshot(path=f); shots.append(f)
            t.out[name] = await t.ev(SAY)
        await t.pg.goto('file://' + os.path.abspath(PAGE)); await t.ev("localStorage.clear()"); await t.pg.reload()
        await shot('01_load', 1500); await shot('02_3s', 2000); await shot('03_8s', 5000)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()")
        await shot('04_letsgo', 1500)
        await t.ev("window.__AJ = { limit: 120000 }")
        log = await t.pg.evaluate(AJ)
        t.out['job'] = log[-3:]
        await shot('05_invoice', 300)
        await t.close(1); await shot('06_after', 2500)
        await t.close(1); await shot('07_after2', 2500)
        t.out['tabs'] = await t.ev("[...document.querySelectorAll('.tabbar .tab')].map(b => b.innerText.trim() + (b.querySelector('.badge') ? '(' + b.querySelector('.badge').innerText + ')' : '') + (b.classList.contains('locked') || b.getAttribute('aria-disabled') === 'true' ? ' locked' : ''))")
        t.done()
    subprocess.run(['montage'] + shots + ['-tile', '4x', '-geometry', '%dx%d+4+4' % (W // 2 if W > 700 else W * 3 // 4, H // 2 if W > 700 else H * 3 // 4), OUT + '/strip.png'], check=False)
asyncio.run(main())
