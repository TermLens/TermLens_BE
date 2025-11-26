import json
import html
import re
from typing import List
from llm_client import LLMClient


def _extract_json_array(text: str) -> List[str]:
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("문장 배열 JSON을 찾지 못했습니다.")

    raw_array = text[start : end + 1]

    # 1차: 정상 JSON 파싱 시도
    try:
        return json.loads(raw_array)
    except json.JSONDecodeError:
        pass

    # 2차: 코드블록, 불필요한 기호 제거 후 완화된 파싱
    cleaned = re.sub(r"^```(?:json)?", "", raw_array.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"```$", "", cleaned).strip()

    # 대괄호 제거 후 줄 또는 쉼표 기준 분리
    trimmed = cleaned.strip()
    if trimmed.startswith("["):
        trimmed = trimmed[1:]
    if trimmed.endswith("]"):
        trimmed = trimmed[:-1]

    candidates = re.split(r"\s*\n\s*|\s*,\s*", trimmed)
    sentences = []
    for item in candidates:
        s = item.strip().lstrip("-•").strip()
        s = s.strip('"').strip("'")
        if s:
            sentences.append(s)

    if not sentences:
        raise ValueError("문장 배열 JSON 파싱에 실패했습니다.")

    return sentences


def _normalize_block(block: str) -> str:
    """
    HTML 태그/엔티티 제거 및 공백/따옴표 정규화로 LLM 입력을 정돈한다.
    """
    text = html.unescape(block)
    text = re.sub(r"<\s*br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[“”]", '"', text)
    text = re.sub(r"[‘’]", "'", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences_block(block: str, client: LLMClient) -> List[str]:
    """
    LLM을 사용해 약관 블록 텍스트를 문장 단위로 분리한다.
    """
    print(f"원본 블록 길이: {len(block)}")
    block = _normalize_block(block)
    print(f"정규화된 블록 길이: {len(block)}")
    if not block:
        return []

    system_instruction = """
당신은 온라인 서비스 이용약관 텍스트를 '조항 단위 문장 리스트'로 나누는 전문 분할기입니다.

[입력]
- 긴 약관 텍스트가 한 번에 들어옵니다.
- 줄바꿈, 불필요한 공백, 일부 특수기호가 섞여 있을 수 있습니다.

[출력 형식]
- 반드시 JSON 배열 하나만 출력합니다. 예:
  ["문장1", "문장2", "문장3"]
- JSON 배열 바깥에 어떤 설명, 주석, 코드블록, 텍스트도 쓰지 마십시오.
- 각 요소는 문자열이어야 하며, 문장 내부의 큰따옴표(")와 역슬래시(\\)는 반드시 \\\" 와 \\\\ 로 이스케이프합니다.

[분할 원칙 – 커버리지]
- 입력 텍스트에 등장하는 의미 있는 내용은 모두 보존해야 합니다.
- 요약, 의역, 재작성 금지: 원문의 의미를 삭제하거나 새 내용을 만들어내지 마십시오.
- 문장 병합은 "서로 바로 인접하고, 하나의 조항을 이루는 연속된 내용"끼리만 허용합니다.
- 같은 텍스트를 두 문장에 중복해서 넣지 마십시오.

[분할 단위 – '조항 단위 문장']
- 한 출력 요소는 '사용자가 한 번에 읽고 이해할 수 있는 하나의 조항'을 담도록 합니다.

[레이아웃/리스트 처리]
- 불릿/번호 리스트가 있는 경우:
  - 각 항목이 독립된 의무/권리/제한을 담고 있으면 항목마다 별도의 요소로 분리합니다.
  - 하나의 항목 안에 여러 문장이 있을 경우, 의미가 크게 달라지지 않는다면 하나의 요소로 둬도 됩니다.
- 표/간단한 항목 나열은 자연스러운 문장 형태로 이어 붙여 하나의 요소로 만들어도 됩니다.
  (단, 내용 자체는 삭제하지 마십시오.)

[전처리 규칙]
- HTML 태그, angle bracket(< >) 등은 제거하거나 평문으로만 남기고, JSON이 깨지지 않게 합니다.
- 의미 없는 장식용 특수기호(예: "****", "------")는 제거해도 됩니다.

[품질 규칙]
- 문장 순서를 입력 순서 그대로 유지합니다.
- 가능한 한 각 요소는 지나치게 길지 않게 나눕니다.
- 의미를 바꾸는 재구성/요약/축약은 절대 하지 마십시오.

위 지침을 따른 결과만을, JSON 문자열 배열 하나로 출력하십시오.
"""


    response = client.generate_response(system_instruction, block)
    print("LLM 분리 전, 정규화된 블록:")
    print(f"{block}")
    print("LLM 분리 직후, 응답")
    print(f"{response}")

    sentences = _extract_json_array(response)
    print("json_array 파싱 후, 문장들:")
    print(f"{sentences}")
    return [str(s).strip() for s in sentences if str(s).strip()]
