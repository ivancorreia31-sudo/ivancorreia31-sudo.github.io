# build 50: the level sheet shows the next legacy star from level 8 (none below), the business-worth row, and once
# selling up is possible a button that closes the sheet and opens Daily on the Legacy card
# usage: python3 b50.py PAGE
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'flat.html'
SHEET = "(() => { const m = document.getElementById('modal'); const n = m.querySelector('.nx50'); return { open: !m.hidden, nx: n ? n.innerText.replace(/\\s+/g, ' ').slice(0, 160) : null, btn: !!m.querySelector('[data-b=nx50]'), rows: m.querySelectorAll('.lv41 li').length }; })()"
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True)
        for name, xp, money, want, btn in [('L5', 3200, 5000, False, False), ('L9', 11000, 40000, True, False), ('L17 rich', 40000, 400000, True, True)]:
            await t.open(fresh=False, patch="s.seenIntro = true; s.xp = %d; s.money = %d; s.legacy = 0" % (xp, money)); await t.close(3)
            await t.ev("__lvl41()"); await t.pg.wait_for_timeout(300)
            r = await t.ev(SHEET); t.out[name] = r
            if bool(r['nx']) != want: t.bad.append('%s: legacy goal shown=%s, expected %s' % (name, bool(r['nx']), want))
            if r['btn'] != btn: t.bad.append('%s: Daily button %s, expected %s' % (name, r['btn'], btn))
            if want and 'Business worth' not in (r['nx'] or ''): t.bad.append('%s: no business worth row' % name)
            if btn:
                await t.ev("document.querySelector('#modal [data-b=nx50]').click()"); await t.pg.wait_for_timeout(700)
                t.out['went'] = await t.ev("({ modal: !document.getElementById('modal').hidden, view: !!document.querySelector('#view-daily .lg47'), tab: document.querySelector('#tab-daily').getAttribute('aria-current') })")
                if t.out['went']['modal'] or not t.out['went']['view']: t.bad.append('the button did not take me to the Legacy card: %s' % t.out['went'])
            await t.close(2)
        t.done()
asyncio.run(main())
