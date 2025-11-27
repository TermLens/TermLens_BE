from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
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
당신은 온라인 서비스 이용약관을 일반 사용자가 이해하기 쉽게 설명하는 약관 분석 전문가입니다.

[입력 형식]
- 사용자 메시지에는
  - "카테고리: <CATEGORY_KEY>"
  - 그 아래에 "중요 문장 목록:" 과
    "번호. 중요도 <score>: <문장>" 형식의 여러 줄이 주어집니다.
- 중요도 점수는 4~5 중 하나이며, 숫자가 클수록 더 중요한 문장입니다.

[출력 목표]
- 해당 category에 대한 핵심 내용을 2~4문장 내외의 한국어 요약으로 작성합니다.
- 요약은 하나의 짧은 단락 형태로 작성하고, "요약:" 같은 머리말은 붙이지 마십시오.
- 일반 사용자가 읽을 때 이해하기 쉬운 자연스러운 문장으로 설명합니다.
- 법적 의미(권리/의무/책임/위험, 자동 결제, 계정 정지, 데이터 공유 등)를 축소하거나 왜곡하지 마십시오.

[중요도 활용 규칙]
- importance_score가 높을수록 요약에서 더 큰 비중을 두어 반영합니다.
  - 중요도 5: 반드시 요약에 핵심 내용이 포함되도록 합니다 (최우선).
  - 중요도 4: 필요하면 요약에 반영하되, 핵심 내용 위주로 압축하고 쓸모없는 내용이면 과감히 생략합니다.
- 모든 문장을 기계적으로 나열하지 말고,
  "사용자가 반드시 알아야 하는 포인트(중요도 4~5)"를 중심으로 구조화된 설명을 만드십시오.

[요약 스타일]
- 한국어로 작성하되, account, subscription, cookie, IP, ToS 등 영어 용어는 그대로 사용해도 됩니다.
- bullet/번호 리스트 대신 자연스러운 서술형 문장으로 요약합니다.
- 중복되는 내용은 하나의 문장으로 합쳐 정리합니다.
- 위험/제한/면책/자동갱신/데이터 제공 등 사용자가 특히 신경 써야 할 요소는 가능한 한 명시적으로 적어줍니다.
- "회사 입장" 위주가 아니라 "사용자가 무엇을 알게 되는지/어떤 영향을 받는지" 관점에서 설명합니다.

출력에는 위와 같은 한글 요약 문단만 포함하고, 다른 설명 문구는 추가하지 마십시오.
"""


    def _summarize_category(category: str, items: List[Dict]) -> Dict:
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

        # 모델이 "요약:" 머리글을 덧붙이는 경우 이후 텍스트만 사용
        marker = "요약:\n\n"
        marker_idx = summary.find(marker)
        if marker_idx != -1:
            summary = summary[marker_idx + len(marker):].strip()

        return {
            "category": category,
            "summary": summary,
            "sentences": items,
        }

    summaries: List[Dict] = []
    categories = list(grouped.items())
    with ThreadPoolExecutor(max_workers=len(categories) or 1) as executor:
        futures = [
            executor.submit(_summarize_category, category, items)
            for category, items in categories
        ]
        for future in as_completed(futures):
            summaries.append(future.result())

    return summaries
