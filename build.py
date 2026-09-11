# -*- coding: utf-8 -*-
"""Bouwt nubloemenbestellen.nl naar dist/."""
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sitegen
import theme
import layout
import content_bestellen as bestellen
import content_gelegenheden as gelegenheden
import content_bloemsoorten as bloemsoorten
import content_hulpmiddelen as hulpmiddelen
import content_nieuws as nieuws

BASIS = layout.BASIS
NAAM = layout.NAAM
MAIL = layout.MAIL
sitegen.SITE["gewijzigd"] = "2026-09-06"

RUBRIEKEN = [bestellen, gelegenheden, bloemsoorten, hulpmiddelen]


def volle_url(mod, p):
    return mod.RUBRIEK["url"] + p["slug"] + "/"


def winkelblok(winkel):
    if not winkel:
        return ""
    kop, tekst = winkel
    return ('<div class="winkel"><h2>%s</h2>%s</div>'
            % (html.escape(kop), sitegen.markdown(tekst)))


def artikelpagina(mod, p):
    url = volle_url(mod, p)
    kruimel = [(mod.RUBRIEK["url"], mod.RUBRIEK["h1"]), (url, p["titel"])]
    volle = p["titel"] + " | " + NAAM if len(p["titel"]) <= 40 else p["titel"]
    meta = {"url": url, "titel": volle,
            "omschrijving": p["omschrijving"], "kruimel": kruimel}
    if p.get("datum"):
        meta["datum"] = p["datum"]
    romp = ['<div class="smal"><article class="tekst">']
    romp.append("<h1>%s</h1>" % html.escape(p["titel"]))
    if p.get("datum"):
        romp.append('<p class="oog">%s</p>' % datumtekst(p["datum"]))
    romp.append('<p class="lood">%s</p>' % html.escape(p["lood"]))
    romp.append(sitegen.markdown(p["body"]))
    romp.append(winkelblok(p.get("winkel")))
    romp.append(verder(mod, p))
    romp.append("</article></div>")
    return meta, "".join(romp)


MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus",
           "september", "oktober", "november", "december"]


def datumtekst(datum):
    jaar, maand, dag = datum.split("-")
    return "%d %s %s" % (int(dag), MAANDEN[int(maand) - 1], jaar)


def verder(mod, huidig):
    andere = [p for p in mod.PAGINAS if p["slug"] != huidig["slug"]][:3]
    if not andere:
        return ""
    items = "".join(
        '<a class="kaart" href="%s"><h3>%s</h3><p>%s</p></a>'
        % (volle_url(mod, p), html.escape(p["titel"]), html.escape(p["kaart"]))
        for p in andere)
    return ('<h2>Verder lezen</h2><div class="rooster k3">%s</div>' % items)


def rubriekpagina(mod):
    r = mod.RUBRIEK
    kaarten = "".join(
        '<a class="kaart" href="%s"><span class="num">%02d</span><h3>%s</h3><p>%s</p></a>'
        % (volle_url(mod, p), n, html.escape(p["titel"]), html.escape(p["kaart"]))
        for n, p in enumerate(mod.PAGINAS, start=1))
    inhoud = ('<div class="wrap"><h1>%s</h1><p class="lood" style="max-width:62ch">%s</p>'
              '<div class="rooster k3">%s</div></div>'
              % (html.escape(r["h1"]), html.escape(r["lood"]), kaarten))
    meta = {"url": r["url"], "titel": r["titel"], "omschrijving": r["omschrijving"],
            "kruimel": [(r["url"], r["h1"])]}
    return meta, inhoud


def nieuwspagina():
    r = nieuws.RUBRIEK
    rijen = "".join(
        '<a class="kaart" href="%s"><span class="num">%s</span><h3>%s</h3><p>%s</p></a>'
        % (nieuws.RUBRIEK["url"] + p["slug"] + "/", datumtekst(p["datum"]),
           html.escape(p["titel"]), html.escape(p["kaart"]))
        for p in gesorteerd_nieuws())
    inhoud = ('<div class="wrap"><h1>%s</h1><p class="lood" style="max-width:62ch">%s</p>'
              '<div class="rooster k2">%s</div>'
              '<p style="margin-top:26px"><a href="/feed.xml">Rss-feed van deze rubriek</a></p>'
              "</div>" % (html.escape(r["h1"]), html.escape(r["lood"]), rijen))
    meta = {"url": r["url"], "titel": r["titel"], "omschrijving": r["omschrijving"],
            "kruimel": [(r["url"], r["h1"])]}
    return meta, inhoud


def gesorteerd_nieuws():
    return sorted(nieuws.PAGINAS, key=lambda p: p["datum"], reverse=True)


def home():
    laatste = gesorteerd_nieuws()[:3]
    nieuwsrij = "".join(
        '<a class="kaart" href="%s"><span class="num">%s</span><h3>%s</h3><p>%s</p></a>'
        % (nieuws.RUBRIEK["url"] + p["slug"] + "/", datumtekst(p["datum"]),
           html.escape(p["titel"]), html.escape(p["kaart"]))
        for p in laatste)
    rubriekkaarten = "".join(
        '<a class="kaart" href="%s"><h3>%s</h3><p>%s</p></a>'
        % (m.RUBRIEK["url"], html.escape(m.RUBRIEK["h1"]), html.escape(m.RUBRIEK["lood"]))
        for m in RUBRIEKEN)
    startkaarten = "".join(
        '<a class="kaart" href="%s"><span class="num">%02d</span><h3>%s</h3><p>%s</p></a>'
        % (u, n, html.escape(t), html.escape(o))
        for n, (u, t, o) in enumerate([
            ("/bestellen/bloemen-online-bestellen/", "Zo verloopt een bestelling",
             "Vijf stappen van keuze tot bevestiging."),
            ("/bestellen/boeket-uitkiezen/", "Het juiste formaat kiezen",
             "Hoogte, kleurgroep en de plek in huis."),
            ("/bestellen/verse-bloemen-of-kunstbloemen/", "Vers, droog of kunst",
             "Houdbaarheid en onderhoud naast elkaar."),
        ], start=1))
    inhoud = """
<section class="held"><div class="wrap">
<div>
<p class="oog">Onafhankelijke gids</p>
<h1>Bloemen bestellen die aankomen zoals bedoeld</h1>
<p class="lood">Welk boeket past bij de gelegenheid, hoe verloopt de bezorging en waar gaat
het mis. Deze site zet de keuzes op een rij, van formaat en kleur tot levertijd, retour en
het kaartje.</p>
<div class="knoppen">
<a class="knop vol" href="/bestellen/">Bestellen en bezorgen</a>
<a class="knop rand" href="/gelegenheden/">Per gelegenheid</a>
</div>
</div>
%(held)s
</div></section>

<div class="wrap">
<h2>Beginnen bij het begin</h2>
<div class="rooster k3">%(start)s</div>
</div>

<section class="strook"><div class="wrap">
<p class="mini">Vier onderwerpen</p>
<div class="rooster k2">%(rubrieken)s</div>
</div></section>

<div class="wrap">
<h2>In het kort</h2>
<ol class="stappen">
<li><strong>Bepaal eerst de datum.</strong> De gewenste bezorgdag bepaalt welk boeket nog
haalbaar is, niet andersom.</li>
<li><strong>Kies het formaat in centimeters.</strong> De woorden klein, middel en groot
betekenen per winkel iets anders.</li>
<li><strong>Controleer het bezorgadres in de bevestigingsmail.</strong> Daar zit de
meestgemaakte fout.</li>
<li><strong>Schrijf het kaartje af met een naam.</strong> Een boeket zonder afzender levert
een raadsel op.</li>
</ol>
</div>

<div class="wrap">
<h2>Laatste artikelen</h2>
<div class="rooster k3">%(nieuws)s</div>
</div>

<div class="wrap">
<div class="winkel">
<h2>Boeketten die niet verwelken</h2>
<p>Wie een boeket zoekt dat na de bezorging blijft staan, vindt bij
<a class="uit" href="https://bloomzy.nl/" rel="nofollow noopener" target="_blank">Bloomzy.nl</a>
zijden boeketten, kunstboeketten, droogboeketten en vazen in beperkte oplage. De collectie
staat op
<a class="uit" href="https://bloomzy.nl/collectie" rel="nofollow noopener" target="_blank">https://bloomzy.nl/collectie</a>.</p>
<p>Zijden boeketten staan op
<a class="uit" href="https://bloomzy.nl/collectie/zijden-boeketten" rel="nofollow noopener" target="_blank">https://bloomzy.nl/collectie/zijden-boeketten</a>,
kunstboeketten op
<a class="uit" href="https://bloomzy.nl/collectie/kunstboeketten" rel="nofollow noopener" target="_blank">https://bloomzy.nl/collectie/kunstboeketten</a>.</p>
</div>
</div>
""" % {"held": theme.HELD_SVG, "start": startkaarten, "rubrieken": rubriekkaarten,
       "nieuws": nieuwsrij}
    meta = {"url": "/", "titel": "Bloemen bestellen en bezorgen | " + NAAM,
            "omschrijving": "Onafhankelijke gids over bloemen bestellen: boeket kiezen, "
                            "bezorging, gelegenheden, bloemsoorten en de fouten die het "
                            "vaakst voorkomen."}
    return meta, inhoud


def tekstpagina(url, titel, omschrijving, h1, lood, body, kruimel=None, noindex=False):
    meta = {"url": url, "titel": titel, "omschrijving": omschrijving,
            "kruimel": kruimel if kruimel is not None else [(url, h1)]}
    if noindex:
        meta["noindex"] = True
    inhoud = ('<div class="smal"><article class="tekst"><h1>%s</h1>'
              '<p class="lood">%s</p>%s</article></div>'
              % (html.escape(h1), html.escape(lood), sitegen.markdown(body)))
    return meta, inhoud


def vaste_paginas():
    uit = []
    uit.append(tekstpagina(
        "/over/", "Over deze site | " + NAAM,
        "Wat op deze site staat, hoe de informatie tot stand komt en waar de verwijzingen "
        "naartoe gaan.",
        "Over deze site",
        "Nu Bloemen Bestellen is een Nederlandstalige gids over het bestellen, bezorgen en "
        "uitkiezen van bloemen.",
        """
## Wat hier staat

De site behandelt vier onderwerpen: het bestelproces met bezorging, betaling en retour, de
keuze per gelegenheid, de eigenschappen van de meest gebruikte bloemsoorten en twee
praktische hulpmiddelen. De teksten zijn geschreven voor wie incidenteel bloemen bestelt en
wil weten wat er komt kijken.

## Hoe de teksten tot stand komen

De informatie komt uit openbare bronnen over consumentenrecht, uit de voorwaarden van
Nederlandse bezorgdiensten en uit de praktijk van bloemenwebwinkels. Waar wetgeving wordt
genoemd, staat het wetsartikel erbij. Prijzen staan er bewust niet in: die veranderen per
seizoen en per winkel.

## Verwijzingen

Op meerdere pagina's staat een verwijzing naar Bloomzy.nl, een Nederlandse webwinkel in
kunstbloemen, zijden boeketten, droogboeketten en vazen. Die verwijzingen staan er omdat
kunstbloemen op veel pagina's het praktische alternatief zijn voor verse bloemen.

## Contact

Vragen en correcties kunnen naar [%(mail)s](mailto:%(mail)s).

## Uitvoering

Voor blijvende boeketten en vazen wordt verwezen naar
[Bloomzy.nl](https://bloomzy.nl/).
""" % {"mail": MAIL}))

    uit.append(tekstpagina(
        "/contact/", "Contact | " + NAAM,
        "Contactgegevens van Nu Bloemen Bestellen: correcties, aanvullingen en vragen over de teksten op deze site.",
        "Contact",
        "Vragen, aanvullingen of correcties op de teksten gaan per e-mail.",
        """
## E-mail

[%(mail)s](mailto:%(mail)s)

Berichten worden op werkdagen gelezen. Er is geen contactformulier en geen telefoonnummer.

## Waarvoor dit adres wel bedoeld is

- Correcties op de inhoud van een pagina.
- Aanvullingen of onderwerpen die ontbreken.
- Vragen over het gebruik van teksten van deze site.

## Waarvoor niet

Bestellingen, bezorgvragen en klachten over een boeket lopen via de winkel waar de
bestelling is geplaatst. Deze site verkoopt niets en heeft geen inzage in bestellingen.

## Bestellen

Boeketten en vazen staan bij [Bloomzy.nl](https://bloomzy.nl/).
""" % {"mail": MAIL}))

    uit.append(tekstpagina(
        "/privacybeleid/", "Privacybeleid | " + NAAM,
        "Welke gegevens Nu Bloemen Bestellen verwerkt, wat er in de serverlogboeken staat en welke rechten bezoekers hebben.",
        "Privacybeleid",
        "Deze site verzamelt zo min mogelijk gegevens. Hieronder staat wat er wel en niet "
        "gebeurt.",
        """
## Geen analyse en geen advertenties

De site gebruikt geen statistiekprogramma, geen advertentienetwerk en geen sociale
knoppen. Er worden geen bezoekersprofielen opgebouwd.

## Serverlogboeken

De hostingpartij legt technische gegevens vast die nodig zijn om de site uit te leveren:
het ip-adres, het tijdstip, de opgevraagde pagina en het type browser. Die gegevens dienen
voor beveiliging en storingsonderzoek en worden niet gekoppeld aan personen.

## E-mail

Wie mailt naar %(mail)s, deelt daarmee een e-mailadres en de inhoud van het bericht. Die
gegevens worden alleen gebruikt om te antwoorden en worden niet gedeeld met derden.

## Externe verwijzingen

Op pagina's staan links naar andere websites, waaronder bloomzy.nl. Vanaf het moment dat
een bezoeker doorklikt, geldt het privacybeleid van die site.

## Rechten

Op grond van de Algemene verordening gegevensbescherming bestaat recht op inzage,
correctie en verwijdering van persoonsgegevens. Een verzoek daartoe kan naar
[%(mail)s](mailto:%(mail)s). Klachten over de verwerking kunnen worden ingediend bij de
Autoriteit Persoonsgegevens.

## Wijzigingen

Wijzigingen in dit beleid verschijnen op deze pagina. Laatste versie: september 2026.
""" % {"mail": MAIL}))

    uit.append(tekstpagina(
        "/cookiebeleid/", "Cookiebeleid | " + NAAM,
        "Nu Bloemen Bestellen plaatst geen cookies en gebruikt geen trackers of ingesloten inhoud van derden.",
        "Cookiebeleid",
        "Deze site plaatst geen cookies.",
        """
## Geen cookies

Er worden geen cookies geplaatst, ook geen functionele. De site bestaat uit vaste pagina's
zonder inlogfunctie, zonder winkelwagen en zonder voorkeuren die bewaard hoeven te worden.

## Geen trackers

Er staat geen statistiekcode, geen advertentiescript en geen ingesloten inhoud van derden
op de pagina's. Er worden dus ook geen verzoeken naar externe servers gedaan tijdens het
laden van een pagina.

## Wat er wel gebeurt

De browser bewaart pagina's tijdelijk in het eigen geheugen om ze sneller te tonen. Dat is
een browserfunctie en geen cookie.

## Na doorklikken

Wie via een link naar een andere website gaat, komt terecht bij een site met een eigen
cookiebeleid. Webwinkels plaatsen doorgaans wel cookies, bijvoorbeeld voor de winkelwagen.

## Vragen

Vragen over dit beleid kunnen naar [%(mail)s](mailto:%(mail)s).
""" % {"mail": MAIL}))
    return uit


def sitemappagina(alle):
    groepen = []
    for mod in RUBRIEKEN + [nieuws]:
        links = "".join('<li><a href="%s">%s</a></li>'
                        % (mod.RUBRIEK["url"] + p["slug"] + "/", html.escape(p["titel"]))
                        for p in mod.PAGINAS)
        groepen.append('<h2>%s</h2><ul>%s</ul>' % (html.escape(mod.RUBRIEK["h1"]), links))
    vast = "".join('<li><a href="%s">%s</a></li>' % (u, n) for u, n in [
        ("/", "Home"), ("/over/", "Over deze site"), ("/contact/", "Contact"),
        ("/privacybeleid/", "Privacybeleid"), ("/cookiebeleid/", "Cookiebeleid")])
    inhoud = ('<div class="smal"><article class="tekst"><h1>Sitemap</h1>'
              '<p class="lood">Alle pagina\'s van deze site op een rij.</p>'
              '<h2>Vaste pagina\'s</h2><ul>%s</ul>%s</article></div>'
              % (vast, "".join(groepen)))
    meta = {"url": "/sitemap/", "titel": "Sitemap | " + NAAM,
            "omschrijving": "Overzicht van alle pagina's van Nu Bloemen Bestellen, gerangschikt per onderwerp.",
            "kruimel": [("/sitemap/", "Sitemap")]}
    return meta, inhoud


def bouw():
    sitegen.leeg_dist()
    paginas = []

    meta, inhoud = home()
    paginas.append((meta, inhoud))

    for mod in RUBRIEKEN:
        paginas.append(rubriekpagina(mod))
        for p in mod.PAGINAS:
            paginas.append(artikelpagina(mod, p))

    paginas.append(nieuwspagina())
    for p in nieuws.PAGINAS:
        paginas.append(artikelpagina(nieuws, p))

    paginas.extend(vaste_paginas())
    alle_meta = [m for m, _ in paginas]
    paginas.append(sitemappagina(alle_meta))

    for meta, inhoud in paginas:
        sitegen.schrijf_pagina(meta["url"], layout.pagina(meta, inhoud))

    # 404
    meta404 = {"url": "/404.html", "titel": "Pagina niet gevonden | " + NAAM,
               "omschrijving": "De opgevraagde pagina bestaat niet of is verplaatst. Via de sitemap staan alle pagina's op een rij.", "noindex": True}
    inhoud404 = ('<div class="smal"><article class="tekst"><h1>Pagina niet gevonden</h1>'
                 '<p class="lood">De opgevraagde pagina bestaat niet of is verplaatst.</p>'
                 '<p>Via de <a href="/sitemap/">sitemap</a> staan alle pagina\'s op een rij. '
                 'De vier onderwerpen beginnen bij <a href="/bestellen/">bestellen en '
                 'bezorgen</a>, <a href="/gelegenheden/">gelegenheden</a>, '
                 '<a href="/bloemsoorten/">bloemsoorten</a> en '
                 '<a href="/hulpmiddelen/">hulpmiddelen</a>.</p></article></div>')
    sitegen.schrijf("404.html", layout.pagina(meta404, inhoud404))

    lijst = [m for m, _ in paginas]
    sitegen.schrijf("sitemap.xml", sitegen.sitemap(lijst, BASIS))
    artikelen = [{"titel": p["titel"], "omschrijving": p["omschrijving"],
                  "url": nieuws.RUBRIEK["url"] + p["slug"] + "/", "datum": p["datum"]}
                 for p in gesorteerd_nieuws()]
    sitegen.schrijf("feed.xml", sitegen.rss(artikelen, BASIS, NAAM,
                                            "Nieuws en achtergrond over bloemen bestellen"))
    sitegen.schrijf("robots.txt",
                    "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASIS)
    sitegen.schrijf("favicon.svg", theme.FAVICON)
    print("paginas:", len(paginas) + 1)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    bouw()
