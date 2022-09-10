#!/bin/bash

set -euo pipefail

export VAULT_ADDR="https://vault.kaccess.net:8200"

export HEADER_VALUE="vault.kaccess.net"

if [[ -z "${VAULT_TOKEN-}" ]]
then
   echo "Authenticate to Hashicorp Vault via token"
   VAULT_TOKEN=$(vault login -token-only -method=aws header_value="${HEADER_VALUE}" "role=jenkins-${PROJECT_ID}-${CFN_ENVIRONMENT}")
   export VAULT_TOKEN
fi

set +x
CFN_CLIENT_BOT_OAUTH_TOKEN=$(vault kv get -field=clientToken "kv2/prj/${CFN_ENVIRONMENT}/${PROJECT_ID}/default/aws/bot/slack")
CFN_CLIENT_BOT_SIGNING_SECRET=$(vault kv get -field=clientSecret "kv2/prj/${CFN_ENVIRONMENT}/${PROJECT_ID}/default/aws/bot/slack")
set -x

export CFN_CLIENT_BOT_OAUTH_TOKEN
export CFN_CLIENT_BOT_SIGNING_SECRET

export CFN_S3_BUCKET_USER_DETAILS=${S3_NAMING_INIT}'-'${PROJECT_ID}'-slack-bot-user'
export CFN_S3_BUCKET_SOURCECODE_DETAILS=${S3_NAMING_INIT}'-'${PROJECT_ID}'-slack-bot-source'

export CFN_LAMBDA_APP_NAME=${PROJECT_ID}'-slack-notifier-bot-lambda'
export CFN_LOG_GROUP_NAME='/aws/lambda/'${CFN_LAMBDA_APP_NAME}

export CFN_LAMBDA_APP_SCHEDULER_NAME=${PROJECT_ID}'-slack-notifier-scheduler-lambda'
export CFN_LOG_GROUP_SCHEDULER_NAME='/aws/lambda/'${CFN_LAMBDA_APP_SCHEDULER_NAME}