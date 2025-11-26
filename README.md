# TermLens_BE

약관 요약과 중요 조항에 대한 평가를 제공합니다.

# 아키텍처

TermLens의 백엔드 아키텍처는 아래의 요소로 구성됩니다.

- AWS
  - Lambda
  - S3
  - DynamoDB
  - Bedrock (with Claude 3.5 Haiku)

# 테스트

LocalStack의 실행을 위해 docker 설치가 필요합니다.

## LocalStack 설치

`scripts/install.sh` 명령으로 pipx와, pipx를 통해 localstack, awslocal이 설치됩니다.

이후 `aws configure` 명령을 통해 가짜 aws credentials를 설정합니다. s3 및 DynamoDB 사용에 필요합니다. 각 요소는 다음과 같이 설정합니다.

```bash
AWS Access Key ID [None]: test
AWS Secret Access Key [None]: test
Default region name [None]: us-east-1
Default output format [None]: json
```

## 로컬 테스트

**docker가 실행된 상태에서** `localstack start` 명령으로 LocalStack을 구동합니다. 이후 터미널에 `Ready`가 나타나면 다른 터미널 창을 열고, 프로젝트 디렉토리에서 아래 작업을 수행합니다.

**스크립트들은 `scripts/스크립트_이름.sh`로 프로젝트 최상위 디렉토리에서 실행해주세요.**

우선, LocalStack에 업로드할 `test-package.zip` 파일을 `scripts/make_zip.sh`을 사용해 생성합니다. docker를 사용해 arm 환경에서도 amd64용 바이너리를 받아오도록 했습니다.

그 다음 `scripts/init.sh` 명령을 통해 람다 함수, S3 버킷, DynamoDB 테이블을 생성합니다. **localstack을 새로 실행할 때마다** 진행해 주셔야 합니다.

생성된 함수의 호출은 `scripts/invoke.sh "www.test.com" "test_tos.txt"`와 같이 할 수 있습니다. 약관 텍스트 파일은 프로젝트 최상위 디렉토리(`.../TermLens/TermLens_BE`)에 넣어주세요.

localstack이 실행 중이고 함수가 만들어진 상태에서 **변경된 코드를 적용**하려면 다시 `test-package.zip` 파일을 만든 뒤 `scripts/update.sh` 명령으로 업데이트합니다.

## AWS 환경에서 테스트

로컬에서는 작동만을 확인하고, 답변 품질에 대한 테스트는 AWS Lambda에, 테스트용 함수에 배포하여 수행합니다.

# 컨벤션

## 커밋 메시지

커밋 메시지의 작성법은 [컨벤셔널 커밋](https://www.conventionalcommits.org/ko/v1.0.0/)을 따릅니다. `feat: `, `fix: `, `test: ` 등의 접두사 뒤에 설명을 덧붙이는 방식입니다. 한국어로 작성합니다.

## 브랜칭 전략

[깃허브 플로우](https://docs.github.com/ko/get-started/using-github/github-flow)와 유사하게, 개별 작업마다 연관된 새로운 브랜치를 생성하고, 해당 브랜치에서 작업 후 main 브랜치에 병합하는 방식으로 개발을 진행합니다. 이때 브랜치의 이름은 `작업 종류/이슈번호-짧은-설명` 으로 합니다.
