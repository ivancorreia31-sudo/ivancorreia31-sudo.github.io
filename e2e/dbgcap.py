# debug: find an oil-change customer, start the job, run the auto player briefly, then show what the cap step looks like
import asyncio, json, os, sys
from h import T
AJ = open('autojob.js').read()
async def main():
    async with T('gl3d.html') as t:
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.money = 30000; s.bays = [null]")
        await t.close(3)
        found = None
        for d in range(16):
            txt = await t.ev("JSON.stringify((JSON.parse(localStorage.getItem('bonnet-up.v1')).board || []).map(j => j.title))")
            if 'oil' in txt.lower(): found = txt; break
            await t.skip_day(); await t.close(3)
        print('board', found)
        await t.open(fresh=False, patch="s.board.sort((a, b) => (/oil change/i.test(b.title) ? 1 : 0) - (/oil change/i.test(a.title) ? 1 : 0))"); await t.close(3)
        # serve customers until the oil one is on the ramp
        for k in range(6):
            await t.act('desk-go'); await t.pg.wait_for_timeout(800)
            m = await t.ev("document.getElementById('modal').innerText.slice(0, 200)")
            if 'oil' in m.lower():
                await t.ev("document.querySelector('[data-b=desk-start44]').click()"); await t.pg.wait_for_timeout(2500); break
            await t.close(1)
            await t.ev("(() => { const b = document.querySelector('[data-b=desk-next], [data-b=desk-skip]'); if (b) b.click(); })()")
        await t.ev("window.__AJ = { limit: 90000 }")
        log = await t.pg.evaluate(AJ)
        print(log[-8:])
        print(await t.ev("(() => { const c = document.querySelector('.capw'); return c ? [c.offsetWidth, c.offsetHeight, c.parentElement.className, c.outerHTML.slice(0, 300)] : null; })()"))
        print(await t.ev("[...document.querySelectorAll('[data-hold]')].map(b => [b.dataset.hold, b.offsetWidth, b.className, b.closest('.step,.pcard,.ov') && b.closest('.step,.pcard,.ov').className])"))
        print(await t.ev("(document.querySelector('.step') || {}).innerText"))
        print('at 195,420:', await t.ev("(() => { const e = document.elementFromPoint(195, 420); return e ? e.tagName + '#' + e.id + '.' + e.className + ' ' + (e.innerText || '').slice(0, 60) : null; })()"))
        await t.pg.screenshot(path='s24/dbgcap.png')
        print(t.errs)
asyncio.run(main())
