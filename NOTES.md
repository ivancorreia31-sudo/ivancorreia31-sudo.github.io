# Bonnet Up: build notes

## Where things are
- Live game: `main` branch of ivancorreia31-sudo/ivancorreia31-sudo.github.io (GitHub Pages): `game.html` (the game),
  `index.html` (landing page that registers `sw.js` and opens the game), `sw.js` (offline cache; its VERSION is
  `bonnet-up-v<BUILD>-<sha1(game.html)[:8]>`), fonts/, three.min.js (r128), icons, manifest, privacy.html.
- The Claude artifact https://claude.ai/artifact/ABLAodQD9zd4nwpQH1zJgD holds the single-file version (Google Fonts and
  three.js from cdnjs). `src/base.html` is that file for the last published build.
- itch.io: `dist/bonnet-up-itch.zip` (index.html = the game page, three.min.js, fonts). The owner uploads it himself.
- Playgama: stopped (owner's call). The rewarded-ad code stays dormant in the game; don't build or send its zip.

## Rules from the owner
- Gold Bolts are earned only, never bought with real money. Rewarded ads only through the Playgama bridge, reward only
  on 'rewarded'.
- Commits: author "Bonnet Up build" <ivancorreia31@googlemail.com> (private: authorship only). Messages end with the
  Co-Authored-By / Claude-Session lines.
- Invented car makes only (no real designs, names or logos). Attached photos never go into the game.

## Publishing build N
1. `tools/build.sh <patches...>` → out/bonnet-up.html, e2e/flat.html, e2e/gl3d.html. `tools/regress.sh N ITEMS`.
2. Artifact: publish out/bonnet-up.html to the URL above with label "Build N".
3. `python3 tools/build_app.py out/bonnet-up.html` → dist/app/* and dist/bonnet-up-itch.zip. Copy dist/app/* into the
   main-branch clone, commit, push. Send the itch zip to the owner.
4. `cp out/bonnet-up.html src/base.html`, move patches to patches/done/, commit and push `dev`.

## History
- Builds 1-47 were made with a long patch chain (p22a... p47e) in a scratch folder that a machine restart wiped on
  Nov 20 2026. Build 47 (src/base.html) is the recovered artifact; tools/build_app.py reproduces the published Build 47
  game.html and sw.js byte for byte. The old test suite (~60 tests) was lost too; e2e/ is its rebuilt replacement.
- Build 47: legacy stars in the save; Legacy card on Daily from L5; sell-up keeps collection/gold/settings; photo prune
  (newest 60 before/afters); Garage of the Week target = median of the last 3 weeks; long-session memory fixes (TEXDRAW
  entries dropped on texture dispose; LITE simple-car shape cache LRU 24 styles / 24 MB).

## Build 48 (published: Pages 7fdc899, artifact v51)
- p48a_world: events suit season and weather (heatwave: dry summer days; new cold snap: winter; potholes: not summer);
  rain chance by season (summer .12, spring .22, autumn .3, winter .32). Seasons are 14 days each from day 1 (Spring).
  window.__ev48(day, weather).
- p48b_catalogue: "Parts catalogue tablet" (tools, L6, base £1,500): parts-shop boxes that fit get a ✓ Fits tag, the
  others dim. window.__shop48.open(id) / .fits().
- p48c_tidy: Legacy rows "Level 7 of 8" / "Business worth £x of £250,000" with ticks; fault book shows found faults and
  sums the rest by area; Items shows owned items first and the rest as small tiles.
- p48d_share: Share button (Web Share API with files) in photo mode and on the before & after card where the phone can
  share pictures; text + link (github.io origin or the Pages URL). The before & after picture is composed when the
  card opens so Safari allows the share straight after the tap. S.stats.shares48.
- p48_ui: BUILD 48, what's new (3 items; 4 for players from before 47).

## Tests (e2e/, run from inside e2e/)
- h.py: harness (T class: open with fresh/save/patch, close sheets, tab/sub, act = click a hidden data-a button,
  skip_day). autojob.js: in-page auto player (bolts, seized nuts with oil fallback, torque, tyre pump hold, cap twist,
  drain/pour holds, parts shop by reading car + boxes, mini-games via __mgWin, quiz) stops at the invoice.
- smoke.py PAGE W H, job.py PAGE N, feat.py PAGE, save.py PAGE, wn.py PAGE BUILD ITEMS, long.py PAGE DAYS, b48.py,
  share48.py. tour48.py / job48.py / prof48.py are play-through and profiling tools (screenshots, CPU profile).
- SwiftShader is slow (1-5 fps with a car on the ramp): anything timed per frame (seized-nut taps, holds) is slow in
  tests but fine on real GPUs.

## Facts worth knowing
- XP for level L = 150·L·(L−1). Content unlocks up to L10; trust44 labour bonus after L6; legacy: sell up at L8 with a
  business worth £250,000, up to 5 stars at +8% labour each.
- The game script is one big closure; tests reach internals only through window.__xxx hooks.
- Selectors: tabs #tab-workshop/jobs/daily/collection/garage; sub-tabs #view-<tab> [data-b=sub][data-v=...];
  reception: [data-a=desk-go] then [data-b=desk-start44]; board: [data-a=accept]; crate [data-b=crate][data-k=style];
  showroom walk [data-b=sh-walk], close #shw22 [data-b=shw-close]; first-person [data-a=fp-walk], exit [data-fp=exit];
  test drive [data-a=g-drive], end [data-dv=end]; phone [data-b=phone35], tabs [data-b=ph36tab]; auctions need a night
  (lots come overnight), [data-a=auction], [data-a=auc-bid], [data-a=auc-walk].

## Build 49 (published: Pages 0a24150, artifact v52)
- p49a_flash: renderer.render is wrapped to remember the last scene/camera; adaptDpr redraws straight after a resize
  (it used to leave the canvas blank until the next frame). window.__dpr49(v) changes the resolution and reads a pixel.
- p49b_small: the welcome card's button row is its last child and sticks to the card's bottom; the step card's
  .st-acts.st-under sticks too. b49.py checks Let's go / Test drive are on screen at 320x568, 360x640, 390x844.
- itch zip: static/itch-index.html (the quarter-turn shell, BonnetShell) is index.html; the game is game.html.
  e2e/itch.py serves the zip over HTTP and checks shell, game, fonts, three.js and the turn button.
- Test pages use static/app-head.txt (it has the [hidden]{display:none!important} rule the game relies on).

## Build 50 (published: Pages a0019ae, artifact v53)
- p50a_next: level41Html shows next50(L) from level 8 (legacy star goal, business worth gauge, data-b=nx50 button to
  the Daily Legacy card when canSellUp).
- p50b_carrier: bayShell21 fits the black front-end carrier (crossmember, slam panel in stepped segments, posts at
  z ±0.66, headlamp backs) and the inner wing walls inside the nose using SK24.fx (foremost paint x at y,z) with a
  1.5 cm gap. Owner saw a black L round the headlamps from under a lifted car. window.__bayNose50() lists any bay piece
  ahead of the nose; e2e/carrier.py runs it on all 69 models (was 69/69 poking out, now 0).
- Debug-only tools (patches/debug/dbg_pick.py, never published): __dbg.pick/pickAll (what's under a screen point,
  even meshes that ignore taps), partBox, isolate, hideRole, nose. e2e/hl2.py/hl3.py: lift a car and look at a part
  from below, find dark pixels and name them.
- Auto player: bleeds brakes in order (RR, RL, FR, FL), skips Customise/To the unit, tunes on the dyno.

## Build 51 (published: Pages a4e4612, artifact v54)
- p51a_lite: liteGeo uses skin24 lod 0 close up (lod 2 far; was 1/2) and seat step 0.045; lamps use the workshop sizes
  and zL51 (the conformLamps24 clamp: |z| ≤ 0.81·SF(faceX, y) − 0.8·halfW). Wipers + aerial close up.
  window.__lite51(style, far) → { reachT, reachH (how far lamps reach round from the tail/nose), tris, styles }.
- p51b_shape: skin24 ends close in a superellipse (EP51 = 5, stations 1−(1−k/nc)^2.2, nc 7/4/2); shoulder rs/rsz
  0.05/0.04 for cars (vans unchanged).
- p51c_probe: probe51(scene, x, y, z, hide, ibl, k) → PMREM render target from a 256 cube (sRGB, tone-mapped, shadows
  not re-rendered, lastS49/lastC49 kept). Workshop: PR51.ws flag (start, ENVS.in loaded, decorSig change) → taken in
  frame() before the render, car hidden. Yard/drive: W.probe51 (setMood, ENVS.out loaded) → taken in driveFrameIn at
  (5.5, 1.3, −9.5), hiding the ride, van, walker and rain, exposure ×0.8. window.__probe51() → { ws, out }.
- p51d_sharp: adaptDpr floor min(1, DPR_MAX) (was 0.75), then POST.auto off; idle workshop DPR respects PREF34.cap.
- Debug: tools/dbg.sh builds e2e/gl3d_dbg.html (patches/debug/dbg_pick.py: + liteShow, skinN, liteN, walkTo, run).
  e2e/carlook.py (yard van at eye height, JS= / ANG= env), closeup.py (big hero shots), vanshot.py, litegallery.py,
  probe.py (evaluate expressions; PAGE=).

## Build 52 (published: Pages 1277344, artifact v55)
- p52a_outside: forecourt stains = TX.stains atlas quads merged into one M.stain mesh (userData.stain52) in
  buildWorld19; POST.thr 0.93 outside / 0.8 elsewhere and toneMappingExposure expoWs52 × 0.9 outside / expoWs52
  elsewhere, set per frame in driveFrameIn, frame, fpFrame and extFrame. window.__out52() → { stain, expo, ws, thr }.
- e2e/outlook.py: six eye-height views round the yard at phone size (JS= runs code in the debug page first).
- SwiftShader has no anisotropic filtering, so ground textures look blurrier in test pictures than on phones.

## Build 53 (published: Pages 1249922, artifact v56)
- p53a_light: LT53 = point lights at the roof fittings (0,0), (±7,0), y 5.05 (0.95, 16 m, decay 2, no shadows);
  visible = PREF34.gfx !== 'save' (set in api.prefs34). Workshop sun 0.9 (was 1.3). Bare concrete roughness 0.72
  (×TX.concreteR), envMapIntensity 0.8. window.__light53(), window.__gfx53(gfx) (test only: resets other prefs).
- p53b_units: 'cladWall' batch material (TX.clad map + TX.cladB bump, vertex colours); cladBox53(w,h,d) maps box faces
  2 m × 1 m per tile. unitOpp walls and the farm barn use it; unit plinth boxes '#5F5D58'; shop front canvas 1024×512
  (drawn at 2×) with lit ribs, plinth, dirt.
- p53c_face: skin24 faceX inverts the superellipse (EP51) ends.
- p53d_pad: padMat53() quilted felt for the bonnet pad (UVs = lid-space x, z). window.__b53() → { pad, clad, lights }.
- Tried and dropped: floor-only gloss (no visible change), contact-shadow decals under workshop props (too small to see
  in a 26 × 24 m room), stronger point lights.
- e2e: wslook.py (phone workshop views, fixed car MODEL/PAINT), roomlook.py (first-person room views via __dbg.fpTo),
  tools: dbgb/ + e2e/gl3d_base.html = debug page of src/base.html for before/after pictures.

## Build 54 (published: Pages d629674, artifact v57)
- p54a_pillar: zIn54(x, y, s) = distance from the centre line to the skin (paint, glass, dark) along ±z (raycast on
  SK24 meshes, cached per skin); inside54(v) = a ray from (−0.1, 1.05, 0) reaches v before the skin. A-pillar beams,
  roof lining (lower / shorter / narrower in turn until its corners are inside) and sun visors (0.29 wide at ±0.27).
  window.__pillar54() → { n, out } liner vertices (every 3rd) outside.
- p54b_seams: door shut lines 4.5 × 5 mm at z 0.9025 (shaped by shapeBody), bottom line at y 0.375 between the seams
  clipped by the arches, archTop(x) start for seams over an arch, fuel flap ring (s > 0, not open cars).
- p54c_mirror: housing rbox(0.10, 0.08, 0.16, 0.03) at x 0.67 + black frame rbox(0.02, …, 0.006) at 0.611 + glass
  0.136 × 0.05 at 0.6005. M.well metalness 0, envMapIntensity 0.3.
- p54d_rear: trim54() after conformLamps24 (not van/open/classic): line(front, y0, y1, z0, z1) = thin box seated with
  seatGeo27 (lift −0.0026); boot sides at the tail lamps' inner edge, bumper line at max(0.40, plateY − 0.085),
  reflectors, chrome lettering (canvas 512×96, plane height 0.04 / 0.036, BADGE54 texture cache, userData.badge54),
  nose bumper line under the lamps split round GR32. window.__badges54().
- e2e: b54.py (ONLY="a;b" limits models), closeup.py (views 0–10, PICK=[[view,x,y]], JS=), insidelook.py.
