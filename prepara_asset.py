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
 'hero':        ('0461', (0.0, 0.0, 0.78, 0.74), (1000, 1800, 2400), .84),
 'hero-m':      ('0461', (0.14, 0.0, 0.72, 0.98), (800, 1200), .84),
 'lampadari':   ('0462', (0.0, 0.05, 0.82, 0.92), (800, 1400), .82),
 'design':      ('0471', (0.08, 0.0, 1.0, 0.88), (800, 1400), .9),
 'arredo':      ('0455', (0.0, 0.26, 1.0, 1.0), (800, 1400), .86),
 'sospensioni': ('0473', (0.0, 0.0, 1.0, 0.9), (800, 1200), .86),
 'storica':     ('0486-foto-storica', (0, 0, 1, 1), (800, 1600), 0),
 'frontale':    ('0481', (0.17, 0.0, 1.0, 0.98), (800, 1400), .9),
 'gocce':       ('0466', (0.08, 0.1, 0.92, 0.82), (800, 1200), .9),
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
    if cosa == 'marchi': prepara_marchi(sys.argv[2])
    if cosa == 'font': prepara_font(sys.argv[2])
