#!/bin/bash
if [[ -z "${STACK_SUFFIX-}" ]]; then
  # Jenkins - Multibranch Pipelines
  if [[ -n "${BRANCH_NAME-}" ]]; then
    if [[ "$BRANCH_NAME" != "main" ]]; then
      STACK_SUFFIX="-${BRANCH_NAME}"
    fi
  # GNU/UNIX
  elif [[ -n "${USER-}" ]]; then
    STACK_SUFFIX="-${USER}"
  # Windows - Git Bash
  elif [[ -n "${USERNAME-}" ]]; then
    STACK_SUFFIX="-${USERNAME}"
  else
    echo "Could not cleanly determine stack suffix!" 1>&2
    exit 1
  fi
  export CFN_STACK_SUFFIX="${STACK_SUFFIX-}"
fi

# stack names
#export CFN_IAM_STACK="${PROJECT_ID}-slack-notifier-bot-${CFN_ENVIRONMENT}-stack-cwe-test${STACK_SUFFIX-}"
export CFN_S3_STACK="${PROJECT_ID}-slack-notifier-bot-${CFN_ENVIRONMENT}-stack-s3${STACK_SUFFIX-}"
export CFN_LAMBDA_STACK="${PROJECT_ID}-slack-notifier-bot-${CFN_ENVIRONMENT}-stack-lambda${STACK_SUFFIX-}"
export CFN_APIGATEWAY_STACK="${PROJECT_ID}-slack-notifier-bot-${CFN_ENVIRONMENT}-stack-apigateway${STACK_SUFFIX-}"
