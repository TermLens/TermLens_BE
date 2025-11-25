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
당신은 텍스트를 문장 단위로 나누는 도우미입니다.
- 한국어/영어 혼합 가능
- 문장 순서를 유지하고, 요약/병합/삭제하지 않습니다.
- 문장 끝의 마침표/기호를 유지합니다.
- 공백/줄바꿈은 다듬되 내용은 바꾸지 않습니다.
- 출력은 반드시 JSON 배열 한 개만 작성합니다(앞뒤 설명/코드블록/백틱 금지).
- 문장 내부의 큰따옴표(")와 역슬래시(\\)는 반드시 \\\" 와 \\\\ 로 이스케이프합니다.
- HTML 태그나 <>가 보이면 제거하거나 평문으로 변환해 JSON이 깨지지 않게 합니다.
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
