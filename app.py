import streamlit as st
import streamlit.components.v1 as components

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="ProBet AI", layout="wide", initial_sidebar_state="collapsed")

# CSS per nascondere elementi di Streamlit e dare look da App
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        height: 100vh !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. CODICE FRONTEND (HTML/JS) POTENZIATO ---
html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>ProBet AI - Potenziato</title>

<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
<script src="https://unpkg.com/lucide@latest"></script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
  body { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #e2e8f0; -webkit-font-smoothing:antialiased; }
  .teko { font-family: 'Teko', sans-serif; }
  .input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:8px; border-radius:6px; width:100%; text-align:center; font-weight:700; }
  .value-box { padding:12px; border-radius:10px; margin-bottom:8px; text-align:center; box-shadow: 0 4px 6px rgba(0,0,0,0.2); border:1px solid; position:relative; overflow:hidden; }
  .val-high { background: linear-gradient(135deg,#15803d 0%,#166534 100%); color:white; border-color:#22c55e; }
  .val-med { background: linear-gradient(135deg,#ca8a04 0%,#a16207 100%); color:#fff; border-color:#facc15; }
  .val-low { background: linear-gradient(135deg,#b91c1c 0%,#991b1b 100%); color:white; border-color:#ef4444; }
  .res { font-size:22px; font-weight:900; margin:2px 0; font-family:'Teko',sans-serif; line-height:1; }
  .prob-badge { font-size:10px; background:rgba(0,0,0,0.28); padding:2px 6px; border-radius:4px; display:inline-block; margin-top:6px; font-weight:700; }
  .confidence-pill { position:absolute; top:6px; right:6px; font-size:10px; background:#fff; color:#000; padding:3px 7px; border-radius:12px; font-weight:800; box-shadow:0 2px 4px rgba(0,0,0,0.2); }
  .loader { width:14px; height:14px; border:2px solid #475569; border-bottom-color:#3b82f6; border-radius:50%; display:inline-block; animation:rotation 1s linear infinite; }
  @keyframes rotation { 0% { transform:rotate(0deg);} 100% { transform:rotate(360deg);} }
  .small { font-size:11px; color:#94a3b8; }
  .note { font-size:12px; color:#94a3b8; margin-top:6px;}
</style>
</head>
<body>
  <header class="fixed top-0 w-full z-30 bg-[#0f172a]/95 backdrop-blur border-b border-slate-800">
    <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3"><div class="text-2xl font-bold teko text-white tracking-wide">PROBET <span class="text-blue-500">AI</span></div></div>
      <div id="status-pill" class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800">
        <div class="loader"></div> <span class="text-[10px] font-bold text-slate-400">LOADING</span></div>
    </div>
  </header>

  <main class="pt-20 px-4 max-w-6xl mx-auto space-y-6 pb-20">
    <div class="flex justify-center">
      <div class="bg-slate-900 p-1 rounded-xl border border-slate-800 flex gap-2 w-full max-w-sm">
        <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-2 text-xs font-bold rounded-lg bg-blue-600 text-white shadow-lg transition-all">SERIE A</button>
        <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-2 text-xs font-bold rounded-lg text-slate-400 hover:bg-slate-800 transition-all">LIGA</button>
      </div>
    </div>

    <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-xl">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
        <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">CASA</label><select id="home" class="mt-1"><option>Attendi...</option></select></div>
        <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">OSPITE</label><select id="away" class="mt-1"><option>Attendi...</option></select></div>
        <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">ARBITRO</label><select id="referee" class="mt-1 text-yellow-400"><option>Attendi...</option></select></div>
      </div>

      <hr class="border-slate-800 mb-5">

      <details class="group bg-black/20 p-4 rounded-xl border border-slate-800/50 mb-5" open>
        <summary class="flex justify-between items-center cursor-pointer font-bold text-slate-400 text-xs uppercase mb-2">
          <span class="flex items-center gap-2"><i data-lucide="edit-3" class="w-3 h-3"></i> Quote Bookmaker</span>
          <i data-lucide="chevron-down" class="w-4 h-4 transition-transform group-open:rotate-180"></i>
        </summary>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
          <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
            <div class="text-[9px] font-bold text-red-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">LINEE FALLI</div>
            <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark mb-2 text-lg font-bold text-white">
            <div class="grid grid-cols-2 gap-2">
              <input type="number" id="line-f-h" value="11.5" class="input-dark text-xs" placeholder="Casa">
              <input type="number" id="line-f-a" value="11.5" class="input-dark text-xs" placeholder="Ospite">
            </div>
          </div>

          <div id="box-tiri-lines" class="bg-slate-950 p-3 rounded-lg border border-slate-800 md:col-span-2">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <div class="text-[9px] font-bold text-blue-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">TIRI TOTALI</div>
                <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark mb-2 font-bold text-white">
                <div class="grid grid-cols-2 gap-2">
                  <input type="number" id="line-t-h" value="12.5" class="input-dark text-xs text-slate-300">
                  <input type="number" id="line-t-a" value="10.5" class="input-dark text-xs text-slate-300">
                </div>
              </div>

              <div class="border-l border-slate-800 pl-4">
                <div class="text-[9px] font-bold text-purple-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">IN PORTA</div>
                <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark mb-2 font-bold text-white">
                <div class="grid grid-cols-2 gap-2">
                  <input type="number" id="line-tp-h" value="4.5" class="input-dark text-xs text-slate-300">
                  <input type="number" id="line-tp-a" value="3.5" class="input-dark text-xs text-slate-300">
                </div>
              </div>

            </div>
          </div>

        </div>
      </details>

      <button onclick="calculate()" class="w-full py-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-black text-xl rounded-xl shadow-[0_0_20px_rgba(59,130,246,0.3)] active:scale-95 transition-all flex justify-center items-center gap-2">
        <i data-lucide="zap" class="w-5 h-5 fill-white"></i> ANALIZZA DATI
      </button>

      <div class="note">Motore: Strength model migliorato • Lambda mix (squadra/avversario/arbitro) • Nessun Monte Carlo ridondante</div>
    </div>

    <div id="results" class="hidden animate-fade-in">
      <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><i data-lucide="alert-circle" class="text-red-400 w-4 h-4"></i><span class="text-sm font-bold text-red-400 uppercase tracking-widest" id="title-falli">Analisi Falli</span></div>
      <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8"></div>

      <div id="sec-tiri" class="hidden">
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><i data-lucide="crosshair" class="text-blue-400 w-4 h-4"></i><span class="text-sm font-bold text-blue-400 uppercase tracking-widest">Tiri Totali (Strength Model)</span></div>
        <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8"></div>

        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><i data-lucide="target" class="text-purple-400 w-4 h-4"></i><span class="text-sm font-bold text-purple-400 uppercase tracking-widest">Tiri In Porta</span></div>
        <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
      </div>
    </div>

  </main>

<script>
/* =========================
   CONFIG & DB
   ========================= */
const MASTER_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTR5vVYi1_EFk97GPmK8wOdZe6cImPcVYYEX-8rIlUyFg2EJjRspgcgBZ0cDAuVP--Aepi-wxEOdCOp/pub?output=csv";
let CURRENT_LEAGUE = 'SERIE_A';
const CONFIG = { SERIE_A: {}, LIGA: {} };
const DB = { refs: [], fc: [], fp: [], tiri: [], tiriStats: {avgHome:0, avgAway:0, avgHomeTP:0, avgAwayTP:0}, cacheTs: 0 };

/* =========================
   UTIL: safe fetch & debounce cache
   ========================= */
async function safeFetch(url) {
  try {
    const res = await fetch(url.includes('?')? url + '&t=' + Date.now() : url + '?t=' + Date.now(), {cache:'no-store'});
    if(!res.ok) return "";
    return await res.text();
  } catch(e) {
    console.error("fetch error", e);
    return "";
  }
}

/* =========================
   INIT
   ========================= */
document.addEventListener('DOMContentLoaded', async () => {
  if(window.lucide) lucide.createIcons();
  await initMasterConfig();
});

/* =========================
   INIT MASTER CONFIG
   ========================= */
async function initMasterConfig() {
  try {
    const r = await safeFetch(MASTER_URL);
    const parsed = Papa.parse(r, {header:false, skipEmptyLines:true}).data;
    const getL = (i) => (parsed[i] && parsed[i][1]) ? parsed[i][1].trim() : "";
    CONFIG.SERIE_A = { arb: getL(0), curr: getL(1), prev: getL(2), tiri: getL(3) };
    CONFIG.LIGA = { arb: getL(4), curr: getL(5), prev: getL(6), tiri: getL(7) };
    const pill = document.getElementById('status-pill');
    if(pill) pill.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500"></span><span class="text-emerald-400 text-[10px] font-bold">SYSTEM READY</span>`;
    switchLeague('SERIE_A');
  } catch(e) { console.error("initMasterConfig error", e); }
}

/* =========================
   SWITCH LEAGUE
   ========================= */
function switchLeague(l) {
  CURRENT_LEAGUE = l;
  const act="bg-blue-600 text-white shadow-lg", inact="text-slate-400 hover:bg-slate-800";
  document.getElementById('btn-sa').className = `flex-1 py-2 text-xs font-bold rounded-lg transition-all ${l==='SERIE_A'?act:inact}`;
  document.getElementById('btn-lg').className = `flex-1 py-2 text-xs font-bold rounded-lg transition-all ${l==='LIGA'?act:inact}`;
  if(document.getElementById('box-tiri-lines')) document.getElementById('box-tiri-lines').style.display = l==='SERIE_A' ? 'block' : 'none';
  loadData();
}

/* =========================
   PARSER E LOAD DATA (ottimizzato)
   ========================= */
async function loadData() {
  const L = CONFIG[CURRENT_LEAGUE];
  if(!L || !L.arb) return;

  // simple cache: ricarica ogni 90s per evitare troppi hit
  const now = Date.now();
  if(DB.cacheTs && (now - DB.cacheTs) < 90_000) { updateSel(); return; }
  DB.cacheTs = now;

  try {
    const [tA, tFc, tFp, tTr] = await Promise.all([
      safeFetch(L.arb), safeFetch(L.curr), safeFetch(L.prev), safeFetch(L.tiri)
    ]);

    // ARBITRI
    const arbD = Papa.parse(tA, {header:false, skipEmptyLines:true}).data;
    let start = 0;
    if(arbD[0] && (String(arbD[0][0]).includes('Arbitro') || String(arbD[0][0]).includes('Media'))) start = 1;
    DB.refs = arbD.slice(start).map(r => ({name:cleanStr(r[0]), avg:cleanNum(r[2]), rawRow: r})).filter(x=>x.name && !isNaN(x.avg));

    // FALLI
    const parseF = (txt) => {
      if(!txt) return [];
      const d = Papa.parse(txt, {header:false, skipEmptyLines:true}).data;
      let s = 0;
      for(let i=0;i<Math.min(5,d.length);i++) if(d[i].join(' ').toUpperCase().includes('SQUADRA')) s=i+1;
      return d.slice(s).map(r => ({Team: cleanStr(r[1]), Loc: (r[2]||"").toUpperCase(), Sub: cleanNum(r[3]), Comm: cleanNum(r[4])})).filter(x=>x.Team);
    };
    DB.fc = parseF(tFc); DB.fp = parseF(tFp);

    // TIRI
    DB.tiri = [];
    if(tTr && tTr.length > 50) {
      const rd = Papa.parse(tTr, {header:false, skipEmptyLines:true}).data;
      let si = -1; for(let i=0;i<Math.min(20,rd.length);i++) if(rd[i][0] && String(rd[i][0]).toLowerCase().includes("squadra")) si = i;
      if(si !== -1) {
        let sumH=0, sumA=0, sumHtp=0, sumAtp=0, count=0;
        DB.tiri = rd.slice(si+1).map(r => {
          if(!r[0]) return null;
          const pc = cleanNum(r[1]) || 1;
          const pf = cleanNum(r[6]) || 1;
          const tfc = cleanNum(r[2]) / pc; const tsc = cleanNum(r[3]) / pc;
          const tff = cleanNum(r[7]) / pf; const tsf = cleanNum(r[8]) / pf;
          const tpfc = cleanNum(r[4]) / pc; const tpsc = cleanNum(r[5]) / pc;
          const tpff = cleanNum(r[9]) / pf; const tpsf = cleanNum(r[10]) / pf;
          sumH += tfc; sumA += tff; sumHtp += tpfc; sumAtp += tpff; count++;
          return { Team: cleanStr(r[0]), TFC: tfc, TSC: tsc, TFF: tff, TSF: tsf, TPC: tpfc, TPSC: tpsc, TPF: tpff, TPSF: tpsf };
        }).filter(x=>x);
        if(count>0) {
          DB.tiriStats.avgHome = sumH / count;
          DB.tiriStats.avgAway = sumA / count;
          DB.tiriStats.avgHomeTP = sumHtp / count;
          DB.tiriStats.avgAwayTP = sumAtp / count;
        }
      }
    }

    updateSel();
  } catch(e) { console.error("loadData error", e); }
}

function cleanNum(v) { return parseFloat(String(v||"").replace(',','.').replace('%','').trim()) || 0; }
function cleanStr(v) { if(!v && v!==0) return ""; return String(v).trim().replace(/\*/g,''); }

/* =========================
   UTILS STATISTICI
   - factorial, poisson, cdf
   - weighted mean, stddev
   ========================= */
function factorial(n) { if(n===0||n===1) return 1; let r=1; for(let i=2;i<=n;i++) r*=i; return r; }
function poisson(k, lambda) { return Math.pow(lambda, k) * Math.exp(-lambda) / factorial(k); }
function poissonCdf(line, lambda) { let p=0; for(let k=0;k<=Math.floor(line);k++) p+=poisson(k, lambda); return p; }
function poissonProbLine(line, lambda, type) { const pUnder = poissonCdf(line, lambda); return type==='OVER' ? (1 - pUnder) * 100 : pUnder * 100; }
function weightedMean(arr, w) { if(!arr.length) return 0; let num=0, den=0; for(let i=0;i<arr.length;i++){num+=arr[i]*w[i]; den+=w[i];} return den? num/den:0; }
function stdDev(arr) { if(!arr.length) return 0; const m = arr.reduce((s,x)=>s+x,0)/arr.length; return Math.sqrt(arr.reduce((s,x)=>s + Math.pow(x-m,2),0)/arr.length); }

/* =========================
   COEFFICIENTE ARBITRO (media + stabilita')
   piu' coerenza -> piu' peso
   ========================= */
function refereeCoefficient(name) {
  const r = DB.refs.find(x => x.name === name);
  if(!r) return {avg: null, weight: 0.0};
  // se nella riga raw abbiamo tanti campi possiamo stimare dispersione (fallback)
  // per ora usiamo avg come base e assegniamo peso in base a quanto vicina è alla mediana
  const avg = r.avg || 24;
  // stima di coerenza: se ci sono tanti arbitri con simile avg, peso più alto (semplice proxy)
  const allAvgs = DB.refs.map(x=>x.avg).filter(x=>x>0);
  const sd = stdDev(allAvgs) || 6;
  // weight: più l'arbitro è lontano dalla media complessiva, meno affidabile -> peso diminuisce.
  const leagueAvg = allAvgs.reduce((s,x)=>s+x,0)/ (allAvgs.length||1);
  const dist = Math.abs(avg - leagueAvg);
  // normalizziamo weight tra 0.2 e 0.9 inversamente a dist/sd
  const raw = Math.max(0, 1 - (dist / (sd*2)));
  const weight = Math.min(0.9, Math.max(0.2, raw));
  return { avg, weight };
}

/* =========================
   STRENGTH MODEL MIGLIORATO (mantiene casa/fuori)
   -> use adaptive weights: più una squadra ha var alta, meno peso alla media league
   ========================= */
function computeExpected(homeName, awayName, refereeName) {
  const h = DB.tiri.find(x=>x.Team.toUpperCase()===homeName.toUpperCase());
  const a = DB.tiri.find(x=>x.Team.toUpperCase()===awayName.toUpperCase());
  const L = DB.tiriStats;
  if(!h || !a || !L.avgHome) return null;

  // adaptive factor based on team's variability relative to league
  // piu' variabile -> riduci contributo della league avg
  const homeShots = [h.TFC, h.TSC, h.TPC, h.TPSC].filter(Boolean);
  const awayShots = [a.TFF, a.TSF, a.TPF, a.TPSF].filter(Boolean);
  const hVar = stdDev(homeShots) || 0; // se zero -> squadra molto costante
  const aVar = stdDev(awayShots) || 0;
  const leagueVar = Math.max(0.1, stdDev(DB.tiri.map(x=>x.TFC)) || 1);

  const adaptHome = 1 - Math.min(0.6, hVar / (leagueVar*2)); // tra 0.4 e 1.0
  const adaptAway = 1 - Math.min(0.6, aVar / (leagueVar*2));

  // Strength formula (conservativa e coerente con Excel)
  const expTiriHome = ((h.TFC * a.TSF) / L.avgHome) * adaptHome;
  const expTiriAway = ((a.TFF * h.TSC) / L.avgAway) * adaptAway;

  const expTPHome = ((h.TPC * a.TPSF) / L.avgHomeTP) * adaptHome;
  const expTPAway = ((a.TPF * h.TPSC) / L.avgAwayTP) * adaptAway;

  // referee mix: usa media arbitro come bias additivo sul totale (non moltiplicativo)
  const refInfo = refereeCoefficient(refereeName);
  const refBias = (refInfo.avg || 0) * 0.02; // piccolo bias aggregato in tiri/falli (tunable)

  // lambda mix: combina squadra/avversario/arbitro per rendere lambda più real-world
  // pesi: squadra attacco 0.5, difesa avversario 0.3, arbitro 0.2 (tunable)
  // applichiamo a tiri e tiri in porta separatamente
  const lambdaHomeShots = 0.5 * expTiriHome + 0.3 * expTiriAway + 0.2 * (refInfo.avg ? refInfo.avg * 0.2 : 0);
  const lambdaAwayShots = 0.5 * expTiriAway + 0.3 * expTiriHome + 0.2 * (refInfo.avg ? refInfo.avg * 0.2 : 0);

  const lambdaHomeTP = 0.5 * expTPHome + 0.3 * expTPAway + 0.2 * (refInfo.avg ? refInfo.avg * 0.06 : 0);
  const lambdaAwayTP = 0.5 * expTPAway + 0.3 * expTPHome + 0.2 * (refInfo.avg ? refInfo.avg * 0.06 : 0);

  // clamp lambda per sicurezza numerica
  const clamp = (v, min=0.01, max=40) => Math.max(min, Math.min(max, v));

  return {
    expTiriHome: clamp(expTiriHome + refBias, 0.01, 100),
    expTiriAway: clamp(expTiriAway + refBias, 0.01, 100),
    expTPHome: clamp(expTPHome + refBias*0.2, 0.01, 100),
    expTPAway: clamp(expTPAway + refBias*0.2, 0.01, 100),
    lambdaHomeShots: clamp(lambdaHomeShots, 0.01, 200),
    lambdaAwayShots: clamp(lambdaAwayShots, 0.01, 200),
    lambdaHomeTP: clamp(lambdaHomeTP, 0.01, 200),
    lambdaAwayTP: clamp(lambdaAwayTP, 0.01, 200),
    refInfo
  };
}

/* =========================
   FALLI: media pesata con arbitro (non moltiplicativo)
   ========================= */
function computeFouls(home, away, refereeName) {
  const getF = (t,loc,dc,dp) => {
    const c = dc.find(x=>x.Team===t && x.Loc && x.Loc.includes(loc));
    const p = dp.find(x=>x.Team===t && x.Loc && x.Loc.includes(loc));
    if(!c) return {c:0, s:0};
    return p ? {c: c.Comm*0.7 + p.Comm*0.3, s: c.Sub*0.7 + p.Sub*0.3} : {c: c.Comm, s: c.Sub};
  };
  const fH = getF(home,'CASA',DB.fc,DB.fp);
  const fA = getF(away,'FUORI',DB.fc,DB.fp);
  const rawTot = ((fH.c + fA.s) / 2) + ((fA.c + fH.s) / 2);

  const rf = refereeCoefficient(refereeName);
  if(rf && rf.avg) {
    // media pesata: 60% rawTot, 40% arbitro (configurabile)
    const finalTot = rawTot * 0.6 + rf.avg * 0.4;
    return { match: finalTot, home: ((fH.c + fA.s)/2) * 0.6 + (rf.avg/2)*0.4, away: ((fA.c + fH.s)/2) * 0.6 + (rf.avg/2)*0.4, ref: rf };
  } else {
    return { match: rawTot, home: ((fH.c + fA.s)/2), away: ((fA.c + fH.s)/2), ref: rf };
  }
}

/* =========================
   RENDER BOX (migliorata)
   ========================= */
function renderBox(id, title, val, lineId, extra={}) {
  const el = document.getElementById(id);
  if(!el) return;
  if(title.includes("MATCH")) el.innerHTML = "";
  const line = parseFloat(document.getElementById(lineId).value) || 0;
  const diff = val - line;
  let c="val-low", tag="PASS", note="NO EDGE", prob=50;

  // probabilità con Poisson (line esatta come nella tua app)
  prob = poissonProbLine(line, val, diff > 0 ? 'OVER' : 'UNDER');

  if(diff >= 1.5) { c="val-high"; tag = `OVER ${line}`; note = "SUPER VALORE"; }
  else if(diff >= 0.5) { c="val-med"; tag = `OVER ${line}`; note = "BUONO"; }
  else if(diff <= -1.5) { c="val-high"; tag = `UNDER ${line}`; note = "SUPER VALORE"; }
  else if(diff <= -0.5) { c="val-med"; tag = `UNDER ${line}`; note = "BUONO"; }
  if(Math.abs(diff) < 0.5) { c="bg-slate-800 border-slate-700"; tag="PASS"; note="NO EDGE"; prob = 50; }

  const conf = prob > 70 ? '⚡ HIGH CONFIDENCE' : (prob > 58 ? '🔆 MEDIUM' : ''); 
  const confHtml = conf ? `<div class="confidence-pill">${conf}</div>` : '';

  el.innerHTML += `
    <div class="value-box ${c} relative">
      ${confHtml}
      <div class="lbl small" style="opacity:0.8">${title}</div>
      <div class="res">${tag}</div>
      <div style="font-size:12px; font-weight:700">AI: ${Number(val).toFixed(2)} | ${note}</div>
      <div class="prob-badge">Prob. ${Number(prob).toFixed(0)}%</div>
      ${extra && extra.note ? `<div class="small" style="margin-top:6px">${extra.note}</div>` : ""}
    </div>
  `;
}

/* =========================
   CALCOLA (entry)
   ========================= */
function calculate() {
  const home = document.getElementById('home').value;
  const away = document.getElementById('away').value;
  const referee = document.getElementById('referee').value;
  if(!home || !away || home === away) return alert("Seleziona squadre e arbitro correttamente.");

  // FALLI coerenti con Excel
  const fouls = computeFouls(home, away, referee);
  renderBox('grid-falli', "MATCH TOTALE", fouls.match, 'line-f-match', { note: `Ref avg: ${fouls.ref && fouls.ref.avg ? fouls.ref.avg.toFixed(1) : 'N/A'}` });
  renderBox('grid-falli', home, fouls.home, 'line-f-h');
  renderBox('grid-falli', away, fouls.away, 'line-f-a');
  document.getElementById('title-falli').innerText = `Analisi Falli (${ fouls.ref && fouls.ref.avg ? 'Ref: ' + fouls.ref.avg.toFixed(1) : 'Ref: NO' })`;

  // TIRI: strength model avanzato con lambda mix
  const sec = document.getElementById('sec-tiri');
  if(CURRENT_LEAGUE === 'SERIE_A' && DB.tiri.length) {
    sec.classList.remove('hidden');
    const e = computeExpected(home, away, referee);
    if(e) {
      // Tiri totali (match)
      const matchTiri = e.expTiriHome + e.expTiriAway;
      renderBox('grid-tiri', "MATCH TOTALE", matchTiri, 'line-t-match', { note: `λ_home:${e.lambdaHomeShots.toFixed(2)} λ_away:${e.lambdaAwayShots.toFixed(2)}` });
      renderBox('grid-tiri', home, e.expTiriHome, 'line-t-h');
      renderBox('grid-tiri', away, e.expTiriAway, 'line-t-a');

      // In porta
      const matchTP = e.expTPHome + e.expTPAway;
      renderBox('grid-tp', "MATCH IN PORTA", matchTP, 'line-tp-match', { note: `λ_homeTP:${e.lambdaHomeTP.toFixed(2)} λ_awayTP:${e.lambdaAwayTP.toFixed(2)}` });
      renderBox('grid-tp', home, e.expTPHome, 'line-tp-h');
      renderBox('grid-tp', away, e.expTPAway, 'line-tp-a');
    }
  } else { if(sec) sec.classList.add('hidden'); }

  const resDiv = document.getElementById('results');
  if(resDiv) { resDiv.classList.remove('hidden'); setTimeout(()=>resDiv.scrollIntoView({behavior:'smooth'}),100); }
}

/* =========================
   UPDATE SELECT
   ========================= */
function updateSel() {
  const h = document.getElementById('home'), a = document.getElementById('away'), r = document.getElementById('referee');
  if(!h || !a || !r) return;
  h.innerHTML=''; a.innerHTML=''; r.innerHTML='<option value="">Seleziona Arbitro</option>';
  [...new Set(DB.tiri.map(x=>x.Team))].sort().forEach(t => { h.add(new Option(t,t)); a.add(new Option(t,t)); });
  [...new Set(DB.refs.map(x=>x.name))].sort().forEach(n => r.add(new Option(n,n)));
}

</script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
