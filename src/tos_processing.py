import json
from typing import Dict, List

from llm_client import LLMClient


def _extract_json_fragment(text: str):
    """
    Extract the first JSON fragment (object or array) from a string response.
    """
    obj_start = text.find("{")
    arr_start = text.find("[")
    starts = [i for i in [obj_start, arr_start] if i != -1]
    if not starts:
        raise ValueError("JSON 시작 구분자를 찾지 못했습니다.")

    start = min(starts)
    end_char = "}" if start == obj_start else "]"
    end = text.rfind(end_char)
    if end == -1:
        raise ValueError("JSON 종료 구분자를 찾지 못했습니다.")

    return json.loads(text[start : end + 1])


def score_sentence_importance(sentences: List[str], client: LLMClient) -> List[Dict]:
    """
    중요도 1~5로 문장별 점수를 산출한다.
    """
    if not sentences:
        return []

    system_instruction = """
당신은 온라인 서비스 이용약관 문장을 중요도 1~5로 평가하는 분석가입니다.
importance_score (1~5):

5 = CRITICAL
  - 사용자의 권리/프라이버시/금전적 리스크에 직접적이고 큰 영향을 미침
  - 예: 넓은 책임 제한, 손해배상 전면 면책, 매우 광범위한 데이터 수집/제3자 공유/보관, 일방적 해지/정지/변경권, 높은 위약금, 자동 결제/자동 갱신 핵심 조항

4 = HIGH
  - 중요하지만 5만큼 극단적이진 않은 조항
  - 예: 어느 정도 제한된 책임 제한, 개인정보 처리/보안/권리 행사 주요 문장, 계정 정지/서비스 제한 조건

3 = MEDIUM
  - 알아두면 좋고 종종 영향을 줄 수 있는 일반적 조항
  - 예: 이용자 의무/금지행위, 일반적 분쟁 해결/관할 규정, 데이터 보관·로그 수집 등

2 = LOW
  - 영향이 크지 않은 부연/절차적 내용
  - 예: 상세 절차, 예외 조항, 중요 문장의 부연

1 = VERY_LOW
  - 실질적 권리/의무/위험에 거의 영향을 주지 않는 내용

규칙:
- 입력으로 주어진 순서에 대응하는 input_index를 반드시 포함합니다.
- sentence 원문을 그대로 포함합니다.
- JSON 배열만 반환하며 키는 input_index, sentence, importance_score를 사용합니다.
"""

    message = json.dumps(
        {
            "sentences": [
                {"input_index": idx, "sentence": sentence}
                for idx, sentence in enumerate(sentences)
            ]
        },
        ensure_ascii=False,
    )

    response = client.generate_response(system_instruction, message)
    parsed = _extract_json_fragment(response)

    results = []
    for item in parsed:
        sentence = str(item.get("sentence", "")).strip()
        try:
            score = int(item.get("importance_score", 0))
        except Exception:
            score = 0
        results.append(
            {
                "input_index": item.get("input_index"),
                "sentence": sentence,
                "importance_score": score,
            }
        )

    # 입력 순서를 유지
    return sorted(results, key=lambda x: x.get("input_index", 0))


def categorize_sentences(scored_sentences: List[Dict], client: LLMClient) -> List[Dict]:
    """
    중요도가 3 이상인 문장을 미리 정의된 카테고리로 분류한다.
    """
    if not scored_sentences:
        return []

    system_instruction = """
당신은 약관 문장을 미리 정의된 카테고리로 분류하는 전문가입니다.
category는 아래 중 하나를 선택하세요. 정확한 키를 그대로 사용합니다.
- USER_ACCOUNT_ACCESS: 회원 가입, 로그인, 계정 생성/삭제, 본인인증, 자격상실, 계정 보안/비밀번호 관리 등
- USER_CONDUCT_ACCEPTABLE_USE: 서비스 사용 시 금지행위, 스팸, 불법행위, 지식재산 침해, 타인 권리 침해, 부정 사용 등
- PAYMENT_PRICING_REFUND: 요금, 과금 방식, 결제 수단, 환불 규정, 구독 자동 갱신, 추가 수수료 부과 등
- CONTENT_IP_LICENSE: 사용자 콘텐츠의 저작권, 라이선스 부여 범위, 2차적 저작물, 회사의 사용 권한 등
- PRIVACY_DATA_COLLECTION: 개인정보/데이터의 수집, 처리, 이용, 제3자 제공, 국제 이전, 데이터 보관 기간 등
- LIABILITY_DISCLAIMER_LIMITATION: 회사 책임 제한, 손해배상 범위, 면책 조항, as-is 제공, 간접손해 배제 등
- TERMINATION_SUSPENSION: 서비스/계정의 해지, 일시 중단, 이용정지, 종료 사유 및 절차, 효과 등
- MODIFICATION_TOS_CHANGES: 약관 변경, 조건 수정, 통지 방식, 변경 효력 발생 시점 등
- DISPUTE_GOVERNING_LAW: 준거법, 관할법원, 분쟁 해결 방식(중재, 조정, 집단소송 포기 등)
- THIRD_PARTY_SERVICE_ADS: 제3자 서비스 연동, 광고, 링크, 제3자 약관 적용 등
- CONSUMER_RIGHTS_PROTECTION: 청약철회, 계약 해지 권리, 환급, 소비자 보호 관련 명시적 권리 부여
- META_INFO_DEFINITIONS: 용어 정의, 문서 구조 안내, 소개 문구, 회사 정보 등
- OTHER: 위 어느 것도 명확히 해당하지 않는 경우

규칙:
- 각 항목에 input_index, sentence, importance_score, category를 포함한 JSON 배열을 반환합니다.
- category는 위 목록 중 하나를 정확히 사용합니다.
"""

    message = json.dumps(
        {"sentences": scored_sentences},
        ensure_ascii=False,
    )

    response = client.generate_response(system_instruction, message)
    parsed = _extract_json_fragment(response)

    results = []
    for item in parsed:
        sentence = str(item.get("sentence", "")).strip()
        try:
            score = int(item.get("importance_score", 0))
        except Exception:
            score = 0
        results.append(
            {
                "input_index": item.get("input_index"),
                "sentence": sentence,
                "importance_score": score,
                "category": item.get("category", "OTHER"),
            }
        )

    return sorted(results, key=lambda x: x.get("input_index", 0))
