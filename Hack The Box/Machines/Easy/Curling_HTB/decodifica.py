import os
import gzip
import bz2
import tarfile
import re

HEX_FILE = "esadecimale.txt"

def parse_hex_dump(filepath):
    """
    Legge il dump esadecimale stile xxd e lo riconverte in byte grezzi.
    Usa una regex per catturare solo i blocchi esadecimali validi.
    """
    binary_data = bytearray()
    print(f"[*] Lettura e conversione di {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            # Rimuove l'offset iniziale (es. 00000000:) se presente
            if ":" in line:
                line = line.split(":", 1)[1]
            
            # Trova solo i blocchi esadecimali composti da 2 a 4 caratteri (es. 425a o f53e)
            # Si ferma prima di toccare la sezione ASCII sulla destra
            hex_blocks = re.findall(r'\b[0-9a-fA-F]{2,4}\b', line)
            
            for block in hex_blocks:
                # Se un blocco è dispari per errore, lo salta per evitare crash
                if len(block) % 2 != 0:
                    continue
                binary_data.extend(bytes.fromhex(block))
    
    return bytes(binary_data)

def get_data_type(data):
    """Rileva il tipo di compressione analizzando i Magic Bytes in memoria."""
    if data.startswith(b'BZh'):
        return "bzip2"
    elif data.startswith(b'\x1f\x8b'):
        return "gzip"
    elif data.startswith(b'\x75\x73\x74\x61\x72') or (len(data) > 262 and data[257:262] == b'ustar'):
        return "tar"
    
    # Prova a decodificare come testo ASCII/UTF-8
    try:
        decoded = data.decode('utf-8')
        if all(c.isprintable() or c in "\n\r\t" for c in decoded[:20]):
            return "text"
    except UnicodeDecodeError:
        pass
        
    return "unknown"

def main():
    if not os.path.exists(HEX_FILE):
        print(f"[-] Errore: Il file '{HEX_FILE}' non esiste nella directory corrente.")
        return

    try:
        current_data = parse_hex_dump(HEX_FILE)
    except Exception as e:
        print(f"[-] Errore nel parsing dell'esadecimale: {e}")
        return

    print("[*] Inizio decompressione dinamica in memoria...")
    
    ciclo = 1
    while True:
        data_type = get_data_type(current_data)
        print(f"    [Strato {ciclo}] Tipo rilevato: {data_type.upper()}")
        
        if data_type == "bzip2":
            try:
                current_data = bz2.decompress(current_data)
            except Exception as e:
                print(f"[-] Errore durante la decompressione BZIP2: {e}")
                break
                
        elif data_type == "gzip":
            try:
                current_data = gzip.decompress(current_data)
            except Exception as e:
                print(f"[-] Errore durante la decompressione GZIP: {e}")
                break
                
        elif data_type == "tar":
            try:
                import io
                with tarfile.open(fileobj=io.BytesIO(current_data), mode='r') as tar:
                    members = tar.getmembers()
                    if not members:
                        print("[-] Archivio TAR vuoto.")
                        break
                    current_data = tar.extractfile(members[0]).read()
            except Exception as e:
                print(f"[-] Errore durante l'estrazione del TAR: {e}")
                break
                
        elif data_type == "text":
            print("\n[+] Matrioska distrutta con successo!")
            print("-" * 50)
            print(current_data.decode('utf-8').strip())
            print("-" * 50)
            break
            
        else:
            print("[-] Formato sconosciuto o dati corrotti. Fine del ciclo.")
            try:
                print(f"Contenuto grezzo finale: {current_data.decode('utf-8', errors='ignore')}")
            except:
                pass
            break
            
        ciclo += 1

if __name__ == "__main__":
    main()
