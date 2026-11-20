# what's new: a returning player from the last build sees this build's sheet once (with the right number of items and
# the build tag), a player from two builds back sees one more item, and a new player sees no sheet at all
# usage: python3 wn.py PAGE BUILD ITEMS   e.g. python3 wn.py flat.html 48 3
import asyncio, sys
from h import T, KEY
PAGE, BUILD, ITEMS = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
SHEET = "(() => { const m = document.getElementById('modal'); return m.hidden ? null : { label: (m.querySelector('.label') || {}).innerText, items: m.querySelectorAll('.news li').length, text: m.innerText.slice(0, 120) }; })()"
async def main():
    async with T(PAGE, init="window.__allSubs = false; window.__noTitle34 = true; window.__noDriveIn37 = true;") as t:
        await t.open(fresh=True)
        t.out['fresh'] = await t.ev(SHEET)
        if t.out['fresh'] and 'new' in (t.out['fresh']['text'] or '').lower(): t.bad.append('a new player saw what’s new')
        for back, want in [(1, ITEMS), (2, ITEMS + 1)]:
            await t.open(fresh=False, patch="s.seenIntro = true; delete s.seen%d; %s" % (BUILD, ''.join('delete s.seen%d; ' % (BUILD - k) for k in range(1, back))))
            await t.pg.wait_for_timeout(1200)
            sh = await t.ev(SHEET); t.out['from_%d' % (BUILD - back)] = sh
            if not sh or 'build %d' % BUILD not in (sh['label'] or '').lower(): t.bad.append('no Build %d sheet for a player from build %d: %s' % (BUILD, BUILD - back, sh))
            elif sh['items'] != want: t.bad.append('player from build %d saw %d items, expected %d' % (BUILD - back, sh['items'], want))
            await t.close(2)
            s = await t.S()
            if not s.get('seen%d' % BUILD): t.bad.append('seen%d not set' % BUILD)
            await t.pg.reload(); await t.pg.wait_for_timeout(2000)
            again = await t.ev(SHEET)
            if again and 'build %d' % BUILD in (again['label'] or '').lower(): t.bad.append('the sheet came back after a reload')
        t.out['build_tag'] = await t.ev("(document.querySelector('.build') || {}).innerText || null")
        t.done()
asyncio.run(main())
