# -*- coding: utf-8 -*-
"""Vormgeving en sjabloon van nubloemenbestellen.nl."""

CSS = """
:root{
  --papier:#fffdf9; --room:#f7f0e6; --inkt:#1e1b19; --grijs:#5f5952;
  --lijn:#e8ded1; --accent:#b23a5f; --accent-diep:#7d2440; --blad:#6c7f68;
  --zand:#fbf5ec; --rond:14px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--papier);color:var(--inkt);
  font-family:"Segoe UI",Inter,Roboto,-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif;
  font-size:17px;line-height:1.65;font-feature-settings:"kern" 1}
img{max-width:100%;height:auto}
a{color:var(--accent-diep);text-underline-offset:3px;text-decoration-thickness:1px}
a:hover{color:var(--accent)}
.wrap{width:min(1120px,calc(100% - 40px));margin-inline:auto}
.smal{width:min(760px,calc(100% - 40px));margin-inline:auto}

/* kopbalk */
.balk{position:sticky;top:0;z-index:20;background:rgba(255,253,249,.94);
  backdrop-filter:saturate(1.4) blur(8px);border-bottom:1px solid var(--lijn)}
.balk .wrap{display:flex;align-items:center;gap:22px;min-height:68px;flex-wrap:wrap}
.merk{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--inkt);
  font-weight:700;letter-spacing:-.02em;font-size:19px}
.merk svg{flex:0 0 auto}
.merk span i{font-style:normal;color:var(--accent)}
nav.hoofd{margin-left:auto;display:flex;gap:4px;flex-wrap:wrap}
nav.hoofd a{padding:8px 12px;border-radius:999px;text-decoration:none;color:var(--grijs);
  font-size:15px;font-weight:600}
nav.hoofd a:hover{background:var(--room);color:var(--inkt)}
nav.hoofd a[aria-current]{background:var(--accent);color:#fff}

/* kruimelpad */
.kruimel{font-size:13.5px;color:var(--grijs);padding:18px 0 0}
.kruimel a{color:var(--grijs);text-decoration:none}
.kruimel a:hover{color:var(--accent);text-decoration:underline}
.kruimel span{opacity:.5;padding:0 6px}

/* koppen */
h1{font-size:clamp(30px,4.4vw,46px);line-height:1.1;letter-spacing:-.03em;margin:.4em 0 .3em}
h2{font-size:clamp(21px,2.4vw,27px);line-height:1.2;letter-spacing:-.02em;margin:2em 0 .5em}
h3{font-size:19px;margin:1.6em 0 .4em;letter-spacing:-.01em}
p{margin:0 0 1.05em}
.lood{font-size:19.5px;color:#413b36;line-height:1.6}
ul,ol{margin:0 0 1.2em;padding-left:1.15em}
li{margin:.3em 0}
ul li::marker{color:var(--accent)}
ol li::marker{color:var(--accent);font-weight:700}

/* held */
.held{position:relative;overflow:hidden;background:
  radial-gradient(60% 90% at 88% 6%,#fbe4ec 0%,rgba(251,228,236,0) 62%),
  radial-gradient(52% 80% at 6% 96%,#e9f0e4 0%,rgba(233,240,228,0) 60%),
  var(--papier)}
.held .wrap{padding:64px 0 54px;display:grid;grid-template-columns:1.25fr .75fr;
  gap:44px;align-items:center}
.held h1{margin-top:0}
.oog{font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--accent);
  font-weight:700;margin:0 0 10px}
.knoppen{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.knop{display:inline-block;padding:13px 22px;border-radius:999px;text-decoration:none;
  font-weight:650;font-size:15.5px}
.knop.vol{background:var(--accent);color:#fff}
.knop.vol:hover{background:var(--accent-diep);color:#fff}
.knop.rand{border:1.5px solid var(--lijn);color:var(--inkt);background:#fff}
.knop.rand:hover{border-color:var(--accent);color:var(--accent)}
.bloemvlak{aspect-ratio:1/1;width:100%;max-width:330px;margin-left:auto}

/* kaarten */
.rooster{display:grid;gap:18px;margin:26px 0 6px}
.rooster.k2{grid-template-columns:repeat(2,1fr)}
.rooster.k3{grid-template-columns:repeat(3,1fr)}
.kaart{border:1px solid var(--lijn);border-radius:var(--rond);background:#fff;
  padding:20px 20px 18px;text-decoration:none;color:inherit;display:block;
  transition:transform .15s ease,border-color .15s ease,box-shadow .15s ease}
a.kaart:hover{transform:translateY(-2px);border-color:#e3c9d2;
  box-shadow:0 10px 24px rgba(125,36,64,.07)}
.kaart h3{margin:0 0 6px;font-size:17.5px}
.kaart p{margin:0;font-size:15px;color:var(--grijs)}
.kaart .num{display:block;font-size:12px;letter-spacing:.14em;color:var(--accent);
  font-weight:700;margin-bottom:8px}

/* stappen */
.stappen{counter-reset:stap;list-style:none;padding:0;margin:24px 0}
.stappen li{counter-increment:stap;position:relative;padding:0 0 18px 52px;margin:0}
.stappen li::before{content:counter(stap);position:absolute;left:0;top:-2px;width:34px;
  height:34px;border-radius:50%;background:var(--room);color:var(--accent-diep);
  font-weight:700;display:grid;place-items:center;font-size:15px}
.stappen li strong{display:block}

/* blokken */
.uitgelicht{background:var(--zand);border-left:3px solid var(--accent);
  border-radius:0 var(--rond) var(--rond) 0;padding:16px 20px;margin:1.6em 0}
.uitgelicht p{margin:0}
.winkel{border:1px solid #ecd7de;background:linear-gradient(180deg,#fff7f9,#fff);
  border-radius:var(--rond);padding:22px 24px;margin:2.2em 0 1em}
.winkel h2{margin:0 0 8px;font-size:20px}
.winkel p:last-child{margin-bottom:0}
.tabelwrap{overflow-x:auto;margin:1.4em 0}
table{border-collapse:collapse;width:100%;font-size:15.5px;min-width:440px}
th,td{text-align:left;padding:11px 12px;border-bottom:1px solid var(--lijn);vertical-align:top}
th{font-size:12.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--grijs)}
tbody tr:nth-child(odd){background:#fffaf5}

.strook{background:var(--room);border-top:1px solid var(--lijn);
  border-bottom:1px solid var(--lijn);margin-top:56px}
.strook .wrap{padding:44px 0}
.mini{font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--grijs);
  font-weight:700;margin:0 0 14px}

main{padding-bottom:40px}
article.tekst{padding-top:6px}

/* voettekst */
footer{background:#241a1d;color:#e8dcdf;margin-top:60px}
footer .wrap{padding:44px 0 30px;display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:30px}
footer h4{margin:0 0 10px;font-size:13px;letter-spacing:.14em;text-transform:uppercase;
  color:#c9a3b0}
footer a{color:#f4e9ec;text-decoration:none}
footer a:hover{text-decoration:underline;color:#fff}
footer ul{list-style:none;padding:0;margin:0}
footer li{margin:.32em 0;font-size:15px}
.slot{border-top:1px solid rgba(255,255,255,.13);font-size:13.5px;color:#bda6ac;
  padding:16px 0 26px}
.slot .wrap{display:flex;gap:14px;flex-wrap:wrap;justify-content:space-between;padding:0}

@media(max-width:860px){
  .held .wrap{grid-template-columns:1fr;padding:40px 0 34px}
  .bloemvlak{max-width:220px;margin:0}
  .rooster.k3{grid-template-columns:repeat(2,1fr)}
  footer .wrap{grid-template-columns:1fr 1fr}
}
@media(max-width:560px){
  body{font-size:16.5px}
  .rooster.k2,.rooster.k3{grid-template-columns:1fr}
  footer .wrap{grid-template-columns:1fr}
  nav.hoofd{margin-left:0;width:100%;padding-bottom:8px}
}
"""

MERK_SVG = ('<svg width="26" height="26" viewBox="0 0 32 32" aria-hidden="true">'
            '<g fill="#b23a5f"><circle cx="16" cy="8" r="5.4"/><circle cx="24" cy="16" r="5.4"/>'
            '<circle cx="16" cy="24" r="5.4"/><circle cx="8" cy="16" r="5.4"/></g>'
            '<circle cx="16" cy="16" r="4.2" fill="#f2c744"/></svg>')

def _bloem(x, y, schaal, kleur, kleur2, hart, blaadjes=6, draai=0):
    """Bouwt een bloem uit spitse bloembladen met een verloop naar het hart."""
    delen = []
    for n in range(blaadjes):
        hoek = draai + n * (360.0 / blaadjes)
        delen.append(
            '<path d="M0 0 C7 -11 8 -24 0 -33 C-8 -24 -7 -11 0 0 Z" '
            'transform="rotate(%.1f)" fill="%s" opacity="%s"/>'
            % (hoek, kleur if n % 2 == 0 else kleur2, "0.95"))
    return ('<g transform="translate(%s %s) scale(%s)">%s'
            '<circle r="7.5" fill="%s"/>'
            '<circle r="3.4" fill="#fff" opacity=".35"/></g>'
            % (x, y, schaal, "".join(delen), hart))


def _knop(x, y, schaal, kleur):
    return ('<g transform="translate(%s %s) scale(%s)">'
            '<path d="M0 0 C9 -6 9 -20 0 -26 C-9 -20 -9 -6 0 0 Z" fill="%s"/>'
            '<path d="M0 -2 C4 -8 4 -19 0 -24" stroke="#fff" stroke-opacity=".28" '
            'stroke-width="2" fill="none"/></g>' % (x, y, schaal, kleur))


HELD_SVG = """
<svg class="bloemvlak" viewBox="0 0 340 340" role="img"
     aria-label="Illustratie van een geschikt boeket in een vaas">
  <defs>
    <linearGradient id="vaas" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#f6ece0"/><stop offset=".55" stop-color="#e7d5bf"/>
      <stop offset="1" stop-color="#cdb391"/>
    </linearGradient>
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#e9ddc9"/><stop offset="1" stop-color="#dcc8ac"/>
    </linearGradient>
    <radialGradient id="gloed" cx=".5" cy=".42" r=".55">
      <stop offset="0" stop-color="#fbe6ee"/><stop offset="1" stop-color="#fbe6ee" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <circle cx="170" cy="140" r="128" fill="url(#gloed)"/>
  <g stroke="#6f8168" stroke-width="3.4" fill="none" stroke-linecap="round">
    <path d="M170 232 C170 190 168 152 166 118"/>
    <path d="M170 232 C158 196 140 172 118 150"/>
    <path d="M170 232 C182 198 204 176 224 158"/>
    <path d="M170 232 C162 202 150 184 134 170"/>
    <path d="M170 232 C178 206 192 190 208 180"/>
    <path d="M170 232 C170 204 176 178 186 148"/>
  </g>
  <g fill="#7d9074">
    <path d="M146 186 C132 178 122 182 116 192 C128 198 140 196 146 186 Z"/>
    <path d="M196 196 C210 188 220 192 226 202 C214 208 202 206 196 196 Z"/>
    <path d="M156 214 C144 210 136 214 132 222 C142 227 152 224 156 214 Z"/>
  </g>
  %(bloemen)s
  <path d="M133 228 h74 l-3 14 h-68 z" fill="#c9ad89"/>
  <path d="M136 242 h68 l-7 62 a16 16 0 0 1 -16 14 h-22 a16 16 0 0 1 -16 -14 z"
        fill="url(#vaas)"/>
  <path d="M143 258 h54 l-4 40 a12 12 0 0 1 -12 10 h-22 a12 12 0 0 1 -12 -10 z"
        fill="url(#water)" opacity=".55"/>
  <path d="M150 250 C146 268 146 288 150 306" stroke="#fff" stroke-opacity=".45"
        stroke-width="4" fill="none" stroke-linecap="round"/>
</svg>
""" % {"bloemen": "".join([
    _bloem(166, 112, 1.0, "#b23a5f", "#c9526f", "#f2c744"),
    _bloem(118, 146, 0.78, "#e0698a", "#ec8ba5", "#f7e3a1"),
    _bloem(226, 154, 0.72, "#7d2440", "#94304f", "#f2c744"),
    _bloem(134, 166, 0.58, "#efc0cf", "#f6d5df", "#f2c744", draai=18),
    _bloem(208, 178, 0.55, "#efc0cf", "#f6d5df", "#f2c744", draai=30),
    _knop(186, 146, 0.7, "#c9526f"),
    _knop(150, 128, 0.55, "#e0698a"),
])}

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
           '<rect width="32" height="32" rx="7" fill="#fffdf9"/>'
           '<g fill="#b23a5f"><circle cx="16" cy="9" r="5"/><circle cx="23" cy="16" r="5"/>'
           '<circle cx="16" cy="23" r="5"/><circle cx="9" cy="16" r="5"/></g>'
           '<circle cx="16" cy="16" r="3.8" fill="#f2c744"/></svg>\n')
