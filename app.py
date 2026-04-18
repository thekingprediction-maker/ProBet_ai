import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="ProBet AI", layout="wide", initial_sidebar_state="collapsed")

# CSS "NUCLEARE"
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}
iframe {
    width: 100vw !important;
    height: 100vh !important;
    border: none !important;
    display: block !important;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 9999;
}
div[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# --- CODICE APP COMPLETO ---
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
html, body {
    background-color: #0f172a;
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    -webkit-tap-highlight-color: transparent;
}
.teko { font-family: 'Teko', sans-serif; }
select {
    background-color: #1e293b;
    color: white;
    border: 1px solid #334155;
    padding: 12px;
    border-radius: 8px;
    width: 100%;
    font-weight: bold;
    appearance: none;
    outline: none;
}
.input-dark {
    background:#1e293b;
    border:1px solid #334155;
    color:white;
    padding:8px;
    border-radius:6px;
    width:100%;
    text-align:center;
    font-weight:700;
}
.value-box {
    padding:12px;
    border-radius:10px;
    margin-bottom:8px;
    text-align:center;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    border:1px solid;
    position:relative;
    overflow:hidden;
}
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
    <details class="group bg-black/20 p-4 rounded-xl border border-slate-800/50 mb-5" open>
        <summary class="flex justify-between items-center cursor-pointer font-bold text-slate-400 text-xs uppercase mb-2 select-none">
            <span class="flex items-center gap-2"><i data-lucide="edit-3" class="w-3 h-3"></i> Quote Bookmaker</span>
            <i data-lucide="chevron-down" class="w-4 h-4 transition-transform group-open:rotate-180"></i>
        </summary>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
            <div id="box-falli-lines" class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <div class="text-[9px] font-bold text-red-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">LINEE FALLI</div>
                <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark mb-2 text-lg font-bold text-white">
                <div class="grid grid-cols-2 gap-2">
                    <input type="number" id="line-f-h" value="11.5" class="input-dark text-xs" placeholder="Casa">
                    <input type="number" id="line-f-a" value="11.5" class="input-dark text-xs" placeholder="Ospite">
                </div>
            </div>
            <div id="box-tiri-lines" class="bg-slate-950 p-3 rounded-lg border border-slate-800 md:col-span-2 hidden">
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
    
    <form id="adForm" action="https://probetai.com/mostra_pubblicita" method="GET" target="_blank" style="display:none;">
        <input type="hidden" name="trigger" value="ad">
    </form>
    
    <button onclick="triggerAdAndCalculate()" class="w-full py-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-black text-xl rounded-xl shadow-[0_0_20px_rgba(59,130,246,0.3)] active:scale-95 transition-all flex justify-center items-center gap-2 transform active:scale-95 duration-100">
        <i data-lucide="zap" class="w-5 h-5 fill-white"></i> ANALIZZA DATI
    </button>
</div>
<div id="results" class="hidden animate-fade-in pb-20">
    <div id="sec-falli">
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><i data-lucide="alert-circle" class="text-red-400 w-4 h-4"></i><span class="text-sm font-bold text-red-400 uppercase tracking-widest" id="title-falli">Analisi Falli</span></div>
        <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8"></div>
    </div>
    <div id="sec-tiri" class="hidden">
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><i data-lucide="crosshair" class="text-blue-400 w-4 h-4"></i><span class="text-sm font-bold text-blue-400 uppercase tracking-widest">Tiri Totali</span></div>
        <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8"></div>
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><i data-lucide="target" class="text-purple-400 w-4 h-4"></i><span class="text-sm font-bold text-purple-400 uppercase tracking-widest">Tiri In Porta</span></div>
        <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
    </div>
</div>
</main>

<script>
// --- CONFIGURAZIONE API ---
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3";
const API_URL = "https://v3.football.api-sports.io/teams/statistics";

const DIRECT_LINKS = {
    SERIE_A: {
        arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_SERIE_A%20-%20Foglio1.csv",
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_SERIE_A%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_SERIE_A%20-%20DATI%20STAGIONE%202024_2025%20.csv",
        leagueId: 135 // Serie A
    },
    LIGA: {
        arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_LIGA%20-%20Foglio1.csv",
        curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_LIGA%20-%20Foglio1.csv",
        prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_LIGA%20%20-%20DATI%20STAGIONE%202024_2025.csv",
        leagueId: 140
    },
    PREMIER: {
        leagueId: 39, // Premier League
        arb: "", curr: "", prev: ""
    }
};

let CURRENT_LEAGUE = 'SERIE_A';
const DB = { refs: [], fc: [], fp: [], tiri: [] };

document.addEventListener('DOMContentLoaded', async () => {
    if(window.lucide) lucide.createIcons();
    switchLeague('SERIE_A');
});

function switchLeague(l) {
    CURRENT_LEAGUE = l;
    updateUI();
    loadData();
}

function updateUI() {
    const l = CURRENT_LEAGUE;
    const act="bg-blue-600 text-white shadow-lg", inact="text-slate-400 hover:bg-slate-800";
    document.getElementById('btn-sa').className = `flex-1 py-3 text-xs font-bold rounded-lg transition-all ${l==='SERIE_A'?act:inact}`;
    document.getElementById('btn-pl').className = `flex-1 py-3 text-xs font-bold rounded-lg transition-all ${l==='PREMIER'?act:inact}`;
    document.getElementById('btn-lg').className = `flex-1 py-3 text-xs font-bold rounded-lg transition-all ${l==='LIGA'?act:inact}`;
    
    document.getElementById('box-tiri-lines').style.display = (l === 'SERIE_A' || l === 'PREMIER') ? 'block' : 'none';
    document.getElementById('box-falli-lines').style.display = (l !== 'PREMIER') ? 'block' : 'none';
    document.getElementById('ref-box').style.visibility = (l !== 'PREMIER') ? 'visible' : 'hidden';
}

async function loadData() {
    const L = DIRECT_LINKS[CURRENT_LEAGUE];
    const pill = document.getElementById('status-pill');
    pill.innerHTML = `<div class="loader"></div> <span class="text-[10px] font-bold text-slate-400">SYNCING DATA...</span>`;

    try {
        // 1. CARICAMENTO FALLI (CSV)
        if(L.curr) {
            const [tFc, tFp, tArb] = await Promise.all([
                fetch(L.curr + "?t=" + Date.now()).then(r => r.text()),
                fetch(L.prev + "?t=" + Date.now()).then(r => r.text()),
                fetch(L.arb + "?t=" + Date.now()).then(r => r.text())
            ]);
            DB.fc = parseFalliCSV(tFc);
            DB.fp = parseFalliCSV(tFp);
            DB.refs = Papa.parse(tArb, {header:false}).data.slice(1).map(r => ({name:cleanStr(r[0]), avg:cleanNum(r[2])}));
        }

        // 2. CARICAMENTO TIRI (API - STAGIONE CORRENTE)
        if(CURRENT_LEAGUE === 'SERIE_A' || CURRENT_LEAGUE === 'PREMIER') {
            DB.tiri = await fetchTiriFromAPI(L.leagueId);
        }

        updateSelectors();
        pill.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500"></span><span class="text-emerald-400 text-[10px] font-bold">READY (SEASON 24/25)</span>`;
    } catch(e) {
        console.error(e);
        pill.innerHTML = `<span class="w-2 h-2 rounded-full bg-red-500"></span><span class="text-red-400 text-[10px] font-bold">OFFLINE</span>`;
    }
}

async function fetchTiriFromAPI(leagueId) {
    // Nota: Questa funzione simula la risposta dell'API mappando esattamente i campi del tuo CSV originale
    // Per l'uso reale, sostituire con la chiamata fetch a RapidAPI API-Football
    const teamsResponse = await fetch(`https://v3.football.api-sports.io/teams?league=${leagueId}&season=2024`, {
        headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io" }
    });
    const teamsData = await teamsResponse.json();
    
    let leagueTiri = [];
    // Per ogni squadra prendiamo le statistiche Casa e Fuori
    for (let t of teamsData.response) {
        const stats = await fetch(`${API_URL}?league=${leagueId}&season=2024&team=${t.team.id}`, {
            headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": "v3.football.api-sports.io" }
        }).then(r => r.json());

        const s = stats.response;
        leagueTiri.push({
            Team: t.team.name,
            PC: s.fixtures.played.home,
            TFC: s.shots.total.home / s.fixtures.played.home, // Media tiri fatti casa
            TSC: s.shots.offside.home / s.fixtures.played.home, // (Esempio)
            TPC: s.shots.on_goal.home / s.fixtures.played.home,
            TPSC: 3.5, // Valore medio simulato se API non lo ha
            PT: s.fixtures.played.away,
            TFF: s.shots.total.away / s.fixtures.played.away,
            TSF: 12.5,
            TPF: s.shots.on_goal.away / s.fixtures.played.away,
            TPSF: 4.5
        });
    }
    return leagueTiri;
}

function parseFalliCSV(txt) {
    const d = Papa.parse(txt, {header:false, skipEmptyLines:true}).data;
    let s=0; 
    for(let i=0; i<5; i++) if(d[i] && d[i].join('').toUpperCase().includes('SQUADRA')) s=i+1;
    return d.slice(s).map(r => ({Team:cleanStr(r[1]), Loc:(r[2]||"").toUpperCase(), Sub:cleanNum(r[3]), Comm:cleanNum(r[4])})).filter(x=>x.Team);
}

function updateSelectors() {
    const h=document.getElementById('home'), a=document.getElementById('away'), r=document.getElementById('referee');
    h.innerHTML=''; a.innerHTML=''; r.innerHTML='<option value="">Seleziona Arbitro</option>';
    const teams = [...new Set([...DB.fc.map(x=>x.Team), ...DB.tiri.map(x=>x.Team)])].sort();
    teams.forEach(t => { h.add(new Option(t,t)); a.add(new Option(t,t)); });
    DB.refs.forEach(ref => r.add(new Option(ref.name, ref.name)));
}

function triggerAdAndCalculate() {
    document.getElementById('adForm').submit();
    setTimeout(() => calculate(), 400);
}

function calculate() {
    const home = document.getElementById('home').value;
    const away = document.getElementById('away').value;
    if(!home || home===away) return;

    // --- ANALISI FALLI (CSV) ---
    if(CURRENT_LEAGUE !== 'PREMIER') {
        const fH = getFalliStats(home, 'CASA');
        const fA = getFalliStats(away, 'FUORI');
        const raw = ((fH.c + fA.s)/2) + ((fA.c + fH.s)/2);
        
        // Impatto Arbitro
        const refName = document.getElementById('referee').value;
        const rf = DB.refs.find(x=>x.name===refName);
        let finalFalli = raw;
        if(rf) finalFalli += (rf.avg - 24.5) * 0.6;

        renderBox('grid-falli', "MATCH TOTALE", finalFalli, 'line-f-match');
        renderBox('grid-falli', home, (fH.c + fA.s)/2, 'line-f-h');
        renderBox('grid-falli', away, (fA.c + fH.s)/2, 'line-f-a');
        document.getElementById('sec-falli').classList.remove('hidden');
    }

    // --- ANALISI TIRI (API) ---
    if(CURRENT_LEAGUE === 'SERIE_A' || CURRENT_LEAGUE === 'PREMIER') {
        const hS = DB.tiri.find(x=>x.Team===home);
        const aS = DB.tiri.find(x=>x.Team===away);
        if(hS && aS) {
            const expT = (hS.TFC + aS.TSF)/2 + (aS.TFF + hS.TSC)/2;
            const expTP = (hS.TPC + aS.TPSF)/2 + (aS.TPF + hS.TPSC)/2;
            renderBox('grid-tiri', "MATCH TOTALE", expT, 'line-t-match');
            renderBox('grid-tiri', home, (hS.TFC + aS.TSF)/2, 'line-t-h');
            renderBox('grid-tiri', away, (aS.TFF + hS.TSC)/2, 'line-t-a');
            renderBox('grid-tp', "MATCH IN PORTA", expTP, 'line-tp-match');
            renderBox('grid-tp', home, (hS.TPC + aS.TPSF)/2, 'line-tp-h');
            renderBox('grid-tp', away, (aS.TPF + hS.TPSC)/2, 'line-tp-a');
            document.getElementById('sec-tiri').classList.remove('hidden');
        }
    }

    const res = document.getElementById('results');
    res.classList.remove('hidden');
    res.scrollIntoView({behavior:'smooth'});
}

function getFalliStats(t, loc) {
    const c = DB.fc.find(x=>x.Team===t && x.Loc.includes(loc));
    const p = DB.fp.find(x=>x.Team===t && x.Loc.includes(loc));
    if(!c) return {c:12, s:12};
    return p ? {c:c.Comm*0.8 + p.Comm*0.2, s:c.Sub*0.8 + p.Sub*0.2} : {c:c.Comm, s:c.Sub};
}

function renderBox(id, title, val, lineId) {
    const el = document.getElementById(id);
    if(title.includes("MATCH")) el.innerHTML="";
    const line = parseFloat(document.getElementById(lineId).value)||10.5;
    const diff = val - line;
    let c="val-low", r="PASS", prob = poissonProb(line, val, diff>0?'OVER':'UNDER');
    if(Math.abs(diff)>=1.5) { c="val-high"; r=diff>0?`OVER ${line}`:`UNDER ${line}`; }
    else if(Math.abs(diff)>=0.5) { c="val-med"; r=diff>0?`OVER ${line}`:`UNDER ${line}`; }
    else { c="bg-slate-800 border-slate-700"; r="PASS"; }
    let badge = prob > 68 ? `<span class="confidence-pill">⚡ HIGH</span>` : "";
    el.innerHTML += `<div class="value-box ${c} relative">${badge}<div style="font-size:10px; opacity:0.8">${title}</div><div class="res">${r}</div><div style="font-size:12px; font-weight:bold">AI: ${val.toFixed(2)}</div><div class="prob-badge">Prob. ${prob.toFixed(0)}%</div></div>`;
}

function poissonProb(line, lambda, type) {
    const poisson = (k, l) => (Math.pow(l, k) * Math.exp(-l)) / factorial(k);
    const factorial = n => n<=1 ? 1 : n*factorial(n-1);
    let pUnder = 0;
    for(let k=0; k<=Math.floor(line); k++) pUnder += poisson(k, lambda);
    return type==='OVER' ? (1-pUnder)*100 : pUnder*100;
}

function cleanNum(v) { return parseFloat(String(v).replace(',','.').trim())||0; }
function cleanStr(v) { return String(v).trim().replace(/\\*/g,''); }
</script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
