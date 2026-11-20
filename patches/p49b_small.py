# build 49 (b): small phones. On a short screen the welcome card and the step card are taller than the space they get,
# and their buttons ("Let's go", "Test drive") sat below the fold until you scrolled the card. The button row now stays
# pinned to the bottom of the card while the words scroll above it.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
# the first-run welcome: the small print goes above the buttons, so the buttons are the card's last row
rep("""    <div class="row"><button class="btn primary" data-a="dismiss-intro">Let’s go</button><button class="btn" data-a="story-start">Play the story</button></div>
    <p class="muted">Everything else is explained when you reach it. The full rules are under <button class="linkish" data-a="intro">How to play</button>.</p>""",
    """    <p class="muted">Everything else is explained when you reach it. The full rules are under <button class="linkish" data-a="intro">How to play</button>.</p>
    <div class="row"><button class="btn primary" data-a="dismiss-intro">Let’s go</button><button class="btn" data-a="story-start">Play the story</button></div>""")
rep("""    <div class="row"><button class="btn primary" data-a="story-start">Play the story</button><button class="btn" data-a="dismiss-intro">Let’s go</button></div>
    <p class="muted">The story has six chapters with Uncle Ray, or just get stuck in.</p>""",
    """    <p class="muted">The story has six chapters with Uncle Ray, or just get stuck in.</p>
    <div class="row"><button class="btn primary" data-a="story-start">Play the story</button><button class="btn" data-a="dismiss-intro">Let’s go</button></div>""")
rep(".ov-card .btn{justify-self:start}",
    ".ov-card .btn{justify-self:start}\n.ov-card > .row:last-child{position:sticky;bottom:-18px;z-index:1;margin:0 -18px -18px;padding:10px 18px 16px;background:var(--panel);box-shadow:0 -1px 0 var(--line)}\n.step .st-acts.st-under{position:sticky;bottom:-12px;z-index:1;background:var(--panel);margin-bottom:-12px;padding:8px 0 12px}")
f.save()
print('p49b ok')
