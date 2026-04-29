import streamlit as st
import streamlit.components.v1 as components

# Configurazione Pagina
st.set_page_config(page_title="PROBET AI V4", layout="wide", initial_sidebar_state="collapsed")

# CSS per pulire l'interfaccia Streamlit
st.markdown("""
    <style>
        [data-testid="stHeader"], footer {display: none !important;}
        .main .block-container { padding: 1rem !important; }
        iframe { border: none !important; }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;900&display=swap');
        body { background: #020617; color: white; font-family: 'Inter', sans-serif; margin: 0; padding: 5px; }
        .teko { font-family: 'Teko', sans-serif; }
        .card-input { background: #1e293b; border-radius: 15px; padding: 15px; border: 1px solid #334155; margin-bottom: 15px; }
        select, input { background: #0f172a; border: 1px solid #475569; color: white; padding: 8px; width: 100%; border-radius: 8px; font-size: 14px; outline: none; }
        .btn-main { background: #3b82f6; width: 100%; padding: 15px; border-radius: 12px; font-weight: 900; color: white; border: none; cursor: pointer; margin-top: 10px; }
        .res-card { background: #0f172a; border-radius: 12px; padding: 12px; border-left: 4px solid #3b82f6; margin-top: 10px; }
        .label-sm { font-size: 10px; color: #94a3b8; text-transform: uppercase; font-weight: 700; }
        .league-btn { cursor: pointer; padding: 8px; border-radius: 6px; font-weight: 800; border: 1px solid #334155; text-align: center; font-size: 10px; background: #0f172a; }
        .league-active { background: #3b82f6; border-color: #3b82f6; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5px; margin-top: 8px; }
        .badge { font-size: 10px; padding: 2px 5px; border-radius: 4px; font-weight: 900; margin-top: 4px; display: inline-block; }
    </style>
</head>
<body>
    <div id="wrapper">
        <div class="text-center mb-4">
            <h1 class="text-5xl font-black teko italic leading-none">PROBET <span class="text-blue-500">AI V4</span></h1>
            <p class="text-blue-400 font-bold text-[9px] uppercase italic tracking-widest">Elite Multi-League System</p>
        </div>

        <div class="grid grid-cols-4 gap-1 mb-4">
            <div id="l135" class="league-btn league-active" onclick="selLeague(135)">SERIE A</div>
            <div id="l39" class="league-btn" onclick="selLeague(39)">PREMIER</div>
            <div id="l78" class="league-btn" onclick="selLeague(78)">BUNDES</div>
            <div id="l140" class="league-btn" onclick="selLeague(140)">LA LIGA</div>
        </div>

        <div class="card-input">
            <div class="space-y-3">
                <div><label class="label-sm">Home Team</label><select id="hTeam"></select></div>
                <div><label class="label-sm">Away Team</label><select id="aTeam"></select></div>
                <div id="refBox"><label class="label-sm text-yellow-500">Arbitro (Serie A)</label><select id="refSel"></select></div>
            </div>

            <div class="grid-3"><input type="number" id="s_tt" value="23.5"><input type="number" id="s_th" value="12.5"><input type="number" id="s_ta" value="10.5"></div>
            <div class="grid-3"><input type="number" id="s_pt" value="8.5"><input type="number" id="s_ph" value="4.5"><input type="number" id="s_pa" value="3.5"></div>
            <div class="grid-3" id="fBox"><input type="number" id="s_ft" value="24.5"><input type="number" id="s_fh" value="12.5"><input type="number" id="s_fa" value="11.5"></div>
            <div class="grid-3"><input type="number" id="s_ct" value="9.5"><input type="number" id="s_ch" value="5.5"><input type="number" id="s_ca" value="4.5"></div>
            <div class="grid-3"><input type="number" id="s_gt" value="4.5"><input type="number" id="s_gh" value="2.5"><input type="number" id="s_ga" value="2.5"></div>

            <button onclick="start()" class="btn-main teko text-2xl italic italic tracking-wider">GENERA ANALISI</button>
        </div>

        <div id="output" class="pb-10"></div>
    </div>

<script>
const K = "75e4107623c05bb4bca2ac8b78b28dca";
const URL = "https://raw.githubusercontent.com/thekingprediction-maker/DATABASE_AVANZATO_2025.csv/main/";
let curL = 135, dbX = [];

function resize() {
    const h = document.getElementById('wrapper').scrollHeight + 40;
    window.parent.postMessage({type: 'streamlit:setFrameHeight', height: h}, '*');
}

function selLeague(id) {
    curL = id;
    document.querySelectorAll('.league-btn').forEach(b => b.classList.remove('league-active'));
    document.getElementById('l'+id).classList.add('league-active');
    document.getElementById('refBox').style.display = (id==135)?'block':'none';
    document.getElementById('fBox').style.display = (id==135)?'grid':'none';
    init();
}

function init() {
    const files = {135:"DATABASE_AVANZATO_SERIEA_2025.csv", 39:"DATABASE_AVANZATO_PREMIER_2025.csv", 78:"DATABASE_AVANZATO_BUNDES_2025.csv", 140:"DATABASE_AVANZATO_LALIGA_2025.csv"};
    Papa.parse(URL + files[curL], { download: true, header: true, complete: (r) => { dbX = r.data; loadT(); } });
    if(curL==135) Papa.parse(URL + "ARBITRI_SERIE_A%20-%20Foglio1.csv", { download: true, header: true, delimiter: ";", complete: (r) => {
        const s = document.getElementById('refSel'); s.innerHTML = "";
        r.data.forEach(x => { let n = x.Arbitro || Object.values(x)[0]; let v = (x["Media Totale"] || "24.5").toString().replace(',','.'); if(n) s.add(new Option(n, v)); });
    }});
}

async function loadT() {
    const r = await fetch(`https://v3.football.api-sports.io/teams?league=${curL}&season=2024`, {headers:{"x-apisports-key":K}});
    const d = await r.json();
    const h = document.getElementById('hTeam'), a = document.getElementById('aTeam');
    h.innerHTML = ""; a.innerHTML = "";
    d.response.sort((a,b)=>a.team.name.localeCompare(b.team.name)).forEach(t => { h.add(new Option(t.team.name, t.team.id)); a.add(new Option(t.team.name, t.team.id)); });
    setTimeout(resize, 400);
}

function getAdv(val, elId) {
    const s = parseFloat(document.getElementById(elId).value);
    const p = Math.min(Math.max(50 + (val-s)*9, 5), 98);
    return `<br><span class="badge ${val>=s?'bg-emerald-500':'bg-red-500'}">${val>=s?'OVER':'UNDER'} ${s} (${(val>=s?p:100-p).toFixed(1)}%)</span>`;
}

async function start() {
    const out = document.getElementById('output');
    out.innerHTML = "<p class='text-center py-5 teko text-xl animate-pulse'>CALCOLO IN CORSO...</p>";
    resize();

    try {
        const idH = document.getElementById('hTeam').value, idA = document.getElementById('aTeam').value;
        const [rH, rA] = await Promise.all([
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2024&team=${idH}`, {headers:{"x-apisports-key":K}}).then(r=>r.json()),
            fetch(`https://v3.football.api-sports.io/teams/statistics?league=${curL}&season=2024&team=${idA}`, {headers:{"x-apisports-key":K}}).then(r=>r.json())
        ]);

        const sH = rH.response, sA = rA.response;
        const xG = parseFloat((dbX.find(x=>x.TeamID==idH)?.xG_Per_Shot || "0.11").toString().replace(',','.'));
        const m = xG / 0.11;

        const tT = (sH.shots.total.average + sA.shots.total.average) * m;
        const pT = (sH.shots.on_goal.average + sA.shots.on_goal.average) * m;
        const cT = sH.corners.for.average + sA.corners.for.average;
        const gT = (sH.cards.yellow.average || 2) + (sA.cards.yellow.average || 2);

        let res = `<div class="res-card"><div>TIRI TOTALI</div><div class="text-3xl font-black teko">${tT.toFixed(2)} ${getAdv(tT, 's_tt')}</div></div>`;
        res += `<div class="res-card border-l-purple-500"><div>IN PORTA</div><div class="text-3xl font-black teko">${pT.toFixed(2)} ${getAdv(pT, 's_pt')}</div></div>`;
        
        if(curL==135) {
            const rf = parseFloat(document.getElementById('refSel').value);
            const fT = (sH.fouls.for.average + sA.fouls.for.average) * 0.7 + (rf * 0.3);
            res += `<div class="res-card border-l-red-500"><div>FALLI</div><div class="text-3xl font-black teko">${fT.toFixed(2)} ${getAdv(fT, 's_ft')}</div></div>`;
        }

        res += `<div class="res-card border-l-cyan-500"><div>CORNER</div><div class="text-3xl font-black teko">${cT.toFixed(2)} ${getAdv(cT, 's_ct')}</div></div>`;
        res += `<div class="res-card border-l-yellow-500"><div>GIALLI</div><div class="text-3xl font-black teko">${gT.toFixed(2)} ${getAdv(gT, 's_gt')}</div></div>`;

        out.innerHTML = res;
        setTimeout(resize, 300);
    } catch(e) { out.innerHTML = "<p class='text-red-500'>Errore Statistiche API</p>"; }
}
init();
</script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=False)
