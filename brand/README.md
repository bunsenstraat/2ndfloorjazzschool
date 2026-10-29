# Huisstijl 2nd Floor Jazz School

## Logo
`2nd floor jazz school` in kleine, vette, smalle letters (Archivo, breedte 62, gewicht 900), met **jazz** in oranje.

| Bestand | Gebruik |
|---|---|
| `logo/logo.svg` / `png/logo.png` | Standaard, op lichte achtergrond |
| `logo/logo-inverse.svg` / `png/logo-inverse.png` | Op donkere achtergrond |
| `logo/logo-ink.svg`, `logo/logo-white.svg` | Eén kleur (stempel, drukwerk, op kleur) |
| `logo/logo-stacked*.svg` / `png/` | Gestapeld, voor vierkante plekken |
| `png/profile-1080.png`, `png/profile-dark-1080.png` | Profielfoto Instagram / Facebook / WhatsApp |
| `logo/icon.svg` / `png/icon-512.png` | App-icoon / favicon |

De SVG's zijn omgezet naar vormen, dus er is geen lettertype nodig om ze te tonen.
Opnieuw genereren: `python make_logo.py` (vereist `fonttools`, `brotli`, `uharfbuzz`).

## Kleuren
| | Hex |
|---|---|
| Inkt | `#141317` |
| Papier | `#efe6d2` |
| Oranje (logo) | `#de6b1f` |
| Mosterdgeel | `#e6b532` |
| Blauw | `#2a5d93` |
| Groen | `#4f7a3f` |

## Lettertypes
- **Archivo** (Black, Extra Condensed): koppen en logo
- **Instrument Serif** (cursief): accenten
- **Hanken Grotesk**: kleine tekst

## Flyers & posts
Templates in `templates/` (in de geest van Reid Miles' Blue Note-hoezen):

- `ritme.html`: balken + twee regels tekst
- `gebroken-woord.html`: één woord over verspringende regels
- `foto.html`: een foto uit de site met grote letters. `layout=crop` (foto boven, kleurvlak met tekst onder) of `layout=letters` (foto ín reuzenletters, bijv. `big=Jazz`). Kies de foto met `photo=studio-drumkit` (bestandsnaam in `assets/img/` zonder `.webp`) en de uitsnede met `pos=50% 30%`.

Open een template in de browser en pas de tekst aan via de adresbalk (uitleg staat linksonder op de pagina).
Exporteren naar een vierkante post (1080×1080 PNG) en een A4-flyer (PDF + PNG):

```
./export.sh ritme samen-spelen
./export.sh gebroken-woord improviseren
./export.sh gebroken-woord samenspel 'w=Sa-men-spel&side=luisteren|en|reageren'
./export.sh ritme open-avond 't1=Open&t2=avond&bg=orange&info=Kom|kennismaken'
```

Bestanden komen in `exports/` (niet in git).

## Campagnes: alles in één keer
Zet een hele campagne in een lijst (`campaigns/<naam>.csv`, te bewerken in Excel of Numbers) met één regel per poster:

| Kolom | Betekenis |
|---|---|
| `name` | bestandsnaam, bijv. `improviseren` |
| `template` | `ritme` of `gebroken-woord` |
| `formats` | optioneel: `post`, `a4` of beide (standaard beide) |
| overige kolommen | template-opties: `t1`, `t2`, `w`, `side`, `info`, `bg`, `accent`, `size`, `bars`, `page`, `qrlabel`, `photo`, `layout`, `pos`, `serif`, `big`, `t2color`; leeg = standaard |
| `share_head`, `share_sub`, `share_facts`, `share_gear` | optioneel: andere tekst in het paneel van de Facebook-afbeelding (standaard: de workshopgegevens). Gebruikt voor de saxofoonles-poster. |

Gebruik `|` voor een nieuwe regel in een tekst. Daarna:

```
python3 campaign.py campaigns/seizoen-2026-27.csv            # alles
python3 campaign.py campaigns/seizoen-2026-27.csv walkin     # alleen regels met "walkin" in de naam
```

Per poster: `exports/<campagne>/<naam>-post.png` (1080×1080), `<naam>-a4.png` en `<naam>-a4.pdf`.

**QR-code:** elke A4-flyer krijgt rechtsonder een QR-code naar de site (standaard `/jazzworkshops/`, of de pagina in kolom `page`).
De link bevat de campagne- en posternaam (`utm_campaign`, `utm_content`), zodat je in de statistieken kunt zien welke flyer bezoekers oplevert.
`qr=none` laat de code weg.

## Posters op de website zetten (om te delen)
Zet in de campagnelijst `publish` op `ja` en vul `share_title` en `share_text` in. Dat is de titel en tekst die
Facebook en WhatsApp bij de poster laten zien. Daarna:

```
python3 brand/campaign.py brand/campaigns/seizoen-2026-27.csv
python3 build.py .
```

Elke gepubliceerde poster krijgt een eigen pagina (`/delen/<naam>/`) met een brede voorbeeldafbeelding (poster + prijs,
duur, dagen en instrumenten) die Facebook en WhatsApp automatisch tonen. Op **`/delen/`** staan alle posters met grote
knoppen: Facebook, WhatsApp, afbeelding opslaan en, op de telefoon, **Delen…** (gewone deelmenu, met de poster als foto).

Facebook onthoudt een voorbeeld een tijd. Na het aanpassen van een poster: plak de link in de
[Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) en klik op *Scrape Again*.
