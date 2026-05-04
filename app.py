import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="PROBET AI V4 PRO - TOTAL ANALYST", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600;700&family=Inter:wght@400;500;700;900&display=swap');

        * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

        html, body { 
            background: #020617; 
            color: white; 
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
        }

        .teko { font-family: 'Teko', sans-serif; }

        .container { 
            max-width: 900px; 
            margin: 0 auto; 
            padding: 16px; 
        }

        @media (min-width: 768px) {
            .container { padding: 32px; }
        }

        /* HEADER */
        .header { text-align: center; margin-bottom: 24px; }
        .header h1 { 
            font-size: clamp(2.5rem, 8vw, 4rem); 
            font-weight: 900; 
            letter-spacing: 0.15em; 
            text-transform: uppercase; 
            font-style: italic;
            line-height: 1;
        }
        .header p { 
            font-size: clamp(0.65rem, 2vw, 0.75rem); 
            color: #60a5fa; 
            font-weight: 700; 
            letter-spacing: 0.2em; 
            text-transform: uppercase; 
            font-style: italic;
            margin-top: 8px;
        }

        /* LEAGUE BUTTONS */
        .league-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8px;
            margin-bottom: 20px;
        }
        @media (min-width: 768px) {
            .league-grid { grid-template-columns: repeat(4, 1fr); gap: 12px; }
        }

        .league-btn { 
            cursor: pointer; 
            padding: 12px 8px; 
            border-radius: 10px; 
            font-weight: 900; 
            border: 1px solid #334155; 
            text-align: center; 
            font-size: 11px; 
            letter-spacing: 0.5px; 
            transition: all 0.3s; 
            background: #0f172a;
            color: #94a3b8;
            white-space: nowrap;
        }
        .league-active { 
            background: linear-gradient(135deg, #3b82f6, #2563eb); 
            border-color: #3b82f6; 
            color: white; 
            box-shadow: 0 0 20px rgba(59, 130, 246, 0.4); 
        }

        /* CARD PREMIUM */
        .card-premium { 
            background: #1e293b; 
            border-radius: 20px; 
            padding: 20px; 
            border: 1px solid #334155;
            margin-bottom: 20px;
        }
        @media (min-width: 768px) {
            .card-premium { padding: 30px; border-radius: 24px; }
        }

        /* FORM GRID */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 16px;
            margin-bottom: 20px;
        }
        @media (min-width: 768px) {
            .form-grid { grid-template-columns: repeat(3, 1fr); gap: 24px; }
        }

        /* INPUTS */
        select, input { 
            background: #0f172a; 
            border: 1px solid #475569; 
            color: white; 
            padding: 14px 12px; 
            width: 100%; 
            border-radius: 12px; 
            font-weight: 700; 
            font-size: 14px; 
            outline: none;
            appearance: none;
            -webkit-appearance: none;
        }
        select {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%2394a3b8' d='M6 8L1 3h10z'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 12px center;
            padding-right: 32px;
        }
        select:focus, input:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.2); }

        /* SPREAD GRID */
        .spread-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 12px;
            padding-top: 16px;
            border-top: 1px solid #334155;
            margin-bottom: 16px;
        }
        @media (min-width: 640px) {
            .spread-grid { grid-template-columns: repeat(3, 1fr); gap: 14px; }
        }

        /* LABELS */
        .label-spread { 
            font-size: 10px; 
            font-weight: 900; 
            color: #94a3b8; 
            text-transform: uppercase; 
            margin-bottom: 6px; 
            display: block; 
            letter-spacing: 1.2px; 
        }

        /* BUTTON */
        .btn-analizza { 
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%); 
            width: 100%; 
            padding: 18px; 
            border-radius: 14px; 
            font-weight: 900; 
            text-transform: uppercase; 
            cursor: pointer; 
            transition: all 0.3s; 
            margin-top: 16px; 
            border: none; 
            color: white; 
            letter-spacing: 2px;
            font-size: clamp(1.1rem, 4vw, 1.5rem);
            font-style: italic;
            font-family: 'Teko', sans-serif;
        }
        .btn-analizza:active { transform: scale(0.98); }
        @media (min-width: 768px) {
            .btn-analizza { padding: 22px; border-radius: 16px; }
        }

        /* RESULTS */
        .results-container { 
            display: none; 
            padding-bottom: 40px;
        }
        .results-container.visible { display: block; }

        .res-box { 
            background: #0f172a; 
            border-radius: 16px; 
            padding: 20px; 
            border-left: 4px solid; 
            margin-bottom: 16px; 
            position: relative;
        }
        @media (min-width: 768px) {
            .res-box { padding: 28px; border-radius: 20px; border-left-width: 5px; }
        }

        .res-box h2 { 
            font-size: clamp(2rem, 7vw, 3.5rem); 
            font-weight: 700;
            line-height: 1.1;
            word-break: break-word;
        }

        .advice-tag { 
            display: inline-block; 
            padding: 4px 12px; 
            border-radius: 8px; 
            font-size: 12px; 
            font-weight: 900; 
            margin-left: 8px; 
            text-transform: uppercase;
            white-space: nowrap;
        }
        @media (min-width: 768px) {
            .advice-tag { padding: 5px 16px; font-size: 14px; margin-left: 14px; }
        }
        .over-tag { background: linear-gradient(135deg, #10b981, #059669); color: white; }
        .under-tag { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; }

        .confidence-bar { 
            height: 6px; 
            border-radius: 3px; 
            background: #1e293b; 
            margin-top: 12px; 
            overflow: hidden; 
        }
        .confidence-fill { 
            height: 100%; 
            border-radius: 3px; 
            transition: width 1s ease; 
        }

        .precision-badge { 
            position: absolute; 
            top: 16px; 
            right: 16px; 
            font-size: 10px; 
            font-weight: 900; 
            padding: 4px 10px; 
            border-radius: 6px; 
            background: rgba(59,130,246,0.15); 
            color: #60a5fa; 
            border: 1px solid rgba(59,130,246,0.3); 
        }

        .split-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 16px;
            padding-top: 12px;
            border-top: 1px solid #1e293b;
        }

        .standings-info { 
            font-size: 11px; 
            color: #64748b; 
            margin-top: 6px; 
            font-weight: 500; 
        }

        .momentum-bar { 
            display: flex; 
            gap: 3px; 
            margin-top: 6px; 
            justify-content: flex-start;
        }
        .momentum-bar.right { justify-content: flex-end; }
        .momentum-dot { 
            width: 20px; 
            height: 20px; 
            border-radius: 4px; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 9px; 
            font-weight: 900; 
            color: white;
        }

        .status-msg { 
            font-size: 12px; 
            font-weight: 700; 
            padding: 10px 14px; 
            border-radius: 10px; 
            margin-bottom: 16px; 
            display: none; 
        }
        .status-err { background: rgba(239, 68, 68, 0.15); color: #ef4444; border: 1px solid #ef4444; }

        /* LOADING */
        .loading-box {
            text-align: center;
            padding: 60px 20px;
        }
        .loading-box h3 {
            font-size: clamp(1.5rem, 5vw, 2.5rem);
            color: #3b82f6;
            font-weight: 900;
            font-style: italic;
            letter-spacing: 0.1em;
            animation: pulse 2s infinite;
        }
        .loading-box p {
            font-size: 13px;
            color: #64748b;
            margin-top: 12px;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* PRO BADGE */
        .pro-badge { 
            background: linear-gradient(135deg, #f59e0b, #d97706); 
            color: #020617; 
            font-size: 10px; 
            font-weight: 900; 
            padding: 3px 10px; 
            border-radius: 6px; 
            text-transform: uppercase; 
            letter-spacing: 1px; 
            vertical-align: middle;
            margin-left: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="teko">PROBET <span style="color:#3b82f6">AI V4</span><span class="pro-badge">PRO</span></h1>
            <p>Elite Multi-League Analysis System - Stagione 2025/2026</p>
        </div>

        <div class="league-grid">
            <div id="btn-7286" class="league-btn league-active" onclick="switchLeague(7286)">SERIE A</div>
            <div id="btn-7293" class="league-btn" onclick="switchLeague(7293)">PREMIER LEAGUE</div>
            <div id="btn-7338" class="league-btn" onclick="switchLeague(7338)">BUNDESLIGA</div>
            <div id="btn-7351" class="league-btn" onclick="switchLeague(7351)">LA LIGA</div>
        </div>

        <div class="card-premium">
            <div id="statusMessage" class="status-msg"></div>

            <div class="form-grid">
                <div><label class="label-spread" style="color:#60a5fa">Home Team</label><select id="homeTeam"></select></div>
                <div><label class="label-spread" style="color:#60a5fa">Away Team</label><select id="awayTeam"></select></div>
                <div id="arbitroContainer"><label class="label-spread" style="color:#fbbf24">Arbitro (Serie A)</label><select id="arbitroSelect"><option value="24.5">Scegli...</option></select></div>
            </div>

            <div class="spread-grid">
                <div><label class="label-spread" style="color:#34d399">Spread Tiri Tot</label><input type="number" id="sprTotalMatch" step="0.5" value="23.5"></div>
                <div><label class="label-spread" style="color:#34d399">Spread Tiri Casa</label><input type="number" id="sprTotalH" step="0.5" value="12.5"></div>
                <div><label class="label-spread" style="color:#34d399">Spread Tiri Osp</label><input type="number" id="sprTotalA" step="0.5" value="10.5"></div>
            </div>

            <div class="spread-grid">
                <div><label class="label-spread" style="color:#a78bfa">Spread Porta Tot</label><input type="number" id="sprOTMatch" step="0.5" value="8.5"></div>
                <div><label class="label-spread" style="color:#a78bfa">Spread Porta Casa</label><input type="number" id="sprOTH" step="0.5" value="4.5"></div>
                <div><label class="label-spread" style="color:#a78bfa">Spread Porta Osp</label><input type="number" id="sprOTA" step="0.5" value="3.5"></div>
            </div>

            <div id="foulsInputs" class="spread-grid">
                <div><label class="label-spread" style="color:#f87171">Spread Falli Tot</label><input type="number" id="sprFoulsMatch" step="0.5" value="24.5"></div>
                <div><label class="label-spread" style="color:#f87171">Spread Falli Casa</label><input type="number" id="sprFoulsH" step="0.5" value="12.5"></div>
                <div><label class="label-spread" style="color:#f87171">Spread Falli Osp</label><input type="number" id="sprFoulsA" step="0.5" value="11.5"></div>
            </div>

            <div class="spread-grid">
                <div><label class="label-spread" style="color:#22d3ee">Spread Corner Tot</label><input type="number" id="sprCornMatch" step="0.5" value="9.5"></div>
                <div><label class="label-spread" style="color:#22d3ee">Spread Corner Casa</label><input type="number" id="sprCornH" step="0.5" value="5.5"></div>
                <div><label class="label-spread" style="color:#22d3ee">Spread Corner Osp</label><input type="number" id="sprCornA" step="0.5" value="4.5"></div>
            </div>

            <div class="spread-grid">
                <div><label class="label-spread" style="color:#fbbf24">Spread Gialli Tot</label><input type="number" id="sprCardsMatch" step="0.5" value="4.5"></div>
                <div><label class="label-spread" style="color:#fbbf24">Spread Gialli Casa</label><input type="number" id="sprCardsH" step="0.5" value="2.5"></div>
                <div><label class="label-spread" style="color:#fbbf24">Spread Gialli Osp</label><input type="number" id="sprCardsA" step="0.5" value="2.5"></div>
            </div>

            <form id="adForm" action="https://probetai.com/mostra_pubblicita" method="GET" target="_blank" style="display:none;">
                <input type="hidden" name="trigger" value="ad">
            </form>

            <button onclick="triggerAdAndCalculate()" class="btn-analizza">GENERA ANALISI ELITE PRO</button>
        </div>

        <div id="results" class="results-container"></div>
    </div>

<script>
const API_KEY = "8546a3b44515070cb8e4b6a8f620ab5b";
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
const REFS_FILE = "ARBITRI_SERIE_A%20-%20Foglio1.csv";
let currentLeague = 7286, dbXG = [];

const LEAGUE_DATA = {
    7286: { name: "SERIE A", file: "DATABASE_AVANZATO_SERIEA_2025.csv", oldId: 135, apiId: 7286, homeAdv: 1.08 },
    7293: { name: "PREMIER LEAGUE", file: "DATABASE_AVANZATO_PREMIER_2025.csv", oldId: 39, apiId: 7293, homeAdv: 1.05 },
    7338: { name: "BUNDESLIGA", file: "DATABASE_AVANZATO_BUNDES_2025.csv", oldId: 78, apiId: 7338, homeAdv: 1.12 },
    7351: { name: "LA LIGA", file: "DATABASE_AVANZATO_LALIGA_2025.csv", oldId: 140, apiId: 7351, homeAdv: 1.06 }
};

function setStatus(msg, type) {
    const el = document.getElementById('statusMessage');
    if (!msg) { el.style.display = 'none'; return; }
    el.textContent = msg;
    el.className = 'status-msg status-' + type;
    el.style.display = 'block';
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
    document.getElementById('arbitroContainer').style.display = isSerieA ? "block" : "none";
    document.getElementById('foulsInputs').style.display = isSerieA ? "grid" : "none";
    loadData();
}

function loadData() {
    const leagueInfo = LEAGUE_DATA[currentLeague];
    Papa.parse(BASE_CSV_URL + leagueInfo.file, { 
        download: true, 
        header: true, 
        skipEmptyLines: true, 
        complete: (r) => { 
            dbXG = r.data; 
            loadTeams(); 
        },
        error: (err) => {
            console.error("Errore CSV:", err);
            setStatus("Errore caricamento database CSV", 'err');
        }
    });

    if(currentLeague === 7286) {
        Papa.parse(BASE_CSV_URL + REFS_FILE, { 
            download: true, 
            header: true, 
            skipEmptyLines: true, 
            delimiter: ";", 
            complete: (r) => {
                const sel = document.getElementById('arbitroSelect'); 
                sel.innerHTML = '<option value="24.5">Scegli Arbitro...</option>';
                r.data.forEach(row => {
                    let name = row.Arbitro || Object.values(row)[0];
                    let val = row["Media Totale"] || Object.values(row)[2];
                    if(name && val) sel.add(new Option(name, val.toString().replace(',', '.')));
                });
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

        let res = await fetch(`https://v3.football.api-sports.io/teams?league=${apiId}&season=2025`, { 
            headers: { "x-apisports-key": API_KEY } 
        });

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        let data = await res.json();

        if (!data.response || data.response.length === 0) {
            apiId = leagueInfo.oldId;
            res = await fetch(`https://v3.football.api-sports.io/teams?league=${apiId}&season=2025`, { 
                headers: { "x-apisports-key": API_KEY } 
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            data = await res.json();
        }

        if (!data.response || data.response.length === 0) {
            throw new Error("Nessuna squadra trovata");
        }

        h.innerHTML = ""; a.innerHTML = "";
        h.add(new Option("-- Seleziona Casa --", ""));
        a.add(new Option("-- Seleziona Ospite --", ""));

        data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
            h.add(new Option(t.team.name, t.team.id)); 
            a.add(new Option(t.team.name, t.team.id));
        });

        setStatus("", "");

    } catch (e) {
        h.innerHTML = '<option>Errore caricamento</option>';
        a.innerHTML = '<option>Errore caricamento</option>';
        setStatus(`Errore: ${e.message}`, 'err');
    }
}

function calcConfidence(pred, spread) {
    const diff = pred - spread;
    const rawProb = 1 / (1 + Math.exp(-diff * 0.85));
    return Math.min(Math.max(rawProb * 100, 8), 96);
}

function getAdviceAdvanced(pred, spread) {
    const conf = calcConfidence(pred, spread);
    const isOver = conf >= 50;
    const displayConf = isOver ? conf : 100 - conf;
    const direction = isOver ? 'OVER' : 'UNDER';
    let precisionLabel = displayConf >= 75 ? 'ALTA' : displayConf >= 60 ? 'MEDIA' : 'BASE';

    return {
        html: `<span class="advice-tag ${isOver ? 'over-tag' : 'under-tag'}">${direction} ${spread} (${displayConf.toFixed(1)}%)</span>`,
        confidence: displayConf,
        isOver: isOver,
        precision: precisionLabel
    };
}

function renderConfidenceBar(confidence) {
    let color = confidence >= 75 ? '#10b981' : confidence >= 60 ? '#f59e0b' : '#ef4444';
    return `<div class="confidence-bar"><div class="confidence-fill" style="width:${confidence}%;background:${color}"></div></div>`;
}

function renderFormBar(results, alignRight) {
    if (!results || results.length === 0) return '';
    let html = `<div class="momentum-bar ${alignRight ? 'right' : ''}">`;
    results.slice(0, 5).reverse().forEach(r => {
        const outcome = r === 'W' ? 'V' : r === 'D' ? 'N' : 'S';
        const color = r === 'W' ? '#10b981' : r === 'D' ? '#f59e0b' : '#ef4444';
        html += `<div class="momentum-dot" style="background:${color}">${outcome}</div>`;
    });
    html += '</div>';
    return html;
}

async function getTeamForm(teamId, apiId) {
    try {
        const res = await fetch(`https://v3.football.api-sports.io/fixtures?team=${teamId}&season=2025&league=${apiId}&last=5`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        if (!data.response || data.response.length === 0) return { results: [], formFactor: 1.0, avgShots: 0, avgCorners: 0, avgCards: 0 };

        let results = [];
        let totalShots = 0, totalCorners = 0, totalCards = 0;
        let count = 0;

        data.response.forEach(fixture => {
            const isHome = fixture.teams.home.id == teamId;
            const teamSide = isHome ? fixture.teams.home : fixture.teams.away;

            if (teamSide.winner === true) results.push('W');
            else if (teamSide.winner === false) results.push('L');
            else results.push('D');

            if (fixture.statistics && fixture.statistics.length > 0) {
                const teamStats = isHome ? fixture.statistics[0] : fixture.statistics[1];
                if (teamStats && teamStats.statistics) {
                    const stats = teamStats.statistics;
                    const shots = stats.find(s => s.type === 'Shots on Goal');
                    const corners = stats.find(s => s.type === 'Corner Kicks');
                    const cards = stats.find(s => s.type === 'Yellow Cards');
                    if (shots) totalShots += parseInt(shots.value) || 0;
                    if (corners) totalCorners += parseInt(corners.value) || 0;
                    if (cards) totalCards += parseInt(cards.value) || 0;
                    count++;
                }
            }
        });

        let formFactor = 1.0;
        results.forEach((r, i) => {
            const weight = (i + 1) / 5;
            if (r === 'W') formFactor += 0.016 * weight;
            else if (r === 'L') formFactor -= 0.016 * weight;
        });

        return {
            results: results,
            formFactor: Math.max(0.92, Math.min(1.08, formFactor)),
            avgShots: count > 0 ? totalShots / count : 0,
            avgCorners: count > 0 ? totalCorners / count : 0,
            avgCards: count > 0 ? totalCards / count : 0
        };
    } catch (e) {
        return { results: [], formFactor: 1.0, avgShots: 0, avgCorners: 0, avgCards: 0 };
    }
}

async function getStandingsMomentum(teamId, apiId) {
    try {
        const res = await fetch(`https://v3.football.api-sports.io/standings?season=2025&league=${apiId}&team=${teamId}`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        if (!data.response || data.response.length === 0) return { position: 10, totalTeams: 20, momentum: 1.0 };

        const standing = data.response[0].league.standings[0][0];
        const position = standing.rank;
        const totalTeams = data.response[0].league.standings[0].length;

        let momentum = 1.0;
        if (position <= 3) momentum = 1.05;
        else if (position <= 6) momentum = 1.03;
        else if (position >= totalTeams - 3) momentum = 1.04;
        else if (position >= totalTeams - 8 && position <= totalTeams - 4) momentum = 0.98;

        return { position, totalTeams, momentum };
    } catch (e) {
        return { position: 10, totalTeams: 20, momentum: 1.0 };
    }
}

async function getFixturesH2H(teamIdH, teamIdA, apiId) {
    try {
        const res = await fetch(`https://v3.football.api-sports.io/fixtures/headtohead?h2h=${teamIdH}-${teamIdA}&last=3`, {
            headers: { "x-apisports-key": API_KEY }
        });
        const data = await res.json();
        if (!data.response || data.response.length === 0) return null;

        let h2hShotsH = 0, h2hShotsA = 0, h2hCorners = 0;
        let count = 0;

        data.response.forEach(fixture => {
            if (fixture.statistics && fixture.statistics.length > 0) {
                const homeStats = fixture.statistics[0];
                const awayStats = fixture.statistics[1];
                if (homeStats && homeStats.statistics) {
                    const stats = homeStats.statistics;
                    const shots = stats.find(s => s.type === 'Shots on Goal');
                    const corners = stats.find(s => s.type === 'Corner Kicks');
                    if (shots) h2hShotsH += parseInt(shots.value) || 0;
                    if (corners) h2hCorners += parseInt(corners.value) || 0;
                }
                if (awayStats && awayStats.statistics) {
                    const stats = awayStats.statistics;
                    const shots = stats.find(s => s.type === 'Shots on Goal');
                    if (shots) h2hShotsA += parseInt(shots.value) || 0;
                }
                count++;
            }
        });

        if (count === 0) return null;
        return {
            avgShotsH: h2hShotsH / count,
            avgShotsA: h2hShotsA / count,
            avgCorners: h2hCorners / count,
            weight: Math.min(count * 0.15, 0.3)
        };
    } catch (e) {
        return null;
    }
}

async function runDeepAnalysis() {
    const resDiv = document.getElementById('results');
    resDiv.classList.add('visible');
    resDiv.innerHTML = `
        <div class="loading-box">
            <h3 class="teko">ANALISI ELITE PRO IN CORSO</h3>
            <p>Recupero forma, classifica e statistiche avanzate...</p>
        </div>
    `;
    resDiv.scrollIntoView({behavior:'smooth', block:'start'});

    try {
        const idH = document.getElementById('homeTeam').value;
        const idA = document.getElementById('awayTeam').value;

        if (!idH || !idA) throw new Error("Seleziona entrambe le squadre");
        if (idH === idA) throw new Error("Le squadre devono essere diverse");

        const leagueInfo = LEAGUE_DATA[currentLeague];
        let apiId = leagueInfo.apiId;

        let statsH, statsA, formH, formA, standH, standA, h2hData;

        try {
            const statsRes = await Promise.all([
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
            ]);
            statsH = statsRes[0]; statsA = statsRes[1];
            if (!statsH.response || !statsA.response) throw new Error("empty");
        } catch (e) {
            apiId = leagueInfo.oldId;
            const statsRes = await Promise.all([
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
                fetch(`https://v3.football.api-sports.io/teams/statistics?league=${apiId}&season=2025&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
            ]);
            statsH = statsRes[0]; statsA = statsRes[1];
        }

        [formH, formA, standH, standA, h2hData] = await Promise.all([
            getTeamForm(idH, apiId),
            getTeamForm(idA, apiId),
            getStandingsMomentum(idH, apiId),
            getStandingsMomentum(idA, apiId),
            getFixturesH2H(idH, idA, apiId)
        ]);

        const sH = statsH.response; 
        const sA = statsA.response;
        const homeAdv = leagueInfo.homeAdv;

        const xGH_raw = dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || "0.11";
        const xGA_raw = dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || "0.11";
        const xGH = parseFloat(xGH_raw.toString().replace(',', '.'));
        const xGA = parseFloat(xGA_raw.toString().replace(',', '.'));
        const bench = (currentLeague === 7293 || currentLeague === 7338) ? 0.12 : 0.11;

        const formFactorH = formH.formFactor;
        const formFactorA = formA.formFactor;
        const momentumH = standH.momentum;
        const momentumA = standA.momentum;

        // TI TOTALI
        const shotsH_avg = sH.shots?.total?.average || 12.5;
        const shotsA_avg = sA.shots?.total?.average || 10.5;
        const xgFactorH = 0.7 + (xGH / bench) * 0.3;
        const xgFactorA = 0.7 + (xGA / bench) * 0.3;

        let cH = shotsH_avg * xgFactorH * homeAdv * formFactorH * momentumH * 0.95;
        let cA = shotsA_avg * xgFactorA * 1.0 * formFactorA * momentumA * 1.05;

        if (h2hData) {
            cH = cH * (1 - h2hData.weight) + h2hData.avgShotsH * h2hData.weight;
            cA = cA * (1 - h2hData.weight) + h2hData.avgShotsA * h2hData.weight;
        }

        if (formH.avgShots > 0 && Math.abs(formH.avgShots - shotsH_avg) / shotsH_avg > 0.2) {
            cH = cH * 0.7 + formH.avgShots * 0.3;
        }
        if (formA.avgShots > 0 && Math.abs(formA.avgShots - shotsA_avg) / shotsA_avg > 0.2) {
            cA = cA * 0.7 + formA.avgShots * 0.3;
        }

        const totalShots = cH + cA;

        // TI IN PORTA
        const onTargetH_avg = sH.shots?.on_goal?.average || 4.2;
        const onTargetA_avg = sA.shots?.on_goal?.average || 3.6;
        const convRateH = onTargetH_avg / shotsH_avg;
        const convRateA = onTargetA_avg / shotsA_avg;
        const precisionH = convRateH * (0.85 + xGH * 2.5);
        const precisionA = convRateA * (0.85 + xGA * 2.5);

        let oH = cH * precisionH * homeAdv * formFactorH;
        let oA = cA * precisionA * formFactorA;
        const totalOnTarget = oH + oA;

        // CORNER
        const cornersForH = sH.corners?.for?.average || 5.2;
        const cornersAgainstH = sH.corners?.against?.average || 4.1;
        const cornersForA = sA.corners?.for?.average || 4.8;
        const cornersAgainstA = sA.corners?.against?.average || 4.4;
        const pressureH = (cornersForH + cornersAgainstA) / 2;
        const pressureA = (cornersForA + cornersAgainstH) / 2;
        const possH = sH.possession?.average || 52;
        const possA = sA.possession?.average || 48;
        const possFactorH = 0.9 + (possH / 100) * 0.2;
        const possFactorA = 0.9 + (possA / 100) * 0.2;

        let pCH = pressureH * possFactorH * homeAdv * formFactorH * 0.92;
        let pCA = pressureA * possFactorA * formFactorA * 1.08;

        if (formH.avgCorners > 0 && Math.abs(formH.avgCorners - cornersForH) / cornersForH > 0.15) {
            pCH = pCH * 0.8 + formH.avgCorners * 0.2;
        }
        if (formA.avgCorners > 0 && Math.abs(formA.avgCorners - cornersForA) / cornersForA > 0.15) {
            pCA = pCA * 0.8 + formA.avgCorners * 0.2;
        }

        const totalCorners = pCH + pCA;

        // CARTELLINI
        const yellowH_avg = sH.cards?.yellow?.average || 2.1;
        const yellowA_avg = sA.cards?.yellow?.average || 2.3;
        const foulsH_avg = sH.fouls?.for?.average || 12.5;
        const foulsA_avg = sA.fouls?.for?.average || 13.0;
        const disciplineH = foulsH_avg / Math.max(yellowH_avg, 0.5);
        const disciplineA = foulsA_avg / Math.max(yellowA_avg, 0.5);
        const intensityFactor = 1.0 + ((foulsH_avg + foulsA_avg) - 24) / 100;

        let cardH = yellowH_avg * intensityFactor * homeAdv * formFactorH * 0.95;
        let cardA = yellowA_avg * intensityFactor * formFactorA * 1.05;

        if (formH.avgCards > 0) cardH = cardH * 0.85 + formH.avgCards * 0.15;
        if (formA.avgCards > 0) cardA = cardA * 0.85 + formA.avgCards * 0.15;

        const totalCards = cardH + cardA;

        // FALLI SERIE A
        let totalFouls = 0, fH = 0, fA = 0;
        if(currentLeague === 7286) {
            const refVal = parseFloat(document.getElementById('arbitroSelect').value) || 24.5;
            const foulsAgainstH = sH.fouls?.against?.average || 11.5;
            const foulsAgainstA = sA.fouls?.against?.average || 12.0;
            fH = ((foulsH_avg + foulsAgainstA) / 2) * 0.6 + (refVal / 2 * 0.4);
            fA = ((foulsA_avg + foulsAgainstH) / 2) * 0.6 + (refVal / 2 * 0.4);
            totalFouls = fH + fA;
        }

        // RENDERING
        let html = "";

        const formHtmlH = renderFormBar(formH.results, false);
        const formHtmlA = renderFormBar(formA.results, true);

        if(currentLeague === 7286) {
            const advFouls = getAdviceAdvanced(totalFouls, parseFloat(document.getElementById('sprFoulsMatch').value));
            const advFoulsH = getAdviceAdvanced(fH, parseFloat(document.getElementById('sprFoulsH').value));
            const advFoulsA = getAdviceAdvanced(fA, parseFloat(document.getElementById('sprFoulsA').value));
            html += `
            <div class="res-box" style="border-left-color:#ef4444">
                <div class="precision-badge">${advFouls.precision}</div>
                <p class="label-spread" style="color:#f87171">Falli Commessi (Serie A)</p>
                <h2 class="teko">${totalFouls.toFixed(2)} ${advFouls.html}</h2>
                ${renderConfidenceBar(advFouls.confidence)}
                <div class="split-grid">
                    <div><p class="label-spread">Casa</p><p class="teko" style="color:#f87171;font-size:1.25rem">${fH.toFixed(2)} ${advFoulsH.html}</p></div>
                    <div class="text-right"><p class="label-spread">Ospite</p><p class="teko" style="color:#f87171;font-size:1.25rem">${fA.toFixed(2)} ${advFoulsA.html}</p></div>
                </div>
            </div>`;
        }

        const advShots = getAdviceAdvanced(totalShots, parseFloat(document.getElementById('sprTotalMatch').value));
        const advShotsH = getAdviceAdvanced(cH, parseFloat(document.getElementById('sprTotalH').value));
        const advShotsA = getAdviceAdvanced(cA, parseFloat(document.getElementById('sprTotalA').value));
        html += `
        <div class="res-box" style="border-left-color:#10b981">
            <div class="precision-badge">${advShots.precision}</div>
            <p class="label-spread" style="color:#34d399">Tiri Totali Previsti</p>
            <h2 class="teko">${totalShots.toFixed(2)} ${advShots.html}</h2>
            ${renderConfidenceBar(advShots.confidence)}
            <div class="split-grid">
                <div>
                    <p class="label-spread">Casa</p>
                    <p class="teko" style="color:#34d399;font-size:1.25rem">${cH.toFixed(2)} ${advShotsH.html}</p>
                    ${formHtmlH}
                    <p class="standings-info">Pos. ${standH.position}° • Forma ${(formFactorH).toFixed(2)}x</p>
                </div>
                <div class="text-right">
                    <p class="label-spread">Ospite</p>
                    <p class="teko" style="color:#34d399;font-size:1.25rem">${cA.toFixed(2)} ${advShotsA.html}</p>
                    ${formHtmlA}
                    <p class="standings-info">Pos. ${standA.position}° • Forma ${(formFactorA).toFixed(2)}x</p>
                </div>
            </div>
        </div>`;

        const advOT = getAdviceAdvanced(totalOnTarget, parseFloat(document.getElementById('sprOTMatch').value));
        const advOTH = getAdviceAdvanced(oH, parseFloat(document.getElementById('sprOTH').value));
        const advOTA = getAdviceAdvanced(oA, parseFloat(document.getElementById('sprOTA').value));
        html += `
        <div class="res-box" style="border-left-color:#a78bfa">
            <div class="precision-badge">${advOT.precision}</div>
            <p class="label-spread" style="color:#a78bfa">Tiri In Porta Previsti</p>
            <h2 class="teko">${totalOnTarget.toFixed(2)} ${advOT.html}</h2>
            ${renderConfidenceBar(advOT.confidence)}
            <div class="split-grid">
                <div><p class="label-spread">Casa</p><p class="teko" style="color:#a78bfa;font-size:1.25rem">${oH.toFixed(2)} ${advOTH.html}</p></div>
                <div class="text-right"><p class="label-spread">Ospite</p><p class="teko" style="color:#a78bfa;font-size:1.25rem">${oA.toFixed(2)} ${advOTA.html}</p></div>
            </div>
        </div>`;

        const advCorn = getAdviceAdvanced(totalCorners, parseFloat(document.getElementById('sprCornMatch').value));
        const advCornH = getAdviceAdvanced(pCH, parseFloat(document.getElementById('sprCornH').value));
        const advCornA = getAdviceAdvanced(pCA, parseFloat(document.getElementById('sprCornA').value));
        html += `
        <div class="res-box" style="border-left-color:#22d3ee">
            <div class="precision-badge">${advCorn.precision}</div>
            <p class="label-spread" style="color:#22d3ee">Calci d'Angolo Previsti</p>
            <h2 class="teko">${totalCorners.toFixed(2)} ${advCorn.html}</h2>
            ${renderConfidenceBar(advCorn.confidence)}
            <div class="split-grid">
                <div><p class="label-spread">Casa</p><p class="teko" style="color:#22d3ee;font-size:1.25rem">${pCH.toFixed(2)} ${advCornH.html}</p></div>
                <div class="text-right"><p class="label-spread">Ospite</p><p class="teko" style="color:#22d3ee;font-size:1.25rem">${pCA.toFixed(2)} ${advCornA.html}</p></div>
            </div>
        </div>`;

        const advCards = getAdviceAdvanced(totalCards, parseFloat(document.getElementById('sprCardsMatch').value));
        const advCardsH = getAdviceAdvanced(cardH, parseFloat(document.getElementById('sprCardsH').value));
        const advCardsA = getAdviceAdvanced(cardA, parseFloat(document.getElementById('sprCardsA').value));
        html += `
        <div class="res-box" style="border-left-color:#fbbf24">
            <div class="precision-badge">${advCards.precision}</div>
            <p class="label-spread" style="color:#fbbf24">Gialli Previsti</p>
            <h2 class="teko">${totalCards.toFixed(2)} ${advCards.html}</h2>
            ${renderConfidenceBar(advCards.confidence)}
            <div class="split-grid">
                <div><p class="label-spread">Casa</p><p class="teko" style="color:#fbbf24;font-size:1.25rem">${cardH.toFixed(2)} ${advCardsH.html}</p></div>
                <div class="text-right"><p class="label-spread">Ospite</p><p class="teko" style="color:#fbbf24;font-size:1.25rem">${cardA.toFixed(2)} ${advCardsA.html}</p></div>
            </div>
        </div>`;

        resDiv.innerHTML = html;
        resDiv.scrollIntoView({behavior:'smooth', block:'start'});
    } catch(e) { 
        resDiv.innerHTML = `<div class="res-box" style="border-left-color:#ef4444"><p style="font-weight:900;color:#ef4444">ERRORE ANALISI</p><p style="color:white">${e.message}</p></div>`; 
    }
}

loadData();
</script>
</body>
</html>
"""
components.html(html_code, height=1200, scrolling=True)
