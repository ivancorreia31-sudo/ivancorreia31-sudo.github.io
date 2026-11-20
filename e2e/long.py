# a later-game garage left to run for weeks: two mechanics on the other ramps, the player skips to closing each day.
# Catches errors in the overnight sums, lists in the save that never stop growing, the weekly report and Garage of the
# Week, and money that runs away. STATE=path also writes the final localStorage (for play-throughs).
# usage: python3 long.py PAGE DAYS
import asyncio, json, os, sys, time
from h import T, KEY
PAGE = sys.argv[1] if len(sys.argv) > 1 else 'flat.html'
DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 30
async def main():
    async with T(PAGE, 390, 800, mobile=False) as t:
        t0 = time.time()
        await t.open(fresh=True)
        await t.open(fresh=False, patch="s.seenIntro = true; s.xp = 10900; s.money = 30000; s.gold = 0; s.owned = Object.assign(s.owned || {}, { bay2: true, bay3: true, recept: true, ads: 2, carwash: true }); s.bays = [null, null, null]; s.sub = Object.assign(s.sub || {}, { garage: 'staff' })")
        await t.close(3)
        await t.tab('garage', 'staff')
        for _ in range(2):
            await t.ev("(() => { const b = [...document.querySelectorAll('[data-a=stf-hire]')].find(x => !x.disabled); if (b) b.click(); })()"); await t.pg.wait_for_timeout(400); await t.close(2)
        s = await t.S(); t.out['staff'] = len(s.get('staff') or [])
        if t.out['staff'] < 2: t.bad.append('could not hire two mechanics')
        await t.tab('workshop')
        days, weeks = [], []; d0 = s['day']
        while True:
            s = await t.S()
            if s['day'] - d0 >= DAYS or s.get('over'): break
            day = s['day']; summ = await t.skip_day(); s = await t.S()
            if s['day'] == day: t.bad.append('day %d never ended' % day); break
            row = {'day': day, 'money': s['money'], 'xp': s['xp'], 'kb': round(len(json.dumps(s)) / 1024, 1), 'rep': round(s.get('rep', 0), 2), 'cmp': len(s.get('complaints') or []), 'warr': len([j for j in (s.get('board') or []) if j and j.get('warranty')]), 'ph': len(((s.get('ph35') or {}).get('list')) or []), 'staffJobs': sum((x.get('jobs') or 0) for x in (s.get('staff') or [])), 'staff': [[x.get('name'), round(x.get('mood', -1), 2) if isinstance(x.get('mood'), (int, float)) else x.get('mood'), x.get('jobs'), x.get('bay')] for x in (s.get('staff') or [])], 'bays': [(b or {}).get('staff') if isinstance(b, dict) else b for b in s.get('bays') or []]}
            days.append(row)
            if 'report' in summ.lower(): weeks.append({'day': day, 'gw': 'garage of the week' in summ.lower(), 'gw44': {k: (s.get('gw44') or {}).get(k) for k in ['wins', 'streak', 'hist']}})
        t.out['rep'] = [[d['day'], d['rep'], d['cmp'], d['warr']] for d in days]
        t.out['days'] = days[::6] + days[-1:]; t.out['weeks'] = weeks; t.out['secs'] = round(time.time() - t0)
        if len(days) < DAYS: t.bad.append('only %d days' % len(days))
        if len(weeks) < DAYS // 7 - 1: t.bad.append('weekly reports missing: %d' % len(weeks))
        if any(not w['gw'] for w in weeks): t.bad.append('a week report without Garage of the Week')
        if days and days[-1]['kb'] > 400: t.bad.append('save is %s KB' % days[-1]['kb'])
        if days and days[-1]['ph'] > 200: t.bad.append('phone list keeps growing: %d' % days[-1]['ph'])
        most = max([d['staffJobs'] for d in days] or [0])
        if most < DAYS // 2: t.bad.append('the mechanics hardly worked: %d jobs' % most)
        t.out['quit'] = [d['day'] for i, d in enumerate(days[1:]) if len(d['staff']) < len(days[i]['staff'])]
        if os.environ.get('STATE'):
            json.dump(await t.ev("Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)]))"), open(os.environ['STATE'], 'w'))
        t.done()
asyncio.run(main())
