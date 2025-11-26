from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

from json_utils import extract_json_fragment as _extract_json_fragment
from llm_client import LLMClient


def _calculate_overall_evaluation(labels: List[str]) -> str:
    """
    good/neutral/bad 라벨을 점수화해 최종 등급(A~E)을 계산한다.
    점수 매핑: good=+1, neutral=0, bad=-1
    """
    if not labels:
        return "E"

    score_map = {"good": 1, "neutral": 0, "bad": -1}
    avg_score = sum(score_map.get(label, 0) for label in labels) / len(labels)

    if avg_score >= 0.8:
        return "A"  # 거의 대부분이 사용자 친화적
    if avg_score >= 0.5:
        return "B"  # good 우세, bad 적음
    if avg_score >= 0.0:
        return "C"  # 중립적이거나 균형
    if avg_score >= -0.5:
        return "D"  # bad가 다소 많음
    return "E"  # bad가 대부분


def evaluate_summary(summary: str, client: LLMClient) -> Dict:
    system_instruction = """
[시스템 지시]
당신은 온라인 서비스 이용약관이 사용자에게 얼마나 유리한지/불리한지를 평가하는 전문가입니다.
입력으로 하나의 요약된 조항 설명(한국어)을 받습니다.
이 요약은 이미 여러 원문 조항을 이해하기 쉽게 풀어쓴 것입니다.

[입력 형식]
- 사용자 메시지에는 "[입력 요약 조항]\\n<요약 텍스트>" 형태로 한 개의 요약 문단이 주어집니다.

[출력 형식]
- 아래 JSON 객체 **한 개만** 출력해야 합니다.
- 키는 반드시 아래 순서를 지키십시오. (score → reasoning → label 순서)
- JSON 앞뒤에 설명/코드블록/주석을 넣지 마십시오.
- label은 반드시 위 네 개 score와 reasoning을 **먼저** 결정한 뒤에, 그 결과를 바탕으로 마지막에 선택해야 합니다.

{
  "fairness_score": 1 | 2 | 3 | 4 | 5,
  "risk_score": 1 | 2 | 3 | 4 | 5,
  "transparency_score": 1 | 2 | 3 | 4 | 5,
  "control_score": 1 | 2 | 3 | 4 | 5,
  "reasoning": "위 label을 선택한 근거를 한국어로 간단히 설명",
  "label": "good" | "neutral" | "bad"
}

[sub score 정의: 모두 1~5점]
각 점수는 **독립적으로** 먼저 평가해야 합니다. 점수를 정한 뒤에 reasoning과 label을 결정합니다.

- fairness_score (공정성)
  - 1: 회사에 일방적으로 유리하고 매우 불공정
  - 2: 회사 쪽에 꽤 유리하며, 사용자는 불리한 조건을 상당 부분 감수해야 함
  - 3: 회사와 사용자의 이해관계가 어느 정도 균형을 이루는 보통 수준
  - 4: 대체로 사용자에게 공정하고, 불리한 요소가 제한적
  - 5: 사용자 보호에 신경 쓰고, 조건이 매우 공정/사용자 친화적

- risk_score (사용자에게 돌아가는 위험/부담)
  - 1: 사용자에게 추가 위험이 거의 없음
  - 2: 작은 수준의 위험/불편만 발생 가능
  - 3: 일반적인 수준의 위험/책임(표준 약관에서 흔히 볼 수 있는 수준)
  - 4: 금전적 손실, 계정/데이터 손실 등 의미 있는 위험이 발생할 수 있음
  - 5: 큰 금전적 손실, 광범위한 데이터 오남용, 계정 영구 정지 등 심각한 위험이 사용자에게 크게 전가됨

- transparency_score (내용의 명확성과 투명성)
  - 1: 조건이 모호하고, 숨겨진 단서·예외가 많아 이해하기 어려움
  - 2: 중요한 부분이 애매하거나 빠져 있어 오해의 여지가 큼
  - 3: 대체로 이해 가능하지만 일부 애매한 부분이 있음
  - 4: 대부분 명확하게 설명되어 있고, 중요한 조건·예외가 드러나 있음
  - 5: 조건, 범위, 예외, 절차가 매우 명확히 설명되어 일반 사용자도 쉽게 이해 가능

- control_score (사용자 통제/선택 가능성)
  - 1: 사용자가 사실상 선택권이 없거나, 통제 수단이 거의 없음
  - 2: 일부 통제 수단이 있으나 매우 제한적이거나 현실적으로 사용하기 어려움
  - 3: 기본적인 통제(설정 변경, 해지, 동의 철회 등)가 가능하지만 조건이 붙어 있음
  - 4: 사용자가 꽤 많은 통제권/해지권/거부권을 가지며, 절차도 비교적 합리적
  - 5: 사용자가 충분한 선택권·거부권·해지권을 가지고, 간단한 절차로 스스로 통제할 수 있음

[레이블 정의]
- good:
  - 사용자의 권리·보호를 강화하거나 회사/사용자 간 균형을 맞추는 조항
  - 회사의 책임을 명확히 하고, 사용자에게 충분한 선택권/통제권/고지 의무를 부여하는 조항
  - 위험 요소가 있더라도, 사용자에게 합리적인 통제 수단(동의/거절/해지/환불/이의 제기 등)이 제공되는 경우

- neutral:
  - 업계에서 일반적으로 볼 수 있는 평균적인 수준의 조항
  - 사용자에게 뚜렷한 큰 이익도, 과도한 불이익도 주지 않는 경우
  - 긍정적/부정적 요소가 섞여 전반적으로 중간 수준으로 보이는 경우

- bad:
  - 사용자의 권리/프라이버시/금전적 이익을 과도하게 제한하거나 회사 쪽으로 심하게 기울어진 조항
  - 높은 위험(광범위한 책임 면책, 일방적 해지/정지/변경, 과도한 데이터 수집·공유, 자동 결제 함정 등)을
    사용자에게 전가하는 조항
  - 사용자에게 충분한 정보·통제권·동의 기회를 제공하지 않는 경우

[평가 절차 (반드시 이 순서를 따르십시오)]
1단계: 점수 결정
  - 요약 조항을 읽고, 위 정의에 따라
    fairness_score, risk_score, transparency_score, control_score 네 개의 점수를 **먼저** 정합니다.

2단계: reasoning 작성
  - 방금 정한 네 점수를 바탕으로,
    - 왜 그런 공정성/위험/투명성/통제 점수를 줬는지
    - 네 개 점수를 바탕으로 label을 어떻게 결정했는지
    를 2~4문장 정도의 한국어로 설명합니다.
  - reasoning은 반드시 위 네 점수와 논리적으로 일관되게 작성해야 합니다.

3단계: label 결정
  - 이미 정한 네 개 점수와 reasoning을 이용해 아래 규칙에 따라 label을 최종적으로 선택합니다.
  - label을 먼저 가정한 뒤 점수를 맞추지 말고, **점수를 먼저 정한 뒤 label을 결정**해야 합니다.
---
이 지침을 따라,
1) 네 개 score를 먼저 정하고,
2) 그 score를 근거로 reasoning을 작성한 뒤,
3) 마지막으로 label을 결정하여,
위에서 제시한 JSON 형식 하나만 출력하십시오.
"""

    message = f"[입력 요약 조항]\n{summary}"
    response = client.generate_response(system_instruction, message)

    return _extract_json_fragment(response)


def evaluate_category_summaries(
    category_summaries: List[Dict], client: LLMClient
) -> Dict:
    """
    카테고리별 요약을 평가하고 전체 약관 등급(A~E)을 계산한다.
    """
    if not category_summaries:
        return {"overall_evaluation": "E", "evaluation_for_each_clause": []}

    def _evaluate_item(item: Dict) -> Dict:
        evaluation = evaluate_summary(item.get("summary", ""), client)
        label = evaluation.get("label", "neutral")
        return {
            "label": label,
            "result": {
                "evaluation": label,
                "summarized_clause": item.get("summary", ""),
                "category": item.get("category", "UNKNOWN"),
                "fairness_score": evaluation.get("fairness_score", -1),
                "risk_score": evaluation.get("risk_score", -1),
                "transparency_score": evaluation.get("transparency_score", -1),
                "control_score": evaluation.get("control_score", -1),
                "reasoning": evaluation.get("reasoning", "error"),
            },
        }

    labels = []
    clause_results = []
    with ThreadPoolExecutor(max_workers=len(category_summaries)) as executor:
        futures = [executor.submit(_evaluate_item, item) for item in category_summaries]
        for future in as_completed(futures):
            data = future.result()
            labels.append(data["label"])
            clause_results.append(data["result"])

    overall = _calculate_overall_evaluation(labels)

    return {
        "overall_evaluation": overall,
        "evaluation_for_each_clause": clause_results,
    }
