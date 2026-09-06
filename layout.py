# -*- coding: utf-8 -*-
"""Sjabloon van nubloemenbestellen.nl."""
import html
import json

import theme

BASIS = "https://nubloemenbestellen.nl"
NAAM = "Nu Bloemen Bestellen"
MAIL = "info@nubloemenbestellen.nl"

MENU = [
    ("/bestellen/", "Bestellen"),
    ("/gelegenheden/", "Gelegenheden"),
    ("/bloemsoorten/", "Bloemsoorten"),
    ("/hulpmiddelen/", "Hulpmiddelen"),
    ("/nieuws/", "Nieuws"),
    ("/contact/", "Contact"),
]

VOET = [
    ("Onderwerpen", [("/bestellen/", "Bestellen en bezorgen"),
                     ("/gelegenheden/", "Gelegenheden"),
                     ("/bloemsoorten/", "Bloemsoorten"),
                     ("/hulpmiddelen/", "Hulpmiddelen"),
                     ("/nieuws/", "Nieuws")]),
    ("Deze site", [("/over/", "Over deze site"),
                   ("/contact/", "Contact"),
                   ("/sitemap/", "Sitemap"),
                   ("/privacybeleid/", "Privacybeleid"),
                   ("/cookiebeleid/", "Cookiebeleid")]),
]


def _kruimel(pad):
    if not pad:
        return ""
    delen = ['<a href="/">Home</a>']
    for url, naam in pad[:-1]:
        delen.append('<a href="%s">%s</a>' % (url, html.escape(naam)))
    delen.append("<b>%s</b>" % html.escape(pad[-1][1]))
    return ('<div class="wrap"><div class="kruimel">%s</div></div>'
            % '<span>/</span>'.join(delen))


def _jsonld(pagina, kruimel):
    blokken = []
    lijst = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASIS + "/"}]
    for n, (url, naam) in enumerate(kruimel or [], start=2):
        lijst.append({"@type": "ListItem", "position": n, "name": naam,
                      "item": BASIS + url})
    if kruimel:
        blokken.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                        "itemListElement": lijst})
    if pagina.get("datum"):
        blokken.append({"@context": "https://schema.org", "@type": "Article",
                        "headline": pagina["titel"], "datePublished": pagina["datum"],
                        "inLanguage": "nl-NL",
                        "mainEntityOfPage": BASIS + pagina["url"],
                        "publisher": {"@type": "Organization", "name": NAAM}})
    return "".join('<script type="application/ld+json">%s</script>'
                   % json.dumps(b, ensure_ascii=False) for b in blokken)


def pagina(p, inhoud):
    actief = ""
    for url, _ in MENU:
        if p["url"] == url or p["url"].startswith(url) and url != "/":
            actief = url
    nav = "".join(
        '<a href="%s"%s>%s</a>' % (url, ' aria-current="page"' if url == actief else "",
                                   html.escape(naam))
        for url, naam in MENU)
    voet = "".join(
        "<div><h4>%s</h4><ul>%s</ul></div>"
        % (kop, "".join('<li><a href="%s">%s</a></li>' % (u, html.escape(n))
                        for u, n in links))
        for kop, links in VOET)
    canoniek = BASIS + p["url"]
    robots = '<meta name="robots" content="noindex,follow">' if p.get("noindex") else ""
    return """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(titel)s</title>
<meta name="description" content="%(omschrijving)s">
<link rel="canonical" href="%(canoniek)s">
%(robots)s
<meta property="og:type" content="website">
<meta property="og:title" content="%(titel)s">
<meta property="og:description" content="%(omschrijving)s">
<meta property="og:url" content="%(canoniek)s">
<meta property="og:locale" content="nl_NL">
<meta name="theme-color" content="#b23a5f">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="%(naam)s" href="/feed.xml">
<style>%(css)s</style>
%(jsonld)s
</head>
<body>
<header class="balk"><div class="wrap">
<a class="merk" href="/">%(merk)s<span>Nu <i>Bloemen</i> Bestellen</span></a>
<nav class="hoofd" aria-label="Hoofdmenu">%(nav)s</nav>
</div></header>
%(kruimel)s
<main>%(inhoud)s</main>
<footer>
<div class="wrap">
<div>
<h4>%(naam)s</h4>
<p style="font-size:15px;color:#cdb9bf;margin:0 0 10px">Onafhankelijke gids over bloemen
bestellen, bezorgen en uitkiezen.</p>
<p style="font-size:15px;margin:0"><a href="mailto:%(mail)s">%(mail)s</a></p>
</div>
%(voet)s
</div>
<div class="slot"><div class="wrap">
<span>%(naam)s</span><span>Redactie in Nederland</span>
</div></div>
</footer>
</body>
</html>
""" % {
        "titel": html.escape(p["titel"]),
        "omschrijving": html.escape(p["omschrijving"]),
        "canoniek": canoniek,
        "robots": robots,
        "css": theme.CSS,
        "jsonld": _jsonld(p, p.get("kruimel")),
        "merk": theme.MERK_SVG,
        "nav": nav,
        "kruimel": _kruimel(p.get("kruimel")),
        "inhoud": inhoud,
        "voet": voet,
        "naam": NAAM,
        "mail": MAIL,
    }
