# build 48 (d): share your work - on phones that can share pictures, the before & after card and photo mode get a Share
# button that hands the picture, a line about the car and a link to the game to the phone's share sheet (Messages,
# WhatsApp, Instagram...). Where sharing pictures isn't possible the button isn't shown and Save works as before.
import sys
sys.path.insert(0, 'b24')
from rep import R
f = R('bonnet-up.html'); rep = f.rep
rep("function photoBlob21(url) {", r"""/* build 48: the share sheet */
const SHARE_URL48 = (() => { try { if (/\.github\.io$/.test(location.hostname)) return location.origin + '/'; } catch (e) { /* no location */ } return 'https://ivancorreia31-sudo.github.io/'; })();
const canShare48 = () => { try { return !!(navigator.share && navigator.canShare && navigator.canShare({ files: [new File([new Blob(['x'], { type: 'image/jpeg' })], 'x.jpg', { type: 'image/jpeg' })] })); } catch (e) { return false; } };
async function share48(url, name, text) {
  if (!url) { toast('Couldn’t make the picture.'); return false; }
  try {
    await navigator.share({ files: [new File([photoBlob21(url)], name, { type: 'image/jpeg' })], text: `${text} ${SHARE_URL48}` });
    S.stats.shares48 = (S.stats.shares48 || 0) + 1; save();
    return true;
  } catch (e) {
    if (e && e.name === 'AbortError') return false;
    toast('Sharing didn’t work here. Save the picture and share it from your photos instead.'); return false;
  }
}
window.__share48 = { can: () => canShare48(), url: SHARE_URL48 };
function photoBlob21(url) {""")
# photo mode
rep("""    <div class="photo21-acts">${canSave ? '<button class="btn primary" data-a="photo-save">Save photo</button>' : ''}<button class="btn" data-a="close-modal">Close</button></div>`);""",
    """    <div class="photo21-acts">${canShare48() ? '<button class="btn primary" data-b="photo-share48">Share</button>' : ''}${canSave ? `<button class="btn${canShare48() ? '' : ' primary'}" data-a="photo-save">Save photo</button>` : ''}<button class="btn" data-a="close-modal">Close</button></div>`);""")
# the before & after card
rep("""      <div class="row ba-acts"><button class="btn primary" data-b="ba-save" data-no="${no}">Save the picture</button><button class="btn" data-a="close-modal">Close</button></div>`);""",
    """      <div class="row ba-acts">${canShare48() ? `<button class="btn primary" data-b="ba-share48" data-no="${no}">Share</button>` : ''}<button class="btn${canShare48() ? '' : ' primary'}" data-b="ba-save" data-no="${no}">Save the picture</button><button class="btn" data-a="close-modal">Close</button></div>`);""")
rep("act22('ba-save', b => baSave22(+b.dataset.no));",
    """act22('ba-save', b => baSave22(+b.dataset.no));
act22('ba-share48', async b => { const no = +b.dataset.no, R = baRec(no); const url = (BAV && BAV.no === no && BAV.share) || await baCompose22(no); share48(url, `bonnet-up-before-after-${no}.jpg`, `Before and after: I fixed up this ${R ? R.model : 'car'} in Bonnet Up 🔧 Play it free:`); });
act22('photo-share48', () => share48(PHOTO21, photoName21(), `My garage in Bonnet Up 🔧 Play it free:`));""")
# compose the picture as soon as the card opens, so Share can open the share sheet straight away (Safari only allows it
# straight after the tap)
rep("    const fr = document.querySelector('#sheet .ba22'); if (!fr) return;",
    "    if (canShare48()) baCompose22(no).then(u => { if (BAV && BAV.no === no) BAV.share = u; }, () => {});\n    const fr = document.querySelector('#sheet .ba22'); if (!fr) return;")
f.save()
print('p48d ok')
