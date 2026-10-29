// Mobile nav
const toggle = document.querySelector('.nav-toggle');
const nav = document.getElementById('nav');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', open);
  });
}

// SoundCloud: load the player only when a track is clicked (faster, no third-party cookies up front)
document.querySelectorAll('[data-sc]').forEach((btn) => {
  btn.addEventListener('click', () => {
    const li = btn.closest('li');
    if (li.querySelector('iframe')) return;
    const iframe = document.createElement('iframe');
    iframe.title = btn.querySelector('.title').textContent + ' — SoundCloud';
    iframe.allow = 'autoplay';
    iframe.src = 'https://w.soundcloud.com/player/?url=' + encodeURIComponent(btn.dataset.sc) +
      '&color=%23b0791f&auto_play=true&hide_related=true&show_comments=false&show_user=true&show_reposts=false&visual=false';
    li.appendChild(iframe);
    btn.setAttribute('aria-expanded', 'true');
  });
});

document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });

// Sharing: on phones the "Delen…" button opens the system share sheet with the poster attached
// (Facebook, WhatsApp, Instagram…). It stays hidden where the browser can't do that.
document.querySelectorAll('[data-share-url]').forEach(async (btn) => {
  if (!navigator.share) return;
  btn.hidden = false;
  btn.addEventListener('click', async () => {
    const { shareUrl: url, shareText: text, shareImage: image } = btn.dataset;
    try {
      if (image && navigator.canShare) {
        const blob = await (await fetch(image)).blob();
        const file = new File([blob], image.split('/').pop(), { type: blob.type || 'image/jpeg' });
        if (navigator.canShare({ files: [file] })) {
          await navigator.share({ files: [file], text: `${text}\n${url}` });
          return;
        }
      }
      await navigator.share({ title: text, text, url });
    } catch (e) { /* cancelled */ }
  });
});

document.querySelectorAll('[data-copy]').forEach((btn) => {
  btn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(btn.dataset.copy);
      const label = btn.lastChild.textContent;
      btn.lastChild.textContent = 'Gekopieerd ✓';
      setTimeout(() => { btn.lastChild.textContent = label; }, 2000);
    } catch (e) { prompt('Kopieer deze link:', btn.dataset.copy); }
  });
});
