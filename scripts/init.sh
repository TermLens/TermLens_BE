#!/bin/bash

# 실제 AWS 환경 배포를 위한 스크립트

# IAM Role ARN (User provided)
ROLE_ARN="arn:aws:iam::010928200297:role/service-role/analyzeTermsOfServices-role-17yqexfq"
REGION="ap-northeast-2"
LAMBDA_NAME="analyzeTermsOfServices"
BUCKET_NAME="termlens-tos-content"
TABLE_NAME="termlens-tos-analysis"

# 1. Lambda Function
echo "[INFO] Checking Lambda Function..."
if aws lambda get-function --function-name "$LAMBDA_NAME" --region "$REGION" > /dev/null 2>&1; then
    echo "[INFO] Lambda function '$LAMBDA_NAME' already exists. Skipping creation."
else
    echo "[INFO] Creating Lambda Function..."
    aws lambda create-function \
        --function-name "$LAMBDA_NAME" \
        --runtime python3.12 \
        --timeout 120 \
        --zip-file fileb://deploy-package.zip \
        --handler lambda_function.lambda_handler \
        --role "$ROLE_ARN" \
        --region "$REGION"
fi

# 2. S3 Bucket
echo "[INFO] Checking S3 Bucket..."
if aws s3api head-bucket --bucket "$BUCKET_NAME" --region "$REGION" > /dev/null 2>&1; then
    echo "[INFO] S3 bucket '$BUCKET_NAME' already exists. Skipping creation."
else
    echo "[INFO] Creating S3 Bucket..."
    aws s3api create-bucket \
        --bucket "$BUCKET_NAME" \
        --region "$REGION" \
        --create-bucket-configuration LocationConstraint="$REGION"
fi

# 3. DynamoDB Table
echo "[INFO] Checking DynamoDB Table..."
if aws dynamodb describe-table --table-name "$TABLE_NAME" --region "$REGION" > /dev/null 2>&1; then
    echo "[INFO] DynamoDB table '$TABLE_NAME' already exists. Skipping creation."
else
    echo "[INFO] Creating DynamoDB Table..."
    aws dynamodb create-table \
        --table-name "$TABLE_NAME" \
        --key-schema AttributeName=url,KeyType=HASH \
        --attribute-definitions AttributeName=url,AttributeType=S \
        --billing-mode PAY_PER_REQUEST \
        --region "$REGION"
fi

echo "[SUCCESS] Initialization complete."
