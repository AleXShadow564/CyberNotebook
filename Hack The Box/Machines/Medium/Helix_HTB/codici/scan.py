#!/usr/bin/env python3
from opcua import Client

URL = "opc.tcp://127.0.0.1:4840/helix/"
client = Client(URL)

try:
    client.connect()
    print("[+] Connesso a Helix! Recupero variabili...")
    
    # Puntiamo al nodo radice dell'impianto emerso nel comando precedente
    plant = client.get_node("ns=2;i=1")
    
    print("\n--- ELENCO VARIABILI DISPONIBILI ---")
    for child in plant.get_children():
        browse_name = child.get_browse_name().Name
        node_id = str(child)
        print(f"[*] Variabile: {browse_name} | NodeID Reale: {node_id}")
        
        # Se ci sono sotto-componenti nidificati, analizza il secondo livello
        try:
            for sub_child in child.get_children():
                sub_name = sub_child.get_browse_name().Name
                sub_id = str(sub_child)
                print(f"    └──> Sotto-nodo: {sub_name} | NodeID: {sub_id}")
        except Exception:
            pass

finally:
    client.disconnect()
    print("\n[*] Scansione terminata.")
