import streamlit as st
import streamlit.components.v1 as components

# Configurazione iniziale
st.set_page_config(page_title="PROBET AI V4", layout="wide", initial_sidebar_state="collapsed")

# --- CSS RADICALE PER ELIMINARE SPAZI E TAGLI ---
st.markdown("""
    <style>
        /* Nasconde l'header e il footer di Streamlit */
        [data-testid="stHeader"], footer {display: none !important;}
        
        /* Elimina i margini interni di Streamlit */
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }

        /* Rimuove lo spazio vuoto in alto che causa il taglio */
        section[data-testid="stSidebar"] + div, section.main > div:first-child {
            padding-top: 0 !important;
        }

        /* Forza l'iframe a ignorare i limiti di Streamlit */
        iframe {
            margin-top: -65px !important; /* Sposta tutto su per non tagliare il titolo */
            border: none !important;
        }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;900&display=swap');
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
        .teko { font-family: 'Teko', sans-serif; }
        .card-premium { background: #1e293b; border-radius: 20px; padding: 15px; border: 1px solid #334155; margin: 10px; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 10px; width: 100%; border-radius: 10px; font-weight: bold; font-size: 16px; outline: none; }
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 18px; border-radius: 15px; font-weight: 900; text-transform: uppercase; border: none; color: white; margin-top: 10px; cursor: pointer; }
        .res-box { background: #0f172a; border-radius: 15px; padding: 15px; border-left: 5px solid #3b82f6; margin: 10px; }
        .label-spread { font-size: 10px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px; display: block; }
        .league-btn { cursor: pointer; padding: 10px; border-radius: 8px; font-weight: 900; border: 1px solid #334155; text-align: center; font-size: 11px; }
        .league-active { background: #3b82f6; color: white; border-color: #3b82f6; }
        .grid-spreads { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; padding-top: 10px; border-top: 1px solid #334155; margin-bottom: 10px; }
        .advice-tag { display: inline-block; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: 900; margin-top: 5px; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
    </style>
</head>
<body>
    <div id="app-content">
        <div class="text-center pt-10 pb-4">
            <h1 class="text-6xl font-black teko tracking-widest text-white uppercase italic leading-none">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-blue-400 font-bold text-[10px] tracking-widest uppercase italic">Elite Multi-League Analysis System</p>
        </div>

        <div class="grid grid-cols-2 gap-2 px-3 mb-4">
            <div id="btn-135" class="league-btn league-active" onclick="switchLeague(135)">SERIE A</div>
            <div id="btn-39" class="league-btn" onclick="switchLeague(39)">PREMIER</div>
            <div id="btn-78" class="league-btn" onclick="switchLeague(78)">BUNDES</div>
            <div id="btn-140" class="league-btn" onclick="switchLeague(140)">LA LIGA</div>
        </div>

        <div class="card-premium">
            <div class="space-y-4 mb-4">
                <div><label class="label-spread text-blue-400">Home Team</label><select id="homeTeam"></select></div>
                <div><label class="label-spread text-blue-400">Away Team</label><select id="awayTeam"></select></div>
                <div id="arbitroContainer"><label class="label-spread text-yellow-500 italic">Arbitro (Serie A)</label><select id="arbitroSelect"></select></div>
            </div>

            <div class="grid-spreads">
                <div><label class="label-spread text-emerald-400">Tiri Tot</label><input type="number" id="sprTotalMatch" step="0.5" value="23.5"></div>
                <div><label class="label-spread text-emerald-400">Tiri H</label><input type="number" id="sprTotalH" step="0.5" value="12.5"></div>
                <div><label class="label-spread text-emerald-400">Tiri A</label><input type="number" id="sprTotalA" step="0.5" value="10.5"></div>
            </div>

            <div class="grid-spreads">
                <div><label class="label-spread text-purple-400">Porta Tot</label><input type="number" id="sprOTMatch" step="0.5" value="8.5"></div>
                <div><label class="label-spread text-purple-400">Porta H</label><input type="number" id="sprOTH" step="0.5" value="4.5"></div>
                <div><label class="label-spread text-purple-400">Porta A</label><input type="number" id="sprOTA" step="0.5" value="3.5"></div>
            </div>

            <div id="foulSection" class="grid-spreads">
                <div><label class="label-spread text-red-400">Falli Tot</label><input type="number" id="sprFoulsMatch" step="0.5" value="24.5"></div>
                <div><label class="label-spread text-red-400">Falli H</label><input type="number" id="sprFoulsH" step="0.5" value="12.5"></div>
                <div><label class="label-spread text-red-400">Falli A</label><input type="number" id="sprFoulsA" step="0.5" value="11.5"></div>
            </div>

            <div class="grid-spreads">
                <div><label class="label-spread text-cyan-400">Corner Tot</label><input type="number" id="sprCornMatch" step="0.5" value="9.5"></div>
                <div><label class="label-spread text-cyan-400">Corner H</label><input type="number" id="sprCornH" step="0.5" value="5.5"></div>
                <div><label class="label-spread text-cyan-400">Corner A</label><input type="number" id="sprCornA" step="0.5" value="4.5"></div>
            </div>

            <div class="grid-spreads">
                <div><label class="label-spread text-yellow-400">Gialli Tot</label><input type="number" id="sprCardsMatch" step="0.5" value="4.5"></div>
                <div><label class="label-spread text-yellow-400">Gialli H</label><input type="number" id="sprCardsH" step="0.5" value="2.5"></div>
                <div><label class="label-spread text-yellow-400">Gialli A</label><input type="number" id="sprCardsA" step="0.5" value="2.5"></div>
            </div>

            <button onclick="runAnalysis()" class="btn-analizza teko text-2xl italic tracking-widest shadow-lg">GENERA ANALISI ELITE</button>
        </div>

        <div id="results" class="pb-10"></div>
    </div>

<script>
const API_KEY = "75e4107623c05bb4bca2ac8b78b28dca";
const BASE_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
let currentLeague = 135, dbXG = [];

// Comunica l'altezza reale a Streamlit
function updateHeight() {
    const height = document.getElementById('app-content').scrollHeight + 50;
    window.parent.postMessage({type: 'streamlit:setFrameHeight', height: height}, '*');
}

function switchLeague(id) {
    currentLeague = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById(`btn-${id}`).classList.add('league-active');
    document.getElementById('arbitroContainer').style.display = (id === 135) ? "block" : "none";
    document.getElementById('foulSection').style.display = (id === 135) ? "grid" : "none";
    loadData();
}

function loadData() {
    const files = {135:"DATABASE_AVANZATO_SERIEA_2025.csv", 39:"DATABASE_AVANZATO_PREMIER_2025.csv", 78:"DATABASE_AVANZATO_BUNDES_2025.csv", 140:"DATABASE_AVANZATO_LALIGA_2025.csv"};
    Papa.parse(BASE_URL + files[currentLeague], {
        download: true, header: true, complete: (r) => { dbXG = r.data; loadTeams(); }
    });
    if(currentLeague === 135) {
        Papa.parse(BASE_URL + "ARBITRI_SERIE_A%20-%20Foglio1.csv", {
            download: true, header: true, delimiter: ";", complete: (r) => {
                const s = document.getElementById('arbitroSelect'); s.innerHTML = "";
                r.data.forEach(row => {
                    let name = row.Arbitro || Object.values(row)[0];
                    let val = (row["Media Totale"] || "24.5").toString().replace(',', '.');
                    if(name) s.add(new Option(name, val));
                });
            }
        });
    }
}

async function loadTeams() {
    const r = await fetch(`https://v3.football.api-sports.io/teams?league=${currentLeague}&season=2024`, {headers:{"x-apisports-key":API_KEY}});
    const d = await r.json();
    const h = document.getElementById('homeTeam'), a = document.getElementById('awayTeam');
    h.innerHTML = ""; a.innerHTML = "";
    d.response.sort((x,y)=>x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
    });
    setTimeout(updateHeight, 500);
}

function getBadge(val, id) {
    const spr = parseFloat(document.getElementById(id).value);
    const prob = Math.min(Math.max(50 + (val - spr) * 8, 5), 98);
    return `<br><span class="advice-tag ${val >= spr ? 'over-tag' : 'under-tag'}">${val >= spr ? 'OVER' : 'UNDER'} ${spr} (${(val >= spr ? prob : 100-prob).toFixed(1)}%)</span>`;
}

async function runAnalysis() {
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-10 teko text-2xl animate-pulse text-blue-400'>ANALISI ELITE IN CORSO...</div>";
    updateHeight();

    try {
        const idH = document.getElementById('homeTeam').value, idA = document.getElementById('awayTeam').value;
        const [sH, sA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2024&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2024&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const stH = sH.response, stA = sA.response;
        const xG = parseFloat((dbXG.find(x=>x.TeamID==idH)?.xG_Per_Shot || "0.11").toString().replace(',','.'));
        const mult = xG / 0.11;

        const tH = (stH.shots.total.average || 12) * mult, tA = (stA.shots.total.average || 10) * mult;
        const oH = (stH.shots.on_goal.average || 4) * mult, oA = (stA.shots.on_goal.average || 3.5) * mult;
        const cH = (stH.corners.for.average + stA.corners.against.average)/2, cA = (stA.corners.for.average + stH.corners.against.average)/2;
        const gH = stH.cards.yellow.average || 2, gA = stA.cards.yellow.average || 2.2;

        let html = "";
        if(currentLeague === 135) {
            const ref = parseFloat(document.getElementById('arbitroSelect').value);
            const fH = (stH.fouls.for.average + stA.fouls.against.average)/2 * 0.7 + (ref/2 * 0.3);
            const fA = (stA.fouls.for.average + stH.fouls.against.average)/2 * 0.7 + (ref/2 * 0.3);
            html += `<div class="res-box border-l-red-500"><p class="label-spread">Falli Totali</p><h2 class="text-4xl font-black teko">${(fH+fA).toFixed(2)} ${getBadge(fH+fA, 'sprFoulsMatch')}</h2></div>`;
        }

        html += `<div class="res-box border-l-emerald-500"><p class="label-spread">Tiri Totali</p><h2 class="text-4xl font-black teko">${(tH+tA).toFixed(2)} ${getBadge(tH+tA, 'sprTotalMatch')}</h2></div>`;
        html += `<div class="res-box border-l-purple-500"><p class="label-spread">Tiri in Porta</p><h2 class="text-4xl font-black teko">${(oH+oA).toFixed(2)} ${getBadge(oH+oA, 'sprOTMatch')}</h2></div>`;
        html += `<div class="res-box border-l-cyan-500"><p class="label-spread">Corner Totali</p><h2 class="text-4xl font-black teko">${(cH+cA).toFixed(2)} ${getBadge(cH+cA, 'sprCornMatch')}</h2></div>`;
        html += `<div class="res-box border-l-yellow-500"><p class="label-spread">Gialli Totali</p><h2 class="text-4xl font-black teko">${(gH+gA).toFixed(2)} ${getBadge(gH+gA, 'sprCardsMatch')}</h2></div>`;

        resDiv.innerHTML = html;
        setTimeout(updateHeight, 300);
    } catch(e) { resDiv.innerHTML = "<div class='text-red-500 p-4'>Errore Dati API</div>"; }
}
loadData();
</script>
</body>
</html>
"""

# Usiamo un'altezza di base sicura, ma lo script updateHeight la sistemerà subito
components.html(html_code, height=1800, scrolling=False)
