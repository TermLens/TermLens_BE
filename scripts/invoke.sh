#!/bin/bash

# jq 설치 확인 및 설치 함수
check_and_install_jq() {
    if ! command -v jq &> /dev/null; then
        echo "jq가 설치되어 있지 않습니다. 설치를 시도합니다..."
        
        if [ -x "$(command -v apt-get)" ]; then
            sudo apt-get update && sudo apt-get install -y jq
        elif [ -x "$(command -v brew)" ]; then
            brew install jq
        else
            echo "지원되는 패키지 매니저를 찾을 수 없습니다. 수동으로 jq를 설치해주세요."
            exit 1
        fi

        if ! command -v jq &> /dev/null; then
            echo "jq 설치에 실패했습니다. 수동으로 설치해주세요."
            exit 1
        fi
        echo "jq가 성공적으로 설치되었습니다."
    fi
}

# jq 확인 및 설치 실행
check_and_install_jq

# 인자 확인
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <url> <file_path>"
    echo "Example: $0 \"www.google.com\" \"tos.txt\""
    exit 1
fi

URL="$1"
FILE_PATH="$2"

# 파일 존재 여부 확인
if [ ! -f "$FILE_PATH" ]; then
    echo "Error: 파일 '$FILE_PATH'을(를) 찾을 수 없습니다."
    exit 1
fi

# 파일 내용 읽기
HTML_CONTENT=$(cat "$FILE_PATH")

# jq를 사용하여 안전하게 JSON payload 생성
PAYLOAD=$(jq -n \
            --arg url "$URL" \
            --arg body "$HTML_CONTENT" \
            '{queryStringParameters: {url: $url}, body: $body}')

# Lambda 함수 호출
echo "Invoking Lambda function (Real AWS)..."
aws lambda invoke \
    --function-name analyzeTermsOfServices \
    --payload "$PAYLOAD" \
    --region ap-northeast-2 \
    --log-type Tail \
    output.json > invoke_result.json

# 결과 처리
echo "================================================================"
echo "[Execution Log]"
# LogResult 필드를 추출
LOG_RESULT=$(cat invoke_result.json | jq -r '.LogResult')

if [ "$LOG_RESULT" != "null" ] && [ -n "$LOG_RESULT" ]; then
    # base64 디코딩 시도, 실패 시 원본 출력 (디버깅용)
    echo "$LOG_RESULT" | base64 -di || echo "[WARN] Base64 decode failed. Raw LogResult: $LOG_RESULT"
else
    echo "[WARN] No LogResult found in response."
fi
echo "================================================================"
echo "[Function Output]"
cat output.json | jq '.'

# 임시 파일 정리
rm invoke_result.json
