// Shared setup for the flyer / post templates: URL options, contact line and the QR code on print flyers.
const q = new URLSearchParams(location.search);
const get = (k, d) => q.get(k) ?? d;
const lines = (s) => s.split('|').join('<br>');
const colour = (c) => (c.startsWith('#') ? c : `var(--${c})`);
const FORMAT = get('format', 'square');

document.documentElement.classList.add(FORMAT);
if (q.has('export')) document.documentElement.classList.add('export');
if (q.has('nograin')) document.documentElement.classList.add('nograin');

function fill(id, html) {
  const el = document.getElementById(id);
  if (el) el.innerHTML = html;
}

fill('contact', lines(get('contact', '2ndfloorjazzschool.nl|06 434 88 440')));

// QR code (print only): points to the site, tagged so visits from paper show up separately.
// ?qr=none hides it, ?qr=<url> overrides the link, ?campaign=<name> tags it.
function addQr() {
  const box = document.getElementById('qr');
  if (!box) return;
  const target = get('qr', '');
  if (FORMAT !== 'a4' || target === 'none') { box.remove(); return; }
  let url = target;
  if (!url) {
    const page = get('page', '/jazzworkshops/');
    const tags = new URLSearchParams({ utm_source: 'flyer', utm_medium: 'print' });
    if (q.get('campaign')) tags.set('utm_campaign', q.get('campaign'));
    if (q.get('name')) tags.set('utm_content', q.get('name'));
    url = `https://www.2ndfloorjazzschool.nl${page}?${tags}`;
  }
  const code = qrcode(0, 'M');
  code.addData(url);
  code.make();
  box.querySelector('.code').innerHTML = code.createSvgTag({ cellSize: 4, margin: 0, scalable: true });
  box.querySelector('.code svg').removeAttribute('width');
  box.querySelector('.code svg').removeAttribute('height');
  fill('qr-label', lines(get('qrlabel', 'Scan voor|meer info')));
}
addQr();
