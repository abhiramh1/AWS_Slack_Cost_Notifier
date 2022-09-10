#!/bin/bash

# http://blog.kablamo.org/2015/11/08/bash-tricks-eux/
set -uxo pipefail
cd "$(dirname "$0")/.." || exit 1

rc=0

astyle --dry-run --style=google --lineend=linux --convert-tabs --mode=java \
  --indent=spaces=2 < Jenkinsfile > Jenkinsfile.formatted
diff -u <(cat -vet Jenkinsfile) <(cat -vet Jenkinsfile.formatted) || rc=$?
if [[ $rc != 0 ]]; then
  cat <<'EOF'
Formatting of Jenkinsfile does not match standard defined for `astyle`.

See the above diff to determine what changes need to occur.

^M$ at the end of lines are Windows line endings. Change line endings to UNIX.
^I characters are tabs. Ensure all indentation is 2 spaces.
EOF
fi
exit $rc
