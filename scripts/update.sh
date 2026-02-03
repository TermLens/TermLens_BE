#!/bin/bash

echo "[INFO] Updating Lambda Function Code..."
aws lambda update-function-code \
    --function-name analyzeTermsOfServices \
    --zip-file fileb://deploy-package.zip \
    --region ap-northeast-2

echo "[SUCCESS] Update complete."
