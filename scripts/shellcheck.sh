#!/bin/bash

# http://blog.kablamo.org/2015/11/08/bash-tricks-eux/
set -uxo pipefail
cd "$(dirname "$0")/.." || exit 1

rc=0
while read -r -u10 file; do
  shellcheck "$file" || rc=$?
done 10< <(find . -type f -name '*.sh')

exit $rc
