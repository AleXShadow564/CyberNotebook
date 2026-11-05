import asyncio
from asyncua import Client, ua

async def main():
    url = "opc.tcp://127.0.0.1:4840/helix"
    
    print("[*] Connessione al server OPC UA di Helix...")
    async with Client(url=url) as client:
        print("[+] Connesso!")
        
        # Mappatura REALE dei nodi basata sulla scansione
        mode_node = client.get_node("ns=2;i=12")
        test_override_node = client.get_node("ns=2;i=13")
        calibration_offset_node = client.get_node("ns=2;i=6")
        trip_active_node = client.get_node("ns=2;i=10")
        temperature_node = client.get_node("ns=2;i=4") # <--- AGGIORNATO

        # 1. Configurazione dello stato iniziale
        print("[*] Impostazione Mode su 'MAINTENANCE'...")
        await mode_node.write_value("MAINTENANCE", ua.VariantType.String)
        
        print("[*] Abilitazione di TestOverride su TRUE...")
        await test_override_node.write_value(True, ua.VariantType.Boolean)
        
        # 2. Controllo iniziale per sicurezza
        trip_status = await trip_active_node.get_value()
        if trip_status:
            print("[X] Errore: Il reattore è già in TRIP. Resetta il lab prima di continuare.")
            return

        current_temp = await temperature_node.get_value()
        print(f"[+] Temperatura iniziale rilevata: {current_temp}°C")

        # 3. Ramping graduale dell'offset
        print("[*] Avvio ramping controllato del CalibrationOffset...")
        current_offset = 0.0
        target_temp = 295.0       # Soglia per aprire la finestra
        max_safety_temp = 304.0   # Evitiamo i 305°C (Trip)

        while True:
            current_temp = await temperature_node.get_value()
            trip_status = await trip_active_node.get_value()

            if trip_status:
                print("[X] CRITICO: Il PLC è andato in TRIP! Ramping fallito.")
                return

            print(f"[>] Offset: {current_offset:.1f} | Temperatura Reattore: {current_temp:.1f}°C")

            # Verifica se siamo entrati nella finestra manutentiva
            if target_temp <= current_temp < max_safety_temp:
                print("\n[+++] FINESTRA MANUTENTIVA RAGGIUNTA E STABILIZZATA!")
                print("[!] Il file /opt/helix/state/maintenance_window è ora attivo.")
                print("[*] Mantengo lo script in esecuzione per bloccare la finestra APERTA.")
                print("[*] APRI UN ALTRO TERMINALE SSH E LANCIA SUBITO:")
                print("    /usr/local/sbin/helix-maint-console\n")
                
                # Ciclo infinito di mantenimento
                while True:
                    await asyncio.sleep(2)
            
            if current_temp >= max_safety_temp:
                print("[X] Attenzione: Temperatura troppo alta, rischio Trip. Blocco preventivo.")
                return

            # Incrementiamo l'offset un po' alla volta per non allarmare il PLC
            current_offset += 1.0 
            await calibration_offset_node.write_value(current_offset, ua.VariantType.Double)
            
            # Pausa per dare tempo al PLC di elaborare la fisica interna
            await asyncio.sleep(0.3)

if __name__ == "__main__":
    asyncio.run(main())
