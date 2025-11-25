import json
from typing import List
from llm_client import LLMClient


def _extract_json_array(text: str) -> List[str]:
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end < start:
        raise ValueError("문장 배열 JSON을 찾지 못했습니다.")
    return json.loads(text[start : end + 1])


def split_sentences_block(block: str, client: LLMClient) -> List[str]:
    """
    LLM을 사용해 약관 블록 텍스트를 문장 단위로 분리한다.
    """
    block = block.strip()
    if not block:
        return []

    system_instruction = """
당신은 텍스트를 문장 단위로 나누는 도우미입니다.
- 한국어/영어 혼합 가능
- 문장 순서를 유지하고, 요약/병합/삭제하지 않습니다.
- 문장 끝의 마침표/기호를 유지합니다.
- 공백/줄바꿈은 다듬되 내용은 바꾸지 않습니다.
출력은 반드시 JSON 배열 형식으로만 작성합니다.
"""

    response = client.generate_response(system_instruction, block)

    sentences = _extract_json_array(response)
    return [str(s).strip() for s in sentences if str(s).strip()]
