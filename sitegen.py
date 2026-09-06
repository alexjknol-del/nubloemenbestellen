"""Kleine statische generator zonder externe afhankelijkheden."""
import html
import os
import re
import shutil
import unicodedata
from datetime import datetime, timezone

SITE = {}


def slug(tekst):
    t = unicodedata.normalize("NFKD", tekst).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t or "kop"


def inline(tekst):
    tekst = html.escape(tekst, quote=False)
    tekst = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", tekst)

    def link(m):
        anker, url = m.group(1), m.group(2)
        if url.startswith("http"):
            return ('<a class="uit" href="%s" rel="nofollow noopener" '
                    'target="_blank">%s</a>' % (url, anker))
        return '<a href="%s">%s</a>' % (url, anker)

    tekst = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, tekst)
    return tekst


def markdown(tekst, koppen=None):
    """Zet de gebruikte opmaaksubset om naar html."""
    regels = tekst.strip("\n").split("\n")
    uit = []
    i = 0
    while i < len(regels):
        r = regels[i]
        if not r.strip():
            i += 1
            continue
        if r.startswith("## "):
            titel = r[3:].strip()
            s = slug(titel)
            if koppen is not None:
                koppen.append((s, titel))
            uit.append('<h2 id="%s">%s</h2>' % (s, inline(titel)))
            i += 1
            continue
        if r.startswith("### "):
            uit.append("<h3>%s</h3>" % inline(r[4:].strip()))
            i += 1
            continue
        if r.startswith("> "):
            blok = []
            while i < len(regels) and regels[i].startswith("> "):
                blok.append(regels[i][2:].strip())
                i += 1
            uit.append('<div class="uitgelicht"><p>%s</p></div>' % inline(" ".join(blok)))
            continue
        if r.startswith("- "):
            items = []
            while i < len(regels) and regels[i].startswith("- "):
                items.append("<li>%s</li>" % inline(regels[i][2:].strip()))
                i += 1
            uit.append("<ul>%s</ul>" % "".join(items))
            continue
        if re.match(r"^\d+\. ", r):
            items = []
            while i < len(regels) and re.match(r"^\d+\. ", regels[i]):
                items.append("<li>%s</li>" % inline(re.sub(r"^\d+\. ", "", regels[i]).strip()))
                i += 1
            uit.append("<ol>%s</ol>" % "".join(items))
            continue
        if r.startswith("|"):
            rijen = []
            while i < len(regels) and regels[i].startswith("|"):
                rijen.append([c.strip() for c in regels[i].strip("|").split("|")])
                i += 1
            kop = rijen[0]
            body = [r2 for r2 in rijen[1:] if not set("".join(r2)) <= set("- ")]
            thead = "".join("<th>%s</th>" % inline(c) for c in kop)
            tbody = "".join(
                "<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in rij)
                for rij in body)
            uit.append('<div class="tabelwrap"><table><thead><tr>%s</tr></thead>'
                       "<tbody>%s</tbody></table></div>" % (thead, tbody))
            continue
        alinea = []
        while i < len(regels) and regels[i].strip() and not re.match(
                r"^(#|-\s|\d+\.\s|>\s|\|)", regels[i]):
            alinea.append(regels[i].strip())
            i += 1
        uit.append("<p>%s</p>" % inline(" ".join(alinea)))
    return "\n".join(uit)


def schrijf(pad, inhoud):
    vol = os.path.join("dist", pad.strip("/"))
    os.makedirs(os.path.dirname(vol) or ".", exist_ok=True)
    with open(vol, "w", encoding="utf-8") as f:
        f.write(inhoud)


def schrijf_pagina(url, inhoud):
    if url == "/":
        schrijf("index.html", inhoud)
    else:
        schrijf(url.strip("/") + "/index.html", inhoud)


def sitemap(paginas, basis):
    regels = ['<?xml version="1.0" encoding="UTF-8"?>',
              '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in paginas:
        if p.get("noindex"):
            continue
        regels.append("  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>"
                      % (basis, p["url"], p.get("datum", SITE["gewijzigd"])))
    regels.append("</urlset>")
    return "\n".join(regels) + "\n"


def rss(artikelen, basis, titel, omschrijving):
    nu = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for a in artikelen:
        d = datetime.strptime(a["datum"], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        items.append(
            "  <item><title>%s</title><link>%s%s</link><guid>%s%s</guid>"
            "<pubDate>%s</pubDate><description>%s</description></item>"
            % (html.escape(a["titel"]), basis, a["url"], basis, a["url"],
               d.strftime("%a, %d %b %Y %H:%M:%S +0000"),
               html.escape(a["omschrijving"])))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n'
            "<title>%s</title>\n<link>%s/</link>\n<description>%s</description>\n"
            "<language>nl-nl</language>\n<lastBuildDate>%s</lastBuildDate>\n%s\n"
            "</channel>\n</rss>\n"
            % (html.escape(titel), basis, html.escape(omschrijving), nu, "\n".join(items)))


def leeg_dist():
    if os.path.isdir("dist"):
        shutil.rmtree("dist")
    os.makedirs("dist")
