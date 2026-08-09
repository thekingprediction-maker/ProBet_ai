from playwright.sync_api import sync_playwright

# SOSTITUISCI questo con l'indirizzo VERO della tua app Streamlit ufficiale
APP_URL = "https://probetai-7xsu6hzmlwqzsmcgtxphcs.streamlit.app"


def wake_app():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        print(f"Visito {APP_URL} ...")
        page.goto(APP_URL, timeout=60000)
        page.wait_for_timeout(5000)  # aspetta 5 secondi che la pagina si carichi

        try:
            # Se l'app era addormentata, compare un pulsante per risvegliarla
            wake_button = page.get_by_text("get this app back up", exact=False)
            if wake_button.count() > 0:
                print("App addormentata, clicco il pulsante di risveglio...")
                wake_button.first.click()
                page.wait_for_timeout(20000)  # aspetta che l'app si risvegli davvero
                print("App risvegliata con successo.")
            else:
                print("App gia' attiva, nessun risveglio necessario.")
        except Exception as e:
            print(f"Nota (non bloccante): {e}")

        browser.close()


if __name__ == "__main__":
    wake_app()
