#!/bin/bash
set -e

# Load .env if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Accept environment and command from arguments
ENVIRONMENT=${1:-staging}
COMMAND=${2:-bootstrap}  # default to bootstrap

# Uppercase keys to match .env variables
PROFILE_VAR="${ENVIRONMENT^^}_PROFILE"
ACCOUNT_VAR="${ENVIRONMENT^^}_ACCOUNT_ID"
REGION_VAR="${ENVIRONMENT^^}_REGION"

# Resolve actual values from .env
PROFILE=${!PROFILE_VAR}
ACCOUNT_ID=${!ACCOUNT_VAR}
REGION=${!REGION_VAR}
IMAGE_NAME=${IMAGE_NAME:-image-processor-cdk}

if [[ -z "$PROFILE" || -z "$ACCOUNT_ID" || -z "$REGION" ]]; then
  echo "❌ Missing .env config for environment: $ENVIRONMENT"
  exit 1
fi

# Define the shared Docker run command
DOCKER_CMD="docker run --rm -it \
  -e AWS_PROFILE=$PROFILE \
  -v \"$PWD\":/app \
  -w /app \
  -v \"$HOME/.aws\":/root/.aws \
  $IMAGE_NAME"

# Run selected CDK command
case $COMMAND in
  bootstrap)
    echo "🚀 Bootstrapping AWS account ${ACCOUNT_ID} in region ${REGION}..."
    eval $DOCKER_CMD cdk bootstrap --profile $PROFILE aws://${ACCOUNT_ID}/${REGION}
    ;;
  synth)
    echo "🧪 Synthesizing CloudFormation template..."
    eval $DOCKER_CMD cdk synth
    ;;
  deploy)
    echo "🚢 Deploying CDK stack..."
    eval $DOCKER_CMD cdk deploy --require-approval never
    ;;
  destroy)
    echo "🔥 Destroying CDK stack..."
    eval $DOCKER_CMD cdk destroy --force
    ;;
  *)
    echo "❌ Unknown command: $COMMAND"
    echo "Usage: ./scripts/cdk-cmd.sh [environment] [bootstrap|synth|deploy|destroy]"
    exit 1
    ;;
esac
