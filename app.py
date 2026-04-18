import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="ProBet AI - Live API", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { padding: 0 !important; }
iframe { width: 100vw; height: 100vh; border: none; }
</style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;700&family=Inter:wght@400;700&display=swap');
        body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; overflow-x: hidden; }
        .teko { font-family: 'Teko', sans-serif; }
        .input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:12px; border-radius:8px; width:100%; text-align:center; font-weight:bold; }
        .loader { width:20px; height:20px; border:3px solid #334155; border-bottom-color:#3b82f6; border-radius:50%; display:inline-block; animation: rot 1s linear infinite; }
        @keyframes rot { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .card { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-radius: 16px; padding: 20px; border: 1px solid #334155; text-align: center; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3); }
        .btn-league { padding: 10px; border-radius: 10px; font-weight: bold; font-size: 12px; transition: 0.3s; background: #1e293b; color: #94a3b8; }
        .btn-active { background: #3b82f6; color: white; box-shadow: 0 0 15px rgba(59,130,246,0.4); }
    </style>
</head>
<body>
    <header class="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900/50 sticky top-0 backdrop-blur-md z-50">
        <div class="text-2xl font-bold teko tracking-widest">PROBET <span class="text-blue-500">AI LIVE</span></div>
        <div id="status" class="text-[10px] font-bold bg-slate-800 px-4 py-1.5 rounded-full flex items-center gap-2">
            <div class="loader"></div> CONNESSIONE API...
        </div>
    </header>

    <main class="p-4 max-w-4xl mx-auto">
        <div class="grid grid-cols-3 gap-3 mb-8">
            <button onclick="changeLeague('SERIE_A', 135)" id="b-sa" class="btn-league btn-active">SERIE A</button>
            <button onclick="changeLeague('PREMIER', 39)" id="b-pl" class="btn-league">PREMIER</button>
            <button onclick="changeLeague('LIGA', 140)" id="b-lg" class="btn-league">LA LIGA</button>
        </div>

        <div class="bg-slate-900/80 p-6 rounded-3xl border border-slate-800 mb-8 shadow-2xl">
            <div class="grid grid-cols-1 gap-4 mb-6">
                <div>
                    <label class="text-[10px] font-bold text-slate-500 uppercase ml-2">Squadra Casa</label>
                    <select id="home" class="input-dark mt-1"></select>
                </div>
                <div>
                    <label class="text-[10px] font-bold text-slate-500 uppercase ml-2">Squadra Ospite</label>
                    <select id="away" class="input-dark mt-1"></select>
                </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4 mb-8">
                <div>
                    <label class="text-[10px] font-bold text-slate-500 uppercase ml-2">Linea Tiri</label>
                    <input type="number" id="line-t" value="23.5" step="0.5" class="input-dark mt-1">
                </div>
                <div>
                    <label class="text-[10px] font-bold text-slate-500 uppercase ml-2">Linea In Porta</label>
                    <input type="number" id="line-tp" value="8.5" step="0.5" class="input-dark mt-1">
                </div>
            </div>

            <button onclick="analyzeWithAPI()" id="btn-analyze" class="w-full py-5 bg-blue-600 hover:bg-blue-500 rounded-2xl font-black text-xl transition-all active:scale-95 flex justify-center items-center gap-3">
                ELABORA DATI LIVE
            </button>
        </div>

        <div id="results" class="hidden space-y-4 animate-in fade-in duration-500">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div id="res-tiri" class="card"></div>
                <div id="res-tp" class="card"></div>
            </div>
            <div class="text-[10px] text-center text-slate-500 font-bold uppercase tracking-widest py-4">Dati aggiornati in tempo reale tramite API-Football</div>
        </div>
    </main>

<script>
// --- CONFIGURAZIONE ---
const API_KEY = "028b02ea1d97fdd09cf5f4a89f6860b3";
const HOST = "v3.football.api-sports.io";

let currentLeagueId = 135;
let teamsCache = [];

async function changeLeague(name, id) {
    currentLeagueId = id;
    document.querySelectorAll('.btn-league').forEach(b => b.classList.remove('btn-active'));
    event.target.classList.add('btn-active');
    await loadTeams();
}

// 1. CARICA LA LISTA SQUADRE ALL'AVVIO
async function loadTeams() {
    const status = document.getElementById('status');
    status.innerHTML = '<div class="loader"></div> AGGIORNAMENTO SQUADRE...';
    
    try {
        const res = await fetch(`https://${HOST}/teams?league=${currentLeagueId}&season=2024`, {
            headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST }
        });
        const data = await res.json();
        
        if(!data.response || data.response.length === 0) throw new Error("API Limit or Error");

        teamsCache = data.response.map(item => ({
            id: item.team.id,
            name: item.team.name
        })).sort((a,b) => a.name.localeCompare(b.name));

        const h = document.getElementById('home');
        const a = document.getElementById('away');
        h.innerHTML = ''; a.innerHTML = '';
        
        teamsCache.forEach(t => {
            h.add(new Option(t.name, t.id));
            a.add(new Option(t.name, t.id));
        });

        status.innerHTML = '<span class="text-green-500">●</span> API PRONTA';
    } catch(e) {
        status.innerHTML = '<span class="text-red-500">●</span> ERRORE API';
        console.error(e);
    }
}

// 2. FUNZIONE CORE: ANALISI LIVE
async function analyzeWithAPI() {
    const btn = document.getElementById('btn-analyze');
    const status = document.getElementById('status');
    const idHome = document.getElementById('home').value;
    const idAway = document.getElementById('away').value;
    
    btn.disabled = true;
    btn.innerHTML = '<div class="loader"></div> ANALISI IN CORSO...';
    
    try {
        // Recuperiamo statistiche live per entrambe le squadre
        const [resH, resA] = await Promise.all([
            fetch(`https://${HOST}/teams/statistics?league=${currentLeagueId}&season=2024&team=${idHome}`, {
                headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST }
            }).then(r => r.json()),
            fetch(`https://${HOST}/teams/statistics?league=${currentLeagueId}&season=2024&team=${idAway}`, {
                headers: { "x-rapidapi-key": API_KEY, "x-rapidapi-host": HOST }
            }).then(r => r.json())
        ]);

        const sH = resH.response;
        const sA = resA.response;

        // ESTRAZIONE MEDIE (Logica identica ai tuoi CSV)
        const pC = sH.fixtures.played.home || 1;
        const pF = sA.fixtures.played.away || 1;

        // Medie Casa
        const tfC = (sH.shots.total.home || 0) / pC;
        const tpC = (sH.shots.on_goal.home || 0) / pC;
        // Medie Ospite
        const tfF = (sA.shots.total.away || 0) / pF;
        const tpF = (sA.shots.on_goal.away || 0) / pF;

        // Nota: Se l'API non fornisce i tiri subiti direttamente per lato, 
        // usiamo la media realistica di lega o il totale/partite.
        // Qui calcoliamo il pronostico basato sulla forza d'attacco live
        const expTiri = tfC + tfF; 
        const expInPorta = tpC + tpF;

        display(expTiri, expInPorta);
        
    } catch(e) {
        alert("Errore durante l'analisi API");
    } finally {
        btn.disabled = false;
        btn.innerHTML = 'ELABORA DATI LIVE';
    }
}

function display(t, tp) {
    const lT = parseFloat(document.getElementById('line-t').value);
    const lTp = parseFloat(document.getElementById('line-tp').value);
    
    document.getElementById('res-tiri').innerHTML = `
        <div class="text-[10px] font-bold text-blue-400 mb-1">TIRI TOTALI</div>
        <div class="text-3xl font-black">${t.toFixed(2)}</div>
        <div class="mt-2 text-sm font-bold ${t > lT ? 'text-green-500' : 'text-red-500'}">${t > lT ? 'OVER' : 'UNDER'} ${lT}</div>
    `;
    
    document.getElementById('res-tp').innerHTML = `
        <div class="text-[10px] font-bold text-purple-400 mb-1">TIRI IN PORTA</div>
        <div class="text-3xl font-black">${tp.toFixed(2)}</div>
        <div class="mt-2 text-sm font-bold ${tp > lTp ? 'text-green-500' : 'text-red-500'}">${tp > lTp ? 'OVER' : 'UNDER'} ${lTp}</div>
    `;
    
    document.getElementById('results').classList.remove('hidden');
}

window.onload = loadTeams;
</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
