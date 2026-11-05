#!/usr/bin/env python3
"""Sito 3F Illuminazioni Finocchiaro Home. Tutti i testi e i dati stanno qui: modifica e rilancia `python3 build.py`."""
import datetime, html, json, os, pathlib, shutil

QUI = pathlib.Path(__file__).parent
VERSIONE = 1
PREFISSO = os.environ.get('PREFISSO', '')      # '' sul dominio; '/3f-sito' sull'indirizzo di prova
BASE = os.environ.get('BASE', 'https://www.3filluminazione.com')
PUBBLICO = False                               # True solo quando il sito va online sul dominio: toglie il noindex

AZIENDA = {
    'marchio': '3F Illuminazioni Finocchiaro Home',
    'breve': '3F Illuminazioni',
    'ragione': '3F Illuminazione S.r.l.',      # dal vecchio sito: DA CONFERMARE con la visura
    'piva': '',                                # DA RICEVERE
    'via': 'C.so Carlo Marx 24', 'cap': '95045', 'citta': 'Misterbianco', 'prov': 'CT',
    'tel': '095 673 0772', 'tel_link': '+390956730772',
    'email': '3filluminazione@libero.it',
    'whatsapp': '',                            # DA RICEVERE, es. 393331234567
    'facebook': '', 'instagram': '',           # DA RICEVERE
    'orari': [],                               # DA RICEVERE, es. [('Lunedì - Sabato', '9:00 - 13:00 / 16:00 - 20:00')]
}

# Bottone sul nome della casa: url None = sito ufficiale non trovato, resta il solo nome
MARCHI = [
    ('Sikrea', 'sikrea.png', 'https://www.sikrea.com'),
    ('Icone', 'icone.png', 'https://iconeluce.com'),
    ("Capo d'Arte", None, None),
    ('Ideal Lux', 'ideal-lux.svg', 'https://www.ideal-lux.com'),
    ('Redo Group', 'redo.png', 'https://redogroup.com'),
    ('Illuminati', 'illuminati.png', 'https://illuminati-lighting.it'),
    ('Ondaluce', 'ondaluce.png', 'https://ondaluce-illuminazione.com/it'),
    ('Exclusive Light', 'exclusive-light.png', None),
    ('Cangini & Tucci', 'cangini-tucci.png', 'https://www.canginietucci.com'),
]

MONDI = [
    ('lampadari', 'Lampadari', 'Cristallo, vetro e metallo: dai classici alle linee più contemporanee, per i soffitti che chiedono una presenza.',
     'Grande lampadario con sfere dorate acceso nello showroom'),
    ('design', 'Luce di design', 'Sospensioni, plafoniere e applique a LED. Forme pensate per disegnare una stanza anche da spente.',
     'Sospensione a LED dalla linea continua in showroom'),
    ('arredo', 'Arredamento', 'Arredi e complementi da scegliere insieme alla luce, perché una casa si guarda tutta intera.',
     'Divano bordeaux nello showroom, sotto le lampade esposte'),
]

SERVIZI = [
    ('Consulenza', 'Ti ascoltiamo e ti accompagniamo nella scelta, stanza per stanza, tra prodotti, stili e misure.'),
    ('Progettazione', 'Studiamo l’illuminazione di abitazioni, attività commerciali e spazi professionali.'),
    ('Fornitura', 'Lampade, arredi e materiale elettrico selezionati per qualità, design e affidabilità.'),
]

ALT_GALLERIA = {
    '0461': 'Lampadario in cristallo con cerchio dorato', '0462': 'Lampadario con sfere dorate acceso', '0471': 'Sospensione a LED dalla linea continua',
    '0473': 'Sospensioni in vetro su base ovale nera', '0466': 'Sospensioni a goccia in vetro e oro', '0470': 'Sospensioni in vetro specchiato e lampadari in cristallo',
    '0464': 'Lampade esposte davanti alla vetrata', '0468': 'Lampadario a bracci curvi davanti alla vetrata', '0467': 'Sospensione con sfere in vetro ambrato',
    '0472': 'Plafoniere circolari a LED accese', '0455': 'Il salone dello showroom con divano bordeaux', '0463': 'Il salone dello showroom visto dall’alto',
    '0456': 'Corsia dello showroom con lampade da tavolo', '0458': 'Tavolo in vetro con lampade da tavolo', '0459': 'Lampade esposte sui banchi dello showroom',
    '0460': 'Plafoniere e paralumi a soffitto', '0465': 'Lampadario a raggi e sospensioni in vetro', '0469': 'Sospensioni in vetro colorato', '0474': 'Veduta del salone espositivo',
    '0475': 'Applique e passaggio verso la sala interna', '0476': 'Lampadari in cristallo a soffitto', '0477': 'Lampadario in metallo specchiato', '0478': 'Corridoio con applique alle pareti',
    '0485': 'Sala interna con pareti colorate e lampade',
}
GALLERIA = list(ALT_GALLERIA)

ANNO = datetime.date.today().year
e = html.escape

def u(p):  # percorso interno
    return PREFISSO + p

def foto(nome, larghe, alt, sizes='100vw', cls='', pigra=True, attr=''):
    src = ', '.join(f'{u(f"/assets/img/{nome}-{l}.webp")} {l}w' for l in larghe)
    return (f'<img src="{u(f"/assets/img/{nome}-{larghe[-1]}.webp")}" srcset="{src}" sizes="{sizes}" alt="{e(alt, quote=True)}"'
            f'{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}{" loading=lazy decoding=async" if pigra else ""} {attr}>')

def filo():
    return '<span class="filo" aria-hidden="true"><i></i></span>'

def bottone(testo, href, cls='btn', freccia=False, nuovo=False):
    extra = ' target="_blank" rel="noopener"' if nuovo else ''
    return f'<a class="{cls}" href="{href}"{extra}>{e(testo)}{"<span aria-hidden=true> ↗</span>" if freccia else ""}</a>'

def griglia_marchi():
    r = []
    for nome, logo, url in MARCHI:
        marca = (f'<img src="{u("/assets/marchi/" + logo)}" alt="" loading="lazy" decoding="async">' if logo
                 else f'<span class="marca-scritta">{e(nome)}</span>')
        azione = (f'<a class="btn-casa" href="{url}" target="_blank" rel="noopener" aria-label="{e(nome, quote=True)}, apri il sito della casa in una nuova scheda">{e(nome)}<span aria-hidden="true"> ↗</span></a>'
                  if url else f'<span class="casa-nome">{e(nome)}</span>')
        r.append(f'<li class="marchio"><div class="marca">{marca}</div>{azione}</li>')
    return f'<ul class="marchi">{"".join(r)}</ul>'

def coppia_apertura():
    """Come sul foglio del cliente: foto antica 'dal 1950' e foto frontale esterna, una accanto all'altra."""
    return (f'<div class="coppia">'
            f'<figure class="accende"><a href="{u("/assets/img/storica-1600.webp")}" data-luce>{foto("storica", (800, 1600), "Il negozio negli anni Cinquanta: pentole, piatti e un uomo sulla porta, in una foto d’epoca", "(max-width:760px) 100vw, 58vw")}</a><figcaption><span class="corsivo">dal 1950</span></figcaption></figure>'
            f'<figure class="accende"><a href="{u("/assets/img/frontale-1400.webp")}" data-luce>{foto("frontale", (800, 1400), "L’ingresso del negozio in Corso Carlo Marx, con l’insegna Lampad’Art e il numero 3F", "(max-width:760px) 100vw, 38vw")}</a><figcaption>Oggi, in Corso Carlo Marx</figcaption></figure>'
            f'</div>')

def tessera(n):
    return (f'<a class="tessera accende" href="{u(f"/assets/img/g{n}-1600.webp")}" data-luce>'
            + foto(f'g{n}', (640, 1600), ALT_GALLERIA[n], '(max-width:760px) 50vw, 30vw') + '</a>')

def schema():
    d = {'@context': 'https://schema.org', '@type': 'HomeGoodsStore', 'name': AZIENDA['marchio'], 'url': BASE + '/',
         'image': BASE + '/assets/og.jpg', 'logo': BASE + '/assets/logo/logo-512.png', 'telephone': AZIENDA['tel_link'], 'email': AZIENDA['email'], 'foundingDate': '1950',
         'description': 'Lampadari, illuminazione e arredamento a Misterbianco (CT).',
         'address': {'@type': 'PostalAddress', 'streetAddress': 'Corso Carlo Marx 24', 'postalCode': AZIENDA['cap'], 'addressLocality': AZIENDA['citta'], 'addressRegion': AZIENDA['prov'], 'addressCountry': 'IT'}}
    sociali = [v for v in (AZIENDA['facebook'], AZIENDA['instagram']) if v]
    if sociali: d['sameAs'] = sociali
    return json.dumps(d, ensure_ascii=False)

def intestazione(attiva, su_foto):
    voci = [('/', 'Home'), ('/storia', 'La storia'), ('/galleria', 'Galleria'), ('/marchi', 'Le case')]
    lk = ''.join(f'<a href="{u(h) or "/"}"{" aria-current=page" if attiva == h else ""}>{t}</a>' for h, t in voci)
    return f'''<a class="salta" href="#contenuto">Vai al contenuto</a>
<header class="testata{' su-foto' if su_foto else ''}" data-testata>
  <a class="logo" href="{u('/') or '/'}" aria-label="{AZIENDA['marchio']}, torna alla home"><img src="{u('/assets/logo/logo.svg')}" alt="" width="220" height="71"></a>
  <nav class="menu" id="menu" aria-label="Menu principale">{lk}<a class="btn btn-sottile" href="{u('/contatti')}"{' aria-current=page' if attiva == '/contatti' else ''}>Contatti</a></nav>
  <button class="apri-menu" type="button" aria-expanded="false" aria-controls="menu" data-menu><span>Menu</span></button>
</header>'''

def piede():
    a = AZIENDA
    soc = ''.join(f'<a href="{v}" target="_blank" rel="noopener">{n}</a>' for n, v in (('Facebook', a['facebook']), ('Instagram', a['instagram'])) if v)
    orari = ''.join(f'<p>{e(g)}<br>{e(o)}</p>' for g, o in a['orari'])
    wa = f'<a href="https://wa.me/{a["whatsapp"]}">WhatsApp</a>' if a['whatsapp'] else ''
    piva = f' · P.IVA {a["piva"]}' if a['piva'] else ''
    return f'''<footer class="piede">
  <div class="piede-griglia">
    <div><img class="logo-piede" src="{u('/assets/logo/logo.svg')}" alt="{a['marchio']}" width="280" height="90" loading="lazy"></div>
    <div><h2>Dove siamo</h2><p>{a['via']}<br>{a['cap']} {a['citta']} ({a['prov']})</p>{orari}</div>
    <div><h2>Contatti</h2><p><a href="tel:{a['tel_link']}">{a['tel']}</a><br><a href="mailto:{a['email']}">{a['email']}</a>{'<br>' + wa if wa else ''}</p>{f'<p class="sociali">{soc}</p>' if soc else ''}</div>
    <div><h2>Il sito</h2><p><a href="{u('/storia')}">La storia</a><br><a href="{u('/galleria')}">Galleria</a><br><a href="{u('/marchi')}">Le case</a><br><a href="{u('/privacy-policy')}">Privacy</a></p></div>
  </div>
  <p class="firma">© {ANNO} {a['ragione']}{piva} · Sito realizzato da <a href="https://freezestudio.it/" target="_blank" rel="noopener">Freeze Studio</a></p>
</footer>
<nav class="barra-mobile" aria-label="Contatti rapidi"><a href="tel:{a['tel_link']}">Chiama</a><a href="{u('/contatti')}#scrivici">Scrivici</a><a href="{u('/contatti')}#mappa">Dove siamo</a></nav>
<dialog class="luce-box" data-box aria-label="Foto ingrandita"><button type="button" class="chiudi" data-chiudi aria-label="Chiudi">×</button><button type="button" class="vai prec" data-prec aria-label="Foto precedente">‹</button><img alt=""><button type="button" class="vai succ" data-succ aria-label="Foto successiva">›</button><p data-didascalia></p></dialog>'''

def pagina(slug, titolo, descr, corpo, attiva=None, su_foto=False, schema_ld=False, prima_foto=''):
    file = {'/': 'index'}.get(slug, slug.strip('/')) + '.html'
    url = BASE + slug
    robots = '' if PUBBLICO else '<meta name="robots" content="noindex,nofollow">'
    ld = f'<script type="application/ld+json">{schema()}</script>' if schema_ld else ''
    (QUI / file).write_text(f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titolo)}</title>
<meta name="description" content="{e(descr, quote=True)}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="it_IT"><meta property="og:site_name" content="{AZIENDA['marchio']}">
<meta property="og:title" content="{e(titolo, quote=True)}"><meta property="og:description" content="{e(descr, quote=True)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/og.jpg">
<meta name="theme-color" content="#2B2D30">
<link rel="icon" href="{u('/favicon.ico')}" sizes="any"><link rel="icon" type="image/svg+xml" href="{u('/assets/logo/icona.svg')}"><link rel="apple-touch-icon" href="{u('/assets/logo/icona-180.png')}">
<link rel="preload" href="{u('/assets/font/cormorant.woff2')}" as="font" type="font/woff2" crossorigin><link rel="preload" href="{u('/assets/font/jost.woff2')}" as="font" type="font/woff2" crossorigin>
{prima_foto}
<link rel="stylesheet" href="{u('/assets/sito.css')}?v={VERSIONE}">
<script>document.documentElement.classList.add('js')</script>
{ld}
</head>
<body>
{intestazione(attiva, su_foto)}
<main id="contenuto">
{corpo}
</main>
{piede()}
<script src="{u('/assets/sito.js')}?v={VERSIONE}" defer></script>
</body>
</html>
''', encoding='utf-8')

def home():
    mondi = ''.join(
        f'<article class="mondo mondo-{i}"><a class="accende" href="{u("/galleria")}" tabindex="-1" aria-hidden="true">{foto(n, (800, 1400), alt, "(max-width:760px) 100vw, 50vw")}</a><div><h3>{t}</h3><p>{d}</p></div></article>'
        for i, (n, t, d, alt) in enumerate(MONDI, 1))
    serv = ''.join(f'<div class="servizio"><h3>{t}</h3><p>{d}</p></div>' for t, d in SERVIZI)
    tess = ''.join(tessera(n) for n in ['0471', '0466', '0470', '0472'])
    a = AZIENDA
    corpo = f'''<section class="hero">
  <picture><source media="(max-width:760px)" srcset="{u('/assets/img/hero-m-800.webp')} 800w, {u('/assets/img/hero-m-1200.webp')} 1200w" sizes="100vw"><img class="hero-foto" src="{u('/assets/img/hero-2400.webp')}" srcset="{u('/assets/img/hero-1000.webp')} 1000w, {u('/assets/img/hero-1800.webp')} 1800w, {u('/assets/img/hero-2400.webp')} 2400w" sizes="100vw" alt="Lampadario in cristallo con cerchio dorato, acceso nello showroom" fetchpriority="high"></picture>
  <div class="hero-testo">
    {filo()}
    <p class="corsivo grande">dal 1950</p>
    <h1>La luce che arreda.</h1>
    <p class="hero-sotto">Lampadari, illuminazione e arredamento nel nostro showroom di Misterbianco.</p>
    <div class="azioni">{bottone('Vieni in showroom', u('/contatti'))}<a class="link-oro" href="{u('/galleria')}">Guarda la galleria</a></div>
  </div>
</section>

<section class="sezione due-colonne storia-breve">
  <figure class="accende storia-foto">{foto('storica', (800, 1600), 'Il negozio in una foto d’epoca: pentole appese, piatti e un uomo sulla porta', '(max-width:760px) 100vw, 55vw')}<figcaption><span class="corsivo">dal 1950</span></figcaption></figure>
  <div class="storia-testo">
    {filo()}
    <h2>Dal 1950 al vostro fianco</h2>
    <p>Azienda storica, nata dalla passione per la luce e dall’esperienza maturata nell’illuminazione e nel materiale elettrico.</p>
    <p>Da allora accompagniamo privati, professionisti e attività commerciali nella scelta più adatta a valorizzare ogni ambiente.</p>
    <a class="link-oro" href="{u('/storia')}">Leggi la nostra storia</a>
  </div>
</section>

<section class="sezione scura">
  <header class="titolo-sezione">{filo()}<h2>Cosa trovi in showroom</h2></header>
  <div class="mondi">{mondi}</div>
</section>

<section class="sezione servizi-blocco">
  <header class="titolo-sezione">{filo()}<h2>Dalla scelta al progetto</h2><p>Progettazione, fornitura e consulenza illuminotecnica per ambienti residenziali e professionali.</p></header>
  <div class="servizi">{serv}</div>
</section>

<section class="sezione scura">
  <header class="titolo-sezione">{filo()}<h2>Galleria</h2></header>
  {coppia_apertura()}
  <div class="tessere tessere-4">{tess}</div>
  <p class="centro">{bottone('Tutta la galleria', u('/galleria'), 'btn btn-vuoto')}</p>
</section>

<section class="sezione">
  <header class="titolo-sezione">{filo()}<h2>Le case che trovi da noi</h2><p>Tocca il nome di una casa per aprire il suo sito.</p></header>
  {griglia_marchi()}
</section>

<section class="visita">
  <div class="accende visita-foto">{foto('gocce', (800, 1200), 'Sospensioni a goccia accese nello showroom', '100vw')}</div>
  <div class="visita-testo">
    {filo()}
    <h2>La luce va vista accesa.</h2>
    <p>{a['via']}, {a['cap']} {a['citta']} ({a['prov']})</p>
    <div class="azioni">{bottone('Come raggiungerci', u('/contatti') + '#mappa')}<a class="link-oro" href="tel:{a['tel_link']}">{a['tel']}</a></div>
  </div>
</section>'''
    pre = f'<link rel="preload" as="image" media="(max-width:760px)" href="{u("/assets/img/hero-m-800.webp")}"><link rel="preload" as="image" media="(min-width:761px)" href="{u("/assets/img/hero-1800.webp")}">'
    pagina('/', f'{AZIENDA["marchio"]} | Lampadari e arredamento a Misterbianco', 'Dal 1950 lampadari, illuminazione e arredamento: showroom a Misterbianco (CT), in Corso Carlo Marx 24, con consulenza e progettazione della luce.', corpo, '/', True, True, pre)

def apertura(titolo, sotto='', corsivo=''):
    c = f'<p class="corsivo grande">{corsivo}</p>' if corsivo else ''
    s = f'<p>{sotto}</p>' if sotto else ''
    return f'<header class="apertura">{filo()}{c}<h1>{titolo}</h1>{s}</header>'

def storia():
    corpo = apertura('La nostra storia', corsivo='dal 1950') + f'''
<section class="sezione-stretta">{coppia_apertura()}</section>
<section class="sezione testo-lungo">
  <h2>Le nostre origini</h2>
  <p>Azienda storica attiva dal 1950, 3F nasce dalla passione per la luce e dall’esperienza maturata nel settore dell’illuminazione e del materiale elettrico. Nel corso degli anni abbiamo accompagnato privati, professionisti e attività commerciali nella scelta delle soluzioni più adatte per valorizzare ogni ambiente.</p>
  <p>Grazie alla collaborazione con importanti case del settore e a una costante attenzione alla qualità e all’innovazione, offriamo prodotti affidabili e soluzioni pensate per unire funzionalità, design ed efficienza energetica.</p>
</section>
<section class="sezione scura">
  <div class="tre-testi">
    <div>{filo()}<h2>La nostra missione</h2><p>Offrire soluzioni di qualità che sappiano coniugare estetica, funzionalità ed efficienza. Selezioniamo ogni giorno prodotti affidabili e innovativi, per abitazioni, attività commerciali e spazi professionali.</p></div>
    <div>{filo()}<h2>Dove guardiamo</h2><p>Al futuro dell’illuminazione, con attenzione all’innovazione tecnologica e alla sostenibilità ambientale: soluzioni moderne ed efficienti, che migliorano il comfort degli ambienti e ne riducono i consumi.</p></div>
    <div>{filo()}<h2>Le persone</h2><p>Dietro 3F c’è un gruppo di professionisti che mette passione, competenza ed esperienza al servizio del cliente: dalla scelta dei prodotti fino alla realizzazione del progetto.</p></div>
  </div>
</section>
<section class="sezione centro">
  <h2 class="titolo-medio">Vieni a conoscerci in showroom</h2>
  <div class="azioni azioni-centro">{bottone('Contatti e indirizzo', u('/contatti'))}<a class="link-oro" href="{u('/galleria')}">Guarda la galleria</a></div>
</section>'''
    pagina('/storia', f'La nostra storia | {AZIENDA["breve"]} Finocchiaro Home', 'Attivi dal 1950 nell’illuminazione: la storia di 3F, dal primo negozio allo showroom di Misterbianco.', corpo, '/storia')

def galleria():
    tess = ''.join(tessera(n) for n in GALLERIA)
    corpo = apertura('Galleria', 'Lo showroom di Misterbianco, tra lampadari, sospensioni e arredi.') + f'''
<section class="sezione-stretta">{coppia_apertura()}<div class="tessere">{tess}</div></section>
<section class="sezione centro"><h2 class="titolo-medio">Dal vivo è un’altra luce</h2><div class="azioni azioni-centro">{bottone('Vieni in showroom', u('/contatti'))}</div></section>'''
    pagina('/galleria', f'Galleria dello showroom | {AZIENDA["breve"]} Finocchiaro Home', 'Le foto dello showroom di Misterbianco: lampadari in cristallo, sospensioni, luci a LED e arredamento.', corpo, '/galleria')

def case():
    corpo = apertura('Le case', 'I marchi che trovi nel nostro showroom. Tocca il nome di una casa per aprire il suo sito.') + f'''
<section class="sezione-stretta">{griglia_marchi()}</section>
<section class="sezione centro"><h2 class="titolo-medio">Cerchi un modello preciso?</h2><div class="azioni azioni-centro">{bottone('Scrivici', u('/contatti') + '#scrivici')}<a class="link-oro" href="tel:{AZIENDA['tel_link']}">{AZIENDA['tel']}</a></div></section>'''
    pagina('/marchi', f'Le case che trovi in showroom | {AZIENDA["breve"]} Finocchiaro Home', 'Sikrea, Icone, Ideal Lux, Redo Group, Illuminati, Ondaluce, Cangini & Tucci e altre case di illuminazione nello showroom di Misterbianco.', corpo, '/marchi')

def contatti():
    a = AZIENDA
    orari = f'<div><h2>Orari</h2>{"".join(f"<p>{e(g)}<br>{e(o)}</p>" for g, o in a["orari"])}</div>' if a['orari'] else ''
    wa = f'<p><a href="https://wa.me/{a["whatsapp"]}">Scrivici su WhatsApp</a></p>' if a['whatsapp'] else ''
    indirizzo_q = 'Corso+Carlo+Marx+24,+95045+Misterbianco+CT'
    corpo = apertura('Contatti', 'Hai bisogno di informazioni sui prodotti o di una consulenza per il tuo progetto? Ti rispondiamo il prima possibile.') + f'''
<section class="sezione-stretta contatti">
  <form class="modulo" id="scrivici" action="https://formsubmit.co/ajax/{a['email']}" method="post" data-modulo novalidate>
    <h2>Scrivici</h2>
    <div class="campo"><label for="nome">Nome e cognome</label><input id="nome" name="nome" autocomplete="name" required></div>
    <div class="campo"><label for="telefono">Telefono</label><input id="telefono" name="telefono" type="tel" autocomplete="tel" inputmode="tel"></div>
    <div class="campo"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
    <div class="campo"><label for="messaggio">Di cosa hai bisogno</label><textarea id="messaggio" name="messaggio" rows="5" required></textarea></div>
    <input type="text" name="_honey" class="nascosto" tabindex="-1" autocomplete="off" aria-hidden="true">
    <input type="hidden" name="_subject" value="Nuova richiesta dal sito"><input type="hidden" name="_template" value="table"><input type="hidden" name="_captcha" value="false">
    <label class="spunta"><input type="checkbox" name="privacy" value="letta" required><span>Ho letto la <a href="{u('/privacy-policy')}" target="_blank" rel="noopener">privacy policy</a></span></label>
    <button class="btn" type="submit">Invia la richiesta</button>
    <p class="esito" data-esito role="status" tabindex="-1"></p>
    <noscript><p>Per inviare il modulo serve JavaScript: scrivici a <a href="mailto:{a['email']}">{a['email']}</a>.</p></noscript>
  </form>
  <div class="recapiti">
    <div><h2>Showroom</h2><p>{a['via']}<br>{a['cap']} {a['citta']} ({a['prov']})</p></div>
    {orari}
    <div><h2>Telefono</h2><p><a href="tel:{a['tel_link']}">{a['tel']}</a></p>{wa}</div>
    <div><h2>Email</h2><p><a href="mailto:{a['email']}">{a['email']}</a></p></div>
  </div>
</section>
<section class="sezione-stretta" id="mappa">
  <div class="mappa" data-mappa data-src="https://www.google.com/maps?q={indirizzo_q}&amp;output=embed">
    <p>La mappa arriva da Google e si carica solo se la apri.</p>
    <div class="azioni azioni-centro"><button class="btn" type="button" data-apri-mappa>Mostra la mappa</button><a class="link-oro" href="https://www.google.com/maps/search/?api=1&amp;query={indirizzo_q}" target="_blank" rel="noopener">Apri in Google Maps</a></div>
  </div>
</section>'''
    pagina('/contatti', f'Contatti | {AZIENDA["breve"]} Finocchiaro Home, Misterbianco', 'Showroom in Corso Carlo Marx 24, Misterbianco (CT). Telefono 095 673 0772. Scrivici per informazioni o per una consulenza.', corpo, '/contatti')

def privacy():
    a = AZIENDA
    piva = f', P.IVA {a["piva"]}' if a['piva'] else ''
    corpo = apertura('Privacy policy') + f'''
<section class="sezione testo-lungo legale">
  <p>Questa pagina spiega come trattiamo i dati di chi visita il sito, secondo il Regolamento UE 2016/679 (GDPR).</p>
  <h2>Titolare del trattamento</h2>
  <p>{a['ragione']}{piva}, {a['via']}, {a['cap']} {a['citta']} ({a['prov']}). Email: <a href="mailto:{a['email']}">{a['email']}</a>, telefono {a['tel']}.</p>
  <h2>Quali dati raccogliamo</h2>
  <p>Solo quelli che ci scrivi nel modulo di contatto: nome, email, telefono se lo indichi, e il tuo messaggio. Li usiamo per risponderti e per gestire la tua richiesta. La base giuridica è la tua richiesta stessa (art. 6, par. 1, lett. b del GDPR).</p>
  <p>Il sito non usa cookie di profilazione né strumenti di statistica. Font e foto sono caricati dal nostro sito, senza servizi esterni.</p>
  <h2>Chi tratta i dati per nostro conto</h2>
  <p>Il modulo viene recapitato alla nostra casella email tramite il servizio FormSubmit. Il sito è ospitato su GitHub Pages, che registra dati tecnici di navigazione come l’indirizzo IP per ragioni di sicurezza. Questi fornitori possono trattare i dati anche fuori dall’Unione europea, con le garanzie previste dal GDPR.</p>
  <h2>Mappa</h2>
  <p>La mappa di Google si carica solo se scegli di aprirla. Da quel momento Google può raccogliere dati e usare cookie secondo la propria informativa. I bottoni delle case aprono i siti dei produttori, che hanno proprie informative.</p>
  <h2>Per quanto tempo</h2>
  <p>Conserviamo le richieste per il tempo necessario a gestirle e per eventuali obblighi di legge. Se diventi cliente, si applicano i tempi previsti per i documenti fiscali.</p>
  <h2>I tuoi diritti</h2>
  <p>Puoi chiederci in ogni momento di accedere ai tuoi dati, correggerli, cancellarli, limitarne l’uso od opporti al trattamento, scrivendo a <a href="mailto:{a['email']}">{a['email']}</a>. Puoi anche presentare reclamo al Garante per la protezione dei dati personali.</p>
  <p class="nota">Ultimo aggiornamento: {datetime.date.today().strftime('%d/%m/%Y')}</p>
</section>'''
    pagina('/privacy-policy', f'Privacy policy | {AZIENDA["breve"]} Finocchiaro Home', 'Come trattiamo i dati di chi visita il sito e di chi ci scrive.', corpo)

def extra():
    corpo = apertura('Qui la luce è spenta', 'La pagina che cerchi non c’è, o ha cambiato indirizzo.') + f'<section class="sezione centro"><div class="azioni azioni-centro">{bottone("Torna alla home", u("/") or "/")}<a class="link-oro" href="{u("/contatti")}">Contatti</a></div></section>'
    pagina('/404', f'Pagina non trovata | {AZIENDA["breve"]}', 'Pagina non trovata.', corpo)
    # I vecchi indirizzi di Wix continuano a funzionare
    for vecchio, nuovo in {'about-us': '/storia', 'projects': '/galleria', 'get-a-quote': '/contatti'}.items():
        (QUI / f'{vecchio}.html').write_text(f'<!doctype html><html lang="it"><meta charset="utf-8"><title>Pagina spostata</title><meta name="robots" content="noindex"><link rel="canonical" href="{BASE}{nuovo}"><meta http-equiv="refresh" content="0;url={u(nuovo)}"><p><a href="{u(nuovo)}">La pagina si è spostata: vai qui</a></p></html>\n', encoding='utf-8')
    pagine = ['/', '/storia', '/galleria', '/marchi', '/contatti', '/privacy-policy']
    (QUI / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{BASE}{p}</loc></url>\n' for p in pagine) + '</urlset>\n', encoding='utf-8')
    (QUI / 'robots.txt').write_text((f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n' if PUBBLICO else 'User-agent: *\nDisallow: /\n'), encoding='utf-8')

if __name__ == '__main__':
    home(); storia(); galleria(); case(); contatti(); privacy(); extra()
    print('Fatto:', sorted(p.name for p in QUI.glob('*.html')))
