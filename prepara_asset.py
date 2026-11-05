#!/usr/bin/env python3
"""Prepara foto, loghi dei marchi, font e icone per il sito. Si rilancia solo se cambiano gli originali."""
import pathlib, subprocess, shutil, sys
from PIL import Image, ImageEnhance, ImageOps, ImageFilter, ImageChops
Image.MAX_IMAGE_PIXELS = None
QUI = pathlib.Path(__file__).parent
CLIENTE = QUI.parent.parent
FOTO = CLIENTE / 'Foto/3F foto sito corrette/Per il sito (2560 px)'
A = QUI / 'assets'; IMG = A / 'img'; MAR = A / 'marchi'; FNT = A / 'font'
for d in (IMG, MAR, FNT): d.mkdir(parents=True, exist_ok=True)

def f(n): return next(FOTO.glob(f'*-{n}.jpg'))

def tono(im, sat=.86, con=1.04):
    """Toni un po' piu' sobri e caldi: le pareti colorate del negozio non devono rubare la scena."""
    im = ImageEnhance.Color(im).enhance(sat); im = ImageEnhance.Contrast(im).enhance(con)
    r, g, b = im.split(); r = r.point(lambda v: min(255, int(v * 1.02))); b = b.point(lambda v: int(v * .96))
    return Image.merge('RGB', (r, g, b))

def salva(im, nome, larg, q=78):
    im = im.copy(); im.thumbnail((larg, larg * 3), Image.LANCZOS)
    p = IMG / f'{nome}-{larg}.webp'; im.save(p, 'WEBP', quality=q, method=6)
    return im.size

# nome: (foto, ritaglio l,t,r,b in frazioni, larghezze, saturazione)
TAGLI = {
 'storica':     ('0486-foto-storica', (0, 0, 1, 1), (800, 1600), 0),
 'frontale':    ('0481', (0.17, 0.0, 1.0, 0.98), (800, 1400), .9),
}
GALLERIA = ['0461','0462','0471','0473','0466','0470','0464','0468','0467','0472','0455','0463','0456','0458','0459','0460','0465','0469','0474','0475','0476','0477','0478','0485']

def prepara_foto():
    dim = {}
    for nome, (n, t, larghe, sat) in TAGLI.items():
        im = Image.open(f(n)).convert('RGB'); W, H = im.size
        im = im.crop((int(t[0]*W), int(t[1]*H), int(t[2]*W), int(t[3]*H)))
        im = ImageOps.grayscale(im).convert('RGB') if sat == 0 else tono(im, sat)
        for l in larghe: dim[nome] = salva(im, nome, l)
    for n in GALLERIA:
        im = tono(Image.open(f(n)).convert('RGB'), .92, 1.02)
        for l in (640, 1600): salva(im, f'g{n}', l, 76)
    return dim


# Pezzi che escono dal buio: foto vere a piena risoluzione, con la stanza intorno abbassata di luce.
# nome: (foto, ritaglio l,t,r,b, centro e raggi della luce in frazioni del ritaglio cx,cy,rx,ry, forza del buio)
PEZZI = {
 'p-cristallo':  ('0461', (.26,.04,.76,.94), (.5,.44,.46,.56), .12),
 'p-tamburo':    ('0476', (.0,.13,.64,.80), (.45,.45,.56,.48), .12),
 'p-specchi':    ('0477', (.08,.08,.96,.82), (.52,.5,.5,.5), .12),
 'p-disco':      ('0462', (.14,.08,.88,.92), (.5,.46,.5,.52), .16),
 'p-gocce':      ('0466', (.1,.1,.88,.84), (.5,.5,.52,.56), .12),
 'p-ovale':      ('0473', (.0,.02,1.0,.92), (.5,.52,.56,.56), .14),
 'p-specchio':   ('0470', (.24,.26,.78,1.0), (.5,.55,.5,.5), .12),
 'p-ambra':      ('0465', (.3,.03,.96,.62), (.55,.52,.52,.58), .14),
 'p-sfere':      ('0469', (.0,.1,1.0,.98), (.55,.48,.56,.56), .14),
 'p-led':        ('0472', (.0,.0,1.0,.82), (.55,.42,.6,.56), .2),
 'p-anello':     ('0460', (.2,.28,.76,.72), (.46,.5,.56,.56), .12),
 'p-linea':      ('0471', (.1,.02,.86,.86), (.5,.5,.56,.56), .18),
 'p-applique':   ('0475', (.62,.04,1.0,.96), (.5,.5,.56,.54), .12),
 'p-tavolo':     ('0458', (.16,.2,.84,.9), (.5,.5,.54,.54), .12),
 'p-paralumi':   ('0456', (.46,.24,.98,.84), (.5,.5,.54,.54), .12),
 'p-divano':     ('0455', (.2,.4,.92,1.0), (.5,.58,.58,.56), .14),
 'p-parete':     ('0478', (.0,.04,.44,.92), (.5,.5,.58,.56), .12),
 'p-salone':     ('0463', (.0,.14,1.0,1.0), (.55,.55,.6,.6), .14),
 'h-1':          ('0461', (.0,.0,.82,.76), (.62,.5,.5,.72), .14),
 'h-2':          ('0462', (.0,.02,1.0,.8), (.6,.42,.5,.72), .16),
 'h-3':          ('0471', (.0,.0,1.0,.82), (.56,.46,.54,.76), .18),
 'h-4':          ('0465', (.0,.0,1.0,.66), (.62,.52,.5,.76), .14),
}

def buio(im, cx, cy, rx, ry, resto=.12):
    W, H = im.size
    pic = Image.new('L', (W // 8, H // 8), 0); w, h = pic.size
    px = pic.load()
    for y in range(h):
        for x in range(w):
            d = ((x / w - cx) / rx) ** 2 + ((y / h - cy) / ry) ** 2
            v = 1.0 if d < .3 else max(0.0, 1 - (d - .3) / 1.15)
            px[x, y] = int(255 * v * v * (3 - 2 * v))
    m = pic.resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(W // 60))
    scura = ImageEnhance.Brightness(ImageEnhance.Color(im).enhance(.25)).enhance(resto)
    # fondo un po' verso l'antracite, non nero puro
    scura = Image.blend(scura, Image.new('RGB', im.size, (33, 35, 38)), .34)
    return Image.composite(im, scura, m)

def prepara_pezzi():
    FULL = CLIENTE / 'Foto/3F foto sito corrette'
    for nome, (n, t, sp, r) in PEZZI.items():
        im = Image.open(FULL / f'IMG_{n}.jpg').convert('RGB'); W, H = im.size
        im = im.crop((int(t[0]*W), int(t[1]*H), int(t[2]*W), int(t[3]*H))); im.thumbnail((2400, 2400), Image.LANCZOS)
        im = tono(im, .92, 1.08); im = buio(im, *sp, r)
        for l in ((1000, 1900) if nome.startswith('h-') else (800, 1500)): salva(im, nome, l, 80)

def bianco(sorgente, nome, soglia=None, larg=480):
    """Logo bianco su trasparente, tagliato ai bordi."""
    im = Image.open(sorgente).convert('RGBA')
    a = im.getchannel('A')
    if soglia is not None:  # sfondo bianco pieno: l'alfa viene dalla luminosita'
        a = ImageOps.invert(ImageOps.grayscale(im.convert('RGB'))).point(lambda v: min(255, int(v * soglia)))
    out = Image.new('RGBA', im.size, (255, 255, 255, 0)); out.putalpha(a)
    bb = a.point(lambda v: 255 if v > 12 else 0).getbbox(); out = out.crop(bb)
    if out.width > larg: out.thumbnail((larg, larg), Image.LANCZOS)
    out.save(MAR / f'{nome}.png', optimize=True)
    return out.size

def prepara_marchi(cartella_extra):
    P = CLIENTE / 'Grafiche/3F partner'; X = pathlib.Path(cartella_extra)
    print(bianco(P/'3.png', 'ideal-lux'), bianco(P/'4.png', 'redo'), bianco(P/'5.png', 'illuminati'), bianco(P/'6.png', 'exclusive-light'), bianco(P/'7.png', 'ondaluce'))
    print(bianco(X/'logo-bianco.png', 'cangini-tucci'), bianco(X/'sikrea.png', 'sikrea'), bianco(X/'logo.png', 'icone'))

def prepara_font(fonti):
    testo = 'U+0020-007E,U+00A0-00FF,U+2013,U+2014,U+2018,U+2019,U+201C,U+201D,U+2026,U+20AC,U+2197'
    for sorg, dest in (('CormorantGaramond[wght].ttf','cormorant'),('CormorantGaramond-Italic[wght].ttf','cormorant-italic'),('Jost[wght].ttf','jost'),('Italianno-Regular.ttf','italianno')):
        subprocess.run([sys.executable,'-m','fontTools','subset',str(pathlib.Path(fonti)/sorg),f'--unicodes={testo}','--flavor=woff2','--layout-features=*',f'--output-file={FNT/(dest+".woff2")}'],check=True)

if __name__ == '__main__':
    cosa = sys.argv[1]
    if cosa == 'foto': print(prepara_foto())
    if cosa == 'pezzi': prepara_pezzi()
    if cosa == 'marchi': prepara_marchi(sys.argv[2])
    if cosa == 'font': prepara_font(sys.argv[2])
