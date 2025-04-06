#!/bin/bash

# Deploy script for different environments
# Usage: ./scripts/deploy.sh [stage]

STAGE=${1:-dev}
echo "Deploying to $STAGE environment..."

# Validate stage
if [[ "$STAGE" != "dev" && "$STAGE" != "prod" ]]; then
  echo "Error: Stage must be 'dev' or 'prod'"
  exit 1
fi

# Deploy with Serverless Framework
echo "Running Serverless deployment..."
serverless deploy --stage $STAGE

# Display deployed API endpoints
echo "Getting API information..."
serverless info --stage $STAGE

echo "Deployment to $STAGE completed!"
