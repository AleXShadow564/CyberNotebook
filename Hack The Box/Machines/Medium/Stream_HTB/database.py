import requests
import argparse

def main():
    url="http://db.htb-airport.htb"
    utente='svc_events'
    password='Yl4aCgh4y2PnU'

    parser=argparse.ArgumentParser(description="tool per il Database della macchina Stream HTB")

    parser.add_argument("-q","--query",required=True,help="query per il database")

    argomenti=parser.parse_args()

    query=argomenti.query

    autenticazione=(utente,password)

    try:
        print("[+] invio query al database...")
        richiesta=requests.post(url=url,auth=autenticazione,data=query)
        if richiesta.status_code==200:
            print("[+] richiesta accettata")
            print(f"[+] codice risposta: {richiesta.status_code}")
            print(richiesta.text)
        else:
            print("[!] errore nella richiesta o codice risposta diverso da 200")
            print(f"[+] codice risposta: {richiesta.status_code}")
                        
    except:
        print("ERRORE TOOL")

if __name__=='__main__':
    main()