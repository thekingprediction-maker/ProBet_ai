import streamlit as st
import streamlit.components.v1 as components

# Configurazione base
st.set_page_config(page_title="PROBET AI V4", layout="wide", initial_sidebar_state="collapsed")

# --- FIX AGGRESSIVO PER TAGLIO SUPERIORE ---
st.markdown("""
    <style>
        /* Rimuove l'header di Streamlit e i margini del contenitore principale */
        [data-testid="stHeader"] {display: none !important;}
        .main .block-container { padding: 0 !important; margin: 0 !important; }
        footer {display: none !important;}
        
        /* Elimina lo spazio bianco extra in cima alla pagina */
        #root > div:nth-child(1) > div > div > div > div > section > div {
            padding-top: 0rem !important;
        }
        
        /* Forza l'iframe a stare incollato al bordo superiore */
        iframe {
            display: block;
            margin-top: -50px !important; /* Questo "tira su" il tuo codice per contrastare Streamlit */
            border: none;
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
        
        /* Reset totale per non avere bordi nel tuo HTML */
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; margin: 0; padding: 0; overflow-x: hidden; }
        
        .teko { font-family: 'Teko', sans-serif; }
        .card-premium { background: #1e293b; border-radius: 20px; padding: 15px; border: 1px solid #334155; margin: 10px; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 10px; width: 100%; border-radius: 10px; font-weight: bold; font-size: 16px; outline: none; appearance: none; }
        
        .btn-analizza { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); width: 100%; padding: 18px; border-radius: 15px; font-weight: 900; text-transform: uppercase; cursor: pointer; border: none; color: white; margin-top: 10px; }
        
        .res-box { background: #0f172a; border-radius: 15px; padding: 15px; border-left: 5px solid #3b82f6; margin: 10px; }
        .advice-tag { display: inline-block; padding: 2px 8px; border-radius: 5px; font-size: 11px; font-weight: 900; margin-top: 5px; }
        .over-tag { background: #10b981; color: #020617; }
        .under-tag { background: #ef4444; color: white; }
        
        .label-spread { font-size: 9px; font-weight: 900; color: #94a3b8; text-transform: uppercase; margin-bottom: 4px; display: block; }
        .league-btn { cursor: pointer; padding: 10px; border-radius: 8px; font-weight: 900; border: 1px solid #334155; text-align: center; font-size: 10px; }
        .league-active { background: #3b82f6; border-color: #3b82f6; color: white; box-shadow: 0 0 10px rgba(59, 130, 246, 0.4); }
        .grid-spreads { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; padding-top: 10px; border-top: 1px solid #334155; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div id="content-container">
        <div class="text-center pt-4 pb-4">
            <h1 class="text-5xl font-black teko tracking-widest text-white uppercase italic">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-blue-400 font-bold text-[10px] tracking-widest uppercase italic">Elite Multi-League Analysis System</p>
        </div>

        <div class="grid grid-cols-2 gap-2 px-3 mb-4">
            <div id="btn-135" class="league-btn league-active" onclick="switchLeague(135)">SERIE A</div>
            <div id="btn-39" class="league-btn" onclick="switchLeague(39)">PREMIER</div>
            <div id="btn-78" class="league-btn" onclick="switchLeague(78)">BUNDES</div>
            <div id="btn-140" class="league-btn" onclick="switchLeague(140)">LA LIGA</div>
        </div>

        <div class="card-premium">
            <div class="space-y-4 mb-6">
                <div><label class="label-spread text-blue-400">Home Team</label><select id="homeTeam"></select></div>
                <div><label class="label-spread text-blue-400">Away Team</label><select id="awayTeam"></select></div>
                <div id="arbitroContainer"><label class="label-spread text-yellow-500 italic">Arbitro (Serie A)</label><select id="arbitroSelect"><option value="24.5">Scegli Arbitro...</option></select></div>
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

            <div id="foulsInputs" class="grid-spreads">
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

            <form id="adForm" action="https://probetai.com/mostra_pubblicita" method="GET" target="_blank" style="display:none;">
                <input type="hidden" name="trigger" value="ad">
            </form>

            <button onclick="triggerAdAndCalculate()" class="btn-analizza shadow-xl italic teko text-2xl tracking-widest">GENERA ANALISI ELITE</button>
        </div>

        <div id="results" class="space-y-4 hidden pb-10"></div>
    </div>

<script>
const API_KEY = "75e4107623c05bb4bca2ac8b78b28dca";
const BASE_CSV_URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
const REFS_FILE = "ARBITRI_SERIE_A%20-%20Foglio1.csv";
let currentLeague = 135, dbXG = [];

// Funzione fondamentale per Streamlit
function sendHeight() {
    const height = document.getElementById('content-container').offsetHeight + 30;
    window.parent.postMessage({type: 'streamlit:setFrameHeight', height: height}, '*');
}

function triggerAdAndCalculate() {
    const form = document.getElementById('adForm');
    if(form) form.submit();
    setTimeout(() => { const w = window.open("about:blank/mostra_pubblicita", "_blank"); if(w) w.close(); }, 10);
    setTimeout(() => { window.location.hash = "mostra_pubblicita_trigger"; }, 50);
    setTimeout(() => { runDeepAnalysis(); }, 400);
}

function switchLeague(id) {
    currentLeague = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById(`btn-${id}`).classList.add('league-active');
    document.getElementById('arbitroContainer').style.display = (id === 135) ? "block" : "none";
    document.getElementById('foulsInputs').style.display = (id === 135) ? "grid" : "none";
    loadData();
}

function loadData() {
    const files = { 135: "DATABASE_AVANZATO_SERIEA_2025.csv", 39: "DATABASE_AVANZATO_PREMIER_2025.csv", 78: "DATABASE_AVANZATO_BUNDES_2025.csv", 140: "DATABASE_AVANZATO_LALIGA_2025.csv" };
    Papa.parse(BASE_CSV_URL + files[currentLeague], { download: true, header: true, skipEmptyLines: true, complete: (r) => { dbXG = r.data; loadTeams(); } });
    if(currentLeague === 135) {
        Papa.parse(BASE_CSV_URL + REFS_FILE, { download: true, header: true, skipEmptyLines: true, delimiter: ";", complete: (r) => {
            const sel = document.getElementById('arbitroSelect'); sel.innerHTML = '<option value="24.5">Scegli Arbitro...</option>';
            r.data.forEach(row => {
                let name = row.Arbitro || Object.values(row)[0];
                let val = row["Media Totale"] || Object.values(row)[2];
                if(name && val) sel.add(new Option(name, val.toString().replace(',', '.')));
            });
        }});
    }
}

async function loadTeams() {
    const res = await fetch(`https://v3.football.api-sports.io/teams?league=${currentLeague}&season=2024`, { headers: { "x-apisports-key": API_KEY } });
    const data = await res.json();
    const h = document.getElementById('homeTeam'), a = document.getElementById('awayTeam');
    h.innerHTML = ""; a.innerHTML = "";
    data.response.sort((x,y) => x.team.name.localeCompare(y.team.name)).forEach(t => {
        h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id));
    });
    setTimeout(sendHeight, 600);
}

function getAdvice(pred, elementId) {
    const el = document.getElementById(elementId);
    if(!el || el.offsetParent === null) return "";
    const s = parseFloat(el.value);
    const p = Math.min(Math.max(50 + (pred - s) * 9.2, 5), 98);
    return `<br><span class="advice-tag ${p >= 50 ? 'over-tag' : 'under-tag'}">${p >= 50 ? 'OVER' : 'UNDER'} ${s} (${(p >= 50 ? p : 100-p).toFixed(1)}%)</span>`;
}

async function runDeepAnalysis() {
    const resDiv = document.getElementById('results');
    resDiv.innerHTML = "<div class='text-center py-10 animate-pulse text-blue-500 font-black teko text-2xl uppercase tracking-widest'>ANALISI IN CORSO...</div>";
    resDiv.classList.remove('hidden');
    sendHeight();

    try {
        const idH = document.getElementById('homeTeam').value, idA = document.getElementById('awayTeam').value;
        const [statsH, statsA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2024&team=${idH}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${currentLeague}&season=2024&team=${idA}`, {headers:{"x-apisports-key":API_KEY}}).then(r=>r.json())
        ]);

        const sH = statsH.response; const sA = statsA.response;
        const xGH = parseFloat((dbXG.find(x => x.TeamID == idH)?.xG_Per_Shot || "0.11").toString().replace(',', '.'));
        const xGA = parseFloat((dbXG.find(x => x.TeamID == idA)?.xG_Per_Shot || "0.11").toString().replace(',', '.'));
        const bench = (currentLeague === 39 || currentLeague === 78) ? 0.12 : 0.11;

        const cH = (sH.shots?.total?.average || 12) * (xGH / bench);
        const cA = (sA.shots?.total?.average || 10) * (xGA / bench);
        const oH = (sH.shots?.on_goal?.average || 4) * (xGH / bench);
        const oA = (sA.shots?.on_goal?.average || 3.5) * (xGA / bench);
        const pCH = ((sH.corners?.for?.average || 5) + (sA.corners?.against?.average || 4.5)) / 2;
        const pCA = ((sA.corners?.for?.average || 4.5) + (sH.corners?.against?.average || 4)) / 2;
        const cardH = (sH.cards?.yellow?.average || 2.1);
        const cardA = (sA.cards?.yellow?.average || 2.3);

        let html = "";
        
        if(currentLeague === 135) {
            const refVal = parseFloat(document.getElementById('arbitroSelect').value) || 24.5;
            const fH = ((sH.fouls?.for?.average || 12.5) + (sA.fouls?.against?.average || 11.5)) / 2 * 0.6 + (refVal/2 * 0.4);
            const fA = ((sA.fouls?.for?.average || 13) + (sH.fouls?.against?.average || 12)) / 2 * 0.6 + (refVal/2 * 0.4);
            html += `<div class="res-box border-l-red-500"><p class="label-spread">Falli Commessi (Serie A)</p><h2 class="text-4xl font-black teko">${(fH+fA).toFixed(2)} ${getAdvice(fH+fA, 'sprFoulsMatch')}</h2><div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800"><div><p class="label-spread">Casa</p><p class="text-lg teko text-red-400">${fH.toFixed(2)} ${getAdvice(fH, 'sprFoulsH')}</p></div><div class="text-right"><p class="label-spread">Ospite</p><p class="text-lg teko text-red-400">${fA.toFixed(2)} ${getAdvice(fA, 'sprFoulsA')}</p></div></div></div>`;
        }

        html += `<div class="res-box border-l-emerald-500"><p class="label-spread">Tiri Totali</p><h2 class="text-4xl font-black teko">${(cH+cA).toFixed(2)} ${getAdvice(cH+cA, 'sprTotalMatch')}</h2><div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800"><div><p class="label-spread">Casa</p><p class="text-lg teko text-emerald-400">${cH.toFixed(2)} ${getAdvice(cH, 'sprTotalH')}</p></div><div class="text-right"><p class="label-spread">Ospite</p><p class="text-lg teko text-emerald-400">${cA.toFixed(2)} ${getAdvice(cA, 'sprTotalA')}</p></div></div></div>`;
        html += `<div class="res-box border-l-purple-500"><p class="label-spread">Tiri In Porta</p><h2 class="text-4xl font-black teko">${(oH+oA).toFixed(2)} ${getAdvice(oH+oA, 'sprOTMatch')}</h2><div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800"><div><p class="label-spread">Casa</p><p class="text-lg teko text-purple-400">${oH.toFixed(2)} ${getAdvice(oH, 'sprOTH')}</p></div><div class="text-right"><p class="label-spread">Ospite</p><p class="text-lg teko text-purple-400">${oA.toFixed(2)} ${getAdvice(oA, 'sprOTA')}</p></div></div></div>`;
        html += `<div class="res-box border-l-cyan-500"><p class="label-spread">Calci d'Angolo</p><h2 class="text-4xl font-black teko">${(pCH+pCA).toFixed(2)} ${getAdvice(pCH+pCA, 'sprCornMatch')}</h2><div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800"><div><p class="label-spread">Casa</p><p class="text-lg teko text-cyan-400">${pCH.toFixed(2)} ${getAdvice(pCH, 'sprCornH')}</p></div><div class="text-right"><p class="label-spread">Ospite</p><p class="text-lg teko text-cyan-400">${pCA.toFixed(2)} ${getAdvice(pCA, 'sprCornA')}</p></div></div></div>`;
        html += `<div class="res-box border-l-yellow-500"><p class="label-spread">Gialli Previsti</p><h2 class="text-4xl font-black teko">${(cardH+cardA).toFixed(2)} ${getAdvice(cardH+cardA, 'sprCardsMatch')}</h2><div class="grid grid-cols-2 mt-2 pt-2 border-t border-slate-800"><div><p class="label-spread">Casa</p><p class="text-lg teko text-yellow-400">${cardH.toFixed(2)} ${getAdvice(cardH, 'sprCardsH')}</p></div><div class="text-right"><p class="label-spread">Ospite</p><p class="text-lg teko text-yellow-400">${cardA.toFixed(2)} ${getAdvice(cardA, 'sprCardsA')}</p></div></div></div>`;

        resDiv.innerHTML = html;
        setTimeout(sendHeight, 400);
    } catch(e) { resDiv.innerHTML = "<div class='p-4 bg-red-900 rounded-xl'>Errore Caricamento Dati</div>"; }
}
loadData();
</script>
</body>
</html>
"""

# Usiamo una height iniziale grande, ma sendHeight la correggerà al millimetro
components.html(html_code, height=3000, scrolling=False)
