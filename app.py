import streamlit as st
import streamlit.components.v1 as components

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="ProBet AI", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0 !important; margin: 0 !important; }
    iframe { width: 100vw !important; height: 100vh !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- CODICE HTML + JS + LOGICA CALCOLO ---
html_all_in_one = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@600&family=Inter:wght@400;700;900&display=swap');
        body { background-color: #0f172a; color: white; font-family: 'Inter', sans-serif; padding-bottom: 50px; }
        .teko { font-family: 'Teko', sans-serif; text-transform: uppercase; }
        .input-dark { background: #1e293b; border: 1px solid #334155; color: white; padding: 10px; border-radius: 8px; width: 100%; font-weight: bold; }
        .btn-league { flex: 1; py: 3; font-weight: bold; border-radius: 8px; transition: 0.3s; font-size: 12px; }
        .active-l { background: #3b82f6; color: white; }
        .inactive-l { background: #1e293b; color: #94a3b8; }
        .card { background: #1e293b; border-radius: 12px; padding: 15px; margin-bottom: 15px; border: 1px solid #334155; }
        .val-box { padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; border: 1px solid rgba(255,255,255,0.1); }
        .over { background: linear-gradient(135deg, #166534, #14532d); border-color: #22c55e; }
        .under { background: linear-gradient(135deg, #991b1b, #7f1d1d); border-color: #ef4444; }
    </style>
</head>
<body>

    <div id="ad-top" class="w-full flex justify-center py-2 min-h-[50px] bg-slate-900/50 mb-4">
        <span class="text-[10px] text-slate-500">PUBBLICITÀ</span>
    </div>

    <div class="px-4 max-w-md mx-auto">
        <div class="flex items-center justify-between mb-6">
            <h1 class="text-3xl teko tracking-widest">PROBET <span class="text-blue-500">AI</span></h1>
            <div id="status" class="text-[10px] bg-slate-800 px-2 py-1 rounded">CARICAMENTO...</div>
        </div>

        <div class="flex gap-2 mb-6">
            <button onclick="changeLeague('SERIE_A')" id="btn-SERIE_A" class="btn-league active-l p-3">SERIE A</button>
            <button onclick="changeLeague('PREMIER')" id="btn-PREMIER" class="btn-league inactive-l p-3">PREMIER</button>
            <button onclick="changeLeague('LIGA')" id="btn-LIGA" class="btn-league inactive-l p-3">LIGA</button>
        </div>

        <div class="card">
            <div class="mb-4">
                <label class="text-[10px] font-bold text-slate-400">SQUADRA CASA</label>
                <select id="home" class="input-dark mt-1"></select>
            </div>
            <div class="mb-4">
                <label class="text-[10px] font-bold text-slate-400">SQUADRA OSPITE</label>
                <select id="away" class="input-dark mt-1"></select>
            </div>
            <div id="ref-div" class="mb-2">
                <label class="text-[10px] font-bold text-slate-400 text-yellow-500">ARBITRO (MEDIA FALLI)</label>
                <select id="ref" class="input-dark mt-1 border-yellow-500/30"></select>
            </div>
        </div>

        <button onclick="startAnalysis()" class="w-full bg-blue-600 hover:bg-blue-500 py-4 rounded-xl font-black text-lg shadow-lg active:scale-95 transition-all mb-8">
            ANALIZZA DATI
        </button>

        <div id="results" class="hidden space-y-4">
            <h3 class="teko text-xl text-blue-400 border-b border-slate-700">PREVISIONE AI</h3>
            <div id="results-content" class="grid grid-cols-1 gap-3"></div>
        </div>
    </div>

    <script>
        const LINKS = {
            SERIE_A: {
                arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_SERIE_A%20-%20Foglio1.csv",
                curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_SERIE_A%20-%20Foglio1.csv",
                prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_SERIE_A%20-%20DATI%20STAGIONE%202024_2025%20.csv",
                tiri: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/TIRI_SERIE_A%20%20-%20DATI%20TIRI%20TOTALI%20E%20TIRI%20IN%20PORTA%20STAGIONE%202025_26.csv"
            },
            PREMIER: {
                tiri: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/TIRI_PREMIER_LEAGUE%20-%20DATI%20TIRI%20TOTALI%20E%20TIRI%20IN%20PORTA%20STAGIONE%202025_26.csv"
            },
            LIGA: {
                arb: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/ARBITRI_LIGA%20-%20Foglio1.csv",
                curr: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_CURR_LIGA%20-%20Foglio1.csv",
                prev: "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/FALLI_PREV_LIGA%20%20-%20DATI%20STAGIONE%202024_2025.csv"
            }
        };

        let currentLeague = 'SERIE_A';
        let db = { falli: [], tiri: [], arbitri: [] };

        async function load() {
            document.getElementById('status').innerText = "CARICAMENTO...";
            const L = LINKS[currentLeague];
            
            try {
                // Carica Arbitri
                if(L.arb) {
                    const res = await fetch(L.arb);
                    const txt = await res.text();
                    db.arbitri = Papa.parse(txt).data.slice(1).map(r => ({n: r[0], m: parseFloat(String(r[2]).replace(',','.')) || 0})).filter(x=>x.n);
                }
                
                // Carica Falli (Corrente + Precedente per media pesata)
                if(L.curr) {
                    const res = await fetch(L.curr);
                    const txt = await res.text();
                    db.falli = Papa.parse(txt).data.slice(1).map(r => ({t: r[1], l: r[2], sub: parseFloat(r[3])||0, comm: parseFloat(r[4])||0})).filter(x=>x.t);
                }

                // Carica Tiri (Logica specifica per saltare intestazioni sporche)
                if(L.tiri) {
                    const res = await fetch(L.tiri);
                    const txt = await res.text();
                    const raw = Papa.parse(txt).data;
                    const startIdx = raw.findIndex(r => r[0] && r[0].includes("Squadra")) + 1;
                    db.tiri = raw.slice(startIdx).map(r => ({
                        t: r[0],
                        tc: (parseFloat(r[2])/parseFloat(r[1]))||0, // Tiri fatti casa / partite
                        tsf: (parseFloat(r[8])/parseFloat(r[6]))||0, // Tiri subiti fuori / partite
                        tpc: (parseFloat(r[4])/parseFloat(r[1]))||0, // In porta fatti casa
                        tpsf: (parseFloat(r[10])/parseFloat(r[6]))||0 // In porta subiti fuori
                    })).filter(x=>x.t);
                }

                updateSelects();
                document.getElementById('status').innerText = "PRONTO";
            } catch(e) {
                document.getElementById('status').innerText = "ERRORE DATI";
            }
        }

        function updateSelects() {
            const h = document.getElementById('home');
            const a = document.getElementById('away');
            const r = document.getElementById('ref');
            h.innerHTML = ''; a.innerHTML = ''; r.innerHTML = '<option value="0">Seleziona Arbitro (Opzionale)</option>';
            
            const teams = [...new Set([...db.falli.map(x=>x.t), ...db.tiri.map(x=>x.t)])].sort();
            teams.forEach(t => {
                h.add(new Option(t, t));
                a.add(new Option(t, t));
            });
            
            db.arbitri.forEach(arb => r.add(new Option(`${arb.n} (${arb.m})`, arb.m)));
            document.getElementById('ref-div').style.display = currentLeague === 'PREMIER' ? 'none' : 'block';
        }

        function changeLeague(l) {
            currentLeague = l;
            ['SERIE_A', 'PREMIER', 'LIGA'].forEach(id => {
                document.getElementById('btn-'+id).className = id === l ? 'btn-league active-l p-3' : 'btn-league inactive-l p-3';
            });
            load();
        }

        function startAnalysis() {
            const h = document.getElementById('home').value;
            const a = document.getElementById('away').value;
            const refM = parseFloat(document.getElementById('ref').value);
            
            if(h === a) return alert("Scegli due squadre diverse!");

            let resultsHtml = '';

            // CALCOLO FALLI
            if(currentLeague !== 'PREMIER') {
                const dataH = db.falli.find(x => x.t === h && x.l === 'CASA') || {comm:12, sub:12};
                const dataA = db.falli.find(x => x.t === a && x.l === 'FUORI') || {comm:12, sub:12};
                let predF = ((dataH.comm + dataA.sub)/2) + ((dataA.comm + dataH.sub)/2);
                if(refM > 0) predF = predF * (refM / 24.5); // Correzione basata sulla media arbitro
                
                resultsHtml += makeBox("FALLI TOTALI", predF, 24.5);
            }

            // CALCOLO TIRI
            const tH = db.tiri.find(x => x.t === h);
            const tA = db.tiri.find(x => x.t === a);
            if(tH && tA) {
                const predT = tH.tc + tA.tsf; // Semplificato: tiri fatti casa + subiti fuori ospite
                const predTP = tH.tpc + tA.tpsf;
                resultsHtml += makeBox("TIRI TOTALI", predT, 23.5);
                resultsHtml += makeBox("TIRI IN PORTA", predTP, 8.5);
            }

            document.getElementById('results-content').innerHTML = resultsHtml;
            document.getElementById('results').classList.remove('hidden');
            
            // LOGICA REFRESH PUBBLICITÀ (Simulata)
            console.log("Analisi eseguita. Richiamo AdMob...");
            if(window.adsbygoogle) { (adsbygoogle = window.adsbygoogle || []).push({}); }
        }

        function makeBox(title, val, line) {
            const isOver = val > line;
            const prob = isOver ? 65 : 62; // Probabilità base simulata per brevità
            return `
                <div class="val-box ${isOver ? 'over' : 'under'}">
                    <div class="text-[10px] opacity-80">${title}</div>
                    <div class="text-2xl font-black">${isOver ? 'OVER' : 'UNDER'} ${line}</div>
                    <div class="text-xs mt-1">AI: ${val.toFixed(1)} | Prob: ${prob}%</div>
                </div>
            `;
        }

        load();
    </script>
</body>
</html>
"""

components.html(html_all_in_one, height=1000, scrolling=True)
