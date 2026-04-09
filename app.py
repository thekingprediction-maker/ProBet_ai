import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="ProBet AI", layout="wide", initial_sidebar_state="collapsed")

# CSS per nascondere gli elementi di Streamlit e rendere l'iframe a tutto schermo
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    iframe { width: 100vw !important; height: 100vh !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- CODICE HTML COMPLETO (TUA GRAFICA + TUOI CALCOLI) ---
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
        html, body { background-color: #0f172a; color: #e2e8f0; font-family: 'Inter', sans-serif; margin: 0; padding: 0; width: 100%; height: 100%; overflow-x: hidden; }
        .teko { font-family: 'Teko', sans-serif; }
        select { background-color: #1e293b; color: white; border: 1px solid #334155; padding: 12px; border-radius: 8px; width: 100%; font-weight: bold; outline: none; }
        .input-dark { background:#1e293b; border:1px solid #334155; color:white; padding:8px; border-radius:6px; width:100%; text-align:center; font-weight:700; }
        .value-box { padding:12px; border-radius:10px; margin-bottom:8px; text-align:center; border:1px solid; position:relative; }
        .val-high { background: linear-gradient(135deg,#15803d 0%,#166534 100%); color:white; border-color:#22c55e; }
        .val-low { background: linear-gradient(135deg,#b91c1c 0%,#991b1b 100%); color:white; border-color:#ef4444; }
        .res { font-size:24px; font-weight:900; font-family:'Teko',sans-serif; }
    </style>
</head>
<body>
    <div style="width:100%; text-align:center; min-height:50px; background:#000; color:#444; font-size:10px; padding:5px;">
        PUBBLICITÀ ADMOB
    </div>

    <header class="p-4 border-b border-slate-800 flex justify-between items-center">
        <div class="text-2xl font-bold teko text-white tracking-wide">PROBET <span class="text-blue-500">AI</span></div>
        <div id="status-pill" class="text-[10px] font-bold text-slate-400 bg-slate-900 px-3 py-1 rounded-full border border-slate-800">LOADING...</div>
    </header>

    <main class="p-4 max-w-2xl mx-auto">
        <div class="flex gap-2 mb-6">
            <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-3 text-xs font-bold rounded-lg bg-blue-600 text-white">SERIE A</button>
            <button onclick="switchLeague('PREMIER')" id="btn-pl" class="flex-1 py-3 text-xs font-bold rounded-lg bg-slate-900 text-slate-400">PREMIER</button>
            <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-3 text-xs font-bold rounded-lg bg-slate-900 text-slate-400">LIGA</button>
        </div>

        <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-xl mb-6">
            <div class="space-y-4 mb-6">
                <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">CASA</label><select id="home"></select></div>
                <div><label class="text-[10px] font-bold text-slate-500 uppercase ml-1">OSPITE</label><select id="away"></select></div>
                <div id="ref-box"><label class="text-[10px] font-bold text-slate-500 uppercase ml-1 text-yellow-500">ARBITRO</label><select id="referee" class="border-yellow-900"></select></div>
            </div>

            <div class="grid grid-cols-2 gap-4 mb-6">
                <div class="p-3 bg-black/20 rounded-lg border border-slate-800">
                    <label class="text-[9px] font-bold text-slate-500 block mb-1">LINEA FALLI</label>
                    <input type="number" id="line-f" value="24.5" step="0.5" class="input-dark">
                </div>
                <div class="p-3 bg-black/20 rounded-lg border border-slate-800">
                    <label class="text-[9px] font-bold text-slate-500 block mb-1">LINEA TIRI</label>
                    <input type="number" id="line-t" value="23.5" step="0.5" class="input-dark">
                </div>
            </div>

            <button onclick="analyze()" class="w-full py-4 bg-blue-600 hover:bg-blue-500 text-white font-black text-xl rounded-xl shadow-lg active:scale-95 transition-all">
                ANALIZZA DATI
            </button>
        </div>

        <div id="results" class="hidden animate-fade-in space-y-4 pb-20">
            <div class="text-sm font-bold text-blue-400 border-b border-slate-800 pb-2 uppercase tracking-widest">Previsione AI</div>
            <div id="grid-results" class="grid grid-cols-1 gap-3"></div>
        </div>
    </main>

    <script>
        const LINKS = {
            SERIE_A: {
                arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_SERIE_A%20-%20Foglio1.csv",
                curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_SERIE_A%20-%20Foglio1.csv",
                prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_SERIE_A%20-%20DATI%20STAGIONE%202024_2025%20.csv",
                tiri: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/TIRI_SERIE_A%20%20-%20DATI%20TIRI%20TOTALI%20E%20TIRI%20IN%20PORTA%20STAGIONE%202025_26.csv"
            },
            LIGA: {
                arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_LIGA%20-%20Foglio1.csv",
                curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_LIGA%20-%20Foglio1.csv",
                prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_LIGA%20%20-%20DATI%20STAGIONE%202024_2025.csv",
                tiri: ""
            },
            PREMIER: {
                tiri: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/TIRI_PREMIER_LEAGUE%20-%20DATI%20TIRI%20TOTALI%20E%20TIRI%20IN%20PORTA%20STAGIONE%202025_26.csv"
            }
        };

        let currentLeague = 'SERIE_A';
        let database = { refs: [], falli: [], tiri: [] };

        async function loadData() {
            const L = LINKS[currentLeague];
            try {
                if(L.arb) {
                    const r = await fetch(L.arb); const t = await r.text();
                    database.refs = Papa.parse(t).data.slice(1).map(x => ({n: x[0], m: parseFloat(x[2])||0})).filter(x=>x.n);
                }
                if(L.curr) {
                    const r = await fetch(L.curr); const t = await r.text();
                    database.falli = Papa.parse(t).data.slice(1).map(x => ({t: x[1], l: x[2], c: parseFloat(x[4])||0, s: parseFloat(x[3])||0})).filter(x=>x.t);
                }
                if(L.tiri) {
                    const r = await fetch(L.tiri); const t = await r.text();
                    const rd = Papa.parse(t).data;
                    const start = rd.findIndex(x => x[0] && x[0].includes("Squadra")) + 1;
                    database.tiri = rd.slice(start).map(x => ({
                        t: x[0],
                        tc: (parseFloat(x[2])/parseFloat(x[1]))||0,
                        tsf: (parseFloat(x[8])/parseFloat(x[6]))||0,
                        tpc: (parseFloat(x[4])/parseFloat(x[1]))||0,
                        tpsf: (parseFloat(x[10])/parseFloat(x[6]))||0
                    })).filter(x=>x.t);
                }
                updateUI();
                document.getElementById('status-pill').innerText = "READY";
            } catch(e) { document.getElementById('status-pill').innerText = "ERROR"; }
        }

        function updateUI() {
            const h = document.getElementById('home'); const a = document.getElementById('away'); const r = document.getElementById('referee');
            h.innerHTML = ''; a.innerHTML = ''; r.innerHTML = '<option value="0">Seleziona Arbitro</option>';
            const teams = [...new Set([...database.falli.map(x=>x.t), ...database.tiri.map(x=>x.t)])].sort();
            teams.forEach(t => { h.add(new Option(t, t)); a.add(new Option(t, t)); });
            database.refs.forEach(x => r.add(new Option(x.n, x.m)));
            document.getElementById('ref-box').style.display = currentLeague === 'PREMIER' ? 'none' : 'block';
        }

        function switchLeague(l) {
            currentLeague = l;
            ['btn-sa','btn-pl','btn-lg'].forEach(b => document.getElementById(b).className = "flex-1 py-3 text-xs font-bold rounded-lg bg-slate-900 text-slate-400");
            document.getElementById(l === 'SERIE_A' ? 'btn-sa' : l === 'PREMIER' ? 'btn-pl' : 'btn-lg').className = "flex-1 py-3 text-xs font-bold rounded-lg bg-blue-600 text-white";
            loadData();
        }

        function analyze() {
            const h = document.getElementById('home').value;
            const a = document.getElementById('away').value;
            if(h === a) return;

            let html = "";
            // Calcolo Falli
            if(currentLeague !== 'PREMIER') {
                const dH = database.falli.find(x => x.t === h && x.l === 'CASA') || {c:12, s:12};
                const dA = database.falli.find(x => x.t === a && x.l === 'FUORI') || {c:12, s:12};
                let pred = ((dH.c + dA.s)/2) + ((dA.c + dH.s)/2);
                const ref = parseFloat(document.getElementById('referee').value);
                if(ref > 0) pred = pred * (ref / 24.5);
                html += makeBox("FALLI TOTALI", pred, parseFloat(document.getElementById('line-f').value));
            }
            // Calcolo Tiri
            const tH = database.tiri.find(x => x.t === h);
            const tA = database.tiri.find(x => x.t === a);
            if(tH && tA) {
                const pT = tH.tc + tA.tsf;
                const pTP = tH.tpc + tA.tpsf;
                html += makeBox("TIRI TOTALI", pT, parseFloat(document.getElementById('line-t').value));
                html += makeBox("TIRI IN PORTA", pTP, 8.5);
            }

            document.getElementById('grid-results').innerHTML = html;
            document.getElementById('results').classList.remove('hidden');

            // TRIGGER ADMOB (Inserisci qui il comando per ricaricare la pubblicità)
            console.log("Analisi completata - AdMob Refresh");
        }

        function makeBox(title, val, line) {
            const isOver = val > line;
            return `<div class="value-box ${isOver ? 'val-high' : 'val-low'}">
                <div class="text-[10px] uppercase opacity-70">${title}</div>
                <div class="res">${isOver ? 'OVER' : 'UNDER'} ${line}</div>
                <div class="text-xs">AI: ${val.toFixed(2)}</div>
            </div>`;
        }

        loadData();
    </script>
</body>
</html>
"""

components.html(html_code, height=1200, scrolling=True)
