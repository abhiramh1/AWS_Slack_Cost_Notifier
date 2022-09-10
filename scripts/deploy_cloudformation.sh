#!/bin/bash

set -euxo pipefail
cd "$(dirname "$0")/.."

# shellcheck disable=SC1091
. scripts/stack_name_vars.sh
# shellcheck disable=SC1091
. scripts/secrets.sh


NONPRIV_ROLE_NAME="infra-cfnrole-${PROJECT_ID}-nonprivileged"
PARAMS_FILE="cloudformation/params/${CFN_ENVIRONMENT}"

DATE_WITH_TIME=`date "+%Y%m%d-%H%M%S"`

CFN_LAMBDA_FILENAME=${DATE_WITH_TIME}'/aws-alert-source.zip'
S3_SOURCE_CODE_LOCATION="s3://"${CFN_S3_BUCKET_SOURCECODE_DETAILS}'/'${CFN_LAMBDA_FILENAME}

export NONPRIV_ROLE_NAME
export PARAMS_FILE
export CFN_LAMBDA_FILENAME

#aws s3 cp "build/billing-alert-test-api.zip" ${S3_SOURCE_CODE_LOCATION} --sse
#aws s3 cp "build/billing-alert-api.zip" ${S3_SOURCE_CODE_LOCATION} --sse

#  cfn_manage deploy-stack \
#    --stack-name "$CFN_S3_STACK" \
#    --template-file 'cloudformation/templates/s3.yml' \
#    --parameters-file "${PARAMS_FILE}/s3.yml" \
#    --role-name "$NONPRIV_ROLE_NAME"

 aws s3 cp "build/billing-alert-api.zip" ${S3_SOURCE_CODE_LOCATION} --sse

  cfn_manage deploy-stack \
    --stack-name "$CFN_LAMBDA_STACK" \
    --template-file 'cloudformation/templates/lambda.yml' \
    --parameters-file "${PARAMS_FILE}/lambda.yml" \
    --role-name "$NONPRIV_ROLE_NAME"

  cfn_manage deploy-stack \
    --stack-name "$CFN_APIGATEWAY_STACK" \
    --template-file 'cloudformation/templates/api_gateway.yml' \
    --parameters-file "${PARAMS_FILE}/api_gateway.yml" \
    --role-name "$NONPRIV_ROLE_NAME"



# Test stack
#cfn_manage deploy-stack \
# --stack-name "$CFN_IAM_STACK" \
# --template-file 'cloudformation/templates/iam.yml' \
# --role-name "$NONPRIV_ROLE_NAME"