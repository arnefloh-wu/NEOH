# -*- coding: utf-8 -*-
"""Erzeugt das interaktive Dashboard Oesterreich als eigenstaendige HTML-Datei.

Aufruf:  python3 dashboard_at.py

Die Seite enthaelt keine Falldaten, sondern einen vorberechneten Wuerfel aus
20 Zellen: Alter (5) x Geschlecht (2) x Zuckersegment (2). Die kleinste Zelle
hat 12 Faelle. Gefiltert wird im Browser durch Summieren der ausgewaehlten
Zellen - das haelt die Seite schnell und laesst keine Rueckschluesse auf
einzelne Befragte zu.

Die Region ist bewusst KEINE Filterdimension. Mit ihr haette der Wuerfel
60 Zellen, davon zwei mit einer einzigen Person - und die Analyse hat
gezeigt, dass die Stichprobe Regionalaussagen ohnehin nicht traegt
(ERGEBNISSE_AT_bekanntheit_demografie.md, Abschnitt 4). Sie erscheint
deshalb nur als Randverteilung in der Tabellenansicht.
"""
import csv, io, json, math
import numpy as np

DATEN = 'NEOH_AT_analyse.csv'
QSF = 'NEOH_AT_Sep2026.qsf'
AUS = 'DASHBOARD_AT.html'
NEOH = '13'
SLIDER = ['emotion_1', 'qualität_1', 'plv_1', 'zufriedenheit_1', 'wom_1']
SLIDER_LABEL = ['Emotionale Bindung', 'Qualität', 'Preis-Leistung',
                'Zufriedenheit', 'Weiterempfehlung']
NUTS1 = {'Wien': 'Ost', 'Niederösterreich': 'Ost', 'Burgenland': 'Ost',
         'Steiermark': 'Süd', 'Kärnten': 'Süd', 'Oberösterreich': 'West',
         'Salzburg': 'West', 'Tirol': 'West', 'Vorarlberg': 'West'}


def markennamen():
    d = json.load(io.open(QSF, encoding='utf-8'))
    for e in d['SurveyElements']:
        p = e.get('Payload')
        if e['Element'] == 'SQ' and isinstance(p, dict) and p.get('DataExportTag') == 'bekanntheit':
            rc = p['RecodeValues']
            return [(rc[str(k)], p['Choices'][str(k)]['Display'])
                    for k in p['ChoiceOrder'] if rc[str(k)] != '99']
    raise SystemExit('bekanntheit nicht gefunden')


def wuerfel():
    from analyse_segmente_text_at import marken_im_text
    d = list(csv.DictReader(io.open(DATEN, encoding='utf-8-sig')))
    marken = markennamen()
    codes = [c for c, _ in marken]

    # Hierarchische Bereinigung wie in Stufe 1
    for r in d:
        for c in codes:
            if r['bekanntheit_%s' % c] != '1':
                for stufe in ('betracht', 'kauf_3monate'):
                    r['%s_%s' % (stufe, c)] = '0'
        r['_u'] = 'NEOH' in (marken_im_text(r['spontan']) if r['spontan'].strip() else [])
        r['_seg'] = '1' if (r['zucker'].strip() and int(r['zucker']) >= 4) else '0'
        r['_reg'] = NUTS1.get(r['bundesland_txt'], '')

    zellen = {}
    for r in d:
        k = (r['alter'], r['geschlecht'], r['_seg'])
        z = zellen.setdefault(k, {
            'a': r['alter'], 'g': r['geschlecht'], 's': r['_seg'],
            'n': 0, 'w': 0.0, 'w2': 0.0, 'u': 0, 'uw': 0.0,
            'b': [[0, 0.0, 0, 0.0, 0, 0.0] for _ in codes],
            'sl': [[0, 0.0, 0.0] for _ in SLIDER]})
        w = float(r['gewicht_quote'])
        z['n'] += 1
        z['w'] += w
        z['w2'] += w * w
        if r['_u']:
            z['u'] += 1
            z['uw'] += w
        for i, c in enumerate(codes):
            if r['bekanntheit_%s' % c] == '1':
                z['b'][i][0] += 1
                z['b'][i][1] += w
            if r['betracht_%s' % c] == '1':
                z['b'][i][2] += 1
                z['b'][i][3] += w
            if r['kauf_3monate_%s' % c] == '1':
                z['b'][i][4] += 1
                z['b'][i][5] += w
        for i, v in enumerate(SLIDER):
            if r[v].strip():
                x = float(r[v])
                z['sl'][i][0] += 1
                z['sl'][i][1] += w
                z['sl'][i][2] += w * x

    def runde(o):
        if isinstance(o, float):
            return round(o, 4)
        if isinstance(o, list):
            return [runde(x) for x in o]
        if isinstance(o, dict):
            return {k: runde(v) for k, v in o.items()}
        return o

    # Randverteilung Region, nur fuer die Tabellenansicht
    regionen = []
    for reg in ['Ost', 'Süd', 'West']:
        teil = [r for r in d if r['_reg'] == reg]
        w = np.array([float(r['gewicht_quote']) for r in teil])
        bek = np.array([r['bekanntheit_%s' % NEOH] == '1' for r in teil], dtype=bool)
        bet = np.array([r['betracht_%s' % NEOH] == '1' for r in teil], dtype=bool)
        kauf = np.array([r['kauf_3monate_%s' % NEOH] == '1' for r in teil], dtype=bool)
        regionen.append({'name': reg, 'n': len(teil),
                         'bek': round(100 * w[bek].sum() / w.sum(), 1),
                         'bet': round(100 * w[bet].sum() / w.sum(), 1),
                         'kauf': round(100 * w[kauf].sum() / w.sum(), 1)})

    return {'marken': [{'c': c, 'n': nm} for c, nm in marken],
            'slider': SLIDER_LABEL,
            'zellen': [runde(z) for z in zellen.values()],
            'regionen': regionen,
            'n_gesamt': len(d)}


SEITE = r"""<title>NEOH Markenmonitor</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: klebende Filterleiste, Kennzahlenstreifen, zweispaltiges Raster,
   darunter die Tabellenansicht. Bei Telefonbreite stapelt alles. */
:root{
  --flaeche:#fcfcfb; --plane:#f6f6f3; --ink:#0b0b0b; --ink2:#52514e; --muted:#898781;
  --grid:#e1e0d9; --base:#c3c2b7; --akzent:#2a78d6; --zweit:#eb6834;
  --st1:#184f95; --st2:#2a78d6; --st3:#86b6ef; --st4:#e9e8e3;
  --chip:#ffffff; --chipan:#2a78d6; --chipant:#ffffff;
  --display:"Archivo","Helvetica Neue",Arial,sans-serif;
  --body:"IBM Plex Sans","Helvetica Neue",Arial,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --flaeche:#1a1a19; --plane:#0d0d0d; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --base:#383835; --akzent:#3987e5; --zweit:#d95926;
  --st1:#b7d3f6; --st2:#5598e7; --st3:#184f95; --st4:#2c2c2a;
  --chip:#232321; --chipan:#3987e5; --chipant:#07131f; color-scheme:dark}}
:root[data-theme="dark"]{
  --flaeche:#1a1a19; --plane:#0d0d0d; --ink:#ffffff; --ink2:#c3c2b7; --muted:#898781;
  --grid:#2c2c2a; --base:#383835; --akzent:#3987e5; --zweit:#d95926;
  --st1:#b7d3f6; --st2:#5598e7; --st3:#184f95; --st4:#2c2c2a;
  --chip:#232321; --chipan:#3987e5; --chipant:#07131f; color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--flaeche);color:var(--ink);font-family:var(--body);
  font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding-inline:18px;padding-block:0 56px}
header{padding-block:30px 18px}
h1{font-family:var(--display);font-weight:700;font-size:clamp(25px,4vw,34px);
  letter-spacing:-.018em;margin:0;text-wrap:balance}
.sub{color:var(--ink2);font-size:14.5px;margin-top:7px;max-width:68ch}
.leiste{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:var(--flaeche);
  border-bottom:1px solid var(--grid);padding-block:11px;margin-bottom:22px}
.filterzeile{display:flex;flex-wrap:wrap;gap:16px 26px;align-items:flex-start}
.fgruppe{min-width:0}
.flabel{font-family:var(--mono);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--muted);margin-bottom:6px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
button.chip{font:inherit;font-size:13px;padding:5px 11px;border-radius:999px;cursor:pointer;
  background:var(--chip);color:var(--ink2);border:1px solid var(--grid);white-space:nowrap}
button.chip[aria-pressed="true"]{background:var(--chipan);color:var(--chipant);
  border-color:var(--chipan);font-weight:600}
button.chip:focus-visible,button.text:focus-visible{outline:2px solid var(--akzent);outline-offset:2px}
button.text{font:inherit;font-size:13px;background:none;border:none;color:var(--akzent);
  cursor:pointer;padding:5px 2px;text-decoration:underline;text-underline-offset:3px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(164px,1fr));gap:1px;
  background:var(--grid);border:1px solid var(--grid);border-radius:10px;overflow:hidden;margin-bottom:24px}
.kpi{background:var(--flaeche);padding:15px 17px}
.kpi .v{font-family:var(--display);font-weight:600;font-size:33px;letter-spacing:-.02em;
  line-height:1.05;font-variant-numeric:tabular-nums}
.kpi .l{font-size:12.5px;color:var(--ink2);margin-top:5px}
.kpi .d{font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:3px}
.raster{display:grid;grid-template-columns:1fr 1fr;gap:22px}
@media(max-width:820px){.raster{grid-template-columns:1fr}}
.karte{border:1px solid var(--grid);border-radius:10px;padding:17px 18px 15px;min-width:0;
  background:var(--flaeche)}
.karte h2{font-family:var(--display);font-weight:600;font-size:16px;margin:0 0 3px;letter-spacing:-.005em}
.karte .hint{font-size:12.5px;color:var(--muted);margin:0 0 13px}
.karte.weit{grid-column:1/-1}
figure{margin:0}
svg{display:block;width:100%;height:auto;overflow:visible}
.legende{display:flex;flex-wrap:wrap;gap:7px 15px;font-size:12px;color:var(--ink2);margin-top:11px}
.legende i{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:6px;vertical-align:1px}
.warn{font-size:12.5px;color:var(--zweit);margin-top:10px;font-weight:500}
table{width:100%;border-collapse:collapse;font-size:13.5px;font-variant-numeric:tabular-nums}
th{text-align:left;font-family:var(--mono);font-weight:500;font-size:10.5px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--muted);padding:0 9px 7px 0;border-bottom:1px solid var(--grid)}
td{padding:6px 9px 6px 0;border-bottom:1px solid var(--grid);color:var(--ink2)}
td.n,th.n{text-align:right}
tr.hi td{color:var(--ink);font-weight:600}
.tabellen{overflow-x:auto}
footer{margin-top:30px;padding-top:15px;border-top:1px solid var(--grid);font-size:12.5px;
  color:var(--muted);display:flex;flex-wrap:wrap;gap:6px 20px;justify-content:space-between}
.tip{position:fixed;pointer-events:none;z-index:40;background:var(--ink);color:var(--flaeche);
  font-size:12.5px;padding:6px 9px;border-radius:6px;opacity:0;transition:opacity .09s;
  font-variant-numeric:tabular-nums;max-width:230px}
.tip.an{opacity:1}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<div class="wrap">
<header>
  <h1>NEOH Markenmonitor Österreich</h1>
  <p class="sub">Markenstudie September 2026, n&nbsp;=&nbsp;567. Filter wirken auf alle
  Kennzahlen gleichzeitig. Alle Anteile beziehen sich auf die jeweils gefilterte
  Teilgruppe.</p>
</header>

<div class="leiste">
  <div class="filterzeile">
    <div class="fgruppe"><div class="flabel">Alter</div><div class="chips" id="f-alter"></div></div>
    <div class="fgruppe"><div class="flabel">Geschlecht</div><div class="chips" id="f-geschlecht"></div></div>
    <div class="fgruppe"><div class="flabel">Zuckerreduktion wichtig</div><div class="chips" id="f-segment"></div></div>
    <div class="fgruppe"><div class="flabel">Gewichtung</div><div class="chips" id="f-gewicht"></div></div>
    <div class="fgruppe"><div class="flabel">&nbsp;</div>
      <button class="text" id="reset" type="button">Filter zurücksetzen</button></div>
  </div>
</div>

<div class="kpis" id="kpis"></div>

<div class="raster">
  <section class="karte">
    <h2>Markenpyramide NEOH</h2>
    <p class="hint">Jede Stufe ist Teilmenge der darunterliegenden.</p>
    <figure id="pyramide"></figure>
    <div class="warn" id="warn-basis" hidden></div>
  </section>

  <section class="karte">
    <h2>Markenbild NEOH</h2>
    <p class="hint">Mittelwerte auf der Skala −100 bis +100, nur Kenner mit Urteil.</p>
    <figure id="brandhealth"></figure>
  </section>

  <section class="karte weit">
    <h2>Gestützte Bekanntheit im Wettbewerb</h2>
    <p class="hint">Alle 20 abgefragten Marken, absteigend. NEOH hervorgehoben.</p>
    <figure id="marken"></figure>
    <div class="legende">
      <span><i style="background:var(--akzent)"></i>NEOH</span>
      <span><i style="background:var(--base)"></i>übrige Marken</span>
    </div>
  </section>

  <section class="karte weit">
    <h2>Tabellenansicht</h2>
    <p class="hint">Dieselben Zahlen zum Nachlesen und Kopieren. Die Region ist
    eine Randverteilung über die Gesamtstichprobe und folgt den Filtern nicht —
    für Regionalaussagen ist die Stichprobe zu klein.</p>
    <div class="tabellen"><table id="tabelle"></table></div>
  </section>
</div>

<footer>
  <span>WU Wien · Dr. Arne Floh · Markenstudie NEOH September 2026</span>
  <span id="stand"></span>
</footer>
</div>
<div class="tip" id="tip" role="status" aria-live="polite"></div>

<script>
const DATA = __DATA__;

const ALTER = {'2':'18–29','3':'30–39','4':'40–49','5':'50–59','6':'60+'};
const GESCHLECHT = {'1':'Männlich','2':'Weiblich'};
const SEGMENT = {'1':'wichtig (4–5)','0':'weniger wichtig (1–3)'};
const NEOH_IDX = DATA.marken.findIndex(m => m.c === '13');

const state = {alter:new Set(), geschlecht:new Set(), segment:new Set(), gewichtet:true};

function chips(host, map, key){
  const el = document.getElementById(host);
  el.innerHTML = '';
  for (const [k,label] of Object.entries(map)){
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'chip'; b.textContent = label;
    b.setAttribute('aria-pressed','false');
    b.addEventListener('click', () => {
      state[key].has(k) ? state[key].delete(k) : state[key].add(k);
      b.setAttribute('aria-pressed', state[key].has(k) ? 'true' : 'false');
      zeichnen();
    });
    el.appendChild(b);
  }
}
function gewichtChips(){
  const el = document.getElementById('f-gewicht');
  el.innerHTML = '';
  [['Gewichtet',true],['Ungewichtet',false]].forEach(([label,val]) => {
    const b = document.createElement('button');
    b.type='button'; b.className='chip'; b.textContent=label;
    b.setAttribute('aria-pressed', state.gewichtet===val ? 'true':'false');
    b.addEventListener('click', () => {
      state.gewichtet = val;
      el.querySelectorAll('button').forEach((x,i) =>
        x.setAttribute('aria-pressed', (i===0)===val ? 'true':'false'));
      zeichnen();
    });
    el.appendChild(b);
  });
}

function auswahl(){
  return DATA.zellen.filter(z =>
    (state.alter.size===0 || state.alter.has(z.a)) &&
    (state.geschlecht.size===0 || state.geschlecht.has(z.g)) &&
    (state.segment.size===0 || state.segment.has(z.s)));
}

function summen(zellen){
  const M = DATA.marken.length;
  const s = {n:0, w:0, w2:0, u:0, uw:0,
             b:Array.from({length:M}, () => [0,0,0,0,0,0]),
             sl:Array.from({length:DATA.slider.length}, () => [0,0,0])};
  for (const z of zellen){
    s.n += z.n; s.w += z.w; s.w2 += z.w2; s.u += z.u; s.uw += z.uw;
    for (let i=0;i<M;i++) for (let j=0;j<6;j++) s.b[i][j] += z.b[i][j];
    for (let i=0;i<s.sl.length;i++) for (let j=0;j<3;j++) s.sl[i][j] += z.sl[i][j];
  }
  return s;
}

const fmt = (v,d=1) => v.toLocaleString('de-AT',{minimumFractionDigits:d,maximumFractionDigits:d});
const basis = s => state.gewichtet ? s.w : s.n;
function anteil(s, i, stufe){           // stufe 0 bekannt, 1 betracht, 2 kauf
  const b = basis(s);
  if (!b) return 0;
  return 100 * s.b[i][stufe*2 + (state.gewichtet?1:0)] / b;
}

function css(name){ return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }

/* ---------------------------------------------------------------- Tooltip */
const tip = document.getElementById('tip');
function tipAn(evt, text){
  tip.textContent = text; tip.classList.add('an');
  const r = tip.getBoundingClientRect();
  let x = evt.clientX + 13, y = evt.clientY - r.height - 9;
  if (x + r.width > innerWidth - 8) x = evt.clientX - r.width - 13;
  if (y < 4) y = evt.clientY + 15;
  tip.style.left = x + 'px'; tip.style.top = y + 'px';
}
function tipAus(){ tip.classList.remove('an'); }

/* ---------------------------------------------------------------- Pyramide */
function zeichnePyramide(s){
  const B = basis(s), i = NEOH_IDX, k = state.gewichtet?1:0;
  const stufen = [
    ['kennt die Marke',  s.b[i][0+k], css('--st3')],
    ['zieht in Betracht',s.b[i][2+k], css('--st2')],
    ['hat gekauft',      s.b[i][4+k], css('--st1')]];
  const W = 560, H = 250, mitte = W*0.40, maxb = W*0.58, zh = (H-26)/3;
  const top = stufen[0][1] || 1;
  let out = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Markenpyramide NEOH">`;
  for (let j=0;j<3;j++){
    const v = B ? 100*stufen[j][1]/B : 0;
    const y = H - 14 - (j+1)*zh;
    const bu = maxb * Math.pow((stufen[j][1]||0)/top, 0.45);
    const bo = j<2 ? maxb * Math.pow((stufen[j+1][1]||0)/top, 0.45) : bu*0.42;
    out += `<path d="M${mitte-bu/2} ${y+zh} L${mitte+bu/2} ${y+zh} L${mitte+bo/2} ${y} L${mitte-bo/2} ${y} Z"
      fill="${stufen[j][2]}" stroke="${css('--flaeche')}" stroke-width="2"
      data-tip="${stufen[j][0]}: ${fmt(v)} %"></path>`;
    out += `<text x="${mitte}" y="${y+zh/2+7}" text-anchor="middle" font-size="19"
      font-weight="600" fill="${j===2?css('--flaeche'):css('--ink')}"
      style="font-family:var(--display)">${fmt(v)}&#8201;%</text>`;
    out += `<text x="${mitte+maxb/2+18}" y="${y+zh/2+5}" font-size="13"
      fill="${css('--ink2')}">${stufen[j][0]}</text>`;
    if (j<2){
      const rate = stufen[j][1] ? 100*stufen[j+1][1]/stufen[j][1] : 0;
      out += `<text x="4" y="${y+5}" font-size="12.5" fill="${css('--muted')}"
        style="font-family:var(--mono)">${fmt(rate,0)}&#8201;% weiter</text>`;
    }
  }
  out += '</svg>';
  document.getElementById('pyramide').innerHTML = out;
}

/* ------------------------------------------------------------- Brand Health */
function zeichneBrandhealth(s){
  const W = 560, zeile = 34, H = DATA.slider.length*zeile + 26;
  const lb = 150, rb = 16, sp = W-lb-rb, vmin=-40, vmax=80;
  const sx = v => lb + sp*(v-vmin)/(vmax-vmin);
  let out = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Markenbild NEOH">`;
  for (let g=vmin+20; g<=vmax; g+=20){
    out += `<line x1="${sx(g)}" y1="6" x2="${sx(g)}" y2="${H-20}" stroke="${css('--grid')}" stroke-width="1"></line>`;
    out += `<text x="${sx(g)}" y="${H-5}" text-anchor="middle" font-size="10.5"
      fill="${css('--muted')}" style="font-family:var(--mono)">${g}</text>`;
  }
  out += `<line x1="${sx(0)}" y1="6" x2="${sx(0)}" y2="${H-20}" stroke="${css('--base')}" stroke-width="1.5"></line>`;
  DATA.slider.forEach((lab,i) => {
    const [n, w, wx] = s.sl[i];
    const m = state.gewichtet ? (w ? wx/w : null) : null;
    const wert = state.gewichtet ? m : (w ? wx/w : null);
    const y = 18 + i*zeile;
    out += `<text x="${lb-12}" y="${y+4}" text-anchor="end" font-size="13" fill="${css('--ink2')}">${lab}</text>`;
    if (wert === null || n === 0){
      out += `<text x="${lb+8}" y="${y+4}" font-size="12" fill="${css('--muted')}">keine Urteile</text>`;
      return;
    }
    const x0 = sx(0), x1 = sx(wert);
    out += `<rect x="${Math.min(x0,x1)}" y="${y-7}" width="${Math.max(2,Math.abs(x1-x0))}" height="14"
      rx="3" fill="${wert>=0?css('--akzent'):css('--zweit')}"
      data-tip="${lab}: ${fmt(wert,0)} (n = ${n})"></rect>`;
    out += `<text x="${x1 + (wert>=0?7:-7)}" y="${y+4}" font-size="12"
      text-anchor="${wert>=0?'start':'end'}" fill="${css('--ink')}"
      style="font-family:var(--mono)">${fmt(wert,0)}</text>`;
  });
  out += '</svg>';
  document.getElementById('brandhealth').innerHTML = out;
}

/* ------------------------------------------------------------- Markenranking */
function zeichneMarken(s){
  const reihen = DATA.marken.map((m,i) => ({name:m.n, v:anteil(s,i,0), neoh:i===NEOH_IDX}))
                            .sort((a,b) => b.v - a.v);
  const W = 1100, zeile = 26, lb = 170, H = reihen.length*zeile + 8;
  const max = Math.max(...reihen.map(r => r.v), 1) * 1.1;
  let out = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Gestützte Bekanntheit aller Marken">`;
  reihen.forEach((r,i) => {
    const y = i*zeile + 4, bw = Math.max(2, (W-lb-62)*r.v/max);
    out += `<text x="${lb-12}" y="${y+14}" text-anchor="end" font-size="13"
      fill="${r.neoh?css('--ink'):css('--ink2')}" font-weight="${r.neoh?600:400}">${r.name}</text>`;
    out += `<rect x="${lb}" y="${y+3}" width="${bw}" height="13" rx="3"
      fill="${r.neoh?css('--akzent'):css('--base')}" data-tip="${r.name}: ${fmt(r.v)} % kennen die Marke"></rect>`;
    out += `<text x="${lb+bw+8}" y="${y+14}" font-size="12"
      fill="${r.neoh?css('--ink'):css('--muted')}" font-weight="${r.neoh?600:400}"
      style="font-family:var(--mono)">${fmt(r.v)}&#8201;%</text>`;
  });
  out += '</svg>';
  document.getElementById('marken').innerHTML = out;
}

/* ---------------------------------------------------------------- Tabelle */
function zeichneTabelle(s){
  const reihen = DATA.marken.map((m,i) => ({
    name:m.n, bek:anteil(s,i,0), bet:anteil(s,i,1), kauf:anteil(s,i,2),
    nb:s.b[i][0], neoh:i===NEOH_IDX})).sort((a,b) => b.bek - a.bek);
  let out = `<thead><tr><th>Marke</th><th class="n">kennt</th><th class="n">erwägt</th>
    <th class="n">gekauft</th><th class="n">Fälle</th></tr></thead><tbody>`;
  for (const r of reihen){
    out += `<tr class="${r.neoh?'hi':''}"><td>${r.name}</td><td class="n">${fmt(r.bek)} %</td>
      <td class="n">${fmt(r.bet)} %</td><td class="n">${fmt(r.kauf)} %</td>
      <td class="n">${r.nb}</td></tr>`;
  }
  out += `</tbody><thead><tr><th>Region (ungefiltert)</th><th class="n">kennt</th>
    <th class="n">erwägt</th><th class="n">gekauft</th><th class="n">Fälle</th></tr></thead><tbody>`;
  for (const r of DATA.regionen){
    out += `<tr><td>${r.name}</td><td class="n">${fmt(r.bek)} %</td><td class="n">${fmt(r.bet)} %</td>
      <td class="n">${fmt(r.kauf)} %</td><td class="n">${r.n}</td></tr>`;
  }
  out += '</tbody>';
  document.getElementById('tabelle').innerHTML = out;
}

/* ---------------------------------------------------------------- Kennzahlen */
function zeichneKpis(s){
  const i = NEOH_IDX;
  const n_eff = s.w2 ? s.w*s.w/s.w2 : 0;
  const ung = s.n ? 100*(state.gewichtet ? s.uw/s.w : s.u/s.n) : 0;
  const bek = anteil(s,i,0);
  const kacheln = [
    {v:fmt(bek)+'&#8201;%', l:'kennen NEOH (gestützt)', d:`${s.b[i][0]} von ${s.n} Fällen`},
    {v:fmt(anteil(s,i,1))+'&#8201;%', l:'ziehen NEOH in Betracht', d:`${s.b[i][2]} Fälle`},
    {v:fmt(anteil(s,i,2))+'&#8201;%', l:'haben gekauft (3 Monate)', d:`${s.b[i][4]} Fälle`},
    {v:fmt(ung)+'&#8201;%', l:'nennen NEOH ungestützt', d:bek ? `Erinnerungsquote ${fmt(100*ung/bek)}&#8201;%` : '—'},
    {v:String(s.n), l:'Fälle in der Auswahl', d:state.gewichtet ? `effektiv ${fmt(n_eff,0)}` : 'ungewichtet'}];
  document.getElementById('kpis').innerHTML = kacheln.map(k =>
    `<div class="kpi"><div class="v">${k.v}</div><div class="l">${k.l}</div><div class="d">${k.d}</div></div>`).join('');
}

/* ---------------------------------------------------------------- Zeichnen */
function zeichnen(){
  const s = summen(auswahl());
  const warn = document.getElementById('warn-basis');
  if (s.n === 0){
    warn.textContent = 'Keine Fälle in dieser Auswahl. Filter lockern.';
    warn.hidden = false;
  } else if (s.n < 50){
    warn.textContent = `Nur ${s.n} Fälle in dieser Auswahl — die Anteile schwanken stark.`;
    warn.hidden = false;
  } else {
    warn.hidden = true;
  }
  zeichneKpis(s);
  zeichnePyramide(s);
  zeichneBrandhealth(s);
  zeichneMarken(s);
  zeichneTabelle(s);
  for (const el of document.querySelectorAll('[data-tip]')){
    el.addEventListener('mousemove', e => tipAn(e, el.getAttribute('data-tip')));
    el.addEventListener('mouseleave', tipAus);
  }
}

chips('f-alter', ALTER, 'alter');
chips('f-geschlecht', GESCHLECHT, 'geschlecht');
chips('f-segment', SEGMENT, 'segment');
gewichtChips();
document.getElementById('reset').addEventListener('click', () => {
  state.alter.clear(); state.geschlecht.clear(); state.segment.clear(); state.gewichtet = true;
  document.querySelectorAll('.chips button').forEach(b => b.setAttribute('aria-pressed','false'));
  document.querySelectorAll('#f-gewicht button').forEach((b,i) => b.setAttribute('aria-pressed', i===0?'true':'false'));
  zeichnen();
});
document.getElementById('stand').textContent =
  'Feld 25.–30. September 2026 · ' + DATA.n_gesamt + ' Fälle nach Qualitätsprüfung';
addEventListener('resize', () => { tipAus(); });
zeichnen();
</script>
"""


def main():
    w = wuerfel()
    seite = SEITE.replace('__DATA__', json.dumps(w, ensure_ascii=False, separators=(',', ':')))
    io.open(AUS, 'w', encoding='utf-8').write(seite)
    print('Geschrieben: %s (%d Zellen, %.0f KB)'
          % (AUS, len(w['zellen']), len(seite) / 1024))
    klein = min(z['n'] for z in w['zellen'])
    print('Kleinste Zelle: %d Faelle - keine Einzelfalldaten in der Seite.' % klein)


if __name__ == '__main__':
    main()
