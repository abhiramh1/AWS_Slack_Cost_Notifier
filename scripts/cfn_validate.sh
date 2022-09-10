#!/bin/bash

# http://blog.kablamo.org/2015/11/08/bash-tricks-eux/
set -uxo pipefail
cd "$(dirname "$0")/.." || exit 1

rc=0

while read -r -u10 file; do
  aws cloudformation validate-template --template-body "file://$(pwd)/${file}" >/dev/null || rc=$?
done 10< <(find ./cloudformation/templates -type f -iname '*.yml' -o -iname '*.yaml' -o -iname '*.json' -o -iname '*.template' -o -iname '*.cf')

exit $rc
