import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="ProBet AI - Pro", layout="wide", initial_sidebar_state="collapsed")

# CSS PER NASCONDERE L'INTERFACCIA STREAMLIT
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
iframe { width: 100vw !important; height: 100vh !important; border: none !important; position: fixed; top: 0; left: 0; z-index: 9999; }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
<script src="https://unpkg.com/lucide@latest"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;700&family=Inter:wght@400;700;900&display=swap');
body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; margin: 0; }
.teko { font-family: 'Teko', sans-serif; }
.input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:10px; border-radius:8px; width:100%; text-align:center; font-weight:700; outline:none; }
.value-box { padding:15px; border-radius:12px; text-align:center; border:1px solid rgba(255,255,255,0.1); position:relative; }
.val-high { background: linear-gradient(135deg,#15803d 0%,#166534 100%); border-color:#22c55e; }
.val-med { background: linear-gradient(135deg,#ca8a04 0%,#a16207 100%); border-color:#facc15; }
.val-low { background: linear-gradient(135deg,#b91c1c 0%,#991b1b 100%); border-color:#ef4444; }
.res-text { font-size:24px; font-weight:900; font-family:'Teko',sans-serif; }
.loader { width:16px; height:16px; border:2px solid #334155; border-bottom-color:#3b82f6; border-radius:50%; display:inline-block; animation: rotation 1s linear infinite; }
@keyframes rotation { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
</head>
<body>
<header class="p-4 bg-slate-900/50 backdrop-blur-md border-b border-slate-800 sticky top-0 z-50">
    <div class="max-w-4xl mx-auto flex justify-between items-center">
        <h1 class="text-2xl font-bold teko tracking-tighter">PROBET <span class="text-blue-500">AI PRO</span></h1>
        <div id="status" class="text-[10px] font-bold px-3 py-1 rounded-full bg-slate-800 flex items-center gap-2">
            <div class="loader"></div> SINCRONIZZAZIONE API
        </div>
    </div>
</header>

<main class="max-w-4xl mx-auto p-4 pb-24">
    <div class="flex gap-2 mb-6 bg-slate-900 p-1 rounded-xl border border-slate-800">
        <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-2 rounded-lg text-xs font-bold transition-all bg-blue-600 text-white">SERIE A</button>
        <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-2 rounded-lg text-xs font-bold transition-all text-slate-400">PREMIER</button>
        <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-2 rounded-lg text-xs font-bold transition-all text-slate-400">LIGA</button>
    </div>

    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-2xl mb-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <div><label class="text-[10px] font-bold text-slate-500 uppercase">Casa</label><select id="home" class="input-dark mt-1"></select></div>
            <div><label class="text-[10px] font-bold text-slate-500 uppercase">Ospite</label><select id="away" class="input-dark mt-1"></select></div>
            <div id="ref-container" class="md:col-span-2"><label class="text-[10px] font-bold text-slate-500 uppercase">Arbitro</label><select id="referee" class="input-dark mt-1 text-yellow-500"></select></div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
            <div class="bg-black/20 p-3 rounded-xl border border-white/5">
                <div class="text-[9px] font-bold text-slate-500 mb-2 uppercase">Linea Falli</div>
                <input type="number" id="line-f" value="24.5" step="0.5" class="input-dark text-lg">
            </div>
            <div class="bg-black/20 p-3 rounded-xl border border-white/5">
                <div class="text-[9px] font-bold text-slate-500 mb-2 uppercase">Linea Tiri Tot</div>
                <input type="number" id="line-t" value="23.5" step="0.5" class="input-dark text-lg">
            </div>
            <div class="bg-black/20 p-3 rounded-xl border border-white/5">
                <div class="text-[9px] font-bold text-slate-500 mb-2 uppercase">Linea In Porta</div>
                <input type="number" id="line-tp" value="8.5" step="0.5" class="input-dark text-lg">
            </div>
        </div>

        <button onclick="analyze()" class="w-full py-4 bg-blue-600 hover:bg-blue-500 text-white font-black rounded-xl transition-all active:scale-95 shadow-lg shadow-blue-900/20">
            ELABORA PRONOSTICO AI
        </button>
    </div>

    <div id="results" class="space-y-8 hidden">
        <div id="section-falli">
            <h3 class="text-xs font-black text-red-500 uppercase tracking-widest mb-4 border-l-4 border-red-500 pl-2">Analisi Falli (Dati CSV)</h3>
            <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
        </div>
        <div id="section-tiri">
            <h3 class="text-xs font-black text-blue-500 uppercase tracking-widest mb-4 border-l-4 border-blue-500 pl-2">Analisi Tiri (Dati API Live)</h3>
            <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
            <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3"></div>
        </div>
    </div>
</main>

<script>
// --- CONFIGURAZIONE CHIAVE E LINK ---
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3”; 
const HOST = "v3.football.api-sports.io";

const LEAGUES = {
    SERIE_A: { id: 135, csvFalli: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_SERIE_A%20-%20Foglio1.csv", csvRefs: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_SERIE_A%20-%20Foglio1.csv" },
    PREMIER: { id: 39, csvFalli: null, csvRefs: null },
    LIGA: { id: 140, csvFalli: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_LIGA%20-%20Foglio1.csv", csvRefs: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_LIGA%20-%20Foglio1.csv" }
};

let CURRENT = 'SERIE_A';
let DB = { teams: [], falli: [], refs: [], tiri: [] };

async function switchLeague(l) {
    CURRENT = l;
    ['btn-sa','btn-pl','btn-lg'].forEach(id => document.getElementById(id).className = "flex-1 py-2 rounded-lg text-xs font-bold transition-all text-slate-400");
    document.getElementById('btn-' + (l==='SERIE_A'?'sa':l==='PREMIER'?'pl':'lg')).className = "flex-1 py-2 rounded-lg text-xs font-bold transition-all bg-blue-600 text-white";
    await loadData();
}

async function loadData() {
    const status = document.getElementById('status');
    status.innerHTML = '<div class="loader"></div> CARICAMENTO...';
    
    try {
        // Carica Falli/Arbitri da CSV se disponibili
        if(LEAGUES[CURRENT].csvFalli) {
            const fRes = await fetch(LEAGUES[CURRENT].csvFalli);
            const rRes = await fetch(LEAGUES[CURRENT].csvRefs);
            const fText = await fRes.text();
            const rText = await rRes.text();
            DB.falli = Papa.parse(fText, {header:true}).data;
            DB.refs = Papa.parse(rText, {header:true}).data;
        }

        // CARICA TIRI DA API (Stagione 2025 o 2024 a seconda della disponibilità API)
        const response = await fetch(`https://${HOST}/teams/statistics?league=${LEAGUES[CURRENT].id}&season=2024`, {
            headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST }
        });
        
        // Se l'API non risponde o dà errore
        if(!response.ok) throw new Error("API Offline");
        
        // Qui carichiamo la lista squadre per popolare i menu
        const tRes = await fetch(`https://${HOST}/teams?league=${LEAGUES[CURRENT].id}&season=2024`, {
            headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST }
        });
        const tData = await tRes.json();
        DB.teams = tData.response.map(r => r.team.name).sort();

        fillSelectors();
        status.innerHTML = '<span class="w-2 h-2 bg-green-500 rounded-full"></span> API ONLINE';
    } catch(e) {
        status.innerHTML = '<span class="w-2 h-2 bg-red-500 rounded-full"></span> ERRORE DATI';
        console.error(e);
    }
}

function fillSelectors() {
    const h = document.getElementById('home');
    const a = document.getElementById('away');
    const r = document.getElementById('referee');
    h.innerHTML = ''; a.innerHTML = ''; r.innerHTML = '<option value="">Seleziona Arbitro</option>';
    
    DB.teams.forEach(t => {
        h.add(new Option(t, t));
        a.add(new Option(t, t));
    });
    
    if(DB.refs.length > 0) {
        DB.refs.forEach(ref => {
            const name = ref[Object.keys(ref)[0]]; // Prende la prima colonna
            if(name) r.add(new Option(name, name));
        });
    }
}

async function fetchTeamStats(teamName) {
    // Trova l'ID squadra dal nome
    const teamInfo = await fetch(`https://${HOST}/teams?search=${teamName}`, {
        headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST }
    }).then(r => r.json());
    
    const id = teamInfo.response[0].team.id;
    
    const stats = await fetch(`https://${HOST}/teams/statistics?league=${LEAGUES[CURRENT].id}&season=2024&team=${id}`, {
        headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST }
    }).then(r => r.json());
    
    const s = stats.response;
    return {
        playedHome: s.fixtures.played.home,
        playedAway: s.fixtures.played.away,
        tFattiC: s.shots.total.home || 0,
        tSubitiC: 0, // Nota: alcune API non danno i subiti direttamente, usiamo medie di lega se manca
        tpFattiC: s.shots.on_goal.home || 0,
        tFattiF: s.shots.total.away || 0,
        tpFattiF: s.shots.on_goal.away || 0
    };
}

async function analyze() {
    const hName = document.getElementById('home').value;
    const aName = document.getElementById('away').value;
    const status = document.getElementById('status');
    
    status.innerHTML = '<div class="loader"></div> ELABORAZIONE...';
    
    try {
        const hStats = await fetchTeamStats(hName);
        const aStats = await fetchTeamStats(aName);
        
        // Calcoli Tiri (Semplificati basati su dati API)
        const avgTiri = (hStats.tFattiC / hStats.playedHome) + (aStats.tFattiF / aStats.playedAway);
        const avgTP = (hStats.tpFattiC / hStats.playedHome) + (aStats.tpFattiF / aStats.playedAway);

        renderResults(avgTiri, avgTP);
        document.getElementById('results').classList.remove('hidden');
        status.innerHTML = '<span class="w-2 h-2 bg-green-500 rounded-full"></span> ANALISI COMPLETATA';
    } catch(e) {
        alert("Errore nel recupero dati live per queste squadre.");
        status.innerHTML = 'ERRORE';
    }
}

function renderResults(tiri, tp) {
    const lineT = parseFloat(document.getElementById('line-t').value);
    const lineTP = parseFloat(document.getElementById('line-tp').value);
    
    const gridT = document.getElementById('grid-tiri');
    const gridTP = document.getElementById('grid-tp');
    
    gridT.innerHTML = createBox("TIRI TOTALI", tiri, lineT);
    gridTP.innerHTML = createBox("TIRI IN PORTA", tp, lineTP);
}

function createBox(title, val, line) {
    const diff = val - line;
    let color = "val-med";
    let advice = diff > 0 ? "OVER" : "UNDER";
    
    if(Math.abs(diff) > 2) color = "val-high";
    if(Math.abs(diff) < 0.5) color = "bg-slate-800";

    return `
        <div class="value-box ${color}">
            <div class="text-[10px] font-bold opacity-70 uppercase">${title}</div>
            <div class="res-text">${advice} ${line}</div>
            <div class="text-xs font-bold mt-1">PREVISTO: ${val.toFixed(2)}</div>
        </div>
    `;
}

// Avvio
document.addEventListener('DOMContentLoaded', () => {
    if(window.lucide) lucide.createIcons();
    loadData();
});
</script>
</body>
</html>
"""

components.html(html_code, height=1000, scrolling=True)
