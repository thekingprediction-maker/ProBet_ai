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
.val-high {
    background: linear-gradient(135deg,#15803d 0%,#166534 100%);
    color:white;
    border-color:#22c55e;
}
.val-med {
    background: linear-gradient(135deg,#ca8a04 0%,#a16207 100%);
    color:#fff;
    border-color:#facc15;
}
.val-low {
    background: linear-gradient(135deg,#b91c1c 0%,#991b1b 100%);
    color:white;
    border-color:#ef4444;
}
.res {
    font-size:22px;
    font-weight:900;
    margin:2px 0;
    font-family:'Teko',sans-serif;
    line-height:1;
}
.prob-badge {
    font-size:10px;
    background:rgba(0,0,0,0.3);
    padding:2px 6px;
    border-radius:4px;
    display:inline-block;
    margin-top:4px;
    font-weight:700;
}
.confidence-pill {
    position:absolute;
    top:6px;
    right:6px;
    font-size:10px;
    background:#fff;
    color:#000;
    padding:3px 7px;
    border-radius:12px;
    font-weight:800;
    box-shadow:0 2px 4px rgba(0,0,0,0.2);
}
.loader {
    width:14px;
    height:14px;
    border:2px solid #475569;
    border-bottom-color:#3b82f6;
    border-radius:50%;
    display:inline-block;
    animation:rotation 1s linear infinite;
}
@keyframes rotation {
    0% { transform:rotate(0deg);}
    100% { transform:rotate(360deg);}
}
header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 50;
    background-color: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid #1e293b;
}
main {
    padding-top: 80px;
    padding-bottom: 40px;
    padding-left: 16px;
    padding-right: 16px;
    max-width: 800px;
    margin: 0 auto;
}
.api-status {
    font-size: 10px;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 600;
    margin-right: 8px;
}
.api-connected { background: #10b981; color: #064e3b; }
.api-error { background: #ef4444; color: #7f1d1d; }
</style>
</head>
<body>
<header>
<div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
    <div class="flex items-center gap-3"><div class="text-2xl font-bold teko text-white tracking-wide">PROBET <span class="text-blue-500">AI</span></div></div>
    <div class="flex items-center gap-2">
        <span id="api-status" class="api-status api-error">API OFFLINE</span>
        <div id="status-pill" class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800"><div class="loader"></div> <span class="text-[10px] font-bold text-slate-400">LOADING</span></div>
    </div>
</div>
</header>
<main>
<div class="flex justify-center mb-6">
    <div class="bg-slate-900 p-1 rounded-xl border border-slate-800 flex gap-2 w-full max-w-md shadow-lg">
        <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3 text-xs font-bold rounded-lg bg-blue-600 text-white shadow-lg transition-all">SERIE A</button>
        <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3 text-xs font-bold rounded-lg text-slate-400 hover:bg-slate-800 transition-all">PREMIER</button>
        <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-3 text-xs font-bold rounded-lg text-slate-400 hover:bg-slate-800 transition-all">LIGA</button>
        <button onclick="switchLeague('BUNDESLIGA')" id="btn-bu" class="flex-1 py-3 text-xs font-bold rounded-lg text-slate-400 hover:bg-slate-800 transition-all">BUNDESLIGA</button>
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
            <span class="flex items-center gap-2"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg> Quote Bookmaker</span>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="transition-transform group-open:rotate-180"><polyline points="6 9 12 15 18 9"></polyline></svg>
        </summary>
        <div class="grid grid-cols-1 gap-4 mt-3">
            <div id="box-falli-lines" class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                <div class="text-[9px] font-bold text-red-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">LINEE FALLI</div>
                <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark mb-2 text-lg font-bold text-white">
                <div class="grid grid-cols-2 gap-2">
                    <input type="number" id="line-f-h" value="11.5" class="input-dark text-xs" placeholder="Casa">
                    <input type="number" id="line-f-a" value="11.5" class="input-dark text-xs" placeholder="Ospite">
                </div>
            </div>
            <div id="box-tiri-lines" class="bg-slate-950 p-3 rounded-lg border border-slate-800 hidden">
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
        <svg width="20" height="20" viewBox="0 0 24 24" fill="white" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg> ANALIZZA DATI
    </button>
</div>
<div id="results" class="hidden animate-fade-in pb-20">
    <div id="sec-falli" class="hidden">
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><span class="text-red-400 text-xl">🚨</span><span class="text-sm font-bold text-red-400 uppercase tracking-widest" id="title-falli">Analisi Falli</span></div>
        <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8"></div>
    </div>
    <div id="sec-tiri" class="hidden">
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><span class="text-blue-400 text-xl">🎯</span><span class="text-sm font-bold text-blue-400 uppercase tracking-widest">Tiri Totali</span></div>
        <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8"></div>
        <div class="flex items-center gap-2 mb-3 mt-8 border-b border-slate-800 pb-2"><span class="text-purple-400 text-xl">🎯</span><span class="text-sm font-bold text-purple-400 uppercase tracking-widest">Tiri In Porta</span></div>
        <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-3"></div>
    </div>
</div>
</main>
<script>
// ============================================
// CONFIGURAZIONE API-FOOTBALL
// ============================================

const API_KEY = "fc1416324cb6bf553a650f97fda0d48a";
const API_BASE = "https://v3.football.api-sports.io";

// League IDs API-Football
const LEAGUE_IDS = {
    'SERIE_A': 135,      // Serie A Italia
    'PREMIER': 39,       // Premier League
    'LIGA': 140,         // La Liga
    'BUNDESLIGA': 78     // Bundesliga
};

// Season attuale
const CURRENT_SEASON = 2024;

// Configurazione campionati
const LEAGUE_CONFIG = {
    SERIE_A: { hasFouls: true, hasShots: true, hasReferees: true },
    PREMIER: { hasFouls: false, hasShots: true, hasReferees: false },
    LIGA: { hasFouls: false, hasShots: true, hasReferees: false },
    BUNDESLIGA: { hasFouls: false, hasShots: true, hasReferees: false }
};

// ============================================
// DATABASE LOCALE
// ============================================
let CURRENT_LEAGUE = 'SERIE_A';
const DB = { 
    teams: [],
    refs: [], 
    fixtures: [],
    teamStats: {},
    tiriStats: {avgHome:0, avgAway:0, avgHomeTP:0, avgAwayTP:0} 
};

// ============================================
// FUNZIONI API
// ============================================

async function fetchAPI(endpoint, params = {}) {
    const url = new URL(API_BASE + endpoint);
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'x-apisports-key': API_KEY,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        
        if (data.errors && Object.keys(data.errors).length > 0) {
            console.error('API Errors:', data.errors);
            return null;
        }
        
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        return null;
    }
}

// ============================================
// INIZIALIZZAZIONE
// ============================================
document.addEventListener('DOMContentLoaded', async () => {
    switchLeague('SERIE_A');
    const pill = document.getElementById('status-pill');
    if(pill) pill.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500"></span><span class="text-emerald-400 text-[10px] font-bold">SYSTEM READY</span>`;
});

// ============================================
// GESTIONE CAMBIO CAMPIONATO
// ============================================
function switchLeague(l) {
    CURRENT_LEAGUE = l;
    const act="bg-blue-600 text-white shadow-lg", inact="text-slate-400 hover:bg-slate-800";
    document.getElementById('btn-sa').className = `flex-1 py-3 text-xs font-bold rounded-lg transition-all ${l==='SERIE_A'?act:inact}`;
    document.getElementById('btn-pl').className = `flex-1 py-3 text-xs font-bold rounded-lg transition-all ${l==='PREMIER'?act:inact}`;
    document.getElementById('btn-lg').className = `flex-1 py-3 text-xs font-bold rounded-lg transition-all ${l==='LIGA'?act:inact}`;
    document.getElementById('btn-bu').className = `flex-1 py-3 text-xs font-bold rounded-lg transition-all ${l==='BUNDESLIGA'?act:inact}`;
    
    const config = LEAGUE_CONFIG[l];
    const boxTiri = document.getElementById('box-tiri-lines');
    const boxFalli = document.getElementById('box-falli-lines');
    const boxRef = document.getElementById('ref-box');
    
    // SOLO SERIE A HA FALLI
    if(config.hasFouls) {
        boxFalli.style.display = 'block';
        boxRef.style.visibility = 'visible';
    } else {
        boxFalli.style.display = 'none';
        boxRef.style.visibility = 'hidden';
    }
    
    // TUTTI HANNO TIRI
    if(config.hasShots) {
        boxTiri.style.display = 'block';
    } else {
        boxTiri.style.display = 'none';
    }
    
    document.getElementById('home').innerHTML = '<option>Caricamento...</option>';
    document.getElementById('away').innerHTML = '<option>Caricamento...</option>';
    document.getElementById('referee').innerHTML = '<option>Attendi...</option>';
    
    loadData();
}

// ============================================
// CARICAMENTO DATI
// ============================================
async function loadData() {
    const apiStatus = document.getElementById('api-status');
    apiStatus.textContent = 'LOADING...';
    apiStatus.className = 'api-status api-error';
    
    const leagueId = LEAGUE_IDS[CURRENT_LEAGUE];
    const config = LEAGUE_CONFIG[CURRENT_LEAGUE];
    
    try {
        // Carica teams
        const teamsData = await fetchAPI('/teams', { league: leagueId, season: CURRENT_SEASON });
        if (teamsData && teamsData.response) {
            DB.teams = teamsData.response.map(t => ({
                id: t.team.id,
                name: t.team.name,
                logo: t.team.logo
            }));
        }
        
        // Carica fixtures per statistiche
        const fixturesData = await fetchAPI('/fixtures', { 
            league: leagueId, 
            season: CURRENT_SEASON,
            status: 'FT'
        });
        
        if (fixturesData && fixturesData.response) {
            DB.fixtures = fixturesData.response;
            await processTeamStats(leagueId);
        }
        
        // SOLO SERIE A - Carica dati arbitri e falli
        if (config.hasReferees && CURRENT_LEAGUE === 'SERIE_A') {
            await loadRefereeData();
        }
        
        apiStatus.textContent = 'API CONNECTED';
        apiStatus.className = 'api-status api-connected';
        updateSel();
        
    } catch(e) { 
        console.error("Error Loading API", e);
        apiStatus.textContent = 'API ERROR - MOCK MODE';
        loadMockData();
    }
}

// Processa statistiche squadre dai fixtures
async function processTeamStats(leagueId) {
    DB.teamStats = {};
    
    // Per ogni fixture, estrai statistiche
    for (const fixture of DB.fixtures.slice(0, 50)) { // Ultimi 50 match
        const fixtureId = fixture.fixture.id;
        const statsData = await fetchAPI('/fixtures/statistics', { fixture: fixtureId });
        
        if (statsData && statsData.response) {
            const homeTeam = statsData.response[0];
            const awayTeam = statsData.response[1];
            
            if (homeTeam && awayTeam) {
                updateTeamStats(homeTeam, 'home');
                updateTeamStats(awayTeam, 'away');
            }
        }
    }
    
    // Calcola medie
    calculateAverages();
}

function updateTeamStats(teamData, location) {
    const teamId = teamData.team.id;
    const teamName = teamData.team.name;
    
    if (!DB.teamStats[teamName]) {
        DB.teamStats[teamName] = {
            name: teamName,
            id: teamId,
            home: { shots: [], shotsOnTarget: [], fouls: [], games: 0 },
            away: { shots: [], shotsOnTarget: [], fouls: [], games: 0 }
        };
    }
    
    const stats = teamData.statistics;
    const locationStats = DB.teamStats[teamName][location];
    
    // Estrai statistiche
    const shots = stats.find(s => s.type === 'Shots Total')?.value || 0;
    const shotsOnTarget = stats.find(s => s.type === 'Shots On Target')?.value || 0;
    const fouls = stats.find(s => s.type === 'Fouls')?.value || 0;
    
    if (shots > 0) locationStats.shots.push(parseInt(shots));
    if (shotsOnTarget > 0) locationStats.shotsOnTarget.push(parseInt(shotsOnTarget));
    if (fouls > 0) locationStats.fouls.push(parseInt(fouls));
    locationStats.games++;
}

function calculateAverages() {
    let totalHomeShots = 0, totalAwayShots = 0;
    let totalHomeTarget = 0, totalAwayTarget = 0;
    let count = 0;
    
    for (const teamName in DB.teamStats) {
        const team = DB.teamStats[teamName];
        
        // Prepara dati per calcoli
        team.avgHomeShots = team.home.shots.length > 0 ? 
            team.home.shots.reduce((a,b) => a+b, 0) / team.home.shots.length : 12;
        team.avgAwayShots = team.away.shots.length > 0 ? 
            team.away.shots.reduce((a,b) => a+b, 0) / team.away.shots.length : 10;
        team.avgHomeTarget = team.home.shotsOnTarget.length > 0 ? 
            team.home.shotsOnTarget.reduce((a,b) => a+b, 0) / team.home.shotsOnTarget.length : 4.5;
        team.avgAwayTarget = team.away.shotsOnTarget.length > 0 ? 
            team.away.shotsOnTarget.reduce((a,b) => a+b, 0) / team.away.shotsOnTarget.length : 3.5;
        team.avgHomeFouls = team.home.fouls.length > 0 ? 
            team.home.fouls.reduce((a,b) => a+b, 0) / team.home.fouls.length : 11;
        team.avgAwayFouls = team.away.fouls.length > 0 ? 
            team.away.fouls.reduce((a,b) => a+b, 0) / team.away.fouls.length : 12;
            
        totalHomeShots += team.avgHomeShots;
        totalAwayShots += team.avgAwayShots;
        totalHomeTarget += team.avgHomeTarget;
        totalAwayTarget += team.avgAwayTarget;
        count++;
    }
    
    if (count > 0) {
        DB.tiriStats = {
            avgHome: totalHomeShots / count,
            avgAway: totalAwayShots / count,
            avgHomeTP: totalHomeTarget / count,
            avgAwayTP: totalAwayTarget / count
        };
    }
}

// Carica dati arbitri (mock per Serie A - API-Football non ha endpoint dedicato)
async function loadRefereeData() {
    // Mock arbitri Serie A con medie realistiche
    DB.refs = [
        {name: 'Daniele Orsato', avg: 26.5},
        {name: 'Marco Guida', avg: 25.8},
        {name: 'Massimiliano Irrati', avg: 27.2},
        {name: 'Gianluca Aureliano', avg: 24.9},
        {name: 'Fabio Maresca', avg: 28.1},
        {name: 'Rosario Abisso', avg: 25.3},
        {name: 'Davide Massa', avg: 26.1},
        {name: 'Luca Pairetto', avg: 24.7},
        {name: 'Matteo Marchetti', avg: 25.6},
        {name: 'Ermanno Feliciani', avg: 26.8}
    ];
}

// Dati mock per fallback
function loadMockData() {
    const mockTeams = {
        'SERIE_A': ['Inter', 'Milan', 'Juventus', 'Napoli', 'Roma', 'Lazio', 'Atalanta', 'Fiorentina', 'Bologna', 'Torino'],
        'PREMIER': ['Manchester City', 'Arsenal', 'Liverpool', 'Chelsea', 'Manchester Utd', 'Tottenham', 'Newcastle', 'Aston Villa', 'West Ham', 'Brighton'],
        'LIGA': ['Real Madrid', 'Barcelona', 'Atletico Madrid', 'Sevilla', 'Real Sociedad', 'Betis', 'Villarreal', 'Athletic Bilbao', 'Valencia', 'Celta Vigo'],
        'BUNDESLIGA': ['Bayern Munich', 'Bayer Leverkusen', 'Dortmund', 'Leipzig', 'Stuttgart', 'Frankfurt', 'Wolfsburg', 'Freiburg', 'Hoffenheim', 'Union Berlin']
    };
    
    const teams = mockTeams[CURRENT_LEAGUE] || [];
    DB.teams = teams.map((t, i) => ({ id: i, name: t }));
    
    // SOLO SERIE A HA FALLI
    if(CURRENT_LEAGUE === 'SERIE_A') {
        loadRefereeData();
    }
    
    // Crea mock stats per tutti
    DB.teamStats = {};
    teams.forEach(t => {
        DB.teamStats[t] = {
            name: t,
            avgHomeShots: 12 + Math.random() * 6,
            avgAwayShots: 10 + Math.random() * 5,
            avgHomeTarget: 4 + Math.random() * 3,
            avgAwayTarget: 3 + Math.random() * 2.5,
            avgHomeFouls: 10 + Math.random() * 4,
            avgAwayFouls: 11 + Math.random() * 5
        };
    });
    
    DB.tiriStats = { avgHome: 13.5, avgAway: 11.2, avgHomeTP: 4.8, avgAwayTP: 3.9 };
    updateSel();
}

function updateSel() {
    const h=document.getElementById('home'), a=document.getElementById('away'), r=document.getElementById('referee');
    if(!h || !a || !r) return;
    
    h.innerHTML='';
    a.innerHTML='';
    r.innerHTML='<option value="">Seleziona Arbitro</option>';
    
    const teamNames = DB.teams.map(t => t.name).sort();
    teamNames.forEach(t => { 
        h.add(new Option(t,t)); 
        a.add(new Option(t,t)); 
    });
    
    if (DB.refs.length > 0) {
        DB.refs.forEach(ref => r.add(new Option(ref.name, ref.name)));
    }
}

// ============================================
// ALGORITMI POTENZIATI
// ============================================
function poisson(k, lambda) { 
    return (Math.pow(lambda, k) * Math.exp(-lambda)) / factorial(k); 
}

function factorial(n) { 
    if (n===0 || n===1) return 1; 
    let r=1; 
    for(let i=2; i<=n; i++) r*=i; 
    return r; 
}

function poissonProb(line, lambda, type) {
    let pUnder = 0;
    for(let k=0; k<=Math.floor(line); k++) pUnder += poisson(k, lambda);
    return type==='OVER' ? (1-pUnder)*100 : pUnder*100;
}

// ============================================
// GESTIONE PUBBLICITÀ
// ============================================
function triggerAdAndCalculate() {
    const form = document.getElementById('adForm');
    if(form) form.submit();
    
    setTimeout(() => {
        const w = window.open("about:blank/mostra_pubblicita", "_blank");
        if(w) w.close();
    }, 10);
    
    setTimeout(() => {
        const originalHash = window.location.hash;
        window.location.hash = "mostra_pubblicita_trigger";
        setTimeout(() => {
            window.location.hash = originalHash || "";
        }, 100);
    }, 50);
    
    setTimeout(() => {
        calculate();
    }, 400);
}

// ============================================
// CALCOLO PRINCIPALE
// ============================================
function calculate() {
    const home = document.getElementById('home').value;
    const away = document.getElementById('away').value;
    
    if(!home || home===away || home==="Attendi...") {
        alert("Seleziona squadre valide.");
        return;
    }
    
    const config = LEAGUE_CONFIG[CURRENT_LEAGUE];
    
    // FALLI - SOLO SERIE A
    if(config.hasFouls) {
        calculateFoulsEnhanced(home, away);
    } else {
        document.getElementById('sec-falli').classList.add('hidden');
    }
    
    // TIRI - TUTTI I CAMPIONATI
    if(config.hasShots) {
        calculateShotsEnhanced(home, away);
    } else {
        document.getElementById('sec-tiri').classList.add('hidden');
    }
    
    const resDiv = document.getElementById('results');
    if(resDiv) {
        resDiv.classList.remove('hidden');
        setTimeout(()=>resDiv.scrollIntoView({behavior:'smooth'}), 100);
    }
}

// Calcolo falli potenziato per Serie A
function calculateFoulsEnhanced(home, away) {
    const ref = document.getElementById('referee').value;
    
    const hStats = DB.teamStats[home];
    const aStats = DB.teamStats[away];
    
    if (!hStats || !aStats) return;
    
    // Algoritmo potenziato con pesi ottimizzati
    const homeWeight = 0.65;
    const awayWeight = 0.35;
    const formFactor = 1.08;
    
    // Media ponderata: casa commette di meno, subisce di più
    const baseHome = ((hStats.avgHomeFouls * 0.7 + aStats.avgAwayFouls * 0.3) * homeWeight + 
                      (aStats.avgAwayFouls * 0.7 + hStats.avgHomeFouls * 0.3) * awayWeight) * formFactor;
    const baseAway = ((aStats.avgAwayFouls * 0.7 + hStats.avgHomeFouls * 0.3) * awayWeight + 
                      (hStats.avgHomeFouls * 0.7 + aStats.avgAwayFouls * 0.3) * homeWeight) * formFactor;
    
    let finalPred = baseHome + baseAway;
    let refInfo = "Ref: NO";
    
    // Fattore arbitro potenziato
    const rf = DB.refs.find(x=>x.name===ref);
    if(rf && rf.avg > 0) {
        // Calcola media league dai dati disponibili
        let sumF = 0, count = 0;
        Object.values(DB.teamStats).forEach(t => {
            sumF += t.avgHomeFouls + t.avgAwayFouls;
            count += 2;
        });
        const leagueAvg = count > 0 ? sumF / count : 24.5;
        const delta = rf.avg - leagueAvg;
        const smoothing = 0.7;
        const finalDelta = delta * smoothing;
        finalPred = finalPred + finalDelta;
        refInfo = `Ref: ${rf.avg} (Impact: ${finalDelta > 0 ? '+' : ''}${finalDelta.toFixed(1)})`;
    }
    
    renderBox('grid-falli', "MATCH TOTALE", finalPred, 'line-f-match');
    renderBox('grid-falli', home, baseHome, 'line-f-h');
    renderBox('grid-falli', away, baseAway, 'line-f-a');
    
    document.getElementById('title-falli').innerText = `Analisi Falli (${refInfo})`;
    document.getElementById('sec-falli').classList.remove('hidden');
}

// Calcolo tiri potenziato per tutti i campionati
function calculateShotsEnhanced(home, away) {
    const hStats = DB.teamStats[home];
    const aStats = DB.teamStats[away];
    
    if(!hStats || !aStats) {
        document.getElementById('sec-tiri').classList.add('hidden');
        return;
    }
    
    // Algoritmo potenziato
    const homeAdvantage = 1.12;
    const momentum = 1.05;
    
    // Tiri attesi con correlazione tra attacco e difesa
    const expHome = ((hStats.avgHomeShots * 0.8 + aStats.avgAwayShots * 0.2) * 0.6 + 
                     (aStats.avgAwayShots * 0.8 + hStats.avgHomeShots * 0.2) * 0.4) * homeAdvantage * momentum;
    const expAway = ((aStats.avgAwayShots * 0.8 + hStats.avgHomeShots * 0.2) * 0.6 + 
                     (hStats.avgHomeShots * 0.8 + aStats.avgAwayShots * 0.2) * 0.4) * momentum;
    
    // Tiri in porta con correlazione
    const homeTargetRate = hStats.avgHomeTarget / hStats.avgHomeShots;
    const awayTargetRate = aStats.avgAwayTarget / aStats.avgAwayShots;
    const leagueAvgRate = (DB.tiriStats.avgHomeTP + DB.tiriStats.avgAwayTP) / (DB.tiriStats.avgHome + DB.tiriStats.avgAway);
    
    const adjHomeTarget = expHome * ((homeTargetRate + leagueAvgRate) / 2);
    const adjAwayTarget = expAway * ((awayTargetRate + leagueAvgRate) / 2);
    
    renderBox('grid-tiri', "MATCH TOTALE", expHome + expAway, 'line-t-match');
    renderBox('grid-tiri', home, expHome, 'line-t-h');
    renderBox('grid-tiri', away, expAway, 'line-t-a');
    
    renderBox('grid-tp', "MATCH IN PORTA", adjHomeTarget + adjAwayTarget, 'line-tp-match');
    renderBox('grid-tp', home, adjHomeTarget, 'line-tp-h');
    renderBox('grid-tp', away, adjAwayTarget, 'line-tp-a');
    
    document.getElementById('sec-tiri').classList.remove('hidden');
}

// ============================================
// RENDERING
// ============================================
function renderBox(id, title, val, lineId) {
    const el = document.getElementById(id);
    if(!el) return;
    if(title.includes("MATCH")) el.innerHTML="";
    
    const line = parseFloat(document.getElementById(lineId).value)||24.5;
    const diff = val - line;
    
    let c="val-low", t="NO VALUE", r="PASS", prob=50;
    prob = poissonProb(line, val, diff>0?'OVER':'UNDER');
    let badge = prob > 65 ? `<span class="confidence-pill">⚡ HIGH CONFIDENCE</span>` : "";
    
    if(diff>=1.5) {
        c="val-high";
        t="SUPER VALORE";
        r=`OVER ${line}`;
    } else if(diff>=0.5) {
        c="val-med";
        t="BUONO";
        r=`OVER ${line}`;
    } else if(diff<=-1.5) {
        c="val-high";
        t="SUPER VALORE";
        r=`UNDER ${line}`;
    } else if(diff<=-0.5) {
        c="val-med";
        t="BUONO";
        r=`UNDER ${line}`;
    }
    
    if(Math.abs(diff) < 0.5) {
        c="bg-slate-800 border-slate-700";
        r="PASS";
        t="NO EDGE";
        prob=50;
        badge="";
    }
    
    el.innerHTML += `<div class="value-box ${c} relative">${badge}<div class="lbl" style="font-size:10px; opacity:0.8">${title}</div><div class="res">${r}</div><div style="font-size:12px; font-weight:bold">AI: ${val.toFixed(2)} | ${t}</div><div class="prob-badge">Prob. ${prob.toFixed(0)}%</div></div>`;
}
</script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
