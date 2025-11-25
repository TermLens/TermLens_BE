# TermLens_BE
약관 요약과 중요 조항에 대한 평가를 제공합니다.
# 아키텍처
- AWS Lambda
- AWS Bedrock
# 테스트
LocalStack의 실행을 위해 docker 설치가 필요합니다.
## LocalStack 설치
```bash
# pipx 설치
sudo apt update
sudo apt install pipx
# 잘 설치되었는지 확인
pipx --version

# LocalStack, awslocal 설치
pipx install localstack --include-deps
pipx install awscli-local[ver1] --include-deps
source ~/.bashrc
# 잘 설치되었는지 확인
localstack --version
awslocal --version
```
wsl 환경에서 `pip install` 명령을 전역으로 쓸 수 없어 pipx를 사용합니다. 전역으로 localstack 및 awslocal을 설치하여 사용 가능한 경우 pipx의 설치가 필요하지 않습니다.
## 로컬 테스트
**docker가 실행된 상태에서** `localstack start` 명령으로 LocalStack을 구동합니다. 이후 터미널에 `Ready`가 나타나면 다른 터미널 창을 열고, 프로젝트 디렉토리에서 아래 작업을 수행합니다.

우선, LocalStack에 업로드할 zip파일을 생성합니다.
```bash
pip install -r requirements.txt -t build/ --upgrade
cp src/*.py build/
cd build
zip -r ../test-package.zip .
cd ..
```

ARM 환경에서는 `pip install...` 명령 대신 아래의 명령을 사용해주세요. LocalStack 및 AWS Lambda 환경에서는 amd64(x86-64)을 기반으로 작동하나, ARM 기반 기기에서 해당 명령으로 설치하게 되면 ARM용 바이너리를 받아와 LocalStack에서 실행하지 못합니다. 아래 명령으로 생성된 `build/` 디렉토리 및 `test-package.zip` 파일은 삭제 시 root 권한이 필요합니다.
```bash
docker run --platform linux/amd64 --rm -v "$(pwd)":/var/task --entrypoint "" public.ecr.aws/lambda/python:3.12 /bin/sh -c "pip install -r requirements.txt -t build/ --upgrade && cp src/*.py build/ && cd build && dnf install -y zip && zip -r ../test-package.zip . && cd .."
```

그 다음 아래의 명령을 통해 람다 함수를 생성합니다.
```bash
awslocal lambda create-function \
    --function-name analyzeTermsOfServices \
    --runtime python3.12 \
    --timeout 120 \
    --zip-file fileb://test-package.zip \
    --handler lambda_function.lambda_handler \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --environment Variables='{GEMINI_API_KEY=여기에_KEY값을_넣어주세요,LLM_PROVIDER=GEMINI}'
```

생성된 함수의 호출은 다음과 같이 할 수 있습니다.
```bash
awslocal lambda invoke --function-name analyzeTermsOfServices \
    --payload '{"queryStringParameters": {"url" : "www.example.com"}, "body" : "약관 텍스트" }' output.json
```
이후 `output.json` 파일에서 응답을 확인할 수 있습니다.

함수가 생성된 상태에서 변경하기 위해서는 `update-function-code`를 사용합니다.
```bash
awslocal lambda update-function-code \
    --function-name analyzeTermsOfServices \
    --zip-file fileb://test-package.zip
```
## AWS 환경에서 테스트
로컬에서는 작동만을 확인하고, 답변 품질에 대한 테스트는 AWS Lambda에, 테스트용 함수에 배포하여 수행합니다.
# 컨벤션
## 커밋 메시지
커밋 메시지의 작성법은 [컨벤셔널 커밋](https://www.conventionalcommits.org/ko/v1.0.0/)을 따릅니다. `feat: `, `fix: `, `test: ` 등의 접두사 뒤에 설명을 덧붙이는 방식입니다. 한국어로 작성합니다.
## 브랜칭 전략
[깃허브 플로우](https://docs.github.com/ko/get-started/using-github/github-flow)와 유사하게, 개별 작업마다 연관된 새로운 브랜치를 생성하고, 해당 브랜치에서 작업 후 main 브랜치에 병합하는 방식으로 개발을 진행합니다. 이때 브랜치의 이름은 `작업 종류/이슈번호-짧은-설명` 으로 합니다. 
