# TermLens_BE

약관 요약과 중요 조항에 대한 평가를 제공합니다.

# 아키텍처

TermLens의 백엔드 아키텍처는 아래의 요소로 구성됩니다.

- AWS
  - Lambda
  - S3
  - DynamoDB
  - Bedrock

# 테스트

AWS CLI가 설치 및 설정(`aws configure`)되어 있어야 합니다.

## AWS 환경 설정

`scripts/init.sh` 명령을 통해 실제 AWS 리소스(Lambda, S3, DynamoDB)를 생성합니다.
스크립트 내부의 `ROLE_ARN`이 유효한지 확인해주세요.

```bash
./scripts/make_zip.sh  # 배포 패키지 생성
./scripts/init.sh      # 리소스 생성 (최초 1회)
```

## 함수 실행

생성된 함수의 호출은 `scripts/invoke.sh "www.test.com" "test_tos.txt"`와 같이 할 수 있습니다.

```bash
./scripts/invoke.sh "http://www.sample.com" "sample_tos.txt"
```

## 코드 업데이트

코드를 수정한 후에는 다음 명령어로 AWS Lambda에 반영합니다.

```bash
./scripts/make_zip.sh
./scripts/update.sh
```

# 컨벤션

## 커밋 메시지

커밋 메시지의 작성법은 [컨벤셔널 커밋](https://www.conventionalcommits.org/ko/v1.0.0/)을 따릅니다. `feat: `, `fix: `, `test: ` 등의 접두사 뒤에 설명을 덧붙이는 방식입니다. 한국어로 작성합니다.

## 브랜칭 전략

[깃허브 플로우](https://docs.github.com/ko/get-started/using-github/github-flow)와 유사하게, 개별 작업마다 연관된 새로운 브랜치를 생성하고, 해당 브랜치에서 작업 후 main 브랜치에 병합하는 방식으로 개발을 진행합니다. 이때 브랜치의 이름은 `작업 종류/이슈번호-짧은-설명` 으로 합니다.
