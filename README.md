# TermLens_BE
약관 요약과 중요 조항에 대한 평가를 제공합니다.

# 아키텍처
AWS Lambda
Gemini

# Getting Started
bash를 기준으로 작성됨

```bash
sudo apt install python3.12-venv
python3 -m venv venv # 가상환경 생성
source venv/bin/activate # 가상환경 사용
pip install -q -U google-genai
```

이후부터 작업 시 `source venv/bin/activate` 명령으로 가상환경을 실행한 후 작업
- `(venv) 사용자명@컴퓨터명:~/.../TermLens_BE` 처럼 앞에 `(venv)`가 붙는지 확인

# 테스트
로컬에서 `lambda_handler()` 메서드를 테스트해야하는 경우 `test_local.py`를 통해 실행
