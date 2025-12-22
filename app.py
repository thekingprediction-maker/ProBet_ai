import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ProBet AI Debug", layout="wide", initial_sidebar_state="collapsed")

# CSS per forzare tutto a schermo intero
st.markdown("""
    <style>
    .block-container { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
    iframe { width: 100vw !important; height: 100vh !important; display: block !important; }
    div[data-testid="stHeader"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>ProBet AI Debug</title>
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.4.1/papaparse.min.js"></script>
<style>
  body { background-color: #0f172a; color: white; font-family: sans-serif; padding: 20px; }
  .debug-box { background: #330000; border: 1px solid red; color: #ffcccc; padding: 15px; margin-bottom: 20px; font-family: monospace; white-space: pre-wrap; font-size: 12px; }
  .success-box { background: #003300; border: 1px solid lime; color: #ccffcc; padding: 15px; margin-bottom: 20px; }
</style>
</head>
<body>

  <h2 class="text-xl font-bold mb-4">MODALITÀ DEBUG</h2>
  
  <div id="log-container"></div>

  <div class="bg-slate-800 p-4 rounded-lg">
    <h3 class="font-bold text-blue-400">Stato Caricamento:</h3>
    <ul id="status-list" class="list-disc ml-5 mt-2 text-sm text-slate-300">
        <li>In attesa...</li>
    </ul>
  </div>

  <script>
    // --- IL TUO LINK ---
    const MASTER_URL = "https://raw.githubusercontent.com/thekingprediction-maker/Server_probetai/refs/heads/main/CONFIG_APP%20-%20Foglio1.csv";
    
    function log(msg, type='info') {
        const div = document.createElement('div');
        div.className = type === 'error' ? 'debug-box' : 'success-box';
        div.innerHTML = `<strong>${type.toUpperCase()}:</strong> ${msg}`;
        document.getElementById('log-container').appendChild(div);
    }

    function addStatus(msg) {
        const li = document.createElement('li');
        li.textContent = msg;
        document.getElementById('status-list').appendChild(li);
    }

    document.addEventListener('DOMContentLoaded', async () => {
        try {
            addStatus("Provo a scaricare il Config App...");
            
            // 1. Scarica il Config
            const response = await fetch(MASTER_URL + "?t=" + Date.now());
            if (!response.ok) throw new Error("Errore HTTP Config: " + response.status);
            
            const text = await response.text();
            addStatus("Config scaricato! Lunghezza: " + text.length + " caratteri.");
            
            if(text.includes("<!DOCTYPE html>")) {
                log("ERRORE GRAVE: Il link del Config punta a una pagina WEB, non al file RAW (CSV).", "error");
                return;
            }

            // 2. Prova a leggerlo
            const data = Papa.parse(text, { header: false, skipEmptyLines: true }).data;
            log("Contenuto Config letto (prime righe):\n" + JSON.stringify(data.slice(0,3), null, 2), "info");

            // 3. Verifica i link interni
            const linkArbitri = (data[0] && data[0][1]) ? data[0][1].trim() : "NON TROVATO";
            addStatus("Link Arbitri trovato: " + linkArbitri.substring(0, 30) + "...");

            if (!linkArbitri.startsWith("http")) {
                log("ERRORE: Il link degli arbitri nel CSV non sembra un URL valido.", "error");
                return;
            }

            // 4. Prova a scaricare il primo file (Arbitri)
            addStatus("Provo a scaricare file Arbitri...");
            const arbRes = await fetch(linkArbitri);
            if (!arbRes.ok) throw new Error("Errore scaricamento Arbitri: " + arbRes.status);
            const arbText = await arbRes.text();
            
            if(arbText.includes("<!DOCTYPE html>")) {
                log("ERRORE GRAVE: Il link DENTRO il file config (quello degli arbitri) non è un link RAW. Punta alla pagina web.", "error");
            } else {
                log("SUCCESS! File Arbitri scaricato correttamente. Il sistema dovrebbe funzionare.", "success");
                addStatus("Tutto sembra OK. Se l'app principale non va, il problema è nel codice dell'interfaccia, non nei dati.");
            }

        } catch (e) {
            log("ERRORE DI SISTEMA: " + e.message, "error");
        }
    });
  </script>
</body>
</html>
"""

components.html(html_code, height=800, scrolling=True)
