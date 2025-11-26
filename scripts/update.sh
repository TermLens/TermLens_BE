#!/bin/bash

awslocal lambda update-function-code \
    --function-name analyzeTermsOfServices \
    --zip-file fileb://test-package.zip