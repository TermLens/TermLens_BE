from collections import defaultdict
from typing import Dict, List

from llm_client import LLMClient


def summarize_by_category(categorized_sentences: List[Dict], client: LLMClient) -> List[Dict]:
    """
    중요 문장을 카테고리별로 묶어 요약합니다.
    """
    if not categorized_sentences:
        return []

    grouped = defaultdict(list)
    for item in categorized_sentences:
        grouped[item["category"]].append(item)

    system_instruction = """
당신은 약관 분석 전문가입니다.
각 카테고리별 중요 문장을 2~4문장 내외로 간결하게 요약하세요.
- 한국어로 작성
- 사용자 권리/의무/리스크 등 핵심 포인트 중심
- 중요도 점수는 참고만 하고 결과 문장에는 숫자를 넣지 않습니다.
"""

    summaries = []
    for category, items in grouped.items():
        message_lines = [
            f"카테고리: {category}",
            "중요 문장 목록:",
        ]
        for idx, entry in enumerate(items, start=1):
            message_lines.append(
                f"{idx}. 중요도 {entry.get('importance_score')}: {entry.get('sentence')}"
            )

        message = "\n".join(message_lines)
        summary = client.generate_response(system_instruction, message).strip()
        summaries.append(
            {
                "category": category,
                "summary": summary,
                "sentences": items,
            }
        )

    return summaries
