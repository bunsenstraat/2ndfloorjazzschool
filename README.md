# 2ndfloorjazzschool.nl

Statische website van de **2nd Floor Jazz School** — jazzworkshops en saxofoonles voor volwassenen in Amsterdam-West, onder leiding van jazzsaxofonist Eldert van Oosten.
Tekst en foto's zijn deels teruggehaald uit het Internet Archive (eldertvanoosten.nl, versies 2009–2025).

## Structuur

| URL | Doel / zoekterm |
|---|---|
| `/` | Home — "jazzworkshop Amsterdam" (studio met contrabas, drums, piano, versterkers) |
| `/jazzworkshops/` | Jazzworkshops + FAQ (enige jazzervaring vereist) |
| `/saxofoonles/` | Saxofoonles voor volwassenen + FAQ |
| `/docent/` | Eldert van Oosten: biografie, bands, muziek (SoundCloud) |
| `/contact/` | Bellen, WhatsApp, e-mail, route |
| `/en/` | Engelse pagina — "jazz workshops Amsterdam" |

Geen framework, geen build-stap nodig om te hosten: upload de map zoals hij is.
Fonts zijn lokaal (geen Google Fonts-verzoeken, AVG-vriendelijk). SoundCloud laadt pas na een klik.

## Aanpassen

De pagina's worden gegenereerd door `build.py` (houdt header, footer en SEO-tags gelijk):

```
python3 build.py .
```

- Domein, telefoon, e-mail en adres staan bovenaan `build.py`.
- Na een wijziging in `assets/css/style.css` of `assets/js/main.js`: verhoog `ASSET_V` in `build.py`, zodat browsers de nieuwe versie laden.
- Kleine tekstwijzigingen kunnen ook direct in de HTML, maar worden dan overschreven bij een volgende build.

## Lokaal bekijken

```
python3 -m http.server 8080
```

## Live zetten — checklist

1. Gehost op **GitHub Pages** vanuit de `main`-branch (root). Elke push naar `main` zet de site automatisch live.
   `CNAME` bevat het domein, `.nojekyll` zorgt dat GitHub de bestanden ongewijzigd serveert.
   DNS bij de registrar: `www` → CNAME `bunsenstraat.github.io`; het kale domein → A-records `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   (`_redirects` en `.htaccess` worden door GitHub Pages genegeerd; ze werken alleen bij Netlify/Cloudflare Pages of Apache.)
2. Laat `2ndfloorjazzschool.nl` uitkomen op `https://www.2ndfloorjazzschool.nl` (canonical-URL's gaan daarvan uit; anders `SITE` in `build.py` aanpassen).
3. Laat **eldertvanoosten.nl** met een 301-redirect naar het nieuwe domein wijzen (met behoud van het pad), zodat bestaande Google-posities meegaan.
4. Google Search Console: nieuw domein verifiëren, `sitemap.xml` indienen, en voor het oude domein de "Adreswijziging"-tool gebruiken.
5. **Google Bedrijfsprofiel** op naam "2nd Floor Jazz School", categorie *Muziekschool*. Vraag deelnemers om reviews.
6. Optioneel niet uploaden: `README.md`, `build.py`, `.claude/`.
