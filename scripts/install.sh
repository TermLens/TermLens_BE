#!/bin/bash

set -e  # 명령 실패 시 스크립트 중단

# 에러 핸들링 함수
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "[ERROR] $1 설치에 실패했습니다."
        exit 1
    fi
    echo "[OK] $1 설치 확인 완료: $($1 --version 2>&1 | head -n 1)"
}

# 패키지 매니저 감지
detect_package_manager() {
    if command -v apt &> /dev/null; then
        echo "apt"
    elif command -v brew &> /dev/null; then
        echo "brew"
    else
        echo "[ERROR] 지원되는 패키지 매니저(apt, brew)를 찾을 수 없습니다."
        exit 1
    fi
}

PKG_MANAGER=$(detect_package_manager)
echo "[INFO] 패키지 매니저: $PKG_MANAGER"

# pipx 설치
echo "[INFO] pipx 설치 중..."
if [ "$PKG_MANAGER" = "apt" ]; then
    sudo apt update
    sudo apt install -y pipx || { echo "[ERROR] pipx 설치 실패"; exit 1; }
elif [ "$PKG_MANAGER" = "brew" ]; then
    brew install pipx || { echo "[ERROR] pipx 설치 실패"; exit 1; }
fi
pipx ensurepath
check_command pipx

# LocalStack 설치
echo "[INFO] LocalStack 설치 중..."
pipx install localstack --include-deps || { echo "[ERROR] LocalStack 설치 실패"; exit 1; }

# awslocal 설치
echo "[INFO] awslocal 설치 중..."
pipx install awscli-local[ver1] --include-deps || { echo "[ERROR] awslocal 설치 실패"; exit 1; }

# PATH 갱신
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null || true

# 설치 확인
check_command localstack
check_command awslocal

echo "[OK] 모든 설치가 성공적으로 완료되었습니다."
