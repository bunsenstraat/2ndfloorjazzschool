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
