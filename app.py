<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ProBet AI - FINAL CONNECT</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Teko:wght@400;600&family=Inter:wght@400;600;700;800&display=swap');
        
        body { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #e2e8f0; }
        .teko { font-family: 'Teko', sans-serif; }
        
        /* Sidebar */
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

        /* Inputs */
        .input-dark {
            background: #1e293b; border: 1px solid #334155; color: white;
            padding: 8px; border-radius: 6px; width: 100%; outline: none; font-size: 0.85rem; font-weight: bold; text-align: center;
        }
        .input-dark:focus { border-color: #3b82f6; }

        select {
            background-color: #1e293b; color: white; border: 1px solid #334155; padding: 12px;
            border-radius: 8px; width: 100%; font-weight: bold; appearance: none;
            background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%233b82f6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
            background-repeat: no-repeat; background-position: right 0.7rem center; background-size: 1em;
        }

        /* --- VALUE BOX STYLES --- */
        .value-box {
            padding: 15px; border-radius: 12px; margin-bottom: 10px; text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2); font-family: sans-serif;
            border-width: 1px; border-style: solid;
        }
        .value-box:hover { transform: translateY(-2px); transition: transform 0.2s; }

        .val-high { background-color: #15803d; color: white; border-color: #22c55e; } 
        .val-med { background-color: #ca8a04; color: #ffffff; border-color: #facc15; } 
        .val-low { background-color: #b91c1c; color: white; border-color: #ef4444; } 

        .lbl { font-size: 12px; text-transform: uppercase; font-weight: 800; opacity: 0.8; letter-spacing: 1px; }
        .res { font-size: 26px; font-weight: 900; margin: 4px 0; font-family: 'Teko', sans-serif; letter-spacing: 1px; line-height: 1; }
        .dtl { font-size: 13px; font-weight: 600; display: inline-block; padding: 4px 10px; border-radius: 20px; background: rgba(0,0,0,0.2); margin-top: 5px; }

        /* Loader */
        .loader {
            width: 16px; height: 16px; border: 2px solid #475569; border-bottom-color: #3b82f6;
            border-radius: 50%; display: inline-block; animation: rotation 1s linear infinite;
        }
        @keyframes rotation { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body class="min-h-screen pb-20">

    <div id="overlay" class="overlay" onclick="toggleSidebar()"></div>
    <aside id="sidebar" class="sidebar shadow-2xl">
        <div class="flex justify-between items-center mb-6 border-b border-slate-800 pb-4">
            <h2 class="text-xl font-bold text-white flex items-center gap-2">
                <i data-lucide="settings-2" class="text-blue-500"></i> CONFIG
            </h2>
            <button onclick="toggleSidebar()"><i data-lucide="x" class="text-slate-400"></i></button>
        </div>

        <div class="mb-4">
            <label class="text-[10px] uppercase font-bold text-slate-500 mb-2 block tracking-widest">1. Campionato</label>
            <div class="grid grid-cols-2 bg-slate-900 p-1 rounded-xl border border-slate-800">
                <button onclick="switchLeague('SERIE_A')" id="side-sa" class="py-2.5 text-xs font-bold rounded-lg transition-all">SERIE A</button>
                <button onclick="switchLeague('LIGA')" id="side-lg" class="py-2.5 text-xs font-bold rounded-lg transition-all">LIGA</button>
            </div>
        </div>

        <div id="links-container" class="space-y-3">
            <h3 class="text-[10px] font-bold text-white uppercase border-b border-slate-700 pb-2">Link Rilevati (Master)</h3>
            </div>

        <button onclick="loadData()" class="w-full mt-6 py-3 bg-blue-600 hover:bg-blue-500 text-white font-bold rounded-xl shadow-lg shadow-blue-900/20 flex justify-center items-center gap-2 text-sm transition-all active:scale-95">
            <i data-lucide="refresh-cw" class="w-4 h-4"></i> RICARICA DATI
        </button>
    </aside>

    <header class="fixed top-0 w-full z-30 bg-[#0f172a]/95 backdrop-blur border-b border-slate-800">
        <div class="max-w-6xl mx-auto px-4 h-20 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <button onclick="toggleSidebar()" class="p-2 bg-slate-800 rounded-lg text-slate-400 hover:text-white transition-colors border border-slate-700"><i data-lucide="menu"></i></button>
                <div class="leading-none">
                    <div class="text-2xl font-bold teko tracking-wide text-white">PROBET <span class="text-blue-500">AI</span></div>
                    <div class="text-[10px] text-slate-500 font-bold tracking-[0.3em]">VERSIONE HTML</div>
                </div>
            </div>
            <div id="status-pill" class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 transition-all">
                <div class="loader"></div>
                <span class="text-[10px] font-bold text-slate-400">CONNESSIONE...</span>
            </div>
        </div>
    </header>

    <main class="pt-24 px-4 max-w-6xl mx-auto space-y-6">

        <div class="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-2xl">
            
            <div class="flex justify-center mb-6">
                <div class="bg-slate-950 p-1 rounded-xl border border-slate-800 flex gap-2 w-full max-w-sm">
                    <button onclick="switchLeague('SERIE_A')" id="btn-sa" class="flex-1 py-2 text-sm font-bold rounded-lg transition-all text-center">🇮🇹 SERIE A</button>
                    <button onclick="switchLeague('LIGA')" id="btn-lg" class="flex-1 py-2 text-sm font-bold rounded-lg transition-all text-center">🇪🇸 LIGA</button>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                    <label class="text-[10px] font-bold text-slate-500 uppercase ml-1">CASA</label>
                    <select id="home" class="mt-1"><option>Caricamento...</option></select>
                </div>
                <div>
                    <label class="text-[10px] font-bold text-slate-500 uppercase ml-1">OSPITE</label>
                    <select id="away" class="mt-1"><option>Caricamento...</option></select>
                </div>
                <div>
                    <label class="text-[10px] font-bold text-slate-500 uppercase ml-1">ARBITRO</label>
                    <select id="referee" class="mt-1 text-yellow-400"><option>Caricamento...</option></select>
                </div>
            </div>

            <hr class="border-slate-800 my-5">

            <details class="group bg-black/20 p-4 rounded-xl border border-slate-800/50 mb-5" open>
                <summary class="flex justify-between items-center cursor-pointer font-bold text-slate-400 text-xs uppercase mb-2">
                    <span class="flex items-center gap-2"><i data-lucide="edit-3" class="w-3 h-3"></i> Quote Bookmaker</span>
                    <i data-lucide="chevron-down" class="w-4 h-4 transition-transform group-open:rotate-180"></i>
                </summary>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3">
                    <div class="bg-slate-950 p-3 rounded-lg border border-slate-800">
                        <div class="text-[9px] font-bold text-red-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">LINEE FALLI</div>
                        <div class="mb-2">
                            <label class="text-[8px] text-slate-500 block text-center">MATCH TOTALI</label>
                            <input type="number" id="line-f-match" value="24.5" step="0.5" class="input-dark text-center font-bold text-lg text-white">
                        </div>
                        <div class="grid grid-cols-2 gap-2">
                            <input type="number" id="line-f-h" value="11.5" step="0.5" class="input-dark text-xs" placeholder="Casa">
                            <input type="number" id="line-f-a" value="11.5" step="0.5" class="input-dark text-xs" placeholder="Ospite">
                        </div>
                    </div>
                    
                    <div id="box-tiri-lines" class="bg-slate-950 p-3 rounded-lg border border-slate-800 md:col-span-2 hidden">
                        <div class="grid grid-cols-2 gap-4 h-full">
                            <div>
                                <div class="text-[9px] font-bold text-blue-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">LINEE TIRI TOTALI</div>
                                <div class="mb-2">
                                    <label class="text-[8px] text-slate-500 block text-center">MATCH</label>
                                    <input type="number" id="line-t-match" value="23.5" step="0.5" class="input-dark text-center text-white font-bold">
                                </div>
                                <div class="grid grid-cols-2 gap-2">
                                    <input type="number" id="line-t-h" value="12.5" step="0.5" class="input-dark text-center text-xs text-slate-300">
                                    <input type="number" id="line-t-a" value="10.5" step="0.5" class="input-dark text-center text-xs text-slate-300">
                                </div>
                            </div>
                            <div class="border-l border-slate-800 pl-4">
                                <div class="text-[9px] font-bold text-purple-400 uppercase mb-2 text-center border-b border-slate-800 pb-1">LINEE IN PORTA</div>
                                <div class="mb-2">
                                    <label class="text-[8px] text-slate-500 block text-center">MATCH</label>
                                    <input type="number" id="line-tp-match" value="8.5" step="0.5" class="input-dark text-center text-white font-bold">
                                </div>
                                <div class="grid grid-cols-2 gap-2">
                                    <input type="number" id="line-tp-h" value="4.5" step="0.5" class="input-dark text-center text-xs text-slate-300">
                                    <input type="number" id="line-tp-a" value="3.5" step="0.5" class="input-dark text-center text-xs text-slate-300">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </details>

            <button onclick="calculate()" class="w-full py-4 bg-gradient-to-r from-blue-600 to-blue-500 hover:from-blue-500 hover:to-blue-400 text-white font-black text-xl tracking-wide rounded-xl shadow-[0_0_20px_rgba(59,130,246,0.3)] active:scale-95 transition-transform flex justify-center items-center gap-2">
                <i data-lucide="zap" class="w-5 h-5 fill-white"></i> ANALIZZA VALORE
            </button>
        </div>

        <div id="results" class="hidden pb-20">
            
            <div class="text-sm font-bold text-red-400 mb-3 border-b border-slate-800 pb-1 uppercase tracking-widest mt-8 flex items-center gap-2">
                <i data-lucide="alert-circle" class="w-4 h-4"></i> <span id="title-falli">Analisi Falli</span>
            </div>
            <div id="grid-falli" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8"></div>

            <div id="sec-tiri" class="hidden">
                <div class="text-sm font-bold text-blue-400 mb-3 border-b border-slate-800 pb-1 uppercase tracking-widest mt-8 flex items-center gap-2">
                    <i data-lucide="crosshair" class="w-4 h-4"></i> ⚽ Analisi Tiri Totali
                </div>
                <div id="grid-tiri" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8"></div>
                
                <div class="text-sm font-bold text-purple-400 mb-3 border-b border-slate-800 pb-1 uppercase tracking-widest mt-8 flex items-center gap-2">
                    <i data-lucide="target" class="w-4 h-4"></i> 🎯 Analisi Tiri In Porta
                </div>
                <div id="grid-tp" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
            </div>

        </div>
    </main>

    <script>
        // --- MASTER CONFIG ---
        const MASTER_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTR5vVYi1_EFk97GPmK8wOdZe6cImPcVYYEX-8rIlUyFg2EJjRspgcgBZ0cDAuVP--Aepi-wxEOdCOp/pub?output=csv";
        
        let CURRENT_LEAGUE = 'SERIE_A';
        const CONFIG = {
            SERIE_A: { arb: "", curr: "", prev: "", tiri: "" },
            LIGA: { arb: "", curr: "", prev: "", tiri: "" }
        };
        const DB = { refs: [], fc: [], fp: [], tiri: [] };

        // --- INIT ---
        document.addEventListener('DOMContentLoaded', async () => {
            lucide.createIcons();
            await initMasterConfig();
        });

        // 1. CARICAMENTO CONFIG MASTER
        async function initMasterConfig() {
            const status = document.getElementById('status-pill');
            
            try {
                const response = await fetch(MASTER_URL + "&t=" + Date.now());
                const csvText = await response.text();
                const data = Papa.parse(csvText, { header: false, skipEmptyLines: true }).data;

                const getLink = (idx) => (data[idx] && data[idx][1]) ? data[idx][1].trim() : "";

                CONFIG.SERIE_A = { arb: getLink(0), curr: getLink(1), prev: getLink(2), tiri: getLink(3) };
                CONFIG.LIGA = { arb: getLink(4), curr: getLink(5), prev: getLink(6), tiri: getLink(7) };

                status.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500"></span><span class="text-emerald-400">CONFIG OK</span>`;
                status.className = "flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-900/30 border border-emerald-500/30";
                
                switchLeague('SERIE_A'); 

            } catch (e) {
                console.error(e);
                status.innerHTML = `<span class="text-red-400">MASTER ERROR</span>`;
            }
        }

        // 2. LEAGUE SWITCH
        function switchLeague(l) {
            CURRENT_LEAGUE = l;
            const btnSa = document.getElementById('side-sa');
            const btnLg = document.getElementById('side-lg');
            const mainBtnSa = document.getElementById('btn-sa');
            const mainBtnLg = document.getElementById('btn-lg');
            const boxTiri = document.getElementById('box-tiri-lines');
            
            // Aggiorna UI Bottoni
            const activeClass = "bg-blue-600 text-white shadow-lg";
            const inactiveClass = "text-slate-400 hover:bg-slate-800";

            if (l === 'SERIE_A') {
                btnSa.className = `flex-1 py-2 text-sm font-bold rounded-lg transition-all ${activeClass}`;
                btnLg.className = `flex-1 py-2 text-sm font-bold rounded-lg transition-all ${inactiveClass}`;
                mainBtnSa.className = `flex-1 py-2 text-sm font-bold rounded-lg transition-all ${activeClass}`;
                mainBtnLg.className = `flex-1 py-2 text-sm font-bold rounded-lg transition-all ${inactiveClass}`;
                boxTiri.classList.remove('hidden');
            } else {
                btnLg.className = `flex-1 py-2 text-sm font-bold rounded-lg transition-all ${activeClass}`;
                btnSa.className = `flex-1 py-2 text-sm font-bold rounded-lg transition-all ${inactiveClass}`;
                mainBtnLg.className = `flex-1 py-2 text-sm font-bold rounded-lg transition-all ${activeClass}`;
                mainBtnSa.className = `flex-1 py-2 text-sm font-bold rounded-lg transition-all ${inactiveClass}`;
                boxTiri.classList.add('hidden');
            }
            
            renderLinksInputs();
            loadData();
        }

        function renderLinksInputs() {
            const container = document.getElementById('links-container');
            const L = CONFIG[CURRENT_LEAGUE];
            
            container.innerHTML = `
                <div><label class="text-[9px] text-slate-500 font-bold uppercase">Arbitri</label><input type="text" id="inp-arb" class="input-dark mt-1" value="${L.arb || ''}"></div>
                <div><label class="text-[9px] text-slate-500 font-bold uppercase">Falli 25/26</label><input type="text" id="inp-curr" class="input-dark mt-1" value="${L.curr || ''}"></div>
                <div><label class="text-[9px] text-slate-500 font-bold uppercase">Falli 24/25</label><input type="text" id="inp-prev" class="input-dark mt-1" value="${L.prev || ''}"></div>
                <div><label class="text-[9px] text-slate-500 font-bold uppercase">Tiri</label><input type="text" id="inp-tiri" class="input-dark mt-1" value="${L.tiri || ''}"></div>
            `;
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('open');
            document.getElementById('overlay').classList.toggle('open');
        }

        // 3. LOAD DATA (BLINDATO v34)
        async function loadData() {
            const status = document.getElementById('status-pill');
            status.innerHTML = `<div class="loader"></div><span class="text-blue-400">LOADING...</span>`;
            
            // Aggiorna config
            CONFIG[CURRENT_LEAGUE].arb = document.getElementById('inp-arb').value;
            CONFIG[CURRENT_LEAGUE].curr = document.getElementById('inp-curr').value;
            CONFIG[CURRENT_LEAGUE].prev = document.getElementById('inp-prev').value;
            CONFIG[CURRENT_LEAGUE].tiri = document.getElementById('inp-tiri').value;

            const L = CONFIG[CURRENT_LEAGUE];
            if (!L.arb || L.arb.length < 10) { 
                status.innerHTML = `<span class="text-orange-400">NO LINKS</span>`; 
                return; 
            }

            try {
                const fetchRaw = async (url) => {
                    if(!url || url.length < 5) return "";
                    const safe = url.includes('?') ? `${url}&t=${Date.now()}` : `${url}?t=${Date.now()}`;
                    const r = await fetch(safe);
                    return await r.text();
                };

                const [txtArb, txtFc, txtFp, txtTiri] = await Promise.all([
                    fetchRaw(L.arb), fetchRaw(L.curr), fetchRaw(L.prev), fetchRaw(L.tiri)
                ]);

                // --- 1. ARBITRI (Posizionale Col 0 e Col 2) ---
                DB.refs = [];
                const arbData = Papa.parse(txtArb, { header: false, skipEmptyLines: true }).data;
                
                let arbStart = 0;
                if(arbData.length > 0 && (arbData[0][0].includes("Arbitro") || arbData[0][0].includes("Media"))) arbStart = 1;

                DB.refs = arbData.slice(arbStart).map(row => {
                    if (!row[0] || !row[2]) return null;
                    return {
                        name: cleanStr(row[0]),
                        avg: cleanNum(row[2])
                    };
                }).filter(x => x && x.name.length > 2);

                // --- 2. FALLI (Forza prime 5 colonne) ---
                const parseF = (csvText) => {
                    if(!csvText) return [];
                    const data = Papa.parse(csvText, { header: false, skipEmptyLines: true }).data;
                    let start = 0;
                    for(let i=0; i<Math.min(5, data.length); i++) {
                        if(data[i].join(' ').toUpperCase().includes('SQUADRA')) { start = i + 1; break; }
                    }
                    return data.slice(start).map(row => ({
                        Team: cleanStr(row[1]),
                        Loc: (row[2]||"").toUpperCase(),
                        Sub: cleanNum(row[3]),
                        Comm: cleanNum(row[4])
                    })).filter(x => x && x.Team);
                };
                
                DB.fc = parseF(txtFc);
                DB.fp = parseF(txtFp);

                // --- 3. TIRI (MAPPATURA v39/40) ---
                DB.tiri = [];
                if (txtTiri && txtTiri.length > 50) {
                    const rawData = Papa.parse(txtTiri, { header: false, skipEmptyLines: true }).data;
                    let startIdx = -1;
                    for(let i=0; i<Math.min(20, rawData.length); i++) {
                        const cell = (rawData[i][0] || "").toString();
                        if(cell.includes("Squadra")) { startIdx = i; break; }
                    }

                    if(startIdx !== -1) {
                        // Mapping ESATTO come da Versione Python 40
                        // 0:Sq, 1:PC, 2:TFC, 3:TSC, 4:TPFC, 5:TPSC, 6:PF, 7:TFF, 8:TSF, 9:TPFF, 10:TPSF
                        DB.tiri = rawData.slice(startIdx + 1).map(row => {
                            if(!row[0]) return null;
                            const pC = cleanNum(row[1]) || 1; 
                            const pF = cleanNum(row[6]) || 1; // Colonna G
                            return {
                                Team: cleanStr(row[0]),
                                // Totali
                                TF_C: cleanNum(row[2])/pC, TS_C: cleanNum(row[3])/pC,
                                TF_F: cleanNum(row[7])/pF, TS_F: cleanNum(row[8])/pF,
                                // Porta
                                TP_C: cleanNum(row[4])/pC, TPS_C: cleanNum(row[5])/pC,
                                TP_F: cleanNum(row[9])/pF, TPS_F: cleanNum(row[10])/pF
                            };
                        }).filter(x => x);
                    }
                }

                updateSelectors();
                status.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500"></span><span class="text-emerald-400">READY</span>`;
                
                document.getElementById('sidebar').classList.remove('open');
                document.getElementById('overlay').classList.remove('open');
                
                // Aggiorna le icone Lucide
                lucide.createIcons();

            } catch (e) {
                console.error(e);
                status.innerHTML = `<span class="text-red-400">ERROR</span>`;
                alert("Errore caricamento dati. Controlla i link.");
            }
        }

        function cleanNum(v) { return parseFloat(String(v).replace(',','.').replace('%','').trim()) || 0; }
        function cleanStr(v) { return String(v).trim().replace(/\*/g,''); }

        function updateSelectors() {
            const h = document.getElementById('home');
            const a = document.getElementById('away');
            const r = document.getElementById('referee');
            h.innerHTML = ''; a.innerHTML = ''; r.innerHTML = '<option value="">Seleziona Arbitro</option>';

            const teams = [...new Set(DB.fc.map(x => x.Team))].sort();
            teams.forEach(t => { if(t) { h.add(new Option(t,t)); a.add(new Option(t,t)); } });
            
            const refs = [...new Set(DB.refs.map(x => x.name))].sort();
            refs.forEach(rf => r.add(new Option(rf,rf))); 
        }

        // --- 4. CALCOLO E RENDER ---
        function calculate() {
            const home = document.getElementById('home').value;
            const away = document.getElementById('away').value;
            const refName = document.getElementById('referee').value;
            
            const lf_m = parseFloat(document.getElementById('line-f-match').value);
            const lf_h = parseFloat(document.getElementById('line-f-h').value);
            const lf_a = parseFloat(document.getElementById('line-f-a').value);

            if(!home || !away || home === "Caricamento...") return alert("Attendi il caricamento dati.");
            if(home === away) return alert("Seleziona squadre diverse.");

            // A. FALLI
            const getF = (t, loc, dc, dp) => {
                const c = dc.find(x => x.Team === t && x.Loc.includes(loc));
                const p = dp.find(x => x.Team === t && x.Loc.includes(loc));
                if(!c) return { c:0, s:0 };
                const cv = {c:c.Comm, s:c.Sub};
                if(!p) return cv;
                return { c: cv.c*0.7 + p.Comm*0.3, s: cv.s*0.7 + p.Sub*0.3 };
            };

            const fH = getF(home, 'CASA', DB.fc, DB.fp);
            const fA = getF(away, 'FUORI', DB.fc, DB.fp);

            const rawH = (fH.c + fA.s)/2;
            const rawA = (fA.c + fH.s)/2;
            const rawTot = rawH + rawA;
            
            let refMult = 1.0;
            if(refName) {
                const r = DB.refs.find(x => x.name === refName);
                if(r && r.avg > 0) refMult = r.avg / 24.5;
            }

            const predF_Tot = rawTot * refMult;
            const predF_H = rawH * refMult;
            const predF_A = rawA * refMult;

            // RENDER FALLI
            const gf = document.getElementById('grid-falli');
            if (gf) {
                gf.innerHTML = "";
                gf.innerHTML += renderValueBox("MATCH TOTALE", predF_Tot, lf_m);
                gf.innerHTML += renderValueBox(home, predF_H, lf_h);
                gf.innerHTML += renderValueBox(away, predF_A, lf_a);
            }
            
            document.getElementById('title-falli').innerText = ` ANALISI FALLI (Ref: ${refMult.toFixed(2)}x)`;

            // B. TIRI
            const secTiri = document.getElementById('sec-tiri');
            if (secTiri) secTiri.classList.add('hidden');

            if(CURRENT_LEAGUE === 'SERIE_A' && DB.tiri.length) {
                const hT = DB.tiri.find(x => x.Team.toUpperCase() === home.toUpperCase());
                const aT = DB.tiri.find(x => x.Team.toUpperCase() === away.toUpperCase());
                
                if(hT && aT) {
                    if (secTiri) secTiri.classList.remove('hidden');
                    
                    const lt_m = parseFloat(document.getElementById('line-t-match').value);
                    const lt_h = parseFloat(document.getElementById('line-t-h').value);
                    const lt_a = parseFloat(document.getElementById('line-t-a').value);
                    const ltp_m = parseFloat(document.getElementById('line-tp-match').value);
                    const ltp_h = parseFloat(document.getElementById('line-tp-h').value);
                    const ltp_a = parseFloat(document.getElementById('line-tp-a').value);

                    // Cross: Attacco Casa vs Difesa Ospite (FORMULA v40)
                    const th = (hT.TF_C + aT.TS_F)/2;
                    const ta = (aT.TF_F + hT.TS_C)/2;
                    
                    const gt = document.getElementById('grid-tiri');
                    if (gt) {
                        gt.innerHTML = "";
                        gt.innerHTML += renderValueBox("MATCH TOT", th+ta, lt_m);
                        gt.innerHTML += renderValueBox(home, th, lt_h);
                        gt.innerHTML += renderValueBox(away, ta, lt_a);
                    }

                    const tph = (hT.TP_C + (aT.TPS_F || aT.TF_F*0.3))/2;
                    const tpa = (aT.TP_F + (hT.TPS_C || hT.TF_C*0.3))/2;

                    const gtp = document.getElementById('grid-tp');
                    if (gtp) {
                        gtp.innerHTML = "";
                        gtp.innerHTML += renderValueBox("MATCH TP", tph+tpa, ltp_m);
                        gtp.innerHTML += renderValueBox(home, tph, ltp_h);
                        gtp.innerHTML += renderValueBox(away, tpa, ltp_a);
                    }
                }
            }

            const resDiv = document.getElementById('results');
            if (resDiv) {
                resDiv.classList.remove('hidden');
                setTimeout(() => resDiv.scrollIntoView({behavior:'smooth'}), 100);
            }
        }

        function renderValueBox(title, predicted, line) {
            const diff = predicted - line;
            let cls = "val-low";
            let lbl = "NO VALUE / RISCHIO";
            let adv = "PASS";

            if (diff >= 1.5) {
                cls = "val-high"; lbl = "💎 SUPER VALORE"; adv = `OVER ${line}`;
            } else if (diff >= 0.5) {
                cls = "val-med"; lbl = "⚖️ BUON VALORE"; adv = `OVER ${line}`;
            } else if (diff <= -1.5) {
                cls = "val-high"; lbl = "💎 SUPER VALORE"; adv = `UNDER ${line}`;
            } else if (diff <= -0.5) {
                cls = "val-med"; lbl = "⚖️ BUON VALORE"; adv = `UNDER ${line}`;
            }

            return `
                <div class="value-box ${cls}">
                    <div class="lbl">${title} (Prev: ${predicted.toFixed(2)})</div>
                    <div class="res">${adv}</div>
                    <div class="dtl">${lbl} (Diff: ${Math.abs(diff).toFixed(2)})</div>
                </div>
            `;
        }

    </script>
</body>
</html>      
