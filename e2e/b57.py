# build 57: the workshop's room and car are drawn merged (each well under half its pieces as draw calls), no roof
# lights, and the merge leaves taps working: a tap on the car still finds a part
# usage: python3 b57.py PAGE
import asyncio, sys
from h import T
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'gl3d.html'
async def main():
    async with T(PAGE) as t:
        await t.open(fresh=True); await t.close(2)
        await t.ev("__car32({ model: 'Hartwell Rowan 1.6' })"); await t.pg.wait_for_timeout(3000)
        t.out['b'] = b = await t.ev("__batch57()")
        if not b['room'] or b['room']['items'] < 100 or b['room']['batches'] > b['room']['items'] / 3: t.bad.append('room not merged: %s' % b['room'])
        if not b['car'] or b['car']['items'] < 100 or b['car']['batches'] > b['car']['items'] / 3: t.bad.append('car not merged: %s' % b['car'])
        t.out['lights'] = l = await t.ev("__light53()")
        if l['on'] != 0: t.bad.append('roof lights: %s' % l)
        # taps find the same things with the merge on and off (900 points over the screen)
        t.out['pick'] = p = await t.ev("__pick57()")
        if not p['merged'] or p['same'] != p['n'] or p['parts'] < 20: t.bad.append('taps differ with the merge: %s' % p)
        t.done()
asyncio.run(main())
