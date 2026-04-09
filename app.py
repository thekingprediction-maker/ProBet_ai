import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="ProBet AI - Pronostici", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CSS PER ELIMINARE SPAZI BIANCHI E HEADER STREAMLIT ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 0 !important; padding-bottom: 0 !important; padding-left: 0 !important; padding-right: 0 !important; }
    iframe { border: none !important; width: 100%; }
    div[data-testid="stHeader"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 1. BANNER ADMOB IN ALTO ---
components.html("""
    <div style="display: flex; justify-content: center; background: #0f172a; padding: 10px 0; height: 60px;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1925129435680887" crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:inline-block;width:320px;height:50px"
             data-ad-client="ca-pub-1925129435680887"
             data-ad-slot="7204639303"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
""", height=70)

# --- 2. IL TUO CODICE COMPLETO (HTML + JS + LOGICA) ---
html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<title>ProBet AI</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
<script src="https://unpkg.com/lucide@latest"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
  html, body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; margin: 0; padding: 0; width: 100%; height: 100%; overflow-x: hidden; }
  .teko { font-family: 'Teko', sans-serif; }
  select { background-color: #1e293b; color: white; border: 1px solid #334155; padding: 12px; border-radius: 8px; width: 100%; font-weight: bold; appearance: none; outline: none; }
  .value-box { padding:12px; border-radius:10px; margin-bottom:8px; text-align:center; border:1px solid; position:relative; }
  .val-high { background: linear-gradient(135deg,#15803d 0%,#166534 100%); border-color:#22c55e; }
  .val-med { background: linear-gradient(135deg,#ca8a04 0%,#a16207 100%); border-color:#facc15; }
  .val-low { background: linear-gradient(135deg,#b91c1c 0%,#991b1b 100%); border-color:#ef4444; }
  .res { font-size:24px; font-weight:900; font-family:'Teko',sans-serif; }
  header { position: sticky; top: 0; width: 100%; z-index: 50; background-color: #0f172a; border-bottom: 1px solid #1e293b; }
</style>
</head>
<body>
  <header class="p-4 flex justify-between items-center">
    <div class="text-2xl font-bold teko text-white">PROBET <span class="text-blue-500">AI</span></div>
    <div id="status-pill" class="text-[10px] text-slate-400 font-bold uppercase border border-slate-800 px-2 py-1 rounded">PRONTO</div>
  </header>

  <main class="p-4 max-w-xl mx-auto">
    <div class="flex gap-2 mb-6 bg-slate-900 p-1 rounded-xl border border-slate-800">
      <button onclick="switchLeague('SERIE_A')" id="btn-SERIE_A" class="flex-1 py-2 text-xs font-bold rounded-lg bg-blue-600 text-white">SERIE A</button>
      <button onclick="switchLeague('PREMIER')" id="btn-PREMIER" class="flex-1 py-2 text-xs font-bold rounded-lg text-slate-400">PREMIER</button>
      <button onclick="switchLeague('LIGA')" id="btn-LIGA" class="flex-1 py-2 text-xs font-bold rounded-lg text-slate-400">LIGA</button>
    </div>

    <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-xl mb-6">
      <div class="space-y-4">
        <div><label class="text-[10px] font-bold text-slate-500 uppercase">Casa</label><select id="home"></select></div>
        <div><label class="text-[10px] font-bold text-slate-500 uppercase">Ospite</label><select id="away"></select></div>
        <div><label class="text-[10px] font-bold text-slate-500 uppercase">Arbitro</label><select id="referee" class="text-yellow-400"></select></div>
      </div>
      <button onclick="calculate()" class="w-full mt-6 py-4 bg-blue-600 hover:bg-blue-500 text-white font-black text-xl rounded-xl transition-all">
        ANALIZZA DATI
      </button>
    </div>

    <div id="results" class="hidden space-y-4 pb-10">
      <h3 class="text-sm font-bold text-red-400 uppercase tracking-widest border-b border-slate-800 pb-2">Analisi Falli</h3>
      <div id="grid-falli" class="grid grid-cols-1 gap-3"></div>
    </div>
  </main>

  <script>
    const LINKS = {
      SERIE_A: {
        arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_SERIE_A%20-%20Foglio1.csv",
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_SERIE_A%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_SERIE_A%20-%20DATI%20STAGIONE%202024_2025%20.csv"
      },
      PREMIER: {
        arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_PREMIER_LEAGUE%20-%20Foglio1.csv",
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_PREMIER_LEAGUE%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_PREMIER_LEAGUE%20-%20DATI%20STAGIONE%202024_2025%20.csv"
      },
      LIGA: {
        arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_LIGA%20-%20Foglio1.csv",
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_LIGA%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_LIGA%20-%20DATI%20STAGIONE%202024_2025%20.csv"
      }
    };

    let currentLeague = 'SERIE_A';
    let dataArb = [], dataCurr = [], dataPrev = [];

    async function loadData() {
      document.getElementById('status-pill').innerText = "CARICAMENTO...";
      const l = LINKS[currentLeague];
      const fetchCSV = url => new Promise(res => Papa.parse(url, {download:true, header:true, complete: results => res(results.data)}));
      
      [dataArb, dataCurr, dataPrev] = await Promise.all([fetchCSV(l.arb), fetchCSV(l.curr), fetchCSV(l.prev)]);
      
      populateSelects();
      document.getElementById('status-pill').innerText = "PRONTO";
    }

    function populateSelects() {
      const h = document.getElementById('home'), a = document.getElementById('away'), r = document.getElementById('referee');
      const teams = [...new Set(dataCurr.map(x => x.Squadra))].filter(Boolean).sort();
      const refs = [...new Set(dataArb.map(x => x.Arbitro))].filter(Boolean).sort();
      
      h.innerHTML = a.innerHTML = teams.map(t => `<option value="${t}">${t}</option>`).join('');
      r.innerHTML = refs.map(ref => `<option value="${ref}">${ref}</option>`).join('');
    }

    function switchLeague(l) {
      currentLeague = l;
      ['SERIE_A','PREMIER','LIGA'].forEach(id => {
        const btn = document.getElementById('btn-'+id);
        btn.className = id === l ? "flex-1 py-2 text-xs font-bold rounded-lg bg-blue-600 text-white" : "flex-1 py-2 text-xs font-bold rounded-lg text-slate-400";
      });
      loadData();
    }

    function calculate() {
      const h = document.getElementById('home').value;
      const a = document.getElementById('away').value;
      const r = document.getElementById('referee').value;
      
      const sH = dataCurr.find(x => x.Squadra === h) || {};
      const sA = dataCurr.find(x => x.Squadra === a) || {};
      const arb = dataArb.find(x => x.Arbitro === r) || {};

      const mediaFalli = (parseFloat(sH['Media Falli Commessi']||0) + parseFloat(sA['Media Falli Commessi']||0) + parseFloat(arb['Media Falli']||0)) / 3;
      
      const grid = document.getElementById('grid-falli');
      grid.innerHTML = `
        <div class="value-box val-high">
          <div class="text-[10px] uppercase opacity-80">Previsione Falli Totali</div>
          <div class="res">${mediaFalli.toFixed(2)}</div>
        </div>
      `;
      document.getElementById('results').classList.remove('hidden');
    }

    window.onload = loadData;
  </script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
