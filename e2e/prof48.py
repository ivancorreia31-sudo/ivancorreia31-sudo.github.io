# build 48: where does the main thread's time go in a saved garage? CPU profile for a few seconds (after optional setup JS),
# printed as the functions with the most self time and the most total time, plus frames per second
# usage: python3 prof48.py PAGE STATE.json SECONDS 'setup js' [W H]
import asyncio, json, os, sys
from collections import Counter
from playwright.async_api import async_playwright
PAGE, STATE, SECS = sys.argv[1], sys.argv[2], float(sys.argv[3])
SETUP = sys.argv[4] if len(sys.argv) > 4 else ''
W, H = (int(sys.argv[5]), int(sys.argv[6])) if len(sys.argv) > 6 else (390, 844)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        ctx = await b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1, has_touch=True, is_mobile=W < 700)
        await ctx.add_init_script("window.__noTitle34 = true; window.__allSubs = false; window.__noDriveIn37 = true;")
        page = await ctx.new_page(); errs = []
        page.on('pageerror', lambda e: errs.append(str(e)[:300]))
        await page.goto('file://' + os.path.abspath(PAGE))
        if STATE != '-':
            await page.evaluate("d => { localStorage.clear(); for (const k in d) localStorage.setItem(k, d[k]); }", json.load(open(STATE))); await page.reload()
        await page.wait_for_timeout(4500)
        if SETUP: print('setup:', await page.evaluate(SETUP)); await page.wait_for_timeout(3500)
        cdp = await ctx.new_cdp_session(page)
        await cdp.send('Profiler.enable'); await cdp.send('Profiler.setSamplingInterval', {'interval': 500}); await cdp.send('Profiler.start')
        fps = await page.evaluate("s => new Promise(r => { let n = 0; const t0 = performance.now(); const f = () => { n++; if (performance.now() - t0 < s * 1000) requestAnimationFrame(f); else r(+(n / s).toFixed(1)); }; requestAnimationFrame(f); })", SECS)
        prof = (await cdp.send('Profiler.stop'))['profile']
        nodes = {n['id']: n for n in prof['nodes']}; parent = {}
        for n in prof['nodes']:
            for c in n.get('children', []): parent[c] = n['id']
        dt = prof['timeDeltas']; samples = prof['samples']; selfc = Counter(); totc = Counter()
        for s, d in zip(samples, dt):
            fr = nodes[s]['callFrame']; selfc['%s:%d' % (fr['functionName'] or '(anon)', fr['lineNumber'] + 1)] += d
            seen = set(); k = s
            while k in nodes:
                f2 = nodes[k]['callFrame']; key = '%s:%d' % (f2['functionName'] or '(anon)', f2['lineNumber'] + 1)
                if key not in seen: totc[key] += d; seen.add(key)
                k = parent.get(k)
                if k is None: break
        total = sum(dt)
        print(json.dumps({'fps': fps, 'profiled_ms': round(total / 1000)}))
        print('SELF'); [print('  %6.0f ms %s' % (v / 1000, k)) for k, v in selfc.most_common(18)]
        print('TOTAL'); [print('  %6.0f ms %s' % (v / 1000, k)) for k, v in totc.most_common(30)]
        print('errors', errs[:4]); await b.close()
asyncio.run(main())
