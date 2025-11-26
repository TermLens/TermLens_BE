#!/bin/bash

awslocal lambda create-function \
    --function-name analyzeTermsOfServices \
    --runtime python3.12 \
    --timeout 120 \
    --zip-file fileb://test-package.zip \
    --handler lambda_function.lambda_handler \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --environment Variables='{GEMINI_API_KEY=여기에_API_KEY를_입력하세요,LLM_PROVIDER=GEMINI}'

awslocal s3api create-bucket --bucket inha-capstone-20-tos-content

awslocal dynamodb create-table \
    --table-name inha-capstone-20-tos-analysis \
    --key-schema AttributeName=url,KeyType=HASH \
    --attribute-definitions AttributeName=url,AttributeType=S \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1