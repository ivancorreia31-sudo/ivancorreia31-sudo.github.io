# play whole jobs with the in-page auto player: the first job of a fresh game, then (in a level-9 garage) a job from the
# board and a big two-complaint job; each must reach the invoice and be paid, with no page errors
# usage: python3 job.py PAGE [N]   (N = how many board jobs after the first, default 2)
import asyncio, json, os, sys, time
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
N = int(sys.argv[2]) if len(sys.argv) > 2 else 2
AJ = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'autojob.js')).read()
async def play(t, name):
    m0 = (await t.S())['money']; t0 = time.time()
    log = await t.pg.evaluate(AJ)
    inv = await t.ev("(() => { const m = document.getElementById('modal'); return m.hidden ? '' : m.innerText.replace(/\\s+/g, ' ').slice(0, 400); })()")
    await t.close(3); await t.pg.wait_for_timeout(800); await t.close(2)
    s = await t.S()
    r = {'secs': round(time.time() - t0), 'steps': len(log), 'end': log[-3:], 'invoice': inv[:140], 'money': [m0, s['money']], 'bays': [bool(b) for b in s['bays']]}
    if 'STOP at invoice' not in log: t.bad.append('%s: never reached the invoice %s' % (name, log[-4:]))
    elif 'PAID' not in inv.upper() and 'paid' not in inv: t.bad.append('%s: invoice not paid: %s' % (name, inv[:120]))
    t.out[name] = r
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True)
        await t.close(2)
        await t.ev("(() => { const b = document.querySelector('[data-a=dismiss-intro]'); if (b) b.click(); })()"); await t.pg.wait_for_timeout(600)
        await play(t, 'first')
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 11000; s.money = 30000; s.bays = [null]")
        await t.close(3)
        for k in range(N):
            await t.tab('jobs'); await t.close(1)
            big = k == N - 1
            if big: await t.ev("(() => { for (let i = 0; i < 8; i++) { const j = window.__big46 && __big46(); if (j) return true; } return false; })()")
            took = await t.ev("big => { const bs = [...document.querySelectorAll('[data-a=accept]:not([disabled])')]; const b = big ? bs[bs.length - 1] : bs[0]; if (!b) return null; const tx = (b.closest('article, section, .ticket') || b.parentElement).innerText.replace(/\\s+/g, ' ').slice(0, 90); b.click(); return tx; }", big)
            if not took:
                # customers at reception: serve the next one and start on their car
                await t.act('desk-go'); await t.pg.wait_for_timeout(900)
                took = await t.ev("(() => { const m = document.getElementById('modal'); const tx = m.hidden ? '' : m.innerText.replace(/\\s+/g, ' ').slice(0, 90); const b = document.querySelector('[data-b=desk-start44]'); if (!b) return null; b.click(); return 'desk: ' + tx; })()")
            await t.pg.wait_for_timeout(2500); await t.close(2)
            if not took: t.bad.append('no job to take (%d): %s' % (k, await t.ev("[document.querySelectorAll('[data-a=accept]').length, document.querySelectorAll('[data-a=accept]:not([disabled])').length, document.getElementById('modal').hidden ? '' : document.getElementById('modal').innerText.slice(0, 80), JSON.parse(localStorage.getItem('bonnet-up.v1')).bays.map(b => !!b)]"))); break
            t.out['took%d' % k] = took
            await play(t, 'job%d' % k)
        t.done()
asyncio.run(main())
