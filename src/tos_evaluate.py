import json
from typing import Dict, List

from llm_client import LLMClient


def _extract_json_fragment(text: str):
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

[목표]
1) 이 요약 조항이 일반 사용자에게 전반적으로 "good / neutral / bad" 중 어디에 해당하는지 분류합니다.
2) 공정성(fairness), 사용자 위험(risk), 투명성(transparency), 통제 가능성(control) 관점에서 각각 1~5점 점수를 매깁니다.
3) 왜 그렇게 판단했는지 간단한 근거를 한국어로 설명합니다.

[레이블 정의]
- good: 사용자 권리/보호를 강화하거나 회사/사용자 간 균형, 뚜렷한 이점, 중간 수준
- bad: 권리/프라이버시/금전적 이익을 과도하게 제한하거나 회사 쪽으로 심하게 기울어진 조항, 높은 위험
- 애매하면 neutral

[점수 스케일 정의] (각 1~5점, 정수)
- fairness_score: 1=매우 불공정, 3=보통, 5=매우 공정
- risk_score: 1=위험 거의 없음, 3=보통, 5=매우 높은 위험
- transparency_score: 1=매우 불명확, 3=보통, 5=매우 명확
- control_score: 1=통제 불가, 3=일부 통제, 5=충분한 통제

[레이블 결정 규칙]
- fairness_score가 낮고 risk_score가 높으면 bad
- fairness_score가 높고 risk_score가 낮으며 control_score가 높으면 good
- 나머지는 neutral, 애매하면 neutral

[출력 형식]
출력은 반드시 아래 JSON 객체 하나만 포함해야 합니다. (추가 텍스트 금지)

{
  "label": "good" | "neutral" | "bad",
  "fairness_score": 1 | 2 | 3 | 4 | 5,
  "risk_score": 1 | 2 | 3 | 4 | 5,
  "transparency_score": 1 | 2 | 3 | 4 | 5,
  "control_score": 1 | 2 | 3 | 4 | 5,
  "reasoning": "위 label을 선택한 근거를 한국어로 간단히 설명"
}
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

    labels = []
    clause_results = []
    for item in category_summaries:
        evaluation = evaluate_summary(item.get("summary", ""), client)
        label = evaluation.get("label", "neutral")
        fairness_score = evaluation.get("fairness_score", -1)
        risk_score = evaluation.get("risk_score", -1)
        transparency_score = evaluation.get("transparency_score", -1)
        control_score = evaluation.get("control_score", -1)
        reasoning = evaluation.get("reasoning", "error")
        category = item.get("category", "UNKNOWN")
        labels.append(label)

        clause_results.append(
            {
                "evaluation": label,
                "summarized_clause": item.get("summary", ""),
                "category": category,
                "fairness_score": fairness_score,
                "risk_score": risk_score,
                "transparency_score": transparency_score,
                "control_score": control_score,
                "reasoning": reasoning,
            }
        )

    overall = _calculate_overall_evaluation(labels)

    return {
        "overall_evaluation": overall,
        "evaluation_for_each_clause": clause_results,
    }
