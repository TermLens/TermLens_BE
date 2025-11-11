# TermLens_BE
약관 요약과 중요 조항에 대한 평가를 제공합니다.

# 아키텍처
AWS Lambda
Gemini

# Getting Started
## 개발환경 구축
bash를 기준으로 작성됨

```bash
sudo apt install python3.12-venv
python3 -m venv venv # 가상환경 생성
source venv/bin/activate # 가상환경 사용
pip install -q -U google-genai
```

이후부터 작업 시 `source venv/bin/activate` 명령으로 가상환경을 실행한 후 작업
- `(venv) 사용자명@컴퓨터명:~/.../TermLens_BE` 처럼 앞에 `(venv)`가 붙는지 확인

## 컨벤션
### 커밋 메시지
커밋 메시지의 작성법은 [컨벤셔널 커밋](https://www.conventionalcommits.org/ko/v1.0.0/)을 따릅니다. `feat: `, `fix: `, `test: ` 등의 접두사 뒤에 설명을 덧붙이는 방식입니다. 한국어로 작성합니다.

### 브랜칭 전략
[깃허브 플로우](https://docs.github.com/ko/get-started/using-github/github-flow)와 유사하게, 개별 작업마다 연관된 새로운 브랜치를 생성하고, 해당 브랜치에서 작업 후 main 브랜치에 병합하는 방식으로 개발을 진행합니다. 이때 브랜치의 이름은 `작업 종류/이슈번호-짧은-설명` 으로 합니다. 

# 테스트
로컬에서 `lambda_handler()` 메서드를 테스트해야하는 경우 `test_local.py`를 통해 실행
