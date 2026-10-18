import json, os, sys

OUT = sys.argv[1]
SITE = "https://www.eldertvanoosten.nl"
PHONE_DISPLAY = "06 434 88 440"
PHONE_TEL = "+31643488440"
WA = "https://wa.me/31643488440"
EMAIL = "eldertvanoosten@gmail.com"
STREET = "Stuyvesantstraat 10-1"
POSTCODE = "1058 AL"
CITY = "Amsterdam"

ICON = {
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 21l1.65-3.8A9 9 0 1 1 7.8 20.3L3 21"/><path d="M9 10a.5.5 0 0 0 1 0V9a.5.5 0 0 0-1 0v1a5 5 0 0 0 5 5h1a.5.5 0 0 0 0-1h-1a.5.5 0 0 0 0 1"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "play": '<svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor" aria-hidden="true"><path d="M7 4v16l13-8z"/></svg>',
}

NAV_NL = [("/", "Home"), ("/saxofoonles/", "Saxofoonles"), ("/jazzworkshops/", "Jazzworkshops"), ("/over/", "Over Eldert"), ("/contact/", "Contact")]
NAV_EN = [("/en/", "Home"), ("/en/#lessons", "Lessons"), ("/en/#workshops", "Workshops"), ("/en/#about", "About"), ("/en/#contact", "Contact")]

BUSINESS = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": SITE + "/#business",
    "name": "Eldert van Oosten — Saxofoonles & Jazzworkshops",
    "alternateName": "2nd Floor Jazz School",
    "description": "Saxofoonles voor beginners en gevorderden en jazzworkshops (improvisatie en samenspel) in een eigen studio in Amsterdam-West.",
    "url": SITE + "/",
    "image": SITE + "/assets/img/og-image.jpg",
    "logo": SITE + "/assets/img/icon-512.png",
    "telephone": PHONE_TEL,
    "email": EMAIL,
    "priceRange": "€€",
    "address": {"@type": "PostalAddress", "streetAddress": STREET, "postalCode": POSTCODE.replace(" ", ""), "addressLocality": CITY, "addressRegion": "Noord-Holland", "addressCountry": "NL"},
    "areaServed": {"@type": "City", "name": "Amsterdam"},
    "founder": {"@id": SITE + "/#eldert"},
    "knowsLanguage": ["nl", "en"],
}
PERSON = {
    "@context": "https://schema.org",
    "@type": "Person",
    "@id": SITE + "/#eldert",
    "name": "Eldert van Oosten",
    "jobTitle": ["Saxofonist", "Saxofoondocent", "Workshopleider jazz"],
    "url": SITE + "/",
    "image": SITE + "/assets/img/eldert-portret.webp",
    "alumniOf": {"@type": "CollegeOrUniversity", "name": "Sweelinck Conservatorium Amsterdam"},
    "knowsAbout": ["Saxofoon", "Jazz", "Improvisatie", "Jazzstandards", "Samenspel"],
    "worksFor": {"@id": SITE + "/#business"},
    "sameAs": ["https://soundcloud.com/eldert-637911487"],
}


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def faq_html(items):
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items) + "</div>"


def crumbs_ld(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (u, n) in enumerate(trail)]}


def page(path, title, desc, body, current, lang="nl", ld=(), alt=None):
    nav = NAV_EN if lang == "en" else NAV_NL
    items = "".join(f'<li><a href="{u}"{" aria-current=\"page\"" if u == current else ""}>{n}</a></li>' for u, n in nav)
    if lang == "en":
        items += '<li><a class="lang" href="/" hreflang="nl" lang="nl">NL</a></li>'
    else:
        items += '<li><a class="lang" href="/en/" hreflang="en" lang="en">EN</a></li>'
    hreflang = ""
    if alt:
        hreflang = (f'<link rel="alternate" hreflang="nl" href="{SITE}{alt["nl"]}">\n'
                    f'<link rel="alternate" hreflang="en" href="{SITE}{alt["en"]}">\n'
                    f'<link rel="alternate" hreflang="x-default" href="{SITE}{alt["nl"]}">\n')
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    T = (lambda nl, en: en) if lang == "en" else (lambda nl, en: nl)
    html = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}{path}">
{hreflang}<meta name="theme-color" content="#17161b">
<meta property="og:type" content="website">
<meta property="og:locale" content="{T('nl_NL', 'en_GB')}">
<meta property="og:site_name" content="Eldert van Oosten">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/instrument-serif.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/hanken-grotesk.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/style.css">
{lds}</head>
<body>
<a class="skip" href="#main">{T('Naar de inhoud', 'Skip to content')}</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{T('/', '/en/')}"><strong>Eldert van Oosten</strong><span>{T('Saxofonist &amp; docent', 'Saxophonist &amp; teacher')}</span></a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav"><span></span>Menu</button>
    <nav class="nav" id="nav" aria-label="{T('Hoofdmenu', 'Main menu')}"><ul>{items}</ul></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <strong>Eldert van Oosten</strong>
      <p>{T('Saxofoonles en jazzworkshops in Amsterdam-West. Jazzsaxofonist en docent sinds 1988.', 'Saxophone lessons and jazz workshops in Amsterdam-West. Jazz saxophonist and teacher since 1988.')}</p>
    </div>
    <div>
      <h2>{T('Pagina’s', 'Pages')}</h2>
      <ul>{"".join(f'<li><a href="{u}">{n}</a></li>' for u, n in nav[1:])}</ul>
    </div>
    <div>
      <h2>Contact</h2>
      <address>{STREET}<br>{POSTCODE} {CITY}<br>
      <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br>
      <a href="mailto:{EMAIL}">{EMAIL}</a></address>
    </div>
    <p class="legal">© <span data-year>2026</span> Eldert van Oosten · {T('Saxofoonles Amsterdam · Jazzworkshops Amsterdam', 'Saxophone lessons Amsterdam · Jazz workshops Amsterdam')}</p>
  </div>
</footer>
<nav class="actionbar" aria-label="{T('Snel contact', 'Quick contact')}">
  <a href="tel:{PHONE_TEL}">{ICON['phone']}{T('Bellen', 'Call')}</a>
  <a href="{WA}">{ICON['wa']}WhatsApp</a>
  <a href="mailto:{EMAIL}">{ICON['mail']}E-mail</a>
</nav>
<script src="/assets/js/main.js" defer></script>
</body>
</html>
"""
    fp = os.path.join(OUT, path.strip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(html)


def contact_buttons(lang="nl"):
    T = (lambda nl, en: en) if lang == "en" else (lambda nl, en: nl)
    return f"""<div class="btns">
  <a class="btn btn-primary" href="tel:{PHONE_TEL}">{ICON['phone']}{T('Bel', 'Call')} {PHONE_DISPLAY}</a>
  <a class="btn btn-ghost" href="{WA}">{ICON['wa']}WhatsApp</a>
  <a class="btn btn-ghost" href="mailto:{EMAIL}">{ICON['mail']}E-mail</a>
</div>"""


def cta(title_html, text, lang="nl"):
    T = (lambda nl, en: en) if lang == "en" else (lambda nl, en: nl)
    return f"""<section class="section-dark cta-band">
  <div class="wrap">
    <div>
      <span class="track" data-n="♪">{T('Aanmelden', 'Get in touch')}</span>
      <h2>{title_html}</h2>
      <p class="lead" style="margin-top:1rem">{text}</p>
    </div>
    <div class="btns" style="margin:0">
      <a class="btn btn-primary" href="tel:{PHONE_TEL}">{ICON['phone']}{PHONE_DISPLAY}</a>
      <a class="btn btn-ghost" href="{WA}">{ICON['wa']}WhatsApp</a>
      <a class="btn btn-ghost" href="mailto:{EMAIL}">{ICON['mail']}E-mail</a>
    </div>
  </div>
</section>"""


def img(name, alt, w, h, cls="", eager=False, sizes="(max-width: 44rem) 50vw, 25vw"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    if os.path.exists(os.path.join(OUT, f"assets/img/{name}-sm.webp")):
        return (f'<img src="/assets/img/{name}.webp" srcset="/assets/img/{name}-sm.webp 640w, /assets/img/{name}.webp 1200w" '
                f'sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" {load}{f" class={cls!r}" if cls else ""}>')
    return f'<img src="/assets/img/{name}.webp" width="{w}" height="{h}" alt="{alt}" {load}{f" class={cls!r}" if cls else ""}>'


# ---------------------------------------------------------------- HOME
home = f"""
<section class="hero">
  <div class="wrap">
    <div>
      <span class="track" data-n="A1">Amsterdam-West · sinds 1988</span>
      <h1 >Saxofoonles &amp; <em>jazzworkshops</em> in Amsterdam<span class="small">bij jazzsaxofonist Eldert van Oosten</span></h1>
      <p class="lead">Leer saxofoon spelen, ontwikkel je eigen geluid of ontdek hoe het is om te improviseren in een band. Persoonlijke lessen voor beginners en gevorderden, en wekelijkse jazzworkshops in een mooie studio in Amsterdam-West.</p>
      <div>{contact_buttons()}</div>
      <ul class="facts">
        <li><b>35+</b><span>jaar lesgeven</span></li>
        <li><b>22</b><span>jaar Muziekschool Leiden</span></li>
        <li><b>Sweelinck</b><span>Conservatorium Amsterdam</span></li>
      </ul>
    </div>
    <figure class="hero-figure">
      {img("workshop-2", "Eldert van Oosten speelt tenorsaxofoon samen met een leerling tijdens een jazzworkshop", 900, 1200, eager=True, sizes="(max-width: 52rem) 100vw, 40vw")}
      <figcaption><b>Live</b> — samen spelen op de einduitvoering van de workshop</figcaption>
    </figure>
  </div>
</section>

<section class="section-alt">
  <div class="wrap">
    <div class="section-head">
      <span class="track" data-n="A2">Wat ik aanbied</span>
      <h2>Twee kanten van <em>dezelfde plaat</em></h2>
      <p class="lead">Individuele saxofoonles voor je toon, techniek en repertoire — en groepsworkshops waarin je leert wat je alleen niet kunt leren: samenspelen.</p>
    </div>
    <div class="cards">
      <a class="card" href="/saxofoonles/">
        <span class="side">Kant A</span>
        {img("workshop-1", "Leerling speelt altsaxofoon in de tuin", 900, 1200, sizes="(max-width: 44rem) 100vw, 50vw").replace('alt=', 'style="object-position:50% 20%" alt=')}
        <div class="card-body">
          <h3>Saxofoonles</h3>
          <p>Privéles voor kinderen en volwassenen, van de allereerste toon tot jazzimprovisatie. Alt-, tenor- en sopraansaxofoon.</p>
          <span class="more">Over de lessen</span>
        </div>
      </a>
      <a class="card" href="/jazzworkshops/">
        <span class="side">Kant B</span>
        {img("workshop-9", "Groepsfoto van de deelnemers aan de jazzworkshop met hun instrumenten", 1200, 900, sizes="(max-width: 44rem) 100vw, 50vw")}
        <div class="card-body">
          <h3>Jazzworkshops</h3>
          <p>Samenspel, ritmiek en improviseren over akkoordenschema’s in een vaste groep. Piano, contrabas, drums en versterkers staan klaar.</p>
          <span class="more">Over de workshops</span>
        </div>
      </a>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <div>
      <span class="track" data-n="A3">Over Eldert</span>
      <h2>Jazzsaxofonist, docent en <em>bandcoach</em></h2>
      <p>Na mijn studie aan het Sweelinck Conservatorium (afdeling improviserend musicus) ben ik in 1988 begonnen als freelance saxofonist en docent. Ik gaf 22 jaar les en workshops aan de Muziekschool Leiden en heb sinds 2010 mijn eigen praktijk en studio in Amsterdam-West.</p>
      <p>Als saxofonist speelde ik in binnen- en buitenland, onder meer met Eye of the Hurricane, De Dijk, het Ricciotti Ensemble, de Sidewinders en het Belleville Trio. Die ervaring op het podium neem ik mee in elke les.</p>
      <p><a href="/over/">Lees meer en luister naar mijn muziek →</a></p>
    </div>
    <div>
      <blockquote class="pull">In mijn lessen staat het plezier van het muziek maken voorop.</blockquote>
      <p class="note" style="margin-top:2rem">Mijn hart ligt bij de jazz — maar ook soul, funk, pop en wereldmuziek komen in de lessen aan bod.</p>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="wrap">
    <div class="section-head">
      <span class="track" data-n="A4">In beeld</span>
      <h2>Een avond bij de <em>workshop</em></h2>
    </div>
    <div class="gallery">
      <figure>{img("workshop-3", "Contrabassist en pianist tijdens een workshopoptreden", 900, 1200)}</figure>
      <figure>{img("workshop-4", "Gitarist speelt tijdens de jazzworkshop", 900, 1200)}</figure>
      <figure>{img("workshop-5", "Pianist en contrabassiste spelen samen", 900, 1200)}</figure>
      <figure>{img("workshop-6", "Saxofoons op tafel, publiek kijkt toe", 900, 1200)}</figure>
    </div>
  </div>
</section>

{cta('Zin om te <em>beginnen?</em>', 'Bel, app of mail voor een kennismakingsles of om je aan te melden voor de jazzworkshop. Ik denk ook graag mee bij de aanschaf van een saxofoon.')}
"""
page("/", "Saxofoonles & Jazzworkshops Amsterdam | Eldert van Oosten",
     "Saxofoonles in Amsterdam voor beginners en gevorderden, en jazzworkshops in Amsterdam-West. Jazzsaxofonist en docent Eldert van Oosten, sinds 1988.",
     home, "/", ld=[BUSINESS, PERSON], alt={"nl": "/", "en": "/en/"})

# ---------------------------------------------------------------- SAXOFOONLES
sax_faq = [
    ("Moet ik al noten kunnen lezen?", "Nee. Noten lezen leer je gewoon tijdens de lessen. Veel lesboeken hebben meespeeltracks, zodat je meteen ervaart hoe het is om met een band te spelen."),
    ("Is saxofoonles ook geschikt voor kinderen?", "Ja, ik geef les aan zowel kinderen als volwassenen. De lessen worden afgestemd op leeftijd, niveau en wat je zelf graag wilt spelen."),
    ("Ik heb nog geen saxofoon. Wat nu?", "Neem gerust contact op voordat je iets koopt. Ik geef advies over het kiezen, huren of kopen van een geschikte (tweedehands) saxofoon en de juiste rietjes en mondstukken."),
    ("Hoe lang duurt een les en wat kost het?", "Lessen duren 40 minuten of een uur, los of als lessenkaart. Neem contact op voor de actuele tarieven en een kennismakingsles."),
    ("Welke saxofoons kan ik bij je leren spelen?", "Altsaxofoon, tenorsaxofoon en sopraansaxofoon. Veel beginners starten op de alt, maar dat hangt af van je smaak en de muziek die je wilt spelen."),
    ("Waar vinden de lessen plaats?", f"In mijn studio aan de {STREET} in Amsterdam-West, goed bereikbaar met openbaar vervoer en de fiets."),
]
sax = f"""
<header class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Kruimelpad"><a href="/">Home</a> / Saxofoonles</nav>
    <span class="track" data-n="A1">Privéles in Amsterdam-West</span>
    <h1>Saxofoonles in Amsterdam voor <em>beginners</em> en <em>gevorderden</em></h1>
    <p class="lead">Persoonlijke saxofoonles voor kinderen en volwassenen. Of je nu nog nooit een saxofoon hebt vastgehouden of al jaren in een big band speelt: we werken aan wat jij nodig hebt — met plezier in het spelen voorop.</p>
    {contact_buttons()}
  </div>
</header>

<section id="beginners">
  <div class="wrap split">
    <div>
      <span class="track" data-n="A2">Beginners</span>
      <h2>Altijd al saxofoon willen <em>spelen?</em></h2>
      <p>Kwam het er nooit van? Dan is dit het moment. De lessen zijn zo opgebouwd dat je binnen ongeveer tien lessen de basisprincipes van het saxofoonspelen onder de knie hebt — en meteen je eerste liedjes speelt.</p>
      <ul class="ticks">
        <li><b>Basistechniek</b> — hoe houd je een saxofoon vast, hoe blaas je erop, wat is een goede houding en hoe vorm je een toon?</li>
        <li><b>Noten lezen</b> — dat hoef je nog niet te kunnen; je leert het al spelend.</li>
        <li><b>Meespelen</b> — advies over lesboeken met meespeeltracks, zodat je hoort hoe het klinkt met een band.</li>
        <li><b>Uit je hoofd spelen</b> — de basis om later zelf melodieën en je eigen solo’s te bedenken.</li>
      </ul>
    </div>
    <figure class="portrait" style="max-width:none">
      {img("workshop-1", "Leerling speelt altsaxofoon", 900, 1200, sizes="(max-width: 52rem) 100vw, 45vw").replace('alt=', 'style="filter:none;aspect-ratio:4/5;object-fit:cover;object-position:50% 15%" alt=')}
    </figure>
  </div>
</section>

<section id="gevorderden" class="section-dark">
  <div class="wrap">
    <div class="section-head">
      <span class="track" data-n="A3">Gevorderden</span>
      <h2>Werken aan je <em>eigen geluid</em></h2>
      <p class="lead">Speel je al een aantal jaren en wil je meer weten over toon, timing en improvisatie? Speel je in een band, big band of blazerssectie? Of zoek je gewoon een nieuwe impuls?</p>
    </div>
    <div class="features" style="border-color:rgba(245,240,230,.15)">
      <div class="feature" style="border-color:rgba(245,240,230,.15)"><span class="num">i.</span><h3>Toon als expressiemiddel</h3><p>Hoe vorm je een toon en hoe werkt dat fysiek? Met een mooi, vrij geluid breng je je muzikale bedoelingen over — net als een zanger.</p></div>
      <div class="feature" style="border-color:rgba(245,240,230,.15)"><span class="num">ii.</span><h3>Klankgeoriënteerd spelen</h3><p>Leer fysieke spanningen herkennen en loslaten, zodat je vrijer en makkelijker speelt. Geïnspireerd op de Lichtenberger-methode.</p></div>
      <div class="feature" style="border-color:rgba(245,240,230,.15)"><span class="num">iii.</span><h3>Repertoire</h3><p>Jazzstandards, blues, funk of eigen stukken uit je hoofd leren — zodat je zonder papier op een jamsessie kunt meespelen.</p></div>
      <div class="feature" style="border-color:rgba(245,240,230,.15)"><span class="num">iv.</span><h3>Theorie &amp; improvisatie</h3><p>Toonladders, akkoorden, akkoordenschema’s en vorm: zo hoor je meer structuur in muziek en improviseer je met meer vrijheid.</p></div>
      <div class="feature" style="border-color:rgba(245,240,230,.15)"><span class="num">v.</span><h3>Bandcoaching</h3><p>Al jaren zet ik leerlingenbands op en begeleid ik ze. Ook saxofoonsecties van big bands kunnen bij mij terecht voor advies.</p></div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="wrap split">
    <div>
      <span class="track" data-n="A4">Praktisch</span>
      <h2>Hoe de lessen <em>werken</em></h2>
      <ul class="ticks">
        <li>Lessen van 40 minuten of een uur, los of met een lessenkaart</li>
        <li>Voor kinderen en volwassenen, alle niveaus</li>
        <li>Alt-, tenor- en sopraansaxofoon</li>
        <li>In mijn studio in Amsterdam-West</li>
        <li>Advies bij het kopen of huren van een saxofoon</li>
      </ul>
      <p class="note">Tarieven en beschikbaarheid? Neem contact op — dan plannen we meteen een kennismakingsles.</p>
    </div>
    <div>
      <span class="track" data-n="A5">Veelgestelde vragen</span>
      {faq_html(sax_faq)}
    </div>
  </div>
</section>

{cta('Plan een <em>kennismakingsles</em>', 'Vertel me wat je wilt leren, dan kijken we samen wat bij je past.')}
"""
page("/saxofoonles/", "Saxofoonles Amsterdam | Eldert van Oosten",
     "Saxofoonles in Amsterdam-West voor kinderen en volwassenen. Leer saxofoon spelen of werk aan toon, improvisatie en repertoire bij jazzsaxofonist Eldert van Oosten.",
     sax, "/saxofoonles/", ld=[BUSINESS, faq_ld(sax_faq), crumbs_ld([("/", "Home"), ("/saxofoonles/", "Saxofoonles")]),
     {"@context": "https://schema.org", "@type": "Service", "serviceType": "Saxofoonles", "name": "Saxofoonles Amsterdam", "provider": {"@id": SITE + "/#business"}, "areaServed": "Amsterdam", "audience": {"@type": "Audience", "audienceType": "Beginners en gevorderden, kinderen en volwassenen"}}],
     alt={"nl": "/saxofoonles/", "en": "/en/"})

# ---------------------------------------------------------------- JAZZWORKSHOPS
ws_faq = [
    ("Voor wie is de jazzworkshop?", "Voor muzikanten die al een tijdje spelen en zich willen ontwikkelen in improvisatie en samenspel. Je hoeft geen jazzervaring te hebben: er zijn groepen voor spelers die net beginnen met improviseren en voor meer ervaren muzikanten."),
    ("Welke instrumenten kunnen meedoen?", "Blazers (saxofoon, trompet, trombone, klarinet, fluit), piano en toetsen, gitaar, contrabas en basgitaar, drums en zang. Piano, contrabas, drumstel en versterkers zijn in de studio aanwezig."),
    ("Wat speel je in de workshop?", "Jazzstandards, blues, latin, eigen stukken en muziek uit het wereldrepertoire. We werken aan een eigen repertoire als groep."),
    ("Treden we ook op?", "Ja, optreden is een belangrijk onderdeel van de cursus. De groepen sluiten af met een uitvoering, onder meer op Buurtboerderij Ons Genoegen."),
    ("Hoe meld ik me aan?", "Bel, app of mail me. We bespreken je ervaring en ik kijk in welke groep je het beste past. Er is altijd plek voor nieuwe deelnemers."),
]
ws = f"""
<header class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Kruimelpad"><a href="/">Home</a> / Jazzworkshops</nav>
    <span class="track" data-n="B1">2nd Floor Jazz School</span>
    <h1>Jazzworkshops in Amsterdam: leer <em>improviseren</em> en samenspelen</h1>
    <p class="lead">In een mooie studio in Amsterdam-West geef ik jazzworkshops aan muzikanten die zich verder willen ontwikkelen op het gebied van improvisatie. Wil je meer weten over samenspel, ritmiek en improviseren over akkoordenschema’s? Meld je dan aan.</p>
    {contact_buttons()}
  </div>
</header>

<section>
  <div class="wrap split">
    <div>
      <span class="track" data-n="B2">De workshop</span>
      <h2>Samen spelen, samen <em>leren</em></h2>
      <p>Na 22 jaar lesgeven aan de Muziekschool Leiden begon ik in 2010 mijn eigen praktijk. De jazzworkshops zijn het hart ervan: vaste groepen van een handvol muzikanten die samen werken aan een repertoire van jazzstandards, eigen stukken en muziek uit het wereldrepertoire.</p>
      <ul class="ticks">
        <li><b>Samenspel</b> — luisteren, reageren, begeleiden en de ruimte geven</li>
        <li><b>Ritmiek</b> — timing, swing, latin en groove</li>
        <li><b>Improvisatie</b> — soleren over akkoordenschema’s en vormen</li>
        <li><b>Theorie</b> — precies genoeg om te begrijpen wat je hoort</li>
        <li><b>Uit het hoofd spelen</b> — loskomen van het papier</li>
      </ul>
    </div>
    <figure class="portrait" style="max-width:none">
      {img("studio-collage", "De studio van 2nd Floor Jazz School met saxofoon, piano, contrabas en drums", 1000, 1333, sizes="(max-width: 52rem) 100vw, 45vw").replace('alt=', 'style="filter:none" alt=')}
      <figcaption>De studio: piano, contrabas, drumstel en versterkers staan klaar.</figcaption>
    </figure>
  </div>
</section>

<section class="section-alt">
  <div class="wrap">
    <div class="section-head">
      <span class="track" data-n="B3">Optreden</span>
      <h2>Van de studio naar het <em>podium</em></h2>
      <p class="lead">Optreden is een belangrijk onderdeel van de workshops. Elk seizoen sluiten we af met een einduitvoering, onder andere op Buurtboerderij ‘Ons Genoegen’.</p>
    </div>
    <div class="gallery">
      <figure class="wide">{img("workshop-9", "Deelnemers van de jazzworkshop na de einduitvoering", 1200, 900, sizes="(max-width: 44rem) 100vw, 50vw")}</figure>
      <figure>{img("workshop-8", "Contrabassist Harm Wijntjes bij de einduitvoering", 900, 1200)}</figure>
      <figure>{img("workshop-7", "Pianist, contrabassiste en publiek bij het optreden", 900, 1200)}</figure>
      <figure>{img("workshop-3", "Contrabas en piano tijdens het optreden", 900, 1200)}</figure>
      <figure>{img("workshop-4", "Gitarist van de workshopgroep", 900, 1200)}</figure>
      <figure>{img("workshop-5", "Piano en contrabas op de buurtboerderij", 900, 1200)}</figure>
      <figure>{img("workshop-2", "Twee saxofonisten spelen samen", 900, 1200)}</figure>
    </div>
  </div>
</section>

<section>
  <div class="wrap split">
    <div>
      <span class="track" data-n="B4">Veelgestelde vragen</span>
      <h2>Goed om te <em>weten</em></h2>
      <p>Twijfel je of de workshop bij je past? Bel of app gerust — dan kijken we samen naar je niveau en de mogelijkheden.</p>
    </div>
    <div>{faq_html(ws_faq)}</div>
  </div>
</section>

{cta('Speel mee in een <em>jazzgroep</em>', 'Er is altijd ruimte voor nieuwe deelnemers. Laat weten wat je speelt en hoe lang al — dan zoek ik de groep die bij je past.')}
"""
page("/jazzworkshops/", "Jazzworkshop Amsterdam | Improvisatie & samenspel",
     "Jazzworkshops in Amsterdam-West: leer improviseren en samenspelen in een vaste groep. Piano, contrabas en drums aanwezig. Voor alle instrumenten.",
     ws, "/jazzworkshops/", ld=[BUSINESS, faq_ld(ws_faq), crumbs_ld([("/", "Home"), ("/jazzworkshops/", "Jazzworkshops")]),
     {"@context": "https://schema.org", "@type": "Course", "name": "Jazzworkshop: improvisatie en samenspel", "description": "Wekelijkse jazzworkshop in Amsterdam-West voor alle instrumenten: samenspel, ritmiek, improvisatie over akkoordenschema’s en optreden.", "inLanguage": "nl", "provider": {"@type": "Organization", "name": "2nd Floor Jazz School — Eldert van Oosten", "url": SITE + "/"}}],
     alt={"nl": "/jazzworkshops/", "en": "/en/"})

# ---------------------------------------------------------------- OVER
tracks = [("Chucho", "https://soundcloud.com/eldert-637911487/chucho"),
          ("While My Lady Sleeps", "https://soundcloud.com/eldert-637911487/whilemyladysleeps"),
          ("Strangers in the Night", "https://soundcloud.com/eldert-637911487/strangers-in-the-night")]
track_html = "".join(f'<li><button type="button" data-sc="{u}" aria-expanded="false"><span class="no">0{i+1}</span><span class="title">{t}</span><span class="play">{ICON["play"]}<span class="skip">Afspelen</span></span></button></li>' for i, (t, u) in enumerate(tracks))
over = f"""
<header class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Kruimelpad"><a href="/">Home</a> / Over Eldert</nav>
    <span class="track" data-n="C1">Biografie</span>
    <h1>Eldert van Oosten, <em>jazzsaxofonist</em> uit Amsterdam</h1>
  </div>
</header>

<section>
  <div class="wrap split">
    <figure class="portrait">
      <img src="/assets/img/eldert-portret.webp" width="240" height="240" alt="Portret van Eldert van Oosten met tenorsaxofoon" style="width:100%">
      <figcaption>Eldert van Oosten op tenorsaxofoon</figcaption>
    </figure>
    <div>
      <p class="lead">Geboren en opgegroeid in Amsterdam. Op mijn twaalfde begon ik op de klarinet, op mijn vijftiende kreeg ik mijn eerste altsaxofoon.</p>
      <p>Toen ik zestien was en saxofonisten als Ben Webster en Sonny Rollins hoorde, wist ik het zeker: ik wilde saxofonist worden. Ik kocht een tenorsaxofoon en ging in 1981 naar het Sweelinck Conservatorium in Amsterdam, waar ik saxofoon studeerde aan de afdeling improviserend musicus. Daar leerde ik veel muzikanten kennen met wie ik nu nog steeds speel.</p>
      <p>Na mijn afstuderen in 1988 werkte ik als freelance saxofonist in heel verschillende stijlen — en die afwisseling is me altijd goed bevallen. Big bands, blues met P.B. and the Nighttrain, pop met De Dijk, klassiek met het Ricciotti Ensemble, jazz met het Amstel Octet en funk met Fresh Cream.</p>
      <p>Naast het spelen gaf ik 22 jaar les en workshops aan de Muziekschool Leiden. Sinds 2010 heb ik mijn eigen praktijk en studio in Amsterdam-West, waar ik <a href="/saxofoonles/">saxofoonles</a> geef en de <a href="/jazzworkshops/">jazzworkshops</a> van de 2nd Floor Jazz School leid.</p>
      <p>En als ik niet speel of lesgeef? Dan ben ik graag op het water of op reis.</p>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="wrap">
    <div class="section-head">
      <span class="track" data-n="C2">Gespeeld met o.a.</span>
      <p class="namelist"><span>Eye of the Hurricane</span> <span>De Dijk</span> <span>Ricciotti Ensemble</span> <span>Amstel Octet</span> <span>P.B. and the Nighttrain</span> <span>Fresh Cream</span> <span>The Sidewinders</span> <span>Belleville Trio</span> <span>Drie Hoog Achter</span></p>
    </div>
    <div class="bands">
      <article class="band">
        <img src="/assets/img/sidewinders.webp" width="900" height="600" alt="The Sidewinders op het strand, Eldert met saxofoon" loading="lazy" decoding="async">
        <h3>The Sidewinders</h3>
        <p>Swingende band met blazers — <a href="https://cavherk.wixsite.com/thesidewinders" rel="noopener">website</a>.</p>
      </article>
      <article class="band">
        <img src="/assets/img/belleville.webp" width="315" height="243" alt="Het Belleville Trio met gasten" loading="lazy" decoding="async">
        <h3>Belleville Trio</h3>
        <p>Jazz met een Parijse knipoog — <a href="http://bellevillejazz.nl/" rel="noopener">website</a>.</p>
      </article>
    </div>
  </div>
</section>

<section class="section-dark" id="muziek">
  <div class="wrap split">
    <div>
      <span class="track" data-n="C3">Muziek</span>
      <h2>Luister <em>mee</em></h2>
      <p>Mijn hart ligt bij de jazz, maar in soul en wereldmuziek kan ik mijn muzikale ei ook goed kwijt. Een paar opnames:</p>
      <p style="font-size:.85rem">De speler wordt pas geladen als je op een nummer klikt.</p>
    </div>
    <ol class="tracks">{track_html}</ol>
  </div>
</section>

{cta('Boekingen &amp; <em>lessen</em>', 'Voor optredens, saxofoonles of de jazzworkshop: neem contact op.')}
"""
page("/over/", "Eldert van Oosten | Jazzsaxofonist Amsterdam",
     "Jazzsaxofonist Eldert van Oosten (Sweelinck Conservatorium) speelde met o.a. De Dijk, Eye of the Hurricane en het Ricciotti Ensemble. Biografie en muziek.",
     over, "/over/", ld=[PERSON, crumbs_ld([("/", "Home"), ("/over/", "Over Eldert")])], alt={"nl": "/over/", "en": "/en/"})

# ---------------------------------------------------------------- CONTACT
contact = f"""
<header class="page-head">
  <div class="wrap">
    <nav class="crumbs" aria-label="Kruimelpad"><a href="/">Home</a> / Contact</nav>
    <span class="track" data-n="D1">Contact</span>
    <h1>Neem <em>contact</em> op</h1>
    <p class="lead">Voor saxofoonles, de jazzworkshop, advies bij het kopen van een saxofoon of het boeken van een band. Bellen of appen gaat het snelst.</p>
  </div>
</header>
<section>
  <div class="wrap">
    <div class="contact-grid">
      <a class="contact-tile" href="tel:{PHONE_TEL}"><small>Bellen</small><b>{PHONE_DISPLAY}</b><span>Ook voor een kennismakingsles</span></a>
      <a class="contact-tile" href="{WA}"><small>WhatsApp</small><b>Stuur een appje</b><span>Ik reageer meestal dezelfde dag</span></a>
      <a class="contact-tile" href="mailto:{EMAIL}?subject=Saxofoonles%20%2F%20jazzworkshop"><small>E-mail</small><b>{EMAIL}</b><span>Vertel kort wat je speelt en zoekt</span></a>
      <a class="contact-tile" href="https://www.google.com/maps/search/?api=1&amp;query=Stuyvesantstraat+10+Amsterdam" rel="noopener"><small>Studio</small><b>{STREET}</b><span>{POSTCODE} {CITY} (West) · route →</span></a>
    </div>
  </div>
</section>
<section class="section-alt">
  <div class="wrap split">
    <div>
      <span class="track" data-n="D2">Handig om te vermelden</span>
      <ul class="ticks">
        <li>Welk instrument je speelt (en welke saxofoon)</li>
        <li>Hoe lang je al speelt — of dat je wilt beginnen</li>
        <li>Wat je graag wilt leren of spelen</li>
        <li>Op welke dagen je meestal kunt</li>
      </ul>
    </div>
    <div>
      <figure class="portrait" style="max-width:none">{img("2nd-floor-folder", "Folder van 2nd Floor Jazz School — jazzworkshops", 500, 1090).replace('alt=', 'style="filter:none;max-width:15rem" alt=')}</figure>
    </div>
  </div>
</section>
"""
page("/contact/", "Contact | Saxofoonles Amsterdam – Eldert van Oosten",
     f"Bel {PHONE_DISPLAY}, app of mail voor saxofoonles of de jazzworkshop in Amsterdam-West. Studio aan de {STREET}, {CITY}.",
     contact, "/contact/", ld=[BUSINESS, crumbs_ld([("/", "Home"), ("/contact/", "Contact")])], alt={"nl": "/contact/", "en": "/en/#contact"})

# ---------------------------------------------------------------- ENGLISH
en = f"""
<section class="hero">
  <div class="wrap">
    <div>
      <span class="track" data-n="A1">Amsterdam-West · since 1988</span>
      <h1 >Saxophone lessons &amp; <em>jazz workshops</em> in Amsterdam<span class="small">with jazz saxophonist Eldert van Oosten</span></h1>
      <p class="lead">Private saxophone lessons in English or Dutch for complete beginners and experienced players, and weekly jazz workshops where you learn to improvise and play together in a band.</p>
      <div>{contact_buttons("en")}</div>
    </div>
    <figure class="hero-figure">
      {img("workshop-2", "Eldert van Oosten playing tenor saxophone with a student", 900, 1200, eager=True, sizes="(max-width: 52rem) 100vw, 40vw")}
      <figcaption><b>Live</b> — playing together at the end-of-season concert</figcaption>
    </figure>
  </div>
</section>
<section class="section-alt" id="lessons">
  <div class="wrap split">
    <div>
      <span class="track" data-n="A2">Saxophone lessons</span>
      <h2>From your first note to your <em>own sound</em></h2>
      <p>Lessons for children and adults on alto, tenor and soprano sax. Beginners learn the basics — holding the horn, breathing, tone, reading music — in about ten lessons. Experienced players work on tone, timing, repertoire, theory and improvisation.</p>
      <ul class="ticks">
        <li>40- or 60-minute private lessons</li>
        <li>Lessons in English or Dutch</li>
        <li>Advice on buying or renting a saxophone</li>
        <li>Coaching for bands and big band sax sections</li>
      </ul>
    </div>
    <div  id="workshops">
      <span class="track" data-n="A3">Jazz workshops</span>
      <h2>Learn to <em>play together</em></h2>
      <p>The 2nd Floor Jazz School runs small, regular groups working on jazz standards, original tunes and world music: ensemble playing, rhythm and improvising over chord changes. Piano, double bass, drums and amps are in the studio. Every season ends with a concert.</p>
      <p>Open to all instruments and levels — including players new to jazz.</p>
    </div>
  </div>
</section>
<section id="about">
  <div class="wrap split">
    <figure class="portrait"><img src="/assets/img/eldert-portret.webp" width="240" height="240" alt="Portrait of Eldert van Oosten with tenor saxophone" style="width:100%" loading="lazy"></figure>
    <div>
      <span class="track" data-n="A4">About</span>
      <h2>Eldert van <em>Oosten</em></h2>
      <p>Amsterdam-born saxophonist, trained at the Sweelinck Conservatory (improvising musician programme, graduated 1988). Taught at the Leiden music school for 22 years before opening his own studio in Amsterdam-West in 2010. Has played with Eye of the Hurricane, De Dijk, the Ricciotti Ensemble, the Sidewinders and the Belleville Trio, among many others.</p>
      <p><a href="/over/" hreflang="nl">Full biography and music (Dutch) →</a></p>
    </div>
  </div>
</section>
<div id="contact">
{cta('Book a <em>first lesson</em>', f'Call, WhatsApp or email. Studio: {STREET}, {POSTCODE} {CITY}.', "en")}
</div>
"""
page("/en/", "Saxophone Lessons Amsterdam | Eldert van Oosten",
     "Saxophone lessons in English in Amsterdam for beginners and advanced players, plus jazz improvisation workshops with saxophonist Eldert van Oosten.",
     en, "/en/", lang="en", ld=[BUSINESS, PERSON], alt={"nl": "/", "en": "/en/"})

# ---------------------------------------------------------------- 404
nf = f"""
<header class="page-head" style="border:0;padding-bottom:6rem">
  <div class="wrap">
    <span class="track" data-n="404">Pagina niet gevonden</span>
    <h1>Deze noot staat <em>niet</em> in de partij</h1>
    <p class="lead">De pagina die je zoekt bestaat niet (meer).</p>
    <div class="btns"><a class="btn btn-primary" href="/">Naar home</a><a class="btn btn-ghost" href="/saxofoonles/">Saxofoonles</a><a class="btn btn-ghost" href="/jazzworkshops/">Jazzworkshops</a></div>
  </div>
</header>"""
page("/404.html", "Pagina niet gevonden | Eldert van Oosten", "Deze pagina bestaat niet.", nf, "")
html404 = open(os.path.join(OUT, "404.html")).read().replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
open(os.path.join(OUT, "404.html"), "w").write(html404)

# ---------------------------------------------------------------- meta files
urls = [("/", "1.0"), ("/saxofoonles/", "0.9"), ("/jazzworkshops/", "0.9"), ("/over/", "0.6"), ("/contact/", "0.7"), ("/en/", "0.6")]
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>2026-10-17</lastmod><priority>{p}</priority></url>\n" for u, p in urls) + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
open(os.path.join(OUT, "site.webmanifest"), "w").write(json.dumps({
    "name": "Eldert van Oosten — Saxofoonles & Jazzworkshops", "short_name": "Eldert", "start_url": "/",
    "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}],
    "theme_color": "#17161b", "background_color": "#f5f0e6", "display": "browser"}, indent=2))
print("built")
