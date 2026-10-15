#!/bin/bash

set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

recipes=(
  ".:nats.c/3.4.0"
)

login=$(aws secretsmanager get-secret-value --region ap-southeast-2 --secret-id prod/conan --query SecretString --output text)
CONAN_LOGIN_USERNAME=$(python3 -c 'import json, sys; print(json.loads(sys.argv[1])["username"])' "$login")
CONAN_PASSWORD=$(python3 -c 'import json, sys; print(json.loads(sys.argv[1])["password"])' "$login")
unset login
export CONAN_LOGIN_USERNAME CONAN_PASSWORD

docker run --rm --network host \
  -e CONAN_LOGIN_USERNAME -e CONAN_PASSWORD \
  -v "$PWD":/recipes -w /recipes \
  rockylinux:9.3 \
  bash -c 'set -euo pipefail
    dnf -y -q install python3-pip
    pip3 install --quiet --no-cache-dir conan==1.60.0
    conan remote add staconan http://conan.sys.trade:9300
    for recipe in "$@"; do
      conan export "${recipe%%:*}" "${recipe#*:}@"
      conan upload "${recipe#*:}" --remote staconan --confirm
    done' publish "${recipes[@]}"
