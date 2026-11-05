from opcua import Client

url = "opc.tcp://127.0.0.1:4840/helix/"
client = Client(url)

try:
    client.connect()
    print("[+] Connesso con successo a Helix OPC UA!")
    
    # Esplora la cartella principale degli oggetti per visualizzare i nodi dei Control Systems
    root = client.get_root_node()
    objects = client.get_objects_node()
    print("Nodi disponibili sotto Objects:")
    for child in objects.get_children():
        print(f" - Nome: {child.get_browse_name()}, ID: {child}")
finally:
    client.disconnect()
