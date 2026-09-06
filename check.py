# -*- coding: utf-8 -*-
"""Controleert de gegenereerde site in dist/."""
import os
import re
import sys
from collections import Counter

TOEGESTANE_HOSTS = {"bloomzy.nl", "www.bloomzy.nl"}
ANKER_OK = re.compile(r"^(Bloomzy\.nl|https://bloomzy\.nl/[^\s]*|https://bloomzy\.nl/)$")
AANSPREEK = re.compile(
    r"(?<![\w-])(je|jij|jou|jouw|jullie|uw|we|wij|ons|onze|onszelf)(?![\w-])", re.I)
DUMMY = re.compile(r"(lorem ipsum|todo|tbd|xxx|placeholder|voorbeeldtekst hier)", re.I)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿]")
BEDRAG = re.compile(r"(€|\beuro\b|\bEUR\b)", re.I)

fouten = []
waarschuwingen = []


def tekst_uit(html):
    zonder = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", html)
    zonder = re.sub(r"(?s)<[^>]+>", " ", zonder)
    return re.sub(r"\s+", " ", zonder)


def loop():
    bestanden = []
    for wortel, _, namen in os.walk("dist"):
        for n in namen:
            if n.endswith(".html"):
                bestanden.append(os.path.join(wortel, n))
    return sorted(bestanden)


def url_van(pad):
    rel = os.path.relpath(pad, "dist")
    if rel == "index.html":
        return "/"
    if rel == "404.html":
        return "/404.html"
    return "/" + rel[: -len("index.html")]


def bestaat(url):
    if url.startswith("#") or url.startswith("mailto:"):
        return True
    kaal = url.split("#")[0].split("?")[0]
    if kaal in ("/feed.xml", "/robots.txt", "/sitemap.xml", "/favicon.svg"):
        return os.path.exists("dist" + kaal)
    if kaal == "/":
        return os.path.exists("dist/index.html")
    return os.path.exists(os.path.join("dist", kaal.strip("/"), "index.html"))


def main():
    bestanden = loop()
    titels, omschrijvingen = Counter(), Counter()
    intern_gelinkt = set()
    for pad in bestanden:
        with open(pad, encoding="utf-8") as f:
            h = f.read()
        url = url_van(pad)
        body = h.split("<body>", 1)[1] if "<body>" in h else h
        inhoud = body.split("<footer>", 1)[0]
        tekst = tekst_uit(inhoud)

        m = re.search(r"<title>(.*?)</title>", h, re.S)
        titel = m.group(1) if m else ""
        if not titel:
            fouten.append("%s: geen title" % url)
        titels[titel] += 1
        if len(titel) > 65:
            waarschuwingen.append("%s: title %d tekens" % (url, len(titel)))

        m = re.search(r'<meta name="description" content="(.*?)">', h, re.S)
        oms = m.group(1) if m else ""
        if not oms:
            fouten.append("%s: geen description" % url)
        omschrijvingen[oms] += 1
        if oms and not (70 <= len(oms) <= 175):
            waarschuwingen.append("%s: description %d tekens" % (url, len(oms)))

        if h.count("<h1") != 1:
            fouten.append("%s: %d h1's" % (url, h.count("<h1")))
        if 'rel="canonical"' not in h:
            fouten.append("%s: geen canonical" % url)

        for teken, naam in [("—", "em-dash"), ("–", "en-dash")]:
            if teken in tekst:
                fouten.append("%s: %s in de tekst" % (url, naam))
        if EMOJI.search(tekst):
            fouten.append("%s: emoji" % url)
        if DUMMY.search(tekst):
            fouten.append("%s: dummytekst" % url)
        if BEDRAG.search(tekst):
            fouten.append("%s: bedrag of valuta in de tekst" % url)
        for m in AANSPREEK.finditer(tekst):
            fouten.append("%s: aanspreekvorm '%s'" % (url, m.group(1)))

        for m in re.finditer(r'<a [^>]*href="([^"]+)"[^>]*>(.*?)</a>', body, re.S):
            href, anker = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
            tag = m.group(0)
            if href.startswith("http"):
                host = href.split("/")[2]
                if host not in TOEGESTANE_HOSTS:
                    fouten.append("%s: externe host %s" % (url, host))
                if 'rel="nofollow noopener"' not in tag:
                    fouten.append("%s: externe link zonder nofollow noopener (%s)" % (url, href))
                if 'target="_blank"' not in tag:
                    fouten.append("%s: externe link zonder target blank (%s)" % (url, href))
                if not ANKER_OK.match(anker):
                    fouten.append("%s: ankertekst '%s'" % (url, anker))
            elif href.startswith("/"):
                if not bestaat(href):
                    fouten.append("%s: kapotte link naar %s" % (url, href))
                intern_gelinkt.add(href.split("#")[0])
            elif href.startswith("#"):
                if ('id="%s"' % href[1:]) not in h:
                    fouten.append("%s: anker %s bestaat niet" % (url, href))
            elif href.startswith("mailto:"):
                pass
            else:
                fouten.append("%s: onbekende link %s" % (url, href))
            if not anker:
                fouten.append("%s: lege link %s" % (url, href))

        for m in re.finditer(r'(src|srcset|data-src)="(https?:)?//([^"]+)"', body):
            fouten.append("%s: externe bron %s" % (url, m.group(3)))
        for m in re.finditer(r'<link ([^>]*)>', h):
            attrs = m.group(1)
            rel = re.search(r'rel="([^"]+)"', attrs)
            href = re.search(r'href="([^"]+)"', attrs)
            if not href:
                continue
            if rel and rel.group(1) in ("canonical", "alternate", "icon"):
                continue
            if href.group(1).startswith("http"):
                fouten.append("%s: externe link-tag %s" % (url, href.group(1)))
        if "<iframe" in h:
            fouten.append("%s: iframe in de html" % url)

    for t, n in titels.items():
        if n > 1:
            fouten.append("dubbele title (%dx): %s" % (n, t))
    for o, n in omschrijvingen.items():
        if n > 1:
            fouten.append("dubbele description (%dx): %s" % (n, o[:60]))

    with open("dist/sitemap.xml", encoding="utf-8") as f:
        sm = f.read()
    in_sitemap = set(re.findall(r"<loc>https?://[^/]+(/[^<]*)</loc>", sm))
    alle = {url_van(p) for p in bestanden if not p.endswith("404.html")}
    for u in alle - in_sitemap:
        fouten.append("ontbreekt in sitemap: %s" % u)
    for u in in_sitemap - alle:
        fouten.append("sitemap verwijst naar onbekende pagina: %s" % u)

    for u in alle - intern_gelinkt - {"/"}:
        waarschuwingen.append("geen interne link naar %s" % u)

    print("paginas gecontroleerd: %d" % len(bestanden))
    if waarschuwingen:
        print("\nwaarschuwingen (%d):" % len(waarschuwingen))
        for w in waarschuwingen:
            print("  " + w)
    if fouten:
        print("\nFOUTEN (%d):" % len(fouten))
        for f_ in fouten:
            print("  " + f_)
        sys.exit(1)
    print("\ngeen fouten")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
