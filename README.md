# eldertvanoosten.nl

Nieuwe statische website voor Eldert van Oosten — saxofoonles & jazzworkshops in Amsterdam.
Tekst en foto's zijn teruggehaald uit het Internet Archive (versies 2009–2025).

## Structuur

| URL | Doel / zoekterm |
|---|---|
| `/` | Home — "saxofoonles Amsterdam", "jazzworkshop Amsterdam" |
| `/saxofoonles/` | Saxofoonles beginners & gevorderden + FAQ |
| `/jazzworkshops/` | Jazzworkshops (2nd Floor Jazz School) + FAQ |
| `/over/` | Biografie, bands, muziek (SoundCloud) |
| `/contact/` | Bellen, WhatsApp, e-mail, route |
| `/en/` | Engelse pagina — "saxophone lessons Amsterdam" |

Geen framework, geen build-stap nodig om te hosten: upload de map zoals hij is.
Fonts zijn lokaal (geen Google Fonts-verzoeken, AVG-vriendelijk). SoundCloud laadt pas na een klik.

## Aanpassen

De pagina's worden gegenereerd door `build.py` (houdt header, footer en SEO-tags gelijk):

```
python3 build.py .
```

Kleine tekstwijzigingen kunnen ook direct in de HTML, maar worden dan overschreven bij een volgende build.

## Live zetten — checklist

1. Upload naar hosting (Netlify, Cloudflare Pages, of Apache-hosting). `_redirects` (Netlify/Cloudflare) en `.htaccess` (Apache) sturen oude URL's door.
2. Controleer dat het domein op `https://www.eldertvanoosten.nl` uitkomt (canonical-URL's gaan daarvan uit).
3. Google Search Console: domein verifiëren en `sitemap.xml` indienen.
4. **Google Bedrijfsprofiel** aanmaken/claimen ("Saxofoonles", Amsterdam) — dit is de grootste winst voor lokale zoekresultaten. Vraag leerlingen om reviews.
5. Niet mee-uploaden is optioneel: `README.md`, `build.py`, `.claude/`.
