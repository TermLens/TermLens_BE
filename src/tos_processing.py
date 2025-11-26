import json
from concurrent.futures import ThreadPoolExecutor, as_completed
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

    batch_size = 7
    system_instruction = """
당신은 온라인 서비스 이용약관 문장을 중요도 1~5로 평가하는 분석가입니다.
입력은 JSON 객체이며, "sentences" 필드 아래에 다음 형태의 리스트가 주어집니다.

{
  "sentences": [
    { "input_index": 0, "sentence": "..." },
    { "input_index": 1, "sentence": "..." },
    ...
  ]
}

당신의 작업:
- 각 sentence에 대해 importance_score (1~5)를 하나씩 부여합니다.
- 결과는 JSON 배열로만 출력하며, 각 요소는 다음 필드를 포함해야 합니다.
  { "input_index": <정수>, "sentence": "<원문 문장>", "importance_score": <1~5 정수> }
- input_index와 sentence는 입력 값을 그대로 복사하되, 앞뒤 공백만 제거합니다.
- 출력 배열의 길이는 입력 "sentences" 리스트 길이와 같아야 하며, 모든 input_index가 포함되어야 합니다.
- JSON 배열 이외의 텍스트(설명, 코드블록, 주석 등)는 절대 출력하지 마십시오.

[importance_score 정의: '사용자 입장에서 얼마나 반드시 알아야 하는지']

5 = CRITICAL (최상위 중요)
  - 사용자의 권리/의무/프라이버시/금전적 리스크에 직접적이고 큰 영향을 미침.
  - 예시:
    - 회사의 책임을 매우 넓게 면책하거나, 손해배상 책임을 거의 전부 부인하는 조항
      (예: "당사는 어떠한 손해에 대해서도 책임을 지지 않습니다.")
    - 자동 결제/자동 갱신의 핵심 조건, 해지하지 않으면 계속 과금되는 구조
    - 광범위한 개인정보/사용자 데이터 수집·이용·제3자 제공·보관을 허용하는 조항
    - 회사가 일방적으로 서비스/계정을 해지·정지·중단할 수 있는 권한을 넓게 가지는 조항
    - 사용자가 큰 금전적 책임 또는 위약금을 부담하게 되는 조항
    - 사용자가 가지는 매우 중요한 권리(광범위한 환불권, 강한 소비자 보호 등)를 명시하는 핵심 조항
  - "이 조항을 모르면 심각한 피해/불이익이 발생할 수 있다" 수준의 내용.

4 = HIGH (매우 중요)
  - 상당히 중요하지만 5점만큼 극단적이진 않은 조항.
  - 예시:
    - 특정 상황에서만 적용되는 책임 제한/손해배상 한도 규정
    - 개인정보 처리, 보안, 이용자의 동의·철회·열람·삭제 권리 등 주요 프라이버시 관련 조항
    - 계정 정지/제한/정상 해지 절차, 유료 서비스 이용 중단 시 효과 등
    - 결제·요금·환불 정책 중에서 일반 사용자가 반드시 알고 있어야 하는 조건
    - 사용자의 중요한 권리(예: 일정 기간 내 무조건 환불 가능)를 부여하는 조항
  - "알면 큰 도움이 되고, 모르면 예상치 못한 문제를 겪을 가능성이 상당한" 수준.

3 = MEDIUM (보통 중요)
  - 알아두면 좋고 실제로도 영향을 줄 수 있지만, 치명적이진 않은 일반적인 조항.
  - 예시:
    - 일반적인 이용자 의무, 금지행위 목록, 계정 보안에 관한 일반 규정
    - 표준적인 관할/준거법/분쟁 해결 방식(특별히 불리하지 않은 수준)
    - 로그/쿠키/사용 기록 보관, 통계 목적의 데이터 이용 등 비교적 통상적인 내용
    - 약관 변경 시 통지 방법, 효력 발생 시점 등 메타 규정
  - "중요하지만, 모른다고 해서 바로 큰 피해로 이어지지는 않음" 수준.

2 = LOW (낮은 중요)
  - 직접적인 영향은 크지 않고, 주로 부연 설명/상세 절차/예외 상황을 다루는 조항.
  - 예시:
    - 이미 중요 문장에서 규정한 사항에 대한 세부 절차, 실무적인 단계 설명
    - 드문 예외 상황이나 기술적 세부 사항
    - 특정 기능에만 제한적으로 적용되는, 일반 사용자가 거의 마주치지 않을 내용
  - 상위 핵심 조항을 이해하기 위한 보조 정보에 가까운 경우.

1 = VERY_LOW (매우 낮은 중요)
  - 실질적인 권리/의무/위험에 거의 영향을 주지 않는 내용.
  - 예시:
    - 순수한 안내/소개 문구, 홍보성 설명
    - 회사 일반 정보, 연락처, 사업자 등록번호 등
    - 정의 조항 중, 실제 사용자의 권리/의무/위험에 거의 연결되지 않는 용어 정의
  - 나중 단계에서 거의 항상 버려져도 될 만한 문장.

[추가 규칙]
- 점수는 '사용자가 이 조항을 알고 있는 것이 얼마나 중요한가' 기준으로 판단합니다.
- 사용자에게 매우 유리한 보호 조항(강한 환불권, 개인정보 보호 강화 등)도 "반드시 알고 있어야 할 권리"라면 4~5점을 줄 수 있습니다.
- 이후 파이프라인에서 중요도 1, 2는 버려집니다.
  - 따라서 "조금이라도 알아두는 게 의미 있는 조항"이면 최소 3 이상을 부여하십시오.
- 애매할 때는 항상 한 단계 낮은 점수를 주어 보수적으로 평가합니다.
"""

    indexed_sentences = [
        {"input_index": idx, "sentence": sentence}
        for idx, sentence in enumerate(sentences)
    ]
    sentence_batches = [
        indexed_sentences[i : i + batch_size]
        for i in range(0, len(indexed_sentences), batch_size)
    ]

    def _score_batch(batch: List[Dict]) -> List[Dict]:
        message = json.dumps({"sentences": batch}, ensure_ascii=False)
        response = client.generate_response(system_instruction, message)
        parsed = _extract_json_fragment(response)

        batch_results = []
        for item in parsed:
            sentence = str(item.get("sentence", "")).strip()
            try:
                score = int(item.get("importance_score", 0))
            except Exception:
                score = 0
            batch_results.append(
                {
                    "input_index": item.get("input_index"),
                    "sentence": sentence,
                    "importance_score": score,
                }
            )
        return batch_results

    all_results: List[Dict] = []
    with ThreadPoolExecutor(max_workers=len(sentence_batches)) as executor:
        futures = [executor.submit(_score_batch, batch) for batch in sentence_batches]
        for future in as_completed(futures):
            all_results.extend(future.result())

    # 입력 순서를 유지
    return sorted(all_results, key=lambda x: x.get("input_index", 0))


def categorize_sentences(scored_sentences: List[Dict], client: LLMClient) -> List[Dict]:
    """
    중요도가 3 이상인 문장을 미리 정의된 카테고리로 분류한다.
    """
    if not scored_sentences:
        return []

    batch_size = 7
    system_instruction = """
당신은 온라인 서비스 이용약관 문장을 미리 정의된 category로 분류하는 전문가입니다.

[입력 형식]
- 입력은 JSON 객체이며, "sentences" 필드 아래에 리스트가 주어집니다.
- 각 항목은 다음과 같은 형태입니다.
  {
    "input_index": <정수>,
    "sentence": "<문장>",
    "importance_score": <정수 1~5>
  }

[출력 형식]
- JSON 배열만 출력해야 합니다. 배열의 각 요소는 다음 필드를 포함합니다.
  {
    "input_index": <정수>,
    "sentence": "<원문 문장>",
    "importance_score": <정수 1~5>,
    "category": "<아래 목록 중 하나>"
  }
- input_index, sentence, importance_score는 입력 값을 그대로 복사하고, category만 추가합니다.
- category 필드는 아래 정의된 키 중 하나를 정확히 사용해야 합니다.
- JSON 배열 이외의 설명/주석/코드블록 텍스트는 절대 출력하지 마십시오.

[category 목록 및 기준]

- USER_ACCOUNT_ACCESS
  - 회원 가입, 로그인, 계정 생성/삭제, 본인인증, 자격 상실, 계정 휴면/복구, 비밀번호/인증정보 관리 등
  - 예: "회원은 비밀번호를 제3자에게 양도할 수 없습니다."

- USER_CONDUCT_ACCEPTABLE_USE
  - 서비스 사용 시 금지행위, 불법행위, 스팸, 해킹, 부정 사용, 타인 권리(초상권·지식재산권 등) 침해 관련 조항
  - 예: "불법적인 목적으로 서비스를 이용해서는 안 됩니다."

- PAYMENT_PRICING_REFUND
  - 요금/가격, 결제 수단, 결제 실패, 청구 주기, 구독/자동 갱신, 환불 규정, 할인/쿠폰, 추가 수수료 등
  - 예: "구독은 매월 자동 갱신되며, 지정일에 결제가 이루어집니다."

- CONTENT_IP_LICENSE
  - 사용자 콘텐츠(글, 사진, 동영상 등)의 저작권 소유, 회사에 부여되는 라이선스 범위, 2차적 저작물 생성, 콘텐츠 이용 권한/제한 등
  - 예: "사용자는 회사에 비독점적, 전세계적, 로열티 없는 라이선스를 부여합니다."

- PRIVACY_DATA_COLLECTION
  - 개인정보/사용자 데이터 수집·이용·제3자 제공·국외 이전, 쿠키/로그/추적, 보관 기간, 익명/가명 처리, 개인정보 권리(열람/정정/삭제 등) 관련
  - 예: "서비스 제공을 위해 이름, 이메일 주소를 수집합니다."

- LIABILITY_DISCLAIMER_LIMITATION
  - 회사 책임 제한, 손해배상 범위, 면책 조항, 간접/특별/부수적 손해 배제, 서비스 "as is" 제공, 보증 부인 등
  - 예: "당사는 간접손해에 대해 책임을 지지 않습니다."

- TERMINATION_SUSPENSION
  - 계정/서비스 이용정지, 해지, 일시 중단, 종료 사유 및 절차, 해지 시 효과(데이터 삭제, 접근 차단 등)
  - 예: "약관 위반 시 사전 통지 없이 계정을 해지할 수 있습니다."

- MODIFICATION_TOS_CHANGES
  - 약관/요금/서비스 내용의 변경, 변경 공지 방법, 효력 발생 시점, 사용자의 동의 방식 등
  - 예: "당사는 필요 시 약관을 변경할 수 있으며, 변경 시 홈페이지에 공지합니다."

- DISPUTE_GOVERNING_LAW
  - 준거법, 관할법원, 국제재판관할, 분쟁 해결 방식(중재, 조정, 집단소송 포기, 관할지 제한 등)
  - 예: "본 약관은 대한민국 법률의 적용을 받습니다."

- THIRD_PARTY_SERVICE_ADS
  - 제3자 서비스/사이트 연동, 소셜 로그인, 외부 링크, 광고 노출, 제3자 약관/정책 적용 등
  - 예: "링크된 제3자 사이트에 대해서는 회사가 책임지지 않습니다."

- CONSUMER_RIGHTS_PROTECTION
  - 청약철회, 환급, 하자보증, 소비자 보호 법령 상 특별한 권리 부여, 고객센터/분쟁조정 지원 등
  - 예: "사용자는 구매 후 7일 이내에 청약을 철회할 수 있습니다."

- META_INFO_DEFINITIONS
  - 용어 정의(예: '회원', '서비스'의 정의), 문서 구조/목적 소개, 회사 정보/주소, 단순 안내 문구 등
  - 예: "이 약관에서 '회사'란 ㈜○○를 말합니다."

- OTHER
  - 위 어느 항목에도 뚜렷하게 속하지 않는 경우
  - 또는 여러 주제를 동시에 포함하지만 특정 카테고리가 우세하지 않을 때 최후의 보류 카테고리로 사용

[판단 규칙]
- 한 문장에는 하나의 category만 부여합니다 (multi-label 금지).
- 여러 주제가 섞인 경우, 문장의 "핵심 초점"이 되는 주제 기준으로 하나를 선택합니다.
  - 예: "유료 구독은 자동 갱신되며, 회사는 이에 대해 책임을 지지 않습니다."
    - 자동 결제 구조가 핵심이면 PAYMENT_PRICING_REFUND,
    - 광범위한 책임 면책이 핵심이면 LIABILITY_DISCLAIMER_LIMITATION.
- 개인정보 관련 내용이 조금이라도 포함되어 있고, 핵심이 데이터 처리/제공/보관이면 PRIVACY_DATA_COLLECTION을 우선합니다.
- 단순 정의/소개/구조 설명은 META_INFO_DEFINITIONS에 배정합니다.
- 애매할 때는 가장 관련성이 높은 카테고리를 보수적으로 선택하고,
  정말 결정하기 어렵다면 OTHER를 사용하십시오.
"""


    sentence_batches = [
        scored_sentences[i : i + batch_size]
        for i in range(0, len(scored_sentences), batch_size)
    ]

    def _categorize_batch(batch: List[Dict]) -> List[Dict]:
        message = json.dumps({"sentences": batch}, ensure_ascii=False)
        response = client.generate_response(system_instruction, message)
        parsed = _extract_json_fragment(response)

        batch_results = []
        for item in parsed:
            sentence = str(item.get("sentence", "")).strip()
            try:
                score = int(item.get("importance_score", 0))
            except Exception:
                score = 0
            batch_results.append(
                {
                    "input_index": item.get("input_index"),
                    "sentence": sentence,
                    "importance_score": score,
                    "category": item.get("category", "OTHER"),
                }
            )
        return batch_results

    all_results: List[Dict] = []
    with ThreadPoolExecutor(max_workers=len(sentence_batches)) as executor:
        futures = [executor.submit(_categorize_batch, batch) for batch in sentence_batches]
        for future in as_completed(futures):
            all_results.extend(future.result())

    return sorted(all_results, key=lambda x: x.get("input_index", 0))
