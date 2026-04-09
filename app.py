import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="ProBet AI", layout="wide", initial_sidebar_state="collapsed")

# --- 1. BANNER PUBBLICITARIO (BANNER_HOME) ---
components.html("""
    <div style="display: flex; justify-content: center; background: #0f172a; padding: 10px 0;">
        <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1925129435680887" crossorigin="anonymous"></script>
        <ins class="adsbygoogle"
             style="display:inline-block;width:320px;height:50px"
             data-ad-client="ca-pub-1925129435680887"
             data-ad-slot="7204639303"></ins>
        <script>
             (adsbygoogle = window.adsbygoogle || []).push({});
        </script>
    </div>
""", height=80)

# --- 2. CSS PER NASCONDERE INTERFACCIA STREAMLIT ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    iframe { border: none !important; width: 100%; }
    div[data-testid="stHeader"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. CODICE DELL'APP PROBET AI ---
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
  html, body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; margin: 0; padding: 0; width: 100%; height: 100%; overflow-x: hidden; -webkit-tap-highlight-color: transparent; }
  .teko { font-family: 'Teko', sans-serif; }
  select { background-color: #1e293b; color: white; border: 1px solid #334155; padding: 12px; border-radius: 8px; width: 100%; font-weight: bold; appearance: none; outline: none; }
  .input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:8px; border-radius:6px; width:100%; text-align:center; font-weight:700; }
  .value-box { padding:12px; border-radius:10px; margin-bottom:8px; text-align:center; box-shadow: 0 4px 6px rgba(0,0,0,0.2); border:1px solid; position:relative; overflow:hidden; }
  .val-high { background: linear-gradient(135deg,#15803d 0%,#166534 100%); color:white; border-color:#22c55e; }
  .val-med { background: linear-gradient(135deg,#ca8a04 0%,#a16207 100%); color:#fff; border-color:#facc15; }
  .val-low { background: linear-gradient(135deg,#b91c1c 0%,#991b1b 100%); color:white; border-color:#ef4444; }
  .res { font-size:22px; font-weight:900; margin:2px 0; font-family:'Teko',sans-serif; line-height:1; }
  .prob-badge { font-size:10px; background:rgba(0,0,0,0.3); padding:2px 6px; border-radius:4px; display:inline-block; margin-top:4px; font-weight:700; }
  .confidence-pill { position:absolute; top:6px; right:6px; font-size:10px; background:#fff; color:#000; padding:3px 7px; border-radius:12px; font-weight:800; box-shadow:0 2px 4px rgba(0,0,0,0.2); }
  .loader { width:14px; height:14px; border:2px solid #475569; border-bottom-color:#3b82f6; border-radius:50%; display:inline-block; animation:rotation 1s linear infinite; }
  @keyframes rotation { 0% { transform:rotate(0deg);} 100% { transform:rotate(360deg);} }
  header { position: fixed; top: 0; left: 0; width: 100%; z-index: 50; background-color: rgba(15, 23, 42, 0.95); backdrop-filter: blur(8px); border-bottom: 1px solid #1e293b; }
  main { padding-top: 80px; padding-bottom: 40px; padding-left: 16px; padding-right: 16px; max-width: 800px; margin: 0 auto; }
</style>
</head>
<body>
  <header>
    <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3"><div class="text-2xl font-bold teko text-white tracking-wide">PROBET <span class="text-blue-500">AI</span></div></div>
      <div id="status-pill" class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800"><div class="loader"></div> <span class="text-[10px] font-bold text-slate-400">LOADING</span></div>
    </div>
  </header>

  <main>
    <div class="flex justify-center mb-6">
      <div class="bg-slate-900 p-1 rounded-xl border border-slate-800 flex gap-2 w-full max-w-sm shadow-lg">
        <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3 text-xs font-bold rounded-lg bg-blue-600 text-white shadow-lg transition-all">SERIE A</button>
        <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3 text-xs font-bold rounded-lg text-slate-400 hover:bg-slate-800 transition-all">PREMIER</button>
        <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-3 text-xs font-bold rounded-lg text-slate-400 hover:bg-slate-800 transition-all">LIGA</button>
      </div>
    </div>

    <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-xl mb-8">
      <div class="grid grid-cols-1 gap-4 mb-5">
        <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">CASA</label><select id="home" class="mt-1"><option>Attendi...</option></select></div>
        <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">OSPITE</label><select id="away" class="mt-1"><option>Attendi...</option></select></div>
        <div id="ref-box"><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">ARBITRO</label><select id="referee" class="mt-1 text-yellow-400"><option>Attendi...</option></select></div>
      </div>
      <hr class="border-slate-800 mb-5 opacity-50">
      <button onclick="calculate()" class="w-full py-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-black text-xl rounded-xl shadow-[0_0_20px_rgba(59,130,246,0.3)] active:scale-95 transition-all flex justify-center items-center gap-2">
        <i data-lucide="zap" class="w-5 h-5 fill-white"></i> ANALIZZA DATI
      </button>
    </div>

    <div id="results" class="hidden animate-fade-in pb-20">
      <div id="sec-falli">
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><i data-lucide="alert-circle" class="text-red-400 w-4 h-4"></i><span class="text-sm font-bold text-red-400 uppercase tracking-widest" id="title-falli">Analisi Falli</span></div>
        <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8"></div>
      </div>
    </div>
  </main>

  <script>
    // La logica JS originale rimane qui...
    const DIRECT_LINKS = {
      SERIE_A: {
        arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_SERIE_A%20-%20Foglio1.csv",
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_SERIE_A%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_SERIE_A%20-%20DATI%20STAGIONE%202024_2025%20.csv"
      }
    };
    // ...resto del tuo script JS...
    function switchLeague(l) { console.log("League switched to", l); loadData(); }
    async function loadData() { 
      const h=document.getElementById('home'), a=document.getElementById('away');
      h.innerHTML='<option>Inter</option><option>Milan</option>'; 
      a.innerHTML='<option>Juve</option><option>Napoli</option>';
    }
    function calculate() { document.getElementById('results').classList.remove('hidden'); }
    document.addEventListener('DOMContentLoaded', () => { switchLeague('SERIE_A'); });
  </script>
</body>
</html>
"""

components.html(html_code, height=1500, scrolling=True)
