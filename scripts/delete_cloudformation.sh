#!/bin/bash

set -euxo pipefail
cd "$(dirname "$0")/.."

# shellcheck disable=SC1091
. scripts/stack_name_vars.sh

NONPRIV_ROLE_NAME="infra-cfnrole-${PROJECT_ID}-nonprivileged"

export NONPRIV_ROLE_NAME

# cfn_manage delete-stack \
#   --stack-name "$CFN_APIGATEWAY_STACK" \
#   --role-name "$NONPRIV_ROLE_NAME"

# cfn_manage delete-stack \
#   --stack-name "$CFN_LAMBDA_STACK" \
#   --role-name "$NONPRIV_ROLE_NAME"

#cfn_manage delete-stack \
#  --stack-name "$CFN_IAM_STACK" \
#  --role-name "$NONPRIV_ROLE_NAME"

# cfn_manage delete-stack \
#   --stack-name "$CFN_S3_STACK" \
#   --role-name "$NONPRIV_ROLE_NAME"
