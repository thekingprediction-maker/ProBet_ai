import streamlit as st
import streamlit.components.v1 as components

# Configura la pagina per usare tutto lo schermo
st.set_page_config(page_title="ProBet AI", layout="wide", initial_sidebar_state="collapsed")

# Nascondi la barra e i menu di Streamlit per farla sembrare un'App vera
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        height: 100vh !important;
    }
    </style>
""", unsafe_allow_html=True)

# QUI INIZIA IL TUO CODICE HTML (INCAPSULATO)
html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ProBet AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
        body { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #e2e8f0; overflow-x: hidden; }
        .teko { font-family: 'Teko', sans-serif; }
        .sidebar {
            position: fixed; top: 0; left: 0; bottom: 0; width: 300px;
            background: #020617; border-right: 1px solid #1e293b;
            transform: translateX(-100%); transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 50; padding: 20px; overflow-y: auto;
        }
        .sidebar.open { transform: translateX(0); }
        .overlay {
            position: fixed; inset: 0; background: rgba(0,0,0,0.8);
            z-index: 40; display: none; backdrop-filter: blur(4px);
        }
        .overlay.open { display: block; }
        .input-dark {
            background: #1e293b; border: 1px solid #334155; color: white;
            padding: 10px; border-radius: 8px; width: 100%; outline: none; font-weight: bold; text-align: center;
        }
        select {
            background-color: #1e293b; color: white; border: 1px solid #334155; padding: 12px;
            border-radius: 8px; width: 100%; font-weight: bold; appearance: none;
        }
        .value-box {
            padding: 15px; border-radius: 12px; margin-bottom: 10px; text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2); border: 1px solid;
        }
        .val-high { background-color: #15803d; color: white; border-color: #22c55e; } 
        .val-med { background-color: #ca8a04; color: #fff; border-color: #facc15; } 
        .val-low { background-color: #b91c1c; color: white; border-color: #ef4444; } 
        .res { font-size: 28px; font-weight: 900; margin: 4px 0; font-family: 'Teko', sans-serif; line-height: 1; }
        .loader {
            width: 16px; height: 16px; border: 2px solid #475569; border-bottom-color: #3b82f6;
            border-radius: 50%; display: inline-block; animation: rotation 1s linear infinite;
        }
        @keyframes rotation { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div id="overlay" class="overlay" onclick="toggleSidebar()"></div>
    <aside id="sidebar" class="sidebar shadow-2xl">
        <div class="flex justify-between items-center mb-6 pb-4 border-b border-slate-800">
            <h2 class="text-xl font-bold text-white">CONFIGURAZIONE</h2>
            <button onclick="toggleSidebar()"><i data-lucide="x"></i></button>
        </div>
        <div class="mb-4">
            <label class="text-[10px] uppercase font-bold text-slate-500 mb-2 block">Campionato</label>
            <div class="grid grid-cols-2 bg-slate-900 p-1 rounded-xl border border-slate-800">
                <button onclick="switchLeague('SERIE_A')" id="side-sa" class="py-2 text-xs font-bold rounded-lg bg-blue-600 text-white">SERIE A</button>
                <button onclick="switchLeague('LIGA')" id="side-lg" class="py-2 text-xs font-bold rounded-lg text-slate-400">LIGA</button>
            </div>
        </div>
        <div id="links-container" class="space-y-3"></div>
        <button onclick="loadData()" class="w-full mt-6 py-3 bg-blue-600 text-white font-bold rounded-xl flex justify-center items-center gap-2">
            <i data-lucide="refresh-cw" class="w-4 h-4"></i> RICARICA
        </button>
    </aside>

    <header class="fixed top-0 w-full z-30 bg-[#0f172a]/95 backdrop-blur border-b border-slate-800">
        <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <button onclick="toggleSidebar()" class="p-2 bg-slate-800 rounded-lg text-white"><i data-lucide="menu"></i></button>
                <div class="text-2xl font-bold teko text-white">PROBET <span class="text-blue-500">AI</span></div>
            </div>
            <div id="status-pill" class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800">
                <span class="text-[10px] font-bold text-slate-400">READY</span>
            </div>
        </div>
    </header>

    <main class="pt-20 px-4 max-w-6xl mx-auto space-y-6 pb-20">
        <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div><label class="text-[10px] font-bold text-slate-500 uppercase">CASA</label><select id="home" class="mt-1"><option>Caricamento...</option></select></div>
                <div><label class="text-[10px] font-bold text-slate-500 uppercase">OSPITE</label><select id="away" class="mt-1"><option>Caricamento...</option></select></div>
                <div><label class="text-[10px] font-bold text-slate-500 uppercase">ARBITRO</label><select id="referee" class="mt-1 text-yellow-400"><option>Caricamento...</option></select></div>
            </div>

            <details class="bg-black/20 p-4 rounded-xl border border-slate-800/50 mb-5" open>
                <summary class="cursor-pointer font-bold text-slate-400 text-xs uppercase mb-2">Quote Bookmaker</summary>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <div class="text-[9px] font-bold text-red-400 uppercase mb-2 text-center">LINEE FALLI</div>
                        <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark mb-2 text-lg">
                        <div class="grid grid-cols-2 gap-2"><input type="number" id="line-f-h" value="11.5" class="input-dark text-xs"><input type="number" id="line-f-a" value="11.5" class="input-dark text-xs"></div>
                    </div>
                    <div id="box-tiri-lines" class="bg-slate-950 p-3 rounded-lg border border-slate-800 md:col-span-2">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <div class="text-[9px] font-bold text-blue-400 uppercase mb-2 text-center">TIRI TOTALI</div>
                                <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark mb-2">
                                <div class="grid grid-cols-2 gap-2"><input type="number" id="line-t-h" value="12.5" class="input-dark text-xs"><input type="number" id="line-t-a" value="10.5" class="input-dark text-xs"></div>
                            </div>
                            <div>
                                <div class="text-[9px] font-bold text-purple-400 uppercase mb-2 text-center">IN PORTA</div>
                                <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark mb-2">
                                <div class="grid grid-cols-2 gap-2"><input type="number" id="line-tp-h" value="4.5" class="input-dark text-xs"><input type="number" id="line-tp-a" value="3.5" class="input-dark text-xs"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </details>

            <button onclick="calculate()" class="w-full py-4 bg-blue-600 text-white font-black text-xl rounded-xl shadow-lg">ANALIZZA VALORE ⚡</button>
        </div>

        <div id="results" class="hidden">
            <div class="text-sm font-bold text-red-400 mb-3 uppercase mt-8" id="title-falli">🛑 Analisi Falli</div>
            <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8"></div>
            <div id="sec-tiri" class="hidden">
                <div class="text-sm font-bold text-blue-400 mb-3 uppercase mt-8">⚽ Tiri Totali</div>
                <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8"></div>
                <div class="text-sm font-bold text-purple-400 mb-3 uppercase mt-8">🎯 Tiri In Porta</div>
                <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
            </div>
        </div>
    </main>

    <script>
        const MASTER_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTR5vVYi1_EFk97GPmK8wOdZe6cImPcVYYEX-8rIlUyFg2EJjRspgcgBZ0cDAuVP--Aepi-wxEOdCOp/pub?output=csv";
        let CURRENT_LEAGUE = 'SERIE_A';
        const CONFIG = { SERIE_A: {}, LIGA: {} };
        const DB = { refs: [], fc: [], fp: [], tiri: [] };

        document.addEventListener('DOMContentLoaded', async () => {
            lucide.createIcons();
            await initMasterConfig();
        });

        async function initMasterConfig() {
            try {
                const r = await fetch(MASTER_URL + "&t=" + Date.now());
                const data = Papa.parse(await r.text(), { header: false }).data;
                const getL = (i) => (data[i] && data[i][1]) ? data[i][1].trim() : "";
                CONFIG.SERIE_A = { arb: getL(0), curr: getL(1), prev: getL(2), tiri: getL(3) };
                CONFIG.LIGA = { arb: getL(4), curr: getL(5), prev: getL(6), tiri: getL(7) };
                switchLeague('SERIE_A');
            } catch(e) { console.error(e); }
        }

        function switchLeague(l) {
            CURRENT_LEAGUE = l;
            document.getElementById('side-sa').className = l==='SERIE_A' ? "py-2 text-xs font-bold rounded-lg bg-blue-600 text-white" : "py-2 text-xs font-bold rounded-lg text-slate-400";
            document.getElementById('side-lg').className = l==='LIGA' ? "py-2 text-xs font-bold rounded-lg bg-blue-600 text-white" : "py-2 text-xs font-bold rounded-lg text-slate-400";
            document.getElementById('box-tiri-lines').style.display = l==='SERIE_A' ? 'block' : 'none';
            renderLinks(); loadData();
        }

        function renderLinks() {
            const L = CONFIG[CURRENT_LEAGUE];
            document.getElementById('links-container').innerHTML = `
                <div><label class="text-[9px] text-slate-500 font-bold">ARBITRI</label><input type="text" id="inp-arb" class="input-dark mt-1" value="${L.arb||''}"></div>
                <div><label class="text-[9px] text-slate-500 font-bold">FALLI 25/26</label><input type="text" id="inp-curr" class="input-dark mt-1" value="${L.curr||''}"></div>
                <div><label class="text-[9px] text-slate-500 font-bold">FALLI 24/25</label><input type="text" id="inp-prev" class="input-dark mt-1" value="${L.prev||''}"></div>
                <div><label class="text-[9px] text-slate-500 font-bold">TIRI</label><input type="text" id="inp-tiri" class="input-dark mt-1" value="${L.tiri||''}"></div>
            `;
        }
        
        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('open');
            document.getElementById('overlay').classList.toggle('open');
        }

        async function loadData() {
            document.getElementById('status-pill').innerHTML = `<div class="loader"></div>`;
            const L = CONFIG[CURRENT_LEAGUE];
            L.arb = document.getElementById('inp-arb').value; L.curr = document.getElementById('inp-curr').value;
            L.prev = document.getElementById('inp-prev').value; L.tiri = document.getElementById('inp-tiri').value;

            if(!L.arb || L.arb.length < 5) return;

            const fetchRaw = async (u) => { if(!u || u.length<5) return ""; const r = await fetch(u.includes('?') ? u+'&t='+Date.now() : u+'?t='+Date.now()); return await r.text(); };
            
            try {
                const [tA, tFc, tFp, tTr] = await Promise.all([ fetchRaw(L.arb), fetchRaw(L.curr), fetchRaw(L.prev), fetchRaw(L.tiri) ]);

                // ARBITRI
                const arbD = Papa.parse(tA, {header:false, skipEmptyLines:true}).data;
                let start=0; if(arbD[0] && arbD[0][0].includes('Arbitro')) start=1;
                DB.refs = arbD.slice(start).map(r => ({name:cleanStr(r[0]), avg:cleanNum(r[2])})).filter(x=>x.name.length>2);

                // FALLI
                const parseF = (txt) => {
                    if(!txt) return [];
                    const d = Papa.parse(txt, {header:false}).data;
                    let s=0; for(let i=0;i<5;i++) if(d[i] && d[i].join(' ').toUpperCase().includes('SQUADRA')) s=i+1;
                    return d.slice(s).map(r => ({Team:cleanStr(r[1]), Loc:(r[2]||"").toUpperCase(), Sub:cleanNum(r[3]), Comm:cleanNum(r[4])})).filter(x=>x.Team);
                };
                DB.fc = parseF(tFc); DB.fp = parseF(tFp);

                // TIRI
                DB.tiri = [];
                if(tTr && tTr.length>50) {
                    const rd = Papa.parse(tTr, {header:false}).data;
                    let si=-1; for(let i=0;i<20;i++) if(rd[i] && rd[i][0].includes("Squadra")) si=i;
                    if(si!==-1) {
                        DB.tiri = rd.slice(si+1).map(r => {
                            if(!r[0]) return null;
                            const pc = cleanNum(r[1])||1; const pf = cleanNum(r[6])||1;
                            return {
                                Team: cleanStr(r[0]),
                                TFC: cleanNum(r[2])/pc, TSC: cleanNum(r[3])/pc,
                                TFF: cleanNum(r[7])/pf, TSF: cleanNum(r[8])/pf,
                                TPC: cleanNum(r[4])/pc, TPSC: cleanNum(r[5])/pc,
                                TPF: cleanNum(r[9])/pf, TPSF: cleanNum(r[10])/pf
                            };
                        }).filter(x=>x);
                    }
                }

                updateSel();
                document.getElementById('status-pill').innerHTML = `<span class="text-green-400 font-bold">OK</span>`;
                document.getElementById('sidebar').classList.remove('open');
                document.getElementById('overlay').classList.remove('open');
            } catch(e) { console.error(e); }
        }

        function cleanNum(v) { return parseFloat(String(v).replace(',','.').replace('%','').trim())||0; }
        function cleanStr(v) { return String(v).trim().replace(/\*/g,''); }

        function updateSel() {
            const h = document.getElementById('home'), a = document.getElementById('away'), r = document.getElementById('referee');
            h.innerHTML=''; a.innerHTML=''; r.innerHTML='<option value="">Seleziona</option>';
            [...new Set(DB.fc.map(x=>x.Team))].sort().forEach(t => { h.add(new Option(t,t)); a.add(new Option(t,t)); });
            [...new Set(DB.refs.map(x=>x.name))].sort().forEach(n => r.add(new Option(n,n)));
        }

        function calculate() {
            const home = document.getElementById('home').value, away = document.getElementById('away').value, ref = document.getElementById('referee').value;
            if(!home || home===away) return alert("Seleziona squadre valide");

            // FALLI
            const getF = (t,loc,dc,dp) => {
                const c = dc.find(x=>x.Team===t && x.Loc.includes(loc)), p = dp.find(x=>x.Team===t && x.Loc.includes(loc));
                if(!c) return {c:0,s:0};
                return p ? {c:c.Comm*0.7+p.Comm*0.3, s:c.Sub*0.7+p.Sub*0.3} : {c:c.Comm, s:c.Sub};
            };
            const fH = getF(home,'CASA',DB.fc,DB.fp), fA = getF(away,'FUORI',DB.fc,DB.fp);
            const raw = ((fH.c+fA.s)/2) + ((fA.c+fH.s)/2);
            let mult = 1.0; const rf = DB.refs.find(x=>x.name===ref); if(rf && rf.avg>0) mult = rf.avg/24.5;
            
            renderBox('grid-falli', "MATCH", raw*mult, 'line-f-match');
            renderBox('grid-falli', home, ((fH.c+fA.s)/2)*mult, 'line-f-h');
            renderBox('grid-falli', away, ((fA.c+fH.s)/2)*mult, 'line-f-a');
            document.getElementById('title-falli').innerText = `🛑 Falli (Ref: ${mult.toFixed(2)}x)`;

            // TIRI
            const sec = document.getElementById('sec-tiri');
            if(CURRENT_LEAGUE==='SERIE_A' && DB.tiri.length) {
                const hT = DB.tiri.find(x=>x.Team.toUpperCase()===home.toUpperCase()), aT = DB.tiri.find(x=>x.Team.toUpperCase()===away.toUpperCase());
                if(hT && aT) {
                    sec.classList.remove('hidden');
                    // Totali (Incrocio)
                    const th = (hT.TFC + aT.TSF)/2, ta = (aT.TFF + hT.TSC)/2;
                    renderBox('grid-tiri', "MATCH", th+ta, 'line-t-match', true);
                    renderBox('grid-tiri', home, th, 'line-t-h', true);
                    renderBox('grid-tiri', away, ta, 'line-t-a', true);
                    
                    // Porta
                    const tph = (hT.TPC + aT.TPSF)/2, tpa = (aT.TPF + hT.TPSC)/2;
                    renderBox('grid-tp', "MATCH", tph+tpa, 'line-tp-match', true);
                    renderBox('grid-tp', home, tph, 'line-tp-h', true);
                    renderBox('grid-tp', away, tpa, 'line-tp-a', true);
                }
            } else { sec.classList.add('hidden'); }

            document.getElementById('results').classList.remove('hidden');
            setTimeout(()=>document.getElementById('results').scrollIntoView({behavior:'smooth'}), 100);
        }

        function renderBox(id, title, val, lineId, clear=false) {
            const el = document.getElementById(id);
            if(clear && title==="MATCH" && document.getElementById(lineId).value.includes("MATCH")) el.innerHTML=""; // Hacky clear
            if(title==="MATCH") el.innerHTML=""; 
            
            const line = parseFloat(document.getElementById(lineId).value);
            const diff = val - line;
            let c="val-low", t="NO VALUE", r="PASS";
            
            if(diff>=1.5) { c="val-high"; t="SUPER VALORE"; r=`OVER ${line}`; }
            else if(diff>=0.5) { c="val-med"; t="BUONO"; r=`OVER ${line}`; }
            else if(diff<=-1.5) { c="val-high"; t="SUPER VALORE"; r=`UNDER ${line}`; }
            else if(diff<=-0.5) { c="val-med"; t="BUONO"; r=`UNDER ${line}`; }

            el.innerHTML += `
                <div class="value-box ${c}">
                    <div class="lbl" style="font-size:10px; opacity:0.8">${title}</div>
                    <div class="res">${r}</div>
                    <div style="font-size:12px; font-weight:bold">AI: ${val.toFixed(2)} | ${t}</div>
                </div>`;
        }
    </script>
</body>
</html>
"""

# Visualizza l'HTML dentro Streamlit
components.html(html_code, height=1200, scrolling=True)
