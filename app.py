import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PROBET AI V4 PRO", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    menu_items=None
)

# CSS INIETTATO PER PULIRE STREAMLIT E OTTIMIZZARE LO SCROLL
hide_streamlit_style = """
<style>
    /* Nasconde elementi Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sfondo Globale Scuro */
    .stApp {
        background-color: #020617 !important;
    }
    
    /* Rimuove padding e margini di Streamlit */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Scrollbar nascosta ma funzionale */
    ::-webkit-scrollbar {
        display: none;
    }
    
    /* Container Streamlit trasparente */
    div[data-testid="stAppViewContainer"] {
        background-color: #020617 !important;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@500;600;700&family=Inter:wght@300;400;600;800&display=swap');

        :root {
            --bg-dark: #020617;
            --card-bg: rgba(30, 41, 59, 0.7);
            --input-bg: rgba(15, 23, 42, 0.8);
            --primary-blue: #3b82f6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; outline: none; }

        html {
            scroll-behavior: smooth;
        }

        body { 
            background-color: var(--bg-dark);
            background-image: radial-gradient(circle at top right, #1e3a8a 0%, transparent 40%),
                              radial-gradient(circle at bottom left, #0f172a 0%, transparent 40%);
            color: var(--text-main); 
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
            -webkit-overflow-scrolling: touch; 
        }

        ::-webkit-scrollbar { width: 0px; background: transparent; }

        .teko { font-family: 'Teko', sans-serif; letter-spacing: 0.05em; }

        .app-wrapper {
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px 16px 80px 16px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            position: relative;
            z-index: 1;
        }

        /* HEADER */
        .header { text-align: center; margin-bottom: 10px; padding-top: 10px; }
        .header h1 { 
            font-size: 3rem; line-height: 0.9; font-weight: 700; text-transform: uppercase; font-style: italic;
            background: linear-gradient(to right, #fff, #94a3b8);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        }
        .header .version {
            font-size: 0.7rem; color: #60a5fa; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 5px; opacity: 0.8;
        }

        /* LEAGUE SELECTOR */
        .league-scroller {
            display: flex; gap: 10px; overflow-x: auto; padding: 4px 4px 14px 4px; margin: 0 -10px; scrollbar-width: none;
        }
        .league-scroller::-webkit-scrollbar { display: none; }
        .league-btn { 
            flex: 0 0 auto; cursor: pointer; padding: 10px 16px; border-radius: 12px; font-weight: 700; font-size: 12px;
            border: 1px solid rgba(255,255,255,0.1); background: rgba(15, 23, 42, 0.6); color: #94a3b8;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); backdrop-filter: blur(4px);
        }
        .league-active { 
            background: var(--primary-blue); border-color: var(--primary-blue); color: white; 
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4); transform: scale(1.05);
        }

        /* MAIN CARD */
        .glass-card { 
            background: var(--card-bg); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            border-radius: 24px; padding: 24px 20px; border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3); margin-bottom: 20px;
        }

        /* INPUTS */
        .input-group { margin-bottom: 16px; }
        .input-label { font-size: 11px; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; display: block; }
        select, input[type="number"] { 
            width: 100%; background: var(--input-bg); border: 1px solid rgba(255,255,255,0.1); color: white; 
            padding: 14px 16px; border-radius: 14px; font-size: 15px; font-weight: 600; transition: all 0.2s; appearance: none;
        }
        select:focus, input:focus { border-color: var(--primary-blue); box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.15); background: #0f172a; }
        select {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%2394a3b8'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M19 9l-7 7-7-7'/%3E%3C/svg%3E");
            background-repeat: no-repeat; background-position: right 16px center; background-size: 16px;
        }

        /* SPREAD GRID */
        .spread-section { margin-top: 24px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); }
        .spread-title { font-size: 12px; font-weight: 800; color: white; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
        .dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .grid-input-item label { font-size: 9px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; display: block; text-align: center; }
        .grid-input-item input { padding: 10px 4px; text-align: center; font-size: 14px; }

        /* BUTTON */
        .btn-action { 
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%); width: 100%; padding: 18px; border-radius: 16px; 
            font-weight: 800; text-transform: uppercase; cursor: pointer; border: none; color: white; font-size: 1.1rem;
            font-family: 'Teko', sans-serif; letter-spacing: 0.1em; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.5);
            transition: transform 0.1s, box-shadow 0.2s; position: relative; overflow: hidden;
        }
        .btn-action:active { transform: scale(0.98); box-shadow: 0 5px 15px -5px rgba(37, 99, 235, 0.5); }
        
        /* RESULTS */
        .result-card {
            background: rgba(15, 23, 42, 0.9); border-radius: 20px; padding: 20px; margin-bottom: 16px;
            border: 1px solid rgba(255,255,255,0.05); position: relative; overflow: hidden;
            animation: slideUp 0.5s ease-out forwards;
            opacity: 0;
            transform: translateY(20px);
        }
        @keyframes slideUp { to { opacity: 1; transform: translateY(0); } }

        .result-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; }
        .border-green::before { background: #10b981; box-shadow: 0 0 15px #10b981; }
        .border-purple::before { background: #a78bfa; box-shadow: 0 0 15px #a78bfa; }
        .border-cyan::before { background: #22d3ee; box-shadow: 0 0 15px #22d3ee; }
        .border-yellow::before { background: #fbbf24; box-shadow: 0 0 15px #fbbf24; }
        .border-red::before { background: #ef4444; box-shadow: 0 0 15px #ef4444; }

        .res-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
        .res-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
        .badge-pro { font-size: 9px; padding: 2px 6px; border-radius: 4px; background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.7); font-weight: 600; }
        .res-value { font-family: 'Teko', sans-serif; font-size: 2.8rem; line-height: 1; font-weight: 600; margin-bottom: 4px; }
        
        .tag-pill { display: inline-flex; align-items: center; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 800; text-transform: uppercase; }
        .tag-over { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .tag-under { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }

        .progress-track { height: 6px; background: rgba(255,255,255,0.05); border-radius: 3px; margin: 12px 0 16px 0; overflow: hidden; }
        .progress-fill { height: 100%; border-radius: 3px; transition: width 1s ease-out; }

        .split-stats { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.05); }
        .stat-col h4 { font-size: 10px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 4px; }
        .stat-col .val { font-family: 'Teko'; font-size: 1.4rem; font-weight: 500; }
        .stat-col.right { text-align: right; }

        .loader-container { text-align: center; padding: 40px 0; }
        .pulse-text { font-family: 'Teko'; font-size: 2rem; color: #3b82f6; animation: pulse 1.5s infinite; }
        @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }

        .hidden { display: none !important; }
        .status-msg { padding: 12px; border-radius: 12px; font-size: 13px; font-weight: 600; margin-bottom: 16px; text-align: center; }
        .status-err { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }
    </style>
</head>
<body>

<div class="app-wrapper">
    
    <div class="header">
        <h1 class="teko">PROBET <span style="color:#3b82f6">AI</span></h1>
        <div class="version">V4 PRO • ELITE ANALYSIS 2026/27</div>
    </div>

    <div class="league-scroller">
        <div id="btn-7286" class="league-btn league-active" onclick="switchLeague(7286)">SERIE A</div>
        <div id="btn-7293" class="league-btn" onclick="switchLeague(7293)">PREMIER</div>
        <div id="btn-7338" class="league-btn" onclick="switchLeague(7338)">BUNDES</div>
        <div id="btn-7351" class="league-btn" onclick="switchLeague(7351)">LA LIGA</div>
    </div>

    <div class="glass-card">
        <div id="statusMessage" class="status-msg hidden"></div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
            <div class="input-group" style="margin-bottom:0">
                <label class="input-label" style="color:#60a5fa">Home Team</label>
                <select id="homeTeam"><option>Caricamento...</option></select>
            </div>
            <div class="input-group" style="margin-bottom:0">
                <label class="input-label" style="color:#60a5fa">Away Team</label>
                <select id="awayTeam"><option>Caricamento...</option></select>
            </div>
        </div>
        
        <div id="arbitroContainer" class="input-group">
            <label class="input-label" style="color:#fbbf24">Arbitro (Serie A)</label>
            <select id="arbitroSelect"><option value="24.5">Seleziona Arbitro...</option></select>
        </div>

        <div class="spread-section">
            <div class="spread-title"><span class="dot" style="background:#34d399"></span> Tiri Totali</div>
            <div class="grid-3">
                <div class="grid-input-item"><label>Tot</label><input type="number" id="sprTotalMatch" step="0.5" value="23.5"></div>
                <div class="grid-input-item"><label>Casa</label><input type="number" id="sprTotalH" step="0.5" value="12.5"></div>
                <div class="grid-input-item"><label>Osp</label><input type="number" id="sprTotalA" step="0.5" value="10.5"></div>
            </div>
        </div>

        <div class="spread-section">
            <div class="spread-title"><span class="dot" style="background:#a78bfa"></span> Tiri In Porta</div>
            <div class="grid-3">
                <div class="grid-input-item"><label>Tot</label><input type="number" id="sprOTMatch" step="0.5" value="8.5"></div>
                <div class="grid-input-item"><label>Casa</label><input type="number" id="sprOTH" step="0.5" value="4.5"></div>
                <div class="grid-input-item"><label>Osp</label><input type="number" id="sprOTA" step="0.5" value="3.5"></div>
            </div>
        </div>

        <div id="foulsInputs" class="spread-section">
            <div class="spread-title"><span class="dot" style="background:#f87171"></span> Falli Commessi</div>
            <div class="grid-3">
                <div class="grid-input-item"><label>Tot</label><input type="number" id="sprFoulsMatch" step="0.5" value="24.5"></div>
                <div class="grid-input-item"><label>Casa</label><input type="number" id="sprFoulsH" step="0.5" value="12.5"></div>
                <div class="grid-input-item"><label>Osp</label><input type="number" id="sprFoulsA" step="0.5" value="11.5"></div>
            </div>
        </div>

        <div class="spread-section">
            <div class="spread-title"><span class="dot" style="background:#22d3ee"></span> Corner</div>
            <div class="grid-3">
                <div class="grid-input-item"><label>Tot</label><input type="number" id="sprCornMatch" step="0.5" value="9.5"></div>
                <div class="grid-input-item"><label>Casa</label><input type="number" id="sprCornH" step="0.5" value="5.5"></div>
                <div class="grid-input-item"><label>Osp</label><input type="number" id="sprCornA" step="0.5" value="4.5"></div>
            </div>
        </div>

        <div class="spread-section">
            <div class="spread-title"><span class="dot" style="background:#fbbf24"></span> Cartellini Gialli</div>
            <div class="grid-3">
                <div class="grid-input-item"><label>Tot</label><input type="number" id="sprCardsMatch" step="0.5" value="4.5"></div>
                <div class="grid-input-item"><label>Casa</label><input type="number" id="sprCardsH" step="0.5" value="2.5"></div>
                <div class="grid-input-item"><label>Osp</label><input type="number" id="sprCardsA" step="0.5" value="2.5"></div>
            </div>
        </div>

        <form id="adForm" action="https://probetai.com/mostra_pubblicita" method="GET" target="_blank" style="display:none;">
            <input type="hidden" name="trigger" value="ad">
        </form>

        <button onclick="triggerAdAndCalculate()" class="btn-action" style="margin-top: 24px;">
            GENERA ANALISI ELITE PRO
        </button>
    </div>

    <div id="results" class="hidden"></div>

</div>

<script>
// La chiamata diretta del browser a v3.football.api-sports.io viene bloccata dal
// browser stesso per policy CORS (il server dell'API non concede il permesso alle
// pagine web di chiamarlo direttamente) - confermato con un test reale il 20/07/2026.
// Tutte le chiamate passano quindi da un piccolo proxy (Firebase Cloud Function) che
// gira lato server, dove la chiave API-Football resta nascosta e sicura.
// IMPORTANTE: dopo aver pubblicato la function su Firebase, incolla qui il suo URL
// (es. "https://us-central1-tuoprogetto.cloudfunctions.net/footballProxy").
const PROXY_BASE_URL = "https://footballproxy-p47hlkstxa-uc.a.run.app";

// Costruisce l'URL da chiamare passando dal proxy invece che direttamente all'API.
function apiUrl(path, paramsObj) {
    const params = new URLSearchParams();
    Object.keys(paramsObj || {}).forEach(k => params.append(k, paramsObj[k]));
    return `${PROXY_BASE_URL}?path=${encodeURIComponent(path)}&${params.toString()}`;
}
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
const REFS_FILE = "ARBITRI_SERIE_A - Foglio1.csv";
let currentLeague = 7286, dbXG = [];

const LEAGUE_DATA = {
    7286: { name: "SERIE A", file: "DATABASE_AVANZATO_SERIEA_2025.csv", oldId: 135, apiId: 7286, homeAdv: 1.08 },
    7293: { name: "PREMIER LEAGUE", file: "DATABASE_AVANZATO_PREMIER_2025.csv", oldId: 39, apiId: 7293, homeAdv: 1.05 },
    7338: { name: "BUNDESLIGA", file: "DATABASE_AVANZATO_BUNDES_2025.csv", oldId: 78, apiId: 7338, homeAdv: 1.12 },
    7351: { name: "LA LIGA", file: "DATABASE_AVANZATO_LALIGA_2025.csv", oldId: 140, apiId: 7351, homeAdv: 1.06 }
};

// Baseline di lega, usate SOLO come ancora per lo shrinkage bayesiano e come fallback
// quando non ci sono abbastanza dati reali (mai come sostituto silenzioso dei dati veri).
// STAGIONE API: durante le prime 3-4 giornate (dati insufficienti per tutte le squadre
// nella stagione nuova) resta su 2025 (stagione precedente). Da settembre in poi, quando
// ci saranno abbastanza partite giocate nella stagione 2025/26 per tutte le squadre
// (incluse le neopromosse), cambiare SOLO questo numero in 2026.
const SEASON = 2025;

// Stagione precedente, usata come "base di partenza" quando la stagione corrente ha
// ancora poche partite giocate (tipico delle prime giornate dopo il cambio di SEASON).
// Il peso tra le due stagioni NON va mai regolato a mano: si autoregola da solo tramite
// combineEstimates, che pesa ogni fonte in base a quanti dati reali ha dietro - man mano
// che la stagione corrente accumula partite, il suo peso cresce e quello della stagione
// precedente scende automaticamente, fino a diventare trascurabile.
const PREVIOUS_SEASON = SEASON - 1;
// Sotto questa soglia di partite giocate nella stagione corrente, si integra anche la
// stagione precedente (chiamate API aggiuntive). Oltre questa soglia, si risparmiano
// le chiamate perche' la stagione corrente ha gia' abbastanza dati da sola.
// NOTA: 10 e non un numero piu' basso - a 5 partite la stagione precedente ha ancora
// un'influenza consistente sul calcolo (per via del meccanismo di pesatura automatica),
// quindi fermarsi li' creerebbe un taglio brusco invece di uno sfumare graduale.
const CURRENT_SEASON_MIN_GAMES = 10;

const LEAGUE_PRIORS = {
    7286: { shots: 12.2, sot: 4.2, corners: 5.0, cards: 2.2, fouls: 12.0 },
    7293: { shots: 11.2, sot: 4.0, corners: 4.8, cards: 1.6, fouls: 10.0 },
    7338: { shots: 12.6, sot: 4.4, corners: 5.2, cards: 1.8, fouls: 11.5 },
    7351: { shots: 11.6, sot: 4.0, corners: 4.9, cards: 2.4, fouls: 11.0 }
};

function setStatus(msg, type) {
    const el = document.getElementById('statusMessage');
    if (!msg) { el.classList.add('hidden'); return; }
    el.textContent = msg;
    el.className = 'status-msg status-' + type;
    el.classList.remove('hidden');
}

function triggerAdAndCalculate() {
    const form = document.getElementById('adForm');
    if(form) form.submit();
    setTimeout(() => {
        const w = window.open("about:blank/mostra_pubblicita", "_blank");
        if(w) w.close();
    }, 10);
    setTimeout(() => {
        window.location.hash = "mostra_pubblicita_trigger";
    }, 50);
    setTimeout(() => {
        runDeepAnalysis();
    }, 400);
}

function switchLeague(id) {
    currentLeague = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById(`btn-${id}`).classList.add('league-active');
    
    const isSerieA = (id === 7286);
    const arbContainer = document.getElementById('arbitroContainer');
    const foulsContainer = document.getElementById('foulsInputs');
    
    if(isSerieA) {
        arbContainer.classList.remove('hidden');
        foulsContainer.classList.remove('hidden');
    } else {
        arbContainer.classList.add('hidden');
        foulsContainer.classList.add('hidden');
    }
    
    loadData();
}

function loadData() {
    const leagueInfo = LEAGUE_DATA[currentLeague];
     Papa.parse(BASE_CSV_URL + leagueInfo.file, { 
        download: true, header: true, skipEmptyLines: true, 
        complete: (r) => { dbXG = r.data; loadTeams(); },
        error: (err) => { console.error("Errore CSV:", err); setStatus("Errore caricamento database CSV", 'err'); }
    });

    if(currentLeague === 7286) {
        // CORRETTO: Adesso usiamo "BASE_CSV_URL + REFS_FILE" per scaricare il file online su GitHub!
        Papa.parse(BASE_CSV_URL + REFS_FILE, { 
            download: true, 
            header: false, 
            skipEmptyLines: true, 
            complete: (r) => {
                const sel = document.getElementById('arbitroSelect'); 
                sel.innerHTML = '<option value="24.5,11,13.5">Seleziona Arbitro...</option>';
                
                const rows = r.data.slice(1);

                rows.forEach(row => {
                    if (row.length >= 5) {
                        let name = row[0]; 
                        let valTotal = row[2]; 
                        let valHome = row[3]; 
                        let valAway = row[4]; 

                        if(name && valTotal && valHome && valAway) {
                            let cleanName = name.toString().trim();
                            let cleanTotal = valTotal.toString().replace(',', '.').trim();
                            let cleanHome = valHome.toString().replace(',', '.').trim();
                            let cleanAway = valAway.toString().replace(',', '.').trim();

                            if (cleanName !== "") {
                                let optionValue = `${cleanTotal},${cleanHome},${cleanAway}`;
                                sel.add(new Option(cleanName, optionValue));
                            }
                        }
                    }
                });
            },
            error: (err) => {
                console.error("Errore nel caricamento del file degli arbitri:", err);
            }
        });
    }
}

async function loadTeams() {
    const h = document.getElementById('homeTeam'), a = document.getElementById('awayTeam');
    h.innerHTML = '<option>Caricamento...</option>';
    a.innerHTML = '<option>Caricamento...</option>';

    try {
        const leagueInfo = LEAGUE_DATA[currentLeague];
        let apiId = leagueInfo.apiId;

        let res = await fetch(apiUrl('teams', { league: apiId, season: SEASON }));
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        let data = await res.json();

        if (!data.response || data.response.length === 0) {
            apiId = leagueInfo.oldId;
            res = await fetch(apiUrl('teams', { league: apiId, season: SEASON }));
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            data = await res.json();
        }

        if (!data.response || data.response.length === 0) throw new Error("Nessuna squadra trovata");

        h.innerHTML = ""; a.innerHTML = "";
        h.add(new Option("-- Seleziona Casa --", ""));
        a.add(new Option("-- Seleziona Ospite --", ""));

        let mergedTeams = [];
        let csvTeamNames = dbXG.map(row => row.TeamName.toLowerCase().trim());

        data.response.forEach(t => {
            const apiTeamName = t.team.name.toLowerCase().trim();
            if(csvTeamNames.includes(apiTeamName)) {
                mergedTeams.push({ id: t.team.id, name: t.team.name });
            }
        });

        let addedIds = new Set(mergedTeams.map(x => x.id.toString()));
        dbXG.forEach(row => {
            if (row.TeamID && !addedIds.has(row.TeamID.toString())) {
                mergedTeams.push({ id: parseInt(row.TeamID), name: row.TeamName });
                addedIds.add(row.TeamID.toString());
            }
        });

        mergedTeams.sort((x,y) => x.name.localeCompare(y.name)).forEach(t => {
            h.add(new Option(t.name, t.id)); 
            a.add(new Option(t.name, t.id));
        });
        setStatus("", "");
    } catch (e) {
        h.innerHTML = '<option>Errore</option>';
        a.innerHTML = '<option>Errore</option>';
        setStatus(`Errore caricamento squadre: ${e.message}`, 'err');
    }
}

/* =========================================================================
   MOTORE STATISTICO
   - Le probabilità Over/Under sono calcolate con un'approssimazione Normale
     (media + varianza reale stimata dai dati), con correzione di continuità,
     al posto di una sigmoide con coefficiente arbitrario.
   - Le stime di media per ogni metrica combinano piu' fonti (stagione,
     forma recente pesata per recency, rendimento casa/trasferta specifico)
     pesando ciascuna fonte in base alla numerosita' del campione.
   - Per cartellini e falli (molto rumorosi) si applica shrinkage bayesiano
     verso una media di lega, per non farsi ingannare da campioni piccoli.
   NOTA: alcuni percorsi di campo dell'endpoint teams/statistics (es. shots,
   corners, fouls, cards) sono stati mantenuti come nel codice originale ma
   NON sono garantiti dallo schema ufficiale API-Football: vanno verificati
   con la chiave a pagamento reale. Per questo motivo il modello pesa di piu'
   le statistiche aggregate direttamente dalle singole partite (piu' affidabili
   perche' calcolate qui) rispetto alla media stagionale dichiarata dall'API.
   ========================================================================= */

// Approssimazione della funzione di errore (Abramowitz-Stegun)
function erf(x) {
    const sign = x >= 0 ? 1 : -1;
    x = Math.abs(x);
    const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741,
          a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
    const t = 1 / (1 + p * x);
    const y = 1 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
    return sign * y;
}

function normalCDF(x, mean, sd) {
    if (!sd || sd <= 0) sd = 0.5;
    return 0.5 * (1 + erf((x - mean) / (sd * Math.sqrt(2))));
}

/* ---- Motore di probabilita' per dati di conteggio (Poisson / Binomiale Negativa) ----
   Tiri, corner, cartellini e falli sono conteggi non-negativi, spesso asimmetrici a media
   bassa: una Normale simmetrica li approssima male, specialmente su linee estreme.
   Poisson/Binomiale Negativa sono lo standard corretto per questo tipo di dato
   (lo stesso approccio usato nei modelli quantitativi di analisi sportiva professionali). */

// Log-gamma (approssimazione di Lanczos), serve per la funzione beta incompleta
function logGamma(x) {
    const g = 7;
    const c = [
        0.99999999999980993, 676.5203681218851, -1259.1392167224028,
        771.32342877765313, -176.61502916214059, 12.507343278686905,
        -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7
    ];
    if (x < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * x)) - logGamma(1 - x);
    x -= 1;
    let a = c[0];
    const t = x + g + 0.5;
    for (let i = 1; i < g + 2; i++) a += c[i] / (x + i);
    return 0.5 * Math.log(2 * Math.PI) + (x + 0.5) * Math.log(t) - t + Math.log(a);
}

// Frazione continua per la funzione beta incompleta (metodo standard, Numerical Recipes)
function betacf(x, a, b) {
    const MAXIT = 200, EPS = 3e-9, FPMIN = 1e-30;
    const qab = a + b, qap = a + 1, qam = a - 1;
    let c = 1, d = 1 - qab * x / qap;
    if (Math.abs(d) < FPMIN) d = FPMIN;
    d = 1 / d;
    let h = d;
    for (let m = 1; m <= MAXIT; m++) {
        const m2 = 2 * m;
        let aa = m * (b - m) * x / ((qam + m2) * (a + m2));
        d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN;
        c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN;
        d = 1 / d;
        h *= d * c;
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
        d = 1 + aa * d; if (Math.abs(d) < FPMIN) d = FPMIN;
        c = 1 + aa / c; if (Math.abs(c) < FPMIN) c = FPMIN;
        d = 1 / d;
        const del = d * c;
        h *= del;
        if (Math.abs(del - 1) < EPS) break;
    }
    return h;
}

// Funzione beta incompleta regolarizzata I_x(a,b)
function regularizedIncompleteBeta(x, a, b) {
    if (x <= 0) return 0;
    if (x >= 1) return 1;
    const bt = Math.exp(logGamma(a + b) - logGamma(a) - logGamma(b) + a * Math.log(x) + b * Math.log(1 - x));
    if (x < (a + 1) / (a + b + 2)) return bt * betacf(x, a, b) / a;
    return 1 - bt * betacf(1 - x, b, a) / b;
}

// CDF di Poisson: P(X <= k), calcolata per somma diretta della PMF (efficiente per i conteggi tipici del calcio)
function poissonCDF(k, lambda) {
    if (lambda <= 0) return 1;
    if (k < 0) return 0;
    let term = Math.exp(-lambda);
    let sum = term;
    for (let i = 1; i <= k; i++) {
        term *= lambda / i;
        sum += term;
    }
    return Math.min(sum, 1);
}

// CDF della Binomiale Negativa (parametrizzata per media e varianza, metodo dei momenti):
// P(X <= k) = I_p(r, k+1), valida solo quando varianza > media (sovradispersione)
function negBinomCDF(k, mu, varr) {
    if (k < 0) return 0;
    if (varr <= mu) return null;
    const r = (mu * mu) / (varr - mu);
    const p = r / (r + mu);
    return regularizedIncompleteBeta(p, r, k + 1);
}

// Probabilita' che il conteggio superi una linea (tipicamente X.5): usa Binomiale Negativa
// se c'e' sovradispersione reale nei dati, altrimenti Poisson. Una dispersione minima
// (varianza = media*1.2) viene imposta quando il dato osservato non e' sufficiente,
// perche' in pratica quasi tutte le statistiche calcistiche sono leggermente sovradisperse.
function probOver(mean, variance, line) {
    if (mean == null || isNaN(mean) || mean <= 0) return 0.5;
    const k = Math.floor(line);
    let varr = variance;
    if (!varr || varr < mean * 1.05) varr = mean * 1.2;
    const cdf = varr > mean ? negBinomCDF(k, mean, varr) : poissonCDF(k, mean);
    return Math.max(0, Math.min(1, 1 - cdf));
}

// Correlazione di "ritmo di gioco" tra le prestazioni delle due squadre nella stessa partita:
// una gara aperta produce piu' tiri, piu' corner e piu' cartellini per ENTRAMBE le squadre
// insieme, quindi sommare le varianze come se fossero indipendenti sottostima l'incertezza
// reale. Il coefficiente 0.20 e' una stima ragionevole non calibrata su dati storici (nessuno
// storico verificato esiste ancora); va considerato un miglioramento qualitativo, non un
// numero misurato.
const RHO_GAME_PACE = 0.20;
function combinedVariance(varH, varA) {
    const vH = Math.max(varH || 0, 0), vA = Math.max(varA || 0, 0);
    return vH + vA + 2 * RHO_GAME_PACE * Math.sqrt(vH * vA);
}

// Media e varianza pesate per recency su un array di valori (ordine: vecchio -> recente)
function weightedStats(values) {
    if (!values || values.length === 0) return { mean: null, variance: null, n: 0 };
    const n = values.length;
    const weights = values.map((_, i) => Math.pow(1.12, i));
    const wSum = weights.reduce((a, b) => a + b, 0);
    const wMean = values.reduce((acc, v, i) => acc + v * weights[i], 0) / wSum;
    let wVar = values.reduce((acc, v, i) => acc + weights[i] * Math.pow(v - wMean, 2), 0) / wSum;
    if (n > 1) wVar = wVar * n / (n - 1);
    return { mean: wMean, variance: wVar, n };
}

// Fonde piu' stime (con relativa numerosita' campionaria) in un'unica media pesata
function combineEstimates(sources) {
    let totalWeight = 0, weightedSum = 0;
    sources.forEach(s => {
        if (s.mean == null || isNaN(s.mean)) return;
        const w = Math.max(s.n || 0, 0.5) * (s.priorWeight || 1);
        weightedSum += s.mean * w;
        totalWeight += w;
    });
    if (totalWeight === 0) return null;
    return weightedSum / totalWeight;
}

// Ritira una stima verso una media di lega quando il campione e' piccolo
function shrinkEstimate(sampleMean, n, priorMean, k) {
    if (sampleMean == null || isNaN(sampleMean)) return priorMean;
    const w = (n || 0) / ((n || 0) + (k || 5));
    return sampleMean * w + priorMean * (1 - w);
}

// Legge un valore manuale opzionale dal CSV (es. per neopromosse prive di storico
// nella lega/stagione corrente). Colonne attese nel CSV: TiriManual, TiriPortaManual.
// Se la colonna manca o e' vuota per quella squadra, ritorna null e si ricade
// sulla media di lega standard (comportamento invariato per tutte le altre squadre).
function getManualValue(teamId, columnName) {
    const row = dbXG.find(x => x.TeamID == teamId);
    if (!row || row[columnName] == null || row[columnName].toString().trim() === '') return null;
    const v = parseFloat(row[columnName].toString().replace(',', '.').trim());
    return isNaN(v) ? null : v;
}

// L'endpoint teams/statistics NON fornisce una media diretta di cartellini a partita:
// li restituisce divisi per fascia oraria (0-15, 16-30, ... 91-105). Per ottenere una
// vera media stagionale bisogna sommare tutte le fasce e dividere per le partite giocate.
// Confermato dalla risposta reale dell'API (test del 20/07/2026): shots, corners e fouls
// NON esistono affatto in questo endpoint, quindi per quelle tre metriche non esiste una
// fonte stagionale utilizzabile qui - il modello si affida a quelle prese da "fixtures"
// (forma, casa/trasferta, H2H), gia' confermate corrette e gia' pesate maggiormente.
function sumSeasonCardBuckets(cardsYellowObj, played) {
    if (!cardsYellowObj || !played) return null;
    const buckets = ['0-15', '16-30', '31-45', '46-60', '61-75', '76-90', '91-105', '106-120'];
    let sum = 0, any = false;
    buckets.forEach(b => {
        const v = cardsYellowObj[b] && cardsYellowObj[b].total;
        if (v != null) { sum += v; any = true; }
    });
    return any ? (sum / played) : null;
}

// Rapporto varianza/media tipico per ciascuna metrica (sovradispersione attesa in dati
// calcistici reali). I cartellini e i falli sono decisioni discrete e dipendenti
// dall'arbitro (piu' "a scatti"), quindi tendono ad avere una dispersione maggiore
// rispetto ai tiri. Questi rapporti sono stime ragionevoli di letteratura di analisi
// sportiva, NON calibrate sui tuoi dati specifici (nessuno storico verificato esiste
// ancora per questa app).
const DISPERSION_RATIO = { shots: 1.20, sot: 1.15, corners: 1.30, cards: 1.60, fouls: 1.40 };

// Sfuma gradualmente la varianza osservata verso una varianza "attesa" (media * rapporto
// di sovradispersione tipico), invece di un taglio netto (Math.max). Piu' partite reali
// si hanno (n alto), piu' ci si fida della varianza osservata; con pochi dati si resta
// vicini al rapporto tipico di mercato per quella metrica.
function blendVariance(empiricalVar, n, mean, metricKey, k) {
    const priorVar = Math.max(mean, 0.1) * (DISPERSION_RATIO[metricKey] || 1.25);
    if (empiricalVar == null || isNaN(empiricalVar) || !n || n < 2) return priorVar;
    const w = n / (n + (k || 4));
    return empiricalVar * w + priorVar * (1 - w);
}

// Limita un valore in un intervallo di plausibilita' realistica per il calcio professionistico.
// Serve solo come rete di sicurezza numerica: con campioni piccoli, una catena di fattori
// moltiplicativi (xG x forma x momentum x H2H) puo' in teoria comporsi verso valori assurdi.
// Non cambia la logica di stima, taglia solo gli estremi statisticamente implausibili.
function clip(value, lo, hi) {
    if (value == null || isNaN(value)) return value;
    return Math.max(lo, Math.min(hi, value));
}

// Genera il markup del pronostico con probabilita' reale + indice di qualita' del dato
function getAdviceAdvanced(mean, variance, n, spread) {
    const p = probOver(mean, variance, spread);
    const confPct = p * 100;
    const isOver = confPct >= 50;
    const displayConf = isOver ? confPct : 100 - confPct;
    const direction = isOver ? 'OVER' : 'UNDER';

    // n puo' legittimamente essere 0 (nessun dato reale trovato, es. neopromossa
    // senza storico): va trattato come "zero campione", non confuso con "sconosciuto".
    const realN = (n === null || n === undefined) ? 0 : n;
    const sampleScore = Math.min(1, realN / 8);
    const distanceScore = Math.abs(displayConf - 50) / 50;
    const qualityIndex = (sampleScore * 0.55) + (distanceScore * 0.45);

    let precisionLabel = qualityIndex >= 0.7 ? 'ALTA' : qualityIndex >= 0.45 ? 'MEDIA' : 'BASE';
    // Se non c'e' nessun dato reale dietro la stima (fallback su media di lega o
    // valore manuale CSV), l'etichetta deve essere onesta: sempre BASE, indipendentemente
    // da quanto la previsione si allontani dalla linea inserita.
    if (realN === 0) precisionLabel = 'BASE';

    return {
        html: `<span class="tag-pill ${isOver ? 'tag-over' : 'tag-under'}">${direction} ${spread} (${displayConf.toFixed(1)}%)</span>`,
        confidence: Math.min(Math.max(displayConf, 5), 95),
        isOver: isOver,
        precision: precisionLabel
    };
}

function renderConfidenceBar(confidence) {
    let color = confidence >= 75 ? '#10b981' : confidence >= 60 ? '#f59e0b' : '#ef4444';
    return `<div class="progress-track"><div class="progress-fill" style="width:${confidence}%;background:${color}"></div></div>`;
}

function renderFormBar(results, alignRight) {
    if (!results || results.length === 0) return '';
    let html = `<div style="display:flex; gap:3px; justify-content:${alignRight ? 'flex-end' : 'flex-start'}; margin-top:6px;">`;
    results.slice(0, 5).reverse().forEach(r => {
        const outcome = r === 'W' ? 'V' : r === 'D' ? 'N' : 'S';
        const color = r === 'W' ? '#10b981' : r === 'D' ? '#f59e0b' : '#ef4444';
        html += `<div style="width:18px;height:18px;border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:8px;font-weight:900;color:white;background:${color}">${outcome}</div>`;
    });
    html += '</div>';
    return html;
}

// Estrae dagli statistics di una fixture il valore di un tipo di statistica
function extractStat(statObj, label) {
    if (!statObj || !statObj.statistics) return null;
    const f = statObj.statistics.find(s => s.type === label);
    if (!f || f.value == null) return null;
    const v = parseInt(f.value);
    return isNaN(v) ? null : v;
}

// Recupera le statistiche dettagliate (tiri, cartellini, corner, falli) di UNA singola
// partita gia' giocata. CONFERMATO con una chiamata reale il 20/07/2026: l'endpoint
// /fixtures in blocco (quando si chiede "le ultime N partite di una squadra") NON include
// queste statistiche, vanno richieste separatamente partita per partita con questo endpoint.
async function getFixtureStatistics(fixtureId) {
    try {
        const res = await fetch(apiUrl('fixtures/statistics', { fixture: fixtureId }));
        const data = await res.json();
        if (!data.response || data.response.length < 2) return null;
        return data.response; // [{team:{id,...}, statistics:[...]}, {team:{id,...}, statistics:[...]}]
    } catch (e) { return null; }
}

// Dentro le statistiche di una partita (2 blocchi, uno per squadra), separa il blocco
// della squadra richiesta ("own") da quello dell'avversario ("opp": quello che concede).
function splitStatsByTeam(statsArray, teamId) {
    if (!statsArray) return { own: null, opp: null };
    const own = statsArray.find(s => s.team && s.team.id == teamId) || null;
    const opp = statsArray.find(s => s.team && s.team.id != teamId) || null;
    return { own, opp };
}

// Forma recente: ultime 8 partite, raccoglie array di statistiche per stimare media+varianza reali.
// Raccoglie sia i dati "fatti" (quello che la squadra produce) sia i dati "subiti" (quello che
// concede), leggendo il blocco statistiche dell'avversario nella stessa partita - stessa logica
// del tuo vecchio foglio manuale con colonne "Fatti"/"Subiti". Le statistiche vengono richieste
// con una chiamata dedicata per ogni partita (vedi getFixtureStatistics), eseguite in parallelo.
async function getTeamForm(teamId, apiId) {
    const empty = { results: [], shots: [], sot: [], corners: [], cards: [], fouls: [],
                     concededShots: [], concededSot: [], concededCorners: [], formFactor: 1.0 };
    try {
        const res = await fetch(apiUrl('fixtures', { team: teamId, season: SEASON, league: apiId, last: 5 }));
        const data = await res.json();
        if (!data.response || data.response.length === 0) return empty;

        const fixtures = data.response.slice().reverse(); // vecchio -> recente per pesatura
        const statsResults = await Promise.all(fixtures.map(fx => getFixtureStatistics(fx.fixture.id)));

        let results = [], shots = [], sot = [], corners = [], cards = [], fouls = [];
        let concededShots = [], concededSot = [], concededCorners = [];

        fixtures.forEach((fixture, idx) => {
            const isHome = fixture.teams.home.id == teamId;
            const teamSide = isHome ? fixture.teams.home : fixture.teams.away;
            if (teamSide.winner === true) results.push('W');
            else if (teamSide.winner === false) results.push('L');
            else results.push('D');

            const { own, opp } = splitStatsByTeam(statsResults[idx], teamId);
            if (own) {
                const totShots = extractStat(own, 'Total Shots');
                const onGoal = extractStat(own, 'Shots on Goal');
                const corn = extractStat(own, 'Corner Kicks');
                const yellow = extractStat(own, 'Yellow Cards');
                const foulsCommitted = extractStat(own, 'Fouls');
                if (totShots != null) shots.push(totShots);
                if (onGoal != null) sot.push(onGoal);
                if (corn != null) corners.push(corn);
                if (yellow != null) cards.push(yellow);
                if (foulsCommitted != null) fouls.push(foulsCommitted);
            }
            if (opp) {
                // "Subiti": quello che l'avversario ha prodotto in questa partita = quello che
                // la squadra in esame ha concesso.
                const concShots = extractStat(opp, 'Total Shots');
                const concSot = extractStat(opp, 'Shots on Goal');
                const concCorn = extractStat(opp, 'Corner Kicks');
                if (concShots != null) concededShots.push(concShots);
                if (concSot != null) concededSot.push(concSot);
                if (concCorn != null) concededCorners.push(concCorn);
            }
        });

        let formFactor = 1.0;
        results.forEach((r, i) => {
            const weight = (i + 1) / results.length;
            if (r === 'W') formFactor += 0.018 * weight;
            else if (r === 'L') formFactor -= 0.018 * weight;
        });
        formFactor = Math.max(0.90, Math.min(1.10, formFactor));

        return { results, shots, sot, corners, cards, fouls, concededShots, concededSot, concededCorners, formFactor };
    } catch (e) { return empty; }
}

// Rendimento specifico per ruolo (casa o trasferta), separato dalla forma generale.
// Raccoglie anche i dati "subiti" per quel ruolo specifico (es. quanti tiri concede
// una squadra quando gioca in trasferta).
async function getVenueAverages(teamId, apiId, venue) {
    const empty = { shots: [], sot: [], corners: [], cards: [], fouls: [],
                     concededShots: [], concededSot: [], concededCorners: [], n: 0 };
    try {
        const res = await fetch(apiUrl('fixtures', { team: teamId, season: SEASON, league: apiId, last: 10 }));
        const data = await res.json();
        if (!data.response) return empty;

        const isHomeVenue = venue === 'home';
        const filtered = data.response
            .filter(f => isHomeVenue ? f.teams.home.id == teamId : f.teams.away.id == teamId)
            .slice(0, 4);
        if (filtered.length === 0) return empty;

        const statsResults = await Promise.all(filtered.map(fx => getFixtureStatistics(fx.fixture.id)));

        let shots = [], sot = [], corners = [], cards = [], fouls = [];
        let concededShots = [], concededSot = [], concededCorners = [];
        filtered.forEach((fixture, idx) => {
            const { own, opp } = splitStatsByTeam(statsResults[idx], teamId);
            if (own) {
                const totShots = extractStat(own, 'Total Shots');
                const onGoal = extractStat(own, 'Shots on Goal');
                const corn = extractStat(own, 'Corner Kicks');
                const yellow = extractStat(own, 'Yellow Cards');
                const foulsCommitted = extractStat(own, 'Fouls');
                if (totShots != null) shots.push(totShots);
                if (onGoal != null) sot.push(onGoal);
                if (corn != null) corners.push(corn);
                if (yellow != null) cards.push(yellow);
                if (foulsCommitted != null) fouls.push(foulsCommitted);
            }
            if (opp) {
                const concShots = extractStat(opp, 'Total Shots');
                const concSot = extractStat(opp, 'Shots on Goal');
                const concCorn = extractStat(opp, 'Corner Kicks');
                if (concShots != null) concededShots.push(concShots);
                if (concSot != null) concededSot.push(concSot);
                if (concCorn != null) concededCorners.push(concCorn);
            }
        });
        return { shots, sot, corners, cards, fouls, concededShots, concededSot, concededCorners, n: filtered.length };
    } catch (e) { return empty; }
}

// Recupera un campione della STAGIONE PRECEDENTE (PREVIOUS_SEASON), da usare come base
// di partenza quando la stagione corrente ha ancora poche partite giocate. Struttura
// identica a getTeamForm/getVenueAverages, ma senza split casa/trasferta (qui basta un
// campione generale piu' ampio) e senza serie W/D/L (non serve il formFactor da qui).
async function getPreviousSeasonSnapshot(teamId, apiId) {
    const empty = { shots: [], sot: [], corners: [], cards: [], fouls: [],
                     concededShots: [], concededSot: [], concededCorners: [], n: 0 };
    try {
        const res = await fetch(apiUrl('fixtures', { team: teamId, season: PREVIOUS_SEASON, league: apiId, last: 6 }));
        const data = await res.json();
        if (!data.response || data.response.length === 0) return empty;

        const fixtures = data.response;
        const statsResults = await Promise.all(fixtures.map(fx => getFixtureStatistics(fx.fixture.id)));

        let shots = [], sot = [], corners = [], cards = [], fouls = [];
        let concededShots = [], concededSot = [], concededCorners = [];

        fixtures.forEach((fixture, idx) => {
            const { own, opp } = splitStatsByTeam(statsResults[idx], teamId);
            if (own) {
                const totShots = extractStat(own, 'Total Shots');
                const onGoal = extractStat(own, 'Shots on Goal');
                const corn = extractStat(own, 'Corner Kicks');
                const yellow = extractStat(own, 'Yellow Cards');
                const foulsCommitted = extractStat(own, 'Fouls');
                if (totShots != null) shots.push(totShots);
                if (onGoal != null) sot.push(onGoal);
                if (corn != null) corners.push(corn);
                if (yellow != null) cards.push(yellow);
                if (foulsCommitted != null) fouls.push(foulsCommitted);
            }
            if (opp) {
                const concShots = extractStat(opp, 'Total Shots');
                const concSot = extractStat(opp, 'Shots on Goal');
                const concCorn = extractStat(opp, 'Corner Kicks');
                if (concShots != null) concededShots.push(concShots);
                if (concSot != null) concededSot.push(concSot);
                if (concCorn != null) concededCorners.push(concCorn);
            }
        });
        return { shots, sot, corners, cards, fouls, concededShots, concededSot, concededCorners, n: fixtures.length };
    } catch (e) { return empty; }
}
async function getStandingsMomentum(teamId, apiId) {
    try {
        const res = await fetch(apiUrl('standings', { season: SEASON, league: apiId, team: teamId }));
        const data = await res.json();
        if (!data.response || data.response.length === 0) return { position: 10, totalTeams: 20, momentum: 1.0 };

        const standing = data.response[0].league.standings[0][0];
        const position = standing.rank;
        const totalTeams = data.response[0].league.standings[0].length;
        const played = (standing.all && standing.all.played) || 1;
        const goalsDiff = standing.goalsDiff || 0;

        const relativePosition = totalTeams > 1 ? (totalTeams - position) / (totalTeams - 1) : 0.5;
        const gdPerGame = goalsDiff / played;
        let momentum = 1.0 + (relativePosition - 0.5) * 0.08 + Math.max(-0.05, Math.min(0.05, gdPerGame * 0.02));
        momentum = Math.max(0.90, Math.min(1.12, momentum));

        return { position, totalTeams, momentum };
    } catch (e) { return { position: 10, totalTeams: 20, momentum: 1.0 }; }
}

// H2H: ultimi 5 precedenti, pesati per recency, con piu' metriche raccolte
async function getFixturesH2H(teamIdH, teamIdA, apiId) {
    try {
        const res = await fetch(apiUrl('fixtures/headtohead', { h2h: `${teamIdH}-${teamIdA}`, last: 3 }));
        const data = await res.json();
        if (!data.response || data.response.length === 0) return null;

        const fixtures = data.response.slice().reverse();
        const statsResults = await Promise.all(fixtures.map(fx => getFixtureStatistics(fx.fixture.id)));

        let wSum = 0, count = 0;
        let acc = { shotsH: 0, shotsA: 0, sotH: 0, sotA: 0, corners: 0, cards: 0, fouls: 0 };

        fixtures.forEach((fixture, i) => {
            const weight = Math.pow(1.15, i);
            const stats = statsResults[i];
            if (stats && stats.length >= 2) {
                const homeStats = splitStatsByTeam(stats, fixture.teams.home.id).own;
                const awayStats = splitStatsByTeam(stats, fixture.teams.away.id).own;
                const tsH = extractStat(homeStats, 'Total Shots');
                const tsA = extractStat(awayStats, 'Total Shots');
                const sgH = extractStat(homeStats, 'Shots on Goal');
                const sgA = extractStat(awayStats, 'Shots on Goal');
                const corn = (extractStat(homeStats, 'Corner Kicks') || 0) + (extractStat(awayStats, 'Corner Kicks') || 0);
                const crd = (extractStat(homeStats, 'Yellow Cards') || 0) + (extractStat(awayStats, 'Yellow Cards') || 0);
                const fls = (extractStat(homeStats, 'Fouls') || 0) + (extractStat(awayStats, 'Fouls') || 0);

                if (tsH != null) acc.shotsH += tsH * weight;
                if (tsA != null) acc.shotsA += tsA * weight;
                if (sgH != null) acc.sotH += sgH * weight;
                if (sgA != null) acc.sotA += sgA * weight;
                acc.corners += corn * weight;
                acc.cards += crd * weight;
                acc.fouls += fls * weight;
                wSum += weight;
                count++;
            }
        });

        if (count === 0 || wSum === 0) return null;
        return {
            avgShotsH: acc.shotsH / wSum, avgShotsA: acc.shotsA / wSum,
            avgSotH: acc.sotH / wSum, avgSotA: acc.sotA / wSum,
            avgCorners: acc.corners / wSum, avgCards: acc.cards / wSum, avgFouls: acc.fouls / wSum,
            weight: Math.min(count * 0.09, 0.28), n: count
        };
    } catch (e) { return null; }
}

async function runDeepAnalysis() {
    const resDiv = document.getElementById('results');
    resDiv.classList.remove('hidden');
    resDiv.innerHTML = `
        <div class="loader-container">
            <div class="pulse-text teko">ELABORAZIONE DATI...</div>
            <p style="font-size:12px;color:#64748b;margin-top:8px">Analisi forma, classifica e H2H in corso</p>
        </div>
    `;
    
    resDiv.scrollIntoView({behavior:'smooth', block:'center'});

    try {
        const idH = document.getElementById('homeTeam').value;
        const idA = document.getElementById('awayTeam').value;

        if (!idH || !idA) throw new Error("Seleziona entrambe le squadre");
        if (idH === idA) throw new Error("Le squadre devono essere diverse");

        const leagueInfo = LEAGUE_DATA[currentLeague];
        // Per l'endpoint teams/statistics, l'ID lega "nuovo" (es. 7286) restituisce
        // quasi sempre un oggetto "guscio vuoto" (confermato con un test reale il
        // 24/07/2026: league.id null, fixtures.played 0). L'ID "vecchio" (es. 135)
        // e' quello confermato funzionante. Si prova quindi PRIMA quello, per non
        // sprecare 2 chiamate API garantite ad ogni singola analisi.
        let apiId = leagueInfo.oldId;

        let statsH, statsA;

        try {
            const statsRes = await Promise.all([
                fetch(apiUrl('teams/statistics', { league: apiId, season: SEASON, team: idH })).then(async r => {
                    if (!r.ok) { const t = await r.text(); console.error("ERRORE teams/statistics idH, status", r.status, ":", t); return { response: null }; }
                    return r.json();
                }),
                fetch(apiUrl('teams/statistics', { league: apiId, season: SEASON, team: idA })).then(async r => {
                    if (!r.ok) { const t = await r.text(); console.error("ERRORE teams/statistics idA, status", r.status, ":", t); return { response: null }; }
                    return r.json();
                })
            ]);
            statsH = statsRes[0]; statsA = statsRes[1];
            // Una risposta e' considerata NON valida se: manca del tutto, e' un array
            // vuoto [], OPPURE e' un oggetto "guscio vuoto" con i campi league/team
            // interni tutti nulli (visto succedere con l'ID nuovo di alcune leghe:
            // l'API risponde con una struttura apparentemente piena ma senza dati veri).
            function isInvalidStatsResponse(s) {
                if (!s || !s.response) return true;
                if (Array.isArray(s.response)) return s.response.length === 0;
                const r = s.response;
                const hollowLeague = !r.league || r.league.id == null;
                const hollowTeam = !r.team || r.team.id == null;
                return hollowLeague || hollowTeam;
            }
            const isEmptyH = isInvalidStatsResponse(statsH);
            const isEmptyA = isInvalidStatsResponse(statsA);
            if (isEmptyH || isEmptyA) throw new Error("empty");
        } catch (e) {
            // Ripiego sull'ID nuovo solo se anche quello vecchio fallisse (raro, ma
            // teniamo la rete di sicurezza per gli altri 3 campionati non ancora
            // testati uno per uno).
            apiId = leagueInfo.apiId;
            const statsRes = await Promise.all([
                fetch(apiUrl('teams/statistics', { league: apiId, season: SEASON, team: idH })).then(async r => {
                    if (!r.ok) { const t = await r.text(); console.error("ERRORE teams/statistics idH, status", r.status, ":", t); return { response: null }; }
                    return r.json();
                }),
                fetch(apiUrl('teams/statistics', { league: apiId, season: SEASON, team: idA })).then(async r => {
                    if (!r.ok) { const t = await r.text(); console.error("ERRORE teams/statistics idA, status", r.status, ":", t); return { response: null }; }
                    return r.json();
                })
            ]);
            statsH = statsRes[0]; statsA = statsRes[1];
        }

        const [formH, formA, standH, standA, h2hData, venueHomeRaw, venueAwayRaw] = await Promise.all([
            getTeamForm(idH, apiId), getTeamForm(idA, apiId),
            getStandingsMomentum(idH, apiId), getStandingsMomentum(idA, apiId),
            getFixturesH2H(idH, idA, apiId),
            getVenueAverages(idH, apiId, 'home'),
            getVenueAverages(idA, apiId, 'away')
        ]);
        const venueH = venueHomeRaw || { shots: [], sot: [], corners: [], cards: [], fouls: [], concededShots: [], concededSot: [], concededCorners: [], n: 0 };
        const venueA = venueAwayRaw || { shots: [], sot: [], corners: [], cards: [], fouls: [], concededShots: [], concededSot: [], concededCorners: [], n: 0 };

        const sH = statsH.response; const sA = statsA.response;
        const momentumH = standH.momentum; const momentumA = standA.momentum;
        const priors = LEAGUE_PRIORS[currentLeague];

        const xGH_raw = dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || "0.11";
        const xGA_raw = dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || "0.11";
        const xGH = parseFloat(xGH_raw.toString().replace(',', '.'));
        const xGA = parseFloat(xGA_raw.toString().replace(',', '.'));
        const bench = (currentLeague === 7293 || currentLeague === 7338) ? 0.12 : 0.11;

        const nSeasonH = (sH?.fixtures?.played?.total) || 10;
        const nSeasonA = (sA?.fixtures?.played?.total) || 10;

        // Recupera la stagione precedente SOLO se serve (poche partite giocate finora
        // nella stagione corrente), per non sprecare chiamate API quando non necessario.
        const needsPrevH = nSeasonH < CURRENT_SEASON_MIN_GAMES;
        const needsPrevA = nSeasonA < CURRENT_SEASON_MIN_GAMES;
        const [prevSeasonHRaw, prevSeasonARaw] = await Promise.all([
            needsPrevH ? getPreviousSeasonSnapshot(idH, apiId) : Promise.resolve(null),
            needsPrevA ? getPreviousSeasonSnapshot(idA, apiId) : Promise.resolve(null)
        ]);
        const emptyPrev = { shots: [], sot: [], corners: [], cards: [], fouls: [], concededShots: [], concededSot: [], concededCorners: [], n: 0 };
        const prevSeasonH = prevSeasonHRaw || emptyPrev;
        const prevSeasonA = prevSeasonARaw || emptyPrev;
        // Peso della stagione precedente: NON fisso, sfuma linearmente da 0.6 fino a 0
        // esattamente al raggiungimento di CURRENT_SEASON_MIN_GAMES. Cosi', nel momento
        // esatto in cui si smette di scaricarla, il suo peso e' gia' arrivato a zero da
        // solo - nessun salto brusco, solo una sfumatura continua che si esaurisce
        // proprio quando il dato smette di essere raccolto.
        function prevSeasonWeight(nCurrentSeason) {
            if (nCurrentSeason >= CURRENT_SEASON_MIN_GAMES) return 0;
            return 0.6 * (CURRENT_SEASON_MIN_GAMES - nCurrentSeason) / CURRENT_SEASON_MIN_GAMES;
        }
        const PREV_WEIGHT_H = prevSeasonWeight(nSeasonH);
        const PREV_WEIGHT_A = prevSeasonWeight(nSeasonA);


        // ---------------- TIRI TOTALI ----------------
        // Modello attacco/difesa: quanti tiri fara' una squadra dipende sia da quanto
        // attacca lei, sia da quanto concede l'avversaria (stessa logica delle colonne
        // "Fatti"/"Subiti" del vecchio foglio manuale, ora automatizzata dall'API).
        // NOTA: teams/statistics NON contiene dati sui tiri (confermato con una chiamata
        // reale il 20/07/2026) quindi questa metrica dipende SOLO dalle statistiche
        // ricavate dalle singole partite (forma recente + casa/trasferta + H2H).
        const formShotsH = weightedStats(formH.shots);
        const formShotsA = weightedStats(formA.shots);
        const venueShotsH = weightedStats(venueH.shots);
        const venueShotsA = weightedStats(venueA.shots);
        // Difesa avversaria: quanto concede l'avversario (in generale e nel ruolo specifico)
        const formConcShotsH = weightedStats(formH.concededShots); // quanto concede H (serve per cA)
        const formConcShotsA = weightedStats(formA.concededShots); // quanto concede A (serve per cH)
        const venueConcShotsH = weightedStats(venueH.concededShots); // quanto concede H in casa (serve per cA)
        const venueConcShotsA = weightedStats(venueA.concededShots); // quanto concede A in trasferta (serve per cH)
        // Stagione precedente (solo se la corrente ha ancora poche partite)
        const prevShotsH = weightedStats(prevSeasonH.shots);
        const prevShotsA = weightedStats(prevSeasonA.shots);
        const prevConcShotsH = weightedStats(prevSeasonH.concededShots);
        const prevConcShotsA = weightedStats(prevSeasonA.concededShots);

        let cH = combineEstimates([
            { mean: formShotsH.mean, n: formShotsH.n, priorWeight: 0.9 },
            { mean: venueShotsH.mean, n: venueShotsH.n, priorWeight: 1.1 },
            { mean: formConcShotsA.mean, n: formConcShotsA.n, priorWeight: 0.7 },
            { mean: venueConcShotsA.mean, n: venueConcShotsA.n, priorWeight: 1.0 },
            { mean: prevShotsH.mean, n: prevShotsH.n, priorWeight: PREV_WEIGHT_H },
            { mean: prevConcShotsA.mean, n: prevConcShotsA.n, priorWeight: PREV_WEIGHT_A * 0.7 }
        ]);
        // Nessun dato reale trovato (tipico di una neopromossa priva di storico in
        // questa lega/stagione): prima si prova il valore manuale dal CSV
        // (colonna "TiriManual", curato a mano), poi solo come ultima spiaggia
        // la media generica di lega.
        if (cH == null) {
            const manualH = getManualValue(idH, 'TiriManual');
            cH = manualH != null ? manualH : priors.shots * leagueInfo.homeAdv;
        }

        let cA = combineEstimates([
            { mean: formShotsA.mean, n: formShotsA.n, priorWeight: 0.9 },
            { mean: venueShotsA.mean, n: venueShotsA.n, priorWeight: 1.1 },
            { mean: formConcShotsH.mean, n: formConcShotsH.n, priorWeight: 0.7 },
            { mean: venueConcShotsH.mean, n: venueConcShotsH.n, priorWeight: 1.0 },
            { mean: prevShotsA.mean, n: prevShotsA.n, priorWeight: PREV_WEIGHT_A },
            { mean: prevConcShotsH.mean, n: prevConcShotsH.n, priorWeight: PREV_WEIGHT_H * 0.7 }
        ]);
        if (cA == null) {
            const manualA = getManualValue(idA, 'TiriManual');
            cA = manualA != null ? manualA : priors.shots;
        }

        const xgFactorH = 0.75 + (xGH / bench) * 0.25;
        const xgFactorA = 0.75 + (xGA / bench) * 0.25;
        cH = cH * xgFactorH * formH.formFactor * momentumH;
        cA = cA * xgFactorA * formA.formFactor * momentumA;

        if (h2hData) {
            cH = cH * (1 - h2hData.weight) + h2hData.avgShotsH * h2hData.weight;
            cA = cA * (1 - h2hData.weight) + h2hData.avgShotsA * h2hData.weight;
        }
        cH = clip(cH, 3, 22);
        cA = clip(cA, 3, 22);

        const varShotsH = blendVariance(formShotsH.variance, formShotsH.n, cH, 'shots', 4);
        const varShotsA = blendVariance(formShotsA.variance, formShotsA.n, cA, 'shots', 4);
        const totalShots = cH + cA;
        const varTotalShots = combinedVariance(varShotsH, varShotsA);

        // ---------------- TIRI IN PORTA ----------------
        // Stesso modello attacco/difesa dei tiri totali (il vecchio foglio manuale
        // tracciava "Tiri in porta Fatti" E "Tiri in porta Subiti" separatamente).
        const formSotH = weightedStats(formH.sot);
        const formSotA = weightedStats(formA.sot);
        const venueSotH = weightedStats(venueH.sot);
        const venueSotA = weightedStats(venueA.sot);
        const formConcSotH = weightedStats(formH.concededSot);
        const formConcSotA = weightedStats(formA.concededSot);
        const venueConcSotH = weightedStats(venueH.concededSot);
        const venueConcSotA = weightedStats(venueA.concededSot);
        const prevSotH = weightedStats(prevSeasonH.sot);
        const prevSotA = weightedStats(prevSeasonA.sot);
        const prevConcSotH = weightedStats(prevSeasonH.concededSot);
        const prevConcSotA = weightedStats(prevSeasonA.concededSot);

        let s_cH = combineEstimates([
            { mean: formSotH.mean, n: formSotH.n, priorWeight: 0.9 },
            { mean: venueSotH.mean, n: venueSotH.n, priorWeight: 1.1 },
            { mean: formConcSotA.mean, n: formConcSotA.n, priorWeight: 0.7 },
            { mean: venueConcSotA.mean, n: venueConcSotA.n, priorWeight: 1.0 },
            { mean: prevSotH.mean, n: prevSotH.n, priorWeight: PREV_WEIGHT_H },
            { mean: prevConcSotA.mean, n: prevConcSotA.n, priorWeight: PREV_WEIGHT_A * 0.7 }
        ]);
        if (s_cH == null) {
            const manualSotH = getManualValue(idH, 'TiriPortaManual');
            s_cH = manualSotH != null ? manualSotH : cH * 0.34;
        }

        let s_cA = combineEstimates([
            { mean: formSotA.mean, n: formSotA.n, priorWeight: 0.9 },
            { mean: venueSotA.mean, n: venueSotA.n, priorWeight: 1.1 },
            { mean: formConcSotH.mean, n: formConcSotH.n, priorWeight: 0.7 },
            { mean: venueConcSotH.mean, n: venueConcSotH.n, priorWeight: 1.0 },
            { mean: prevSotA.mean, n: prevSotA.n, priorWeight: PREV_WEIGHT_A },
            { mean: prevConcSotH.mean, n: prevConcSotH.n, priorWeight: PREV_WEIGHT_H * 0.7 }
        ]);
        if (s_cA == null) {
            const manualSotA = getManualValue(idA, 'TiriPortaManual');
            s_cA = manualSotA != null ? manualSotA : cA * 0.34;
        }

        s_cH = s_cH * formH.formFactor * momentumH;
        s_cA = s_cA * formA.formFactor * momentumA;

        if (h2hData) {
            s_cH = s_cH * (1 - h2hData.weight) + h2hData.avgSotH * h2hData.weight;
            s_cA = s_cA * (1 - h2hData.weight) + h2hData.avgSotA * h2hData.weight;
        }
        s_cH = clip(s_cH, 1, 10);
        s_cA = clip(s_cA, 1, 10);
        // Vincolo logico: i tiri in porta non possono superare i tiri totali della stessa squadra
        s_cH = Math.min(s_cH, cH);
        s_cA = Math.min(s_cA, cA);

        const varSotH = blendVariance(formSotH.variance, formSotH.n, s_cH, 'sot', 4);
        const varSotA = blendVariance(formSotA.variance, formSotA.n, s_cA, 'sot', 4);
        const totalSOT = s_cH + s_cA;
        const varTotalSOT = combinedVariance(varSotH, varSotA);

        // ---------------- CORNER ----------------
        // Stesso modello attacco/difesa: quanti corner conquista H dipende anche da
        // quanti ne concede A (squadre che schiacciano/si difendono basso ne concedono di piu').
        const formCornH = weightedStats(formH.corners);
        const formCornA = weightedStats(formA.corners);
        const venueCornH = weightedStats(venueH.corners);
        const venueCornA = weightedStats(venueA.corners);
        const formConcCornH = weightedStats(formH.concededCorners);
        const formConcCornA = weightedStats(formA.concededCorners);
        const venueConcCornH = weightedStats(venueH.concededCorners);
        const venueConcCornA = weightedStats(venueA.concededCorners);
        const prevCornH = weightedStats(prevSeasonH.corners);
        const prevCornA = weightedStats(prevSeasonA.corners);

        let pCornH = combineEstimates([
            { mean: formCornH.mean, n: formCornH.n, priorWeight: 0.9 },
            { mean: venueCornH.mean, n: venueCornH.n, priorWeight: 1.1 },
            { mean: formConcCornA.mean, n: formConcCornA.n, priorWeight: 0.7 },
            { mean: venueConcCornA.mean, n: venueConcCornA.n, priorWeight: 1.0 },
            { mean: prevCornH.mean, n: prevCornH.n, priorWeight: PREV_WEIGHT_H }
        ]);
        if (pCornH == null) pCornH = priors.corners * leagueInfo.homeAdv;

        let pCornA = combineEstimates([
            { mean: formCornA.mean, n: formCornA.n, priorWeight: 0.9 },
            { mean: venueCornA.mean, n: venueCornA.n, priorWeight: 1.1 },
            { mean: formConcCornH.mean, n: formConcCornH.n, priorWeight: 0.7 },
            { mean: venueConcCornH.mean, n: venueConcCornH.n, priorWeight: 1.0 },
            { mean: prevCornA.mean, n: prevCornA.n, priorWeight: PREV_WEIGHT_A }
        ]);
        if (pCornA == null) pCornA = priors.corners;

        pCornH = pCornH * formH.formFactor * momentumH;
        pCornA = pCornA * formA.formFactor * momentumA;

        if (h2hData) {
            pCornH = pCornH * (1 - h2hData.weight * 0.8) + (h2hData.avgCorners / 2) * (h2hData.weight * 0.8);
            pCornA = pCornA * (1 - h2hData.weight * 0.8) + (h2hData.avgCorners / 2) * (h2hData.weight * 0.8);
        }
        pCornH = clip(pCornH, 1, 9);
        pCornA = clip(pCornA, 1, 9);

        const varCornH = blendVariance(formCornH.variance, formCornH.n, pCornH, 'corners', 4);
        const varCornA = blendVariance(formCornA.variance, formCornA.n, pCornA, 'corners', 4);
        const totalCorners = pCornH + pCornA;
        const varTotalCorners = combinedVariance(varCornH, varCornA);

        // ---------------- CARTELLINI ----------------
        const seasonCardsH = sumSeasonCardBuckets(sH?.cards?.yellow, nSeasonH); // dato REALE, ricostruito dalle fasce orarie
        const seasonCardsA = sumSeasonCardBuckets(sA?.cards?.yellow, nSeasonA);
        const formCardsH = weightedStats(formH.cards);
        const formCardsA = weightedStats(formA.cards);
        // Fonte casa/trasferta: gia' scaricata da getVenueAverages ma prima non veniva
        // usata qui, lasciando i cartellini senza rete di sicurezza quando stagione e
        // forma generale risultano entrambe vuote (a differenza di tiri/corner, che
        // hanno sempre questa terza fonte).
        const venueCardsH = weightedStats(venueH.cards);
        const venueCardsA = weightedStats(venueA.cards);
        const prevCardsH = weightedStats(prevSeasonH.cards);
        const prevCardsA = weightedStats(prevSeasonA.cards);

        let baseCardsH = combineEstimates([
            { mean: seasonCardsH, n: nSeasonH, priorWeight: 0.8 },
            { mean: formCardsH.mean, n: formCardsH.n, priorWeight: 1.0 },
            { mean: venueCardsH.mean, n: venueCardsH.n, priorWeight: 1.0 },
            { mean: prevCardsH.mean, n: prevCardsH.n, priorWeight: PREV_WEIGHT_H }
        ]);
        baseCardsH = shrinkEstimate(baseCardsH, (formCardsH.n || 0) + (venueCardsH.n || 0) + nSeasonH, priors.cards, 6);

        let baseCardsA = combineEstimates([
            { mean: seasonCardsA, n: nSeasonA, priorWeight: 0.8 },
            { mean: formCardsA.mean, n: formCardsA.n, priorWeight: 1.0 },
            { mean: venueCardsA.mean, n: venueCardsA.n, priorWeight: 1.0 },
            { mean: prevCardsA.mean, n: prevCardsA.n, priorWeight: PREV_WEIGHT_A }
        ]);
        baseCardsA = shrinkEstimate(baseCardsA, (formCardsA.n || 0) + (venueCardsA.n || 0) + nSeasonA, priors.cards, 6);

        let refFactor = 1.0;
        if (currentLeague === 7286) {
            const refSelectedVal = document.getElementById('arbitroSelect').value;
            const refParts = refSelectedVal.split(',');
            const refTotal = parseFloat(refParts[0]) || 24.5;
            refFactor = refTotal / 24.5;
        }

        let pCardsH = baseCardsH * refFactor * (2.05 - formH.formFactor);
        let pCardsA = baseCardsA * refFactor * (2.05 - formA.formFactor);

        if (h2hData) {
            pCardsH = pCardsH * (1 - h2hData.weight * 0.6) + (h2hData.avgCards / 2) * (h2hData.weight * 0.6);
            pCardsA = pCardsA * (1 - h2hData.weight * 0.6) + (h2hData.avgCards / 2) * (h2hData.weight * 0.6);
        }
        pCardsH = clip(pCardsH, 0.3, 5);
        pCardsA = clip(pCardsA, 0.3, 5);

        const varCardsH = blendVariance(formCardsH.variance, formCardsH.n, pCardsH, 'cards', 5);
        const varCardsA = blendVariance(formCardsA.variance, formCardsA.n, pCardsA, 'cards', 5);
        const totalCards = pCardsH + pCardsA;
        const varTotalCards = combinedVariance(varCardsH, varCardsA);

        // ---------------- FALLI (SOLO SERIE A) ----------------
        let totalFouls = 0, pFoulsH = 0, pFoulsA = 0, varTotalFouls = 1, varFoulsH = 1, varFoulsA = 1;
        let formFoulsH = { n: 0 }, formFoulsA = { n: 0 };
        if (currentLeague === 7286) {
            formFoulsH = weightedStats(formH.fouls);
            formFoulsA = weightedStats(formA.fouls);
            // Fonte casa/trasferta: stessa correzione gia' fatta per i cartellini,
            // che avevano lo stesso identico problema strutturale (nessuna rete di
            // sicurezza quando la sola "forma generale" risulta vuota).
            const venueFoulsH = weightedStats(venueH.fouls);
            const venueFoulsA = weightedStats(venueA.fouls);
            const prevFoulsH = weightedStats(prevSeasonH.fouls);
            const prevFoulsA = weightedStats(prevSeasonA.fouls);

            let baseFoulsH = combineEstimates([
                { mean: formFoulsH.mean, n: formFoulsH.n, priorWeight: 1.0 },
                { mean: venueFoulsH.mean, n: venueFoulsH.n, priorWeight: 1.0 },
                { mean: prevFoulsH.mean, n: prevFoulsH.n, priorWeight: PREV_WEIGHT_H }
            ]);
            baseFoulsH = shrinkEstimate(baseFoulsH, (formFoulsH.n || 0) + (venueFoulsH.n || 0), priors.fouls, 5);

            let baseFoulsA = combineEstimates([
                { mean: formFoulsA.mean, n: formFoulsA.n, priorWeight: 1.0 },
                { mean: venueFoulsA.mean, n: venueFoulsA.n, priorWeight: 1.0 },
                { mean: prevFoulsA.mean, n: prevFoulsA.n, priorWeight: PREV_WEIGHT_A }
            ]);
            baseFoulsA = shrinkEstimate(baseFoulsA, (formFoulsA.n || 0) + (venueFoulsA.n || 0), priors.fouls, 5);

            const refSelectedVal = document.getElementById('arbitroSelect').value;
            const refParts = refSelectedVal.split(',');
            const refHomeAverage = parseFloat(refParts[1]) || 11.0;
            const refAwayAverage = parseFloat(refParts[2]) || 13.5;
            const refHomeMultiplier = refHomeAverage / 11.5;
            const refAwayMultiplier = refAwayAverage / 12.5;

            pFoulsH = baseFoulsH * refHomeMultiplier * (2.05 - formH.formFactor);
            pFoulsA = baseFoulsA * refAwayMultiplier * (2.05 - formA.formFactor);

            if (h2hData) {
                pFoulsH = pFoulsH * (1 - h2hData.weight * 0.5) + (h2hData.avgFouls / 2) * (h2hData.weight * 0.5);
                pFoulsA = pFoulsA * (1 - h2hData.weight * 0.5) + (h2hData.avgFouls / 2) * (h2hData.weight * 0.5);
            }
            pFoulsH = clip(pFoulsH, 4, 19);
            pFoulsA = clip(pFoulsA, 4, 19);

            varFoulsH = blendVariance(formFoulsH.variance, formFoulsH.n, pFoulsH, 'fouls', 5);
            varFoulsA = blendVariance(formFoulsA.variance, formFoulsA.n, pFoulsA, 'fouls', 5);
            totalFouls = pFoulsH + pFoulsA;
            varTotalFouls = combinedVariance(varFoulsH, varFoulsA);
        }

        // LETTURA INPUT DEGLI SPREAD CORRENTI DELL'UTENTE
        const sprTotalMatch = parseFloat(document.getElementById('sprTotalMatch').value);
        const sprTotalH = parseFloat(document.getElementById('sprTotalH').value);
        const sprTotalA = parseFloat(document.getElementById('sprTotalA').value);

        const sprOTMatch = parseFloat(document.getElementById('sprOTMatch').value);
        const sprOTH = parseFloat(document.getElementById('sprOTH').value);
        const sprOTA = parseFloat(document.getElementById('sprOTA').value);

        const sprCornMatch = parseFloat(document.getElementById('sprCornMatch').value);
        const sprCornH = parseFloat(document.getElementById('sprCornH').value);
        const sprCornA = parseFloat(document.getElementById('sprCornA').value);

        const sprCardsMatch = parseFloat(document.getElementById('sprCardsMatch').value);
        const sprCardsH = parseFloat(document.getElementById('sprCardsH').value);
        const sprCardsA = parseFloat(document.getElementById('sprCardsA').value);

        // STRUTTURAZIONE PREVISIONI (probabilita' reale + indice di qualita' del dato)
        const advTotal = getAdviceAdvanced(totalShots, varTotalShots, Math.min(8, (formShotsH.n || 0) + (formShotsA.n || 0)), sprTotalMatch);
        const advTotalH = getAdviceAdvanced(cH, varShotsH, formShotsH.n, sprTotalH);
        const advTotalA = getAdviceAdvanced(cA, varShotsA, formShotsA.n, sprTotalA);

        const advOT = getAdviceAdvanced(totalSOT, varTotalSOT, Math.min(8, (formSotH.n || 0) + (formSotA.n || 0)), sprOTMatch);
        const advOTH = getAdviceAdvanced(s_cH, varSotH, formSotH.n, sprOTH);
        const advOTA = getAdviceAdvanced(s_cA, varSotA, formSotA.n, sprOTA);

        const advCorn = getAdviceAdvanced(totalCorners, varTotalCorners, Math.min(8, (formCornH.n || 0) + (formCornA.n || 0)), sprCornMatch);
        const advCornH = getAdviceAdvanced(pCornH, varCornH, formCornH.n, sprCornH);
        const advCornA = getAdviceAdvanced(pCornA, varCornA, formCornA.n, sprCornA);

        const advCards = getAdviceAdvanced(totalCards, varTotalCards, Math.min(8, (formCardsH.n || 0) + (formCardsA.n || 0)), sprCardsMatch);
        const advCardsH = getAdviceAdvanced(pCardsH, varCardsH, formCardsH.n, sprCardsH);
        const advCardsA = getAdviceAdvanced(pCardsA, varCardsA, formCardsA.n, sprCardsA);

        let finalHTML = `
            <div class="result-card border-green">
                <div class="res-header">
                    <span class="res-label" style="color:#10b981">Tiri Totali Match</span>
                    <span class="badge-pro">PRECISIONE ${advTotal.precision}</span>
                </div>
                <div class="res-value">${totalShots.toFixed(2)}</div>
                <div class="mb-2">${advTotal.html}</div>
                ${renderConfidenceBar(advTotal.confidence)}
                <div class="split-stats">
                    <div class="stat-col">
                        <h4>Home Prediction</h4>
                        <div class="val">${cH.toFixed(1)}</div>
                        <div class="mt-1">${advTotalH.html}</div>
                        ${renderFormBar(formH.results, false)}
                    </div>
                    <div class="stat-col right">
                        <h4>Away Prediction</h4>
                        <div class="val">${cA.toFixed(1)}</div>
                        <div class="mt-1">${advTotalA.html}</div>
                        ${renderFormBar(formA.results, true)}
                    </div>
                </div>
            </div>

            <div class="result-card border-purple">
                <div class="res-header">
                    <span class="res-label" style="color:#a78bfa">Tiri In Porta</span>
                    <span class="badge-pro">PRECISIONE ${advOT.precision}</span>
                </div>
                <div class="res-value">${totalSOT.toFixed(2)}</div>
                <div class="mb-2">${advOT.html}</div>
                ${renderConfidenceBar(advOT.confidence)}
                <div class="split-stats">
                    <div class="stat-col">
                        <h4>Home SOT</h4>
                        <div class="val">${s_cH.toFixed(1)}</div>
                        <div class="mt-1">${advOTH.html}</div>
                    </div>
                    <div class="stat-col right">
                        <h4>Away SOT</h4>
                        <div class="val">${s_cA.toFixed(1)}</div>
                        <div class="mt-1">${advOTA.html}</div>
                    </div>
                </div>
            </div>
        `;

        // INNESTO CARD FALLI SOLO SE SERIE A ATTIVA
        if (currentLeague === 7286) {
            const sprFoulsMatch = parseFloat(document.getElementById('sprFoulsMatch').value);
            const sprFoulsH = parseFloat(document.getElementById('sprFoulsH').value);
            const sprFoulsA = parseFloat(document.getElementById('sprFoulsA').value);

            const advFouls = getAdviceAdvanced(totalFouls, varTotalFouls, Math.min(8, (formFoulsH.n || 0) + (formFoulsA.n || 0)), sprFoulsMatch);
            const advFoulsH = getAdviceAdvanced(pFoulsH, varFoulsH, formFoulsH.n, sprFoulsH);
            const advFoulsA = getAdviceAdvanced(pFoulsA, varFoulsA, formFoulsA.n, sprFoulsA);

            finalHTML += `
                <div class="result-card border-red">
                    <div class="res-header">
                        <span class="res-label" style="color:#f87171">Falli Commessi</span>
                        <span class="badge-pro">PRECISIONE ${advFouls.precision}</span>
                    </div>
                    <div class="res-value">${totalFouls.toFixed(2)}</div>
                    <div class="mb-2">${advFouls.html}</div>
                    ${renderConfidenceBar(advFouls.confidence)}
                    <div class="split-stats">
                        <div class="stat-col">
                            <h4>Home Fouls</h4>
                            <div class="val">${pFoulsH.toFixed(1)}</div>
                            <div class="mt-1">${advFoulsH.html}</div>
                        </div>
                        <div class="stat-col right">
                            <h4>Away Fouls</h4>
                            <div class="val">${pFoulsA.toFixed(1)}</div>
                            <div class="mt-1">${advFoulsA.html}</div>
                        </div>
                    </div>
                </div>
            `;
        }

        // AGGIUNTA CARDS CORNER E CARTELLINI
        finalHTML += `
            <div class="result-card border-cyan">
                <div class="res-header">
                    <span class="res-label" style="color:#22d3ee">Corner Totali</span>
                    <span class="badge-pro">PRECISIONE ${advCorn.precision}</span>
                </div>
                <div class="res-value">${totalCorners.toFixed(2)}</div>
                <div class="mb-2">${advCorn.html}</div>
                ${renderConfidenceBar(advCorn.confidence)}
                <div class="split-stats">
                    <div class="stat-col">
                        <h4>Home Corners</h4>
                        <div class="val">${pCornH.toFixed(1)}</div>
                        <div class="mt-1">${advCornH.html}</div>
                    </div>
                    <div class="stat-col right">
                        <h4>Away Corners</h4>
                        <div class="val">${pCornA.toFixed(1)}</div>
                        <div class="mt-1">${advCornA.html}</div>
                    </div>
                </div>
            </div>

            <div class="result-card border-yellow">
                <div class="res-header">
                    <span class="res-label" style="color:#fbbf24">Cartellini Gialli</span>
                    <span class="badge-pro">PRECISIONE ${advCards.precision}</span>
                </div>
                <div class="res-value">${totalCards.toFixed(2)}</div>
                <div class="mb-2">${advCards.html}</div>
                ${renderConfidenceBar(advCards.confidence)}
                <div class="split-stats">
                    <div class="stat-col">
                        <h4>Home Cards</h4>
                        <div class="val">${pCardsH.toFixed(1)}</div>
                        <div class="mt-1">${advCardsH.html}</div>
                    </div>
                    <div class="stat-col right">
                        <h4>Away Cards</h4>
                        <div class="val">${pCardsA.toFixed(1)}</div>
                        <div class="mt-1">${advCardsA.html}</div>
                    </div>
                </div>
            </div>
        `;

        resDiv.innerHTML = finalHTML;
    } catch (e) {
        resDiv.innerHTML = `
            <div class="status-msg status-err" style="margin:20px 0">
                Errore Analisi: ${e.message}
            </div>
        `;
    }
}

// Avvio Iniziale automatico
loadData();
</script>

</body>
</html>
"""

components.html(html_code, height=1800, scrolling=True)
