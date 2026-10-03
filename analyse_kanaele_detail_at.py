# -*- coding: utf-8 -*-
"""Kontaktkanaele im Detail, mit Grafiken. Oesterreich.

Aufruf:  python3 analyse_kanaele_detail_at.py [--png]

Geht ueber die Reichweitentabelle hinaus und beantwortet die Fragen, die fuer
eine Kanalentscheidung zaehlen:

  1  Exklusive Reichweite - wen erreicht ein Kanal, den sonst keiner erreicht
  2  Reichweitenaufbau - welcher Kanal bringt wie viel zusaetzlich dazu
  3  Ueberlappung - welche Kanaele treffen dieselben Menschen
  4  Zielgruppenindex - wen ein Kanal ueber- und unterdurchschnittlich erreicht
  5  Kanalkombinationen und ihr Zusammenhang mit dem Funnel

Schreibt ERGEBNISSE_AT_kanaele_detail.txt, die Grafiken als SVG nach
grafiken/ und mit --png zusaetzlich als PNG (benoetigt Chromium).

Alles bezieht sich auf die 287 NEOH-Kenner: Nur sie wurden gefragt. Die
Reichweiten sind Reichweiten innerhalb dieser Gruppe, keine Reichweiten in
der Bevoelkerung.
"""
import csv, io, os, subprocess, sys, itertools
import numpy as np

DATEN = 'NEOH_AT_analyse.csv'
AUS_TXT = 'ERGEBNISSE_AT_kanaele_detail.txt'
GRAFIK = 'grafiken'

KANAL = {1: 'TV-Werbung', 2: 'Printwerbung', 3: 'Werbung auf Websites',
         4: 'Instagram/Facebook', 5: 'YouTube', 6: 'TikTok',
         7: 'Influencer', 8: 'Supermarkt', 9: 'Mundpropaganda',
         10: 'Außenwerbung'}
ALTER = ['18 bis 29 Jahre', '30 bis 39 Jahre', '40 bis 49 Jahre',
         '50 bis 59 Jahre', '60 Jahre und älter']
ALTER_KURZ = ['18–29', '30–39', '40–49', '50–59', '60+']

INK, INK2, MUTED = '#0b0b0b', '#52514e', '#898781'
GRID, BASE, FLAECHE = '#e1e0d9', '#c3c2b7', '#fdfdfc'
AKZENT = '#2a78d6'
# Divergierende Paare fuer den Index: blau (ueber) gegen rot (unter),
# neutraler Grauton in der Mitte - kein Farbton am Nullpunkt.
DIV_HOCH = ['#cde2fb', '#9ec5f4', '#5598e7', '#256abf', '#0d366b']
DIV_NIED = ['#f6d5d5', '#eaa9a9', '#d96d6d', '#b93a3a', '#8a2020']
NEUTRAL = '#f0efec'

zeilen = []
def sag(z=''):
    zeilen.append(z)
    print(z)


def de(v, dec=1):
    return ('%.*f' % (dec, v)).replace('.', ',')


def main():
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    k = [r for r in d if r['neoh_bekannt'] == '1']
    w = np.array([float(r['gewicht_quote']) for r in k])
    M = np.array([[r['kanal_%d' % i] == '1' for i in range(1, 11)] for r in k])
    erw = np.array([r['neoh_betracht'] == '1' for r in k], dtype=bool)
    n = len(k)
    anteil = lambda m: 100 * float(w[m].sum() / w.sum())

    sag('KONTAKTKANAELE IM DETAIL - OESTERREICH')
    sag('=' * 78)
    sag('Basis: %d NEOH-Kenner, davon %d mit mindestens einem Kontakt im letzten'
        % (n, int(M.any(1).sum())))
    sag('Monat. Alle Reichweiten gelten innerhalb der Kenner, nicht in der')
    sag('Bevoelkerung - gefragt wurden nur Kenner.')
    sag('')

    # ---------------------------------------------------------------- 1
    sag('1. EXKLUSIVE REICHWEITE')
    sag('-' * 78)
    sag('Wie viele Kenner erreicht ein Kanal, die ueber keinen anderen Kanal')
    sag('erreicht werden? Das ist die Frage, die ueber Streichen oder Behalten')
    sag('entscheidet - nicht die Gesamtreichweite.')
    sag('')
    sag('%-22s %10s %12s %8s' % ('Kanal', 'gesamt', 'exklusiv', 'Anteil'))
    excl = {}
    for i in range(10):
        nur = M[:, i] & (M.sum(1) == 1)
        g, e = anteil(M[:, i]), anteil(nur)
        excl[i] = e
        sag('%-22s %9.1f%% %11.1f%% %7.0f%%'
            % (KANAL[i + 1], g, e, 100 * e / g if g else 0))
    sag('')
    sag('Der Supermarkt erreicht ein Viertel aller Kenner exklusiv. Websites und')
    sag('Influencer erreichen niemanden, der nicht ohnehin anders erreicht wird -')
    sag('ihre Gesamtreichweite ist vollstaendig gedeckt.')
    sag('')

    # ---------------------------------------------------------------- 2
    sag('2. REICHWEITENAUFBAU')
    sag('-' * 78)
    sag('Kanaele in der Reihenfolge ihres groessten zusaetzlichen Beitrags.')
    sag('')
    rest, erreicht, kum = set(range(10)), np.zeros(n, dtype=bool), []
    while rest:
        best = max(rest, key=lambda i: w[M[:, i] & ~erreicht].sum())
        zu = anteil(M[:, best] & ~erreicht)
        erreicht = erreicht | M[:, best]
        rest.discard(best)
        kum.append((KANAL[best + 1], zu, anteil(erreicht)))
    sag('%-22s %12s %14s' % ('Kanal', 'zusätzlich', 'kumuliert'))
    for nm, zu, ges in kum:
        sag('%-22s %+11.1f Pp. %13.1f%%' % (nm, zu, ges))
    sag('')
    sag('Zwei Kanaele - Supermarkt und Instagram/Facebook - decken %s %% der'
        % de(kum[1][2], 0))
    sag('erreichbaren Kenner ab. Die uebrigen acht bringen zusammen %s Punkte.'
        % de(kum[-1][2] - kum[1][2]))
    sag('')

    # ---------------------------------------------------------------- 3
    sag('3. UEBERLAPPUNG')
    sag('-' * 78)
    sag('Anteil der Kenner mit Kontakt in beiden Kanaelen, in Prozent.')
    sag('')
    gross = [i for i in range(10) if M[:, i].sum() >= 20]
    sag('%-18s' % '' + ''.join('%9s' % KANAL[i + 1][:8] for i in gross))
    ueber = np.zeros((len(gross), len(gross)))
    for a, i in enumerate(gross):
        zeile = '%-18s' % KANAL[i + 1][:18]
        for b, j in enumerate(gross):
            v = anteil(M[:, i] & M[:, j])
            ueber[a, b] = v
            zeile += '%8.1f%%' % v if i != j else '%9s' % '—'
        sag(zeile)
    sag('')

    # ---------------------------------------------------------------- 4
    sag('4. ZIELGRUPPENINDEX NACH ALTER')
    sag('-' * 78)
    sag('Index 100 = Reichweite des Kanals unter allen Kennern. 150 heisst:')
    sag('In dieser Altersgruppe erreicht der Kanal anderthalbmal so viele.')
    sag('Ein Punkt steht fuer eine Zelle mit weniger als fuenf Kontakten - dort')
    sag('waere jeder Index eine Scheingenauigkeit.')
    sag('')
    idx = np.full((10, len(ALTER)), np.nan)
    sag('%-22s' % '' + ''.join('%9s' % a for a in ALTER_KURZ))
    for i in range(10):
        if M[:, i].sum() < 15:
            continue
        basis = anteil(M[:, i])
        zeile = '%-22s' % KANAL[i + 1]
        for j, a in enumerate(ALTER):
            sel = np.array([r['alter_txt'] == a for r in k], dtype=bool)
            if sel.sum() < 20:
                zeile += '%9s' % '–'
                continue
            if int((M[:, i] & sel).sum()) < 5:
                zeile += '%9s' % '·'          # Zelle zu duenn besetzt
                continue
            r_ = 100 * w[M[:, i] & sel].sum() / w[sel].sum()
            idx[i, j] = 100 * r_ / basis if basis else np.nan
            zeile += '%9.0f' % idx[i, j]
        sag(zeile)
    sag('')

    # ---------------------------------------------------------------- 5
    sag('5. KANALKOMBINATIONEN UND FUNNEL')
    sag('-' * 78)
    handel = M[:, 7]
    digital = M[:, [2, 3, 4, 5, 6]].any(1)
    komb = [('nur Handel', handel & ~digital), ('nur Digital', digital & ~handel),
            ('beides', handel & digital), ('weder noch', ~handel & ~digital)]
    sag('%-18s %6s %10s %12s' % ('', 'n', 'Anteil', 'erwägen'))
    for lab, m in komb:
        sag('%-18s %6d %9.1f%% %11.1f%%'
            % (lab, int(m.sum()), anteil(m), anteil(erw & m) / anteil(m) * 100 if m.sum() else 0))
    sag('')
    sag('Die Unterschiede sind nicht als Wirkung zu lesen (siehe')
    sag('ERGEBNISSE_AT_kanaele.md, Abschnitt 3) - die Zahl der Kanaele traegt')
    sag('zur Erwaegung nichts bei, sobald das Markenurteil kontrolliert ist.')
    sag('')

    grafiken(kum, excl, idx, ueber, gross)
    sag('Grafiken: %s/kanaele_aufbau.svg, _index.svg, _ueberlappung.svg' % GRAFIK)
    sag('Geschrieben: %s' % AUS_TXT)
    io.open(AUS_TXT, 'w', encoding='utf-8').write('\n'.join(zeilen) + '\n')
    if '--png' in sys.argv:
        png()


# ------------------------------------------------------------------ Grafiken
def kopf(b, h, titel, unter):
    return ('<svg viewBox="0 0 %d %d" width="%d" height="%d" '
            'xmlns="http://www.w3.org/2000/svg" font-family="Helvetica,Arial,sans-serif">'
            '<rect width="%d" height="%d" fill="%s"/>'
            '<text x="26" y="34" font-size="17" font-weight="600" fill="%s">%s</text>'
            '<text x="26" y="54" font-size="12.5" fill="%s">%s</text>'
            % (b, h, b, h, b, h, FLAECHE, INK, titel, MUTED, unter))


def grafiken(kum, excl, idx, ueber, gross):
    os.makedirs(GRAFIK, exist_ok=True)

    # --- Reichweitenaufbau: Stufenkurve mit Zuwachsbalken
    B, H = 860, 470
    lb, rb, tb, bb = 170, 56, 86, 64
    s = [kopf(B, H, 'Reichweitenaufbau der Kontaktkanäle',
              'Kumulierte Reichweite unter den NEOH-Kennern, Kanäle nach größtem Zusatzbeitrag geordnet')]
    maxv = 85.0
    zh = (H - tb - bb) / len(kum)
    sx = lambda v: lb + (B - lb - rb) * v / maxv
    for g in range(0, int(maxv) + 1, 20):
        s.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="1"/>'
                 % (sx(g), tb - 8, sx(g), H - bb + 6, GRID))
        s.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="11" fill="%s">%d %%</text>'
                 % (sx(g), H - bb + 22, MUTED, g))
    vorher = 0.0
    for i, (nm, zu, ges) in enumerate(kum):
        y = tb + i * zh
        s.append('<text x="%d" y="%.1f" text-anchor="end" font-size="13" fill="%s">%s</text>'
                 % (lb - 12, y + zh / 2 + 4, INK2, nm))
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="%s"/>'
                 % (sx(0), y + zh * 0.22, sx(vorher) - sx(0), zh * 0.56, '#dfe4e7'))
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="%s"/>'
                 % (sx(vorher), y + zh * 0.22, max(1.2, sx(ges) - sx(vorher)), zh * 0.56, AKZENT))
        s.append('<text x="%.1f" y="%.1f" font-size="12" fill="%s" font-weight="600">%s %%</text>'
                 % (sx(ges) + 8, y + zh / 2 + 4, INK, de(ges, 0)))
        if zu >= 1.2:
            s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" fill="#ffffff">+%s</text>'
                     % ((sx(vorher) + sx(ges)) / 2, y + zh / 2 + 4, de(zu, 0)))
        vorher = ges
    s.append('<text x="26" y="%d" font-size="11.5" fill="%s">Blau: zusätzliche Reichweite '
             'dieses Kanals. Grau: bereits durch die darüberliegenden erreicht.</text>'
             % (H - 14, MUTED))
    s.append('</svg>')
    io.open('%s/kanaele_aufbau.svg' % GRAFIK, 'w', encoding='utf-8').write(''.join(s))

    # --- Zielgruppenindex als Heatmap
    # Nur Kanaele, die in der Mehrzahl der Altersgruppen tragen - sonst
    # zeigt die Grafik vor allem Luecken.
    reihen = [i for i in range(10) if (~np.isnan(idx[i])).sum() >= 3]
    B, H = 760, 132 + 38 * len(reihen)
    lb, zb = 200, 38
    s = [kopf(B, H, 'Wen welcher Kanal erreicht',
              'Index 100 = Reichweite des Kanals unter allen Kennern, '
              'Zellen unter fünf Kontakten bleiben leer')]
    bw = (B - lb - 40) / len(ALTER_KURZ)
    for j, a in enumerate(ALTER_KURZ):
        s.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="12" '
                 'font-weight="600" fill="%s">%s</text>' % (lb + bw * (j + .5), 80, INK2, a))
    for r, i in enumerate(reihen):
        y = 92 + r * zb
        s.append('<text x="%d" y="%.1f" text-anchor="end" font-size="13" fill="%s">%s</text>'
                 % (lb - 14, y + zb / 2 + 4, INK2, KANAL[i + 1]))
        for j in range(len(ALTER_KURZ)):
            v = idx[i, j]
            x = lb + bw * j
            if np.isnan(v):
                farbe, txt, tf = NEUTRAL, '–', MUTED
            else:
                ab = v - 100
                stufe = min(4, int(abs(ab) // 35))
                farbe = NEUTRAL if abs(ab) < 15 else (DIV_HOCH if ab > 0 else DIV_NIED)[stufe]
                txt, tf = '%d' % round(v), ('#ffffff' if stufe >= 3 and abs(ab) >= 15 else INK)
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" '
                     'stroke="%s" stroke-width="2"/>' % (x, y, bw, zb - 4, farbe, FLAECHE))
            s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="13" '
                     'font-weight="600" fill="%s">%s</text>' % (x + bw / 2, y + zb / 2 + 1, tf, txt))
    s.append('<text x="26" y="%d" font-size="11.5" fill="%s">Blau: überdurchschnittlich. '
             'Rot: unterdurchschnittlich. Grau: nahe dem Durchschnitt oder Basis zu klein.</text>'
             % (H - 14, MUTED))
    s.append('</svg>')
    io.open('%s/kanaele_index.svg' % GRAFIK, 'w', encoding='utf-8').write(''.join(s))

    # --- Ueberlappungsmatrix
    m = len(gross)
    B = 150 + 70 * m
    H = 110 + 46 * m
    s = [kopf(B, H, 'Überlappung der Kanäle',
              'Anteil der Kenner mit Kontakt in beiden Kanälen')]
    lb, zh2, bw2 = 150, 46, 70
    for j, jj in enumerate(gross):
        s.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="11.5" fill="%s">%s</text>'
                 % (lb + bw2 * (j + .5), 80, INK2, KANAL[jj + 1][:9]))
    maxv = max(ueber[a][b] for a in range(m) for b in range(m) if a != b) or 1
    for a in range(m):
        y = 92 + a * zh2
        s.append('<text x="%d" y="%.1f" text-anchor="end" font-size="12.5" fill="%s">%s</text>'
                 % (lb - 12, y + zh2 / 2 + 4, INK2, KANAL[gross[a] + 1][:17]))
        for b in range(m):
            x = lb + bw2 * b
            if a == b:
                s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" '
                         'stroke="%s" stroke-width="2"/>' % (x, y, bw2, zh2 - 4, NEUTRAL, FLAECHE))
                continue
            v = ueber[a][b]
            t = min(1.0, v / maxv)
            stufe = DIV_HOCH[min(4, int(t * 4.999))]
            s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" '
                     'stroke="%s" stroke-width="2"/>' % (x, y, bw2, zh2 - 4, stufe, FLAECHE))
            s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="12" '
                     'fill="%s">%s</text>' % (x + bw2 / 2, y + zh2 / 2 + 1,
                                              '#ffffff' if t > 0.55 else INK, de(v, 0)))
    s.append('</svg>')
    io.open('%s/kanaele_ueberlappung.svg' % GRAFIK, 'w', encoding='utf-8').write(''.join(s))


def png():
    js = """
const fs=require('fs');
function lade(){for(const p of ['playwright','/tmp/node_modules/playwright']){try{return require(p)}catch(e){}}
  throw new Error('playwright fehlt')}
function browser(){if(process.env.PW_BROWSER)return process.env.PW_BROWSER;
  const w='/opt/pw-browsers'; if(!fs.existsSync(w))return null;
  for(const d of fs.readdirSync(w).filter(x=>x.startsWith('chromium-')).sort().reverse()){
    const c=`${w}/${d}/chrome-linux/chrome`; if(fs.existsSync(c))return c} return null}
(async()=>{const {chromium}=lade(); let b;
  try{b=await chromium.launch()}catch(e){const x=browser(); if(!x)throw e; b=await chromium.launch({executablePath:x})}
  const p=await b.newPage({deviceScaleFactor:2});
  for(const f of fs.readdirSync('grafiken').filter(x=>x.endsWith('.svg'))){
    await p.goto('file://'+process.cwd()+'/grafiken/'+f);
    const el=await p.$('svg'); await el.screenshot({path:'grafiken/'+f.replace('.svg','.png')});
  }
  await b.close(); console.log('PNG geschrieben');})();
"""
    io.open('/tmp/_svg2png.js', 'w').write(js)
    subprocess.run(['node', '/tmp/_svg2png.js'], check=True)


if __name__ == '__main__':
    main()
