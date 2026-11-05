# Sito 3F Illuminazioni Finocchiaro Home

Sito statico (HTML, CSS, JS), senza Wix. Tutti i testi e i dati sono in `build.py`.

## Modificare
1. Cambia i dati in `build.py` (`AZIENDA`, `MARCHI`, `MONDI`, `SERVIZI`, `ALT_GALLERIA`).
2. Lancia `python3 build.py`.
3. Se cambi CSS o JS, aumenta `VERSIONE` in `build.py`.

Foto, loghi dei marchi e font si rigenerano con `prepara_asset.py`. Il logo si rigenera con `_lavoro/esporta_logo.py`.

## Anteprima
`python3 anteprima.py 4412`, poi http://localhost:4412

## Dati da ricevere dal cliente (in `AZIENDA`)
- `piva` e conferma di `ragione`
- `orari`
- `whatsapp`, `facebook`, `instagram`
- nome esatto e sito di Capo d'Arte; sito di Exclusive Light (in `MARCHI`)

## Andare online
Il sito ora ha `PUBBLICO = False`: non si fa indicizzare da Google.
1. Indirizzo di prova attuale: https://antoniofreeze.github.io/3f-sito/ (repo antoniofreeze/3f-sito, Pages da main). Per aggiornarlo: `PREFISSO=/3f-sito BASE=https://antoniofreeze.github.io/3f-sito python3 build.py`, poi commit e push.
2. Per il dominio: metti `PUBBLICO = True`, lancia `python3 build.py` senza variabili, aggiungi il file `CNAME` con `www.3filluminazione.com`.
3. Il dominio è registrato presso Wix (scade il 17/03/2027) e usa i DNS di Wix. In Wix: A @ → 185.199.108.153, .109, .110, .111; CNAME www → account GitHub + `.github.io`. La posta è su Libero: niente MX da conservare, ma controlla i record prima di cambiarli.
4. Attiva HTTPS su GitHub, invia una prova del modulo e clicca "Activate Form" nella mail di FormSubmit su 3filluminazione@libero.it.
5. Search Console: nuova proprietà e sitemap. Solo dopo si può disdire il piano Wix (trasferendo prima il dominio se non si vuole lasciarlo su Wix).
