import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

from json_utils import extract_json_fragment as _extract_json_fragment
from llm_client import LLMClient


def score_sentence_importance(sentences: List[str], client: LLMClient) -> List[Dict]:
    """
    중요도 1~5로 문장별 점수를 산출한다.
    """
    if not sentences:
        return []

    batch_size = 5
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
        response = client.generate_response(system_instruction, message, model_size="small")
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

    batch_size = 5
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

- 계정 관리 및 가입 조건
  - 서비스를 누가 가입 및 이용할 수 있는지(연령, 거주 국가), 비밀번호/로그인 정보 관리 방식(비밀번호 변경, 계정 양도 금지 조항도 포함), 휴면 계정 및 장기 미사용 계정 처리 방식
  - 예: "당사 서비스는 만 14세 미만 사용자는 이용할 수 없습니다."

- 결제 및 환불 규정
  - 돈 관련해서 사용자가 반드시 알아야 하는 내용(요금, 수수료, 결제 수단, 환불 정책, 무료 체험 후 자동 유료 전환 등)
  - 예: “디지털 콘텐츠의 특성상 다운로드가 시작된 이후에는 청약철회 및 환불이 불가능합니다.”

- 개인정보 및 데이터 수집
  - 수집하는 데이터 항목(이름, 이메일, 결제정보, 기기 정보, 위치 등), 데이터 이용 목적, 제3자 제공·국외 이전 및 광고 네트워크·분석 도구와의 데이터 공유 여부, 보관 기간 및 파기 시점, 이용자의 데이터 권리(열람, 정정, 삭제, 처리 정지 요청) 등
  - 예: "당사는 맞춤형 광고 제공을 위해 귀하의 서비스 이용 정보를 제휴 광고사와 공유할 수 있습니다."

- 이용자 콘텐츠의 라이선스
  - 이용자가 올리는 게시물/사진/동영상 등의 소유권, 회사에 부여되는 라이선스 범위, 2차적 저작물 생성, 게시물 삭제/비공개, 저작권 침해 관련 내용
  - 예: "회원이 게시한 콘텐츠의 저작권은 회원에게 있으나, 회사는 이를 전 세계적으로 무상 이용할 수 있는 라이선스를 가집니다."

- 금지사항
  - 서비스 사용 시 금지행위(불법행위, 스팸, 해킹, 자동화 수단, 타인 괴롭힘, 명예훼손, 지식재산권 침해 등) 및 위반 시 경고·기능 제한·차단 등
  - 예: "스팸 메시지 발송, 무단 광고 게시 등의 행위를 하는 경우, 회사는 관련 게시물을 삭제하거나 서비스 이용을 제한할 수 있습니다."

- 약관 및 서비스 변경
  - 약관/정책/가격/서비스 기능 등을 일방적으로 변경할 수 있는 권한, 변경 공지 방식, 효력 발생 시점, 변경에 동의하지 않을 경우 처리(해지 등)
  - 예: "회사는 관련 법령을 위반하지 않는 범위에서 이 약관을 수시로 변경할 수 있으며, 변경된 약관은 홈페이지에 공지한 날로부터 7일 후 효력이 발생합니다."

- 책임 제한 및 면책
  - 서비스가 잘못되거나, 데이터가 날아가거나, 피해가 발생했을 때 회사가 어디까지 책임지는지 (혹은 안 지는지), 사용자가 회사에 배상해야 하는 의무 등을 모으는 카테고리
  - 예: "어떠한 경우에도 당사는 이용자에게 발생한 간접적, 우발적, 특별 또는 결과적 손해에 대해 책임을 지지 않습니다."

- 분쟁 해결 및 준거법
  - 문제가 생겼을 때 어떤 국가/지역의 법을 적용하는지(준거법), 어느 법원이 관할하는지(관할법원), 중재·조정·집단소송 포기 등 분쟁 해결 방식
  - 예: "본 약관과 관련된 분쟁은 대한민국 법률을 준거법으로 하며, 서울중앙지방법원을 전속 관할로 합니다."

- 제3자 서비스
  - 소셜 로그인, 외부 서비스·앱 연동, 제3자 약관/정책 적용, 서비스 내 광고·스폰서 콘텐츠, 외부 사이트 링크 및 그에 대한 책임 제한 등
  - 예: "링크된 제3자 웹사이트의 내용과 개인정보 처리에 대해서는 회사가 책임지지 않습니다."

- 기타
  - 위 어느 category에도 뚜렷하게 속하지 않는 조항
  - 여러 주제를 동시에 다루어 특정 category 하나를 우선하기 어렵거나, 단순 안내·형식적 문구 등 위 핵심 category와 직접적으로 관련되지 않은 경우

[판단 규칙]
- 한 문장에는 하나의 category만 부여합니다 (multi-label 금지).
- 여러 주제가 섞인 경우, 문장의 "핵심 초점"이 되는 주제 기준으로 하나를 선택합니다.
  - 예: "유료 구독은 자동 갱신되며, 회사는 이에 대해 책임을 지지 않습니다."
    - 자동 결제 구조가 핵심이면 "결제 및 환불 규정",
    - 전반적인 책임 부인이 중심이면 → "책임 제한 및 면책"
- 개인정보/데이터 처리(수집·이용·보관·제3자 제공·쿠키 등)가 문장의 핵심이면, 가능한 한 "개인정보 및 데이터 수집"으로 분류합니다.
- 애매할 때는 가장 관련성이 높은 category를 보수적으로 선택하고, 정말 어느 쪽으로도 분류하기 어려운 경우에만 "기타"를 사용하십시오.
"""


    sentence_batches = [
        scored_sentences[i : i + batch_size]
        for i in range(0, len(scored_sentences), batch_size)
    ]

    def _categorize_batch(batch: List[Dict]) -> List[Dict]:
        message = json.dumps({"sentences": batch}, ensure_ascii=False)
        response = client.generate_response(system_instruction, message, model_size="small")
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
