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
- 긴 약관 텍스트 전체가 한 번에 들어옵니다.
- 줄바꿈, 공백, 특수기호, HTML, 머리말/꼬리말 등이 섞여 있을 수 있습니다.
- 그래도 **내용을 고치지 말고** 그대로 문장 경계만 찾아서 나누어야 합니다.

[출력 형식]
- 반드시 JSON 배열 하나만 출력합니다. 예:
  ["문장1", "문장2", "문장3"]
- JSON 배열 바깥에는 어떤 설명, 주석, 코드블록, 텍스트도 쓰지 마십시오.
- 각 요소는 문자열이어야 하며, 문장 내부의 큰따옴표(")와 역슬래시(\\)는 반드시 \\\" 와 \\\\ 로 이스케이프합니다.
- 각 요소 문자열의 **앞뒤 불필요한 공백만** 제거할 수 있습니다. 문장 내부의 공백/줄바꿈/기호는 가능한 한 그대로 둡니다.

[분할 원칙 – 내용 보존]
- 입력 텍스트에 등장하는 **모든 내용이 출력 어딘가에 그대로 포함**되어야 합니다.
- **요약 금지**: 문장을 줄이거나 압축하지 마십시오.
- **의역 금지**: 표현을 더 쉬운 말로 바꾸지 마십시오.
- **재작성 금지**: 문장 구조를 바꾸지 마십시오.
- **삭제 금지**: 의미 있는 텍스트(단어, 숫자, 문장부호 등)를 삭제하지 마십시오.
- **추가 금지**: 원문에 없는 단어/문장/기호를 새로 만들지 마십시오.
- 한 출력 요소는 반드시 **입력 텍스트의 연속된 일부(substring)** 여야 합니다.
  - 즉, 출력에 들어가는 글자 순서는 항상 원문 순서와 같아야 합니다.
  - 원문에 없는 글자 조합을 만들지 마세요.

[분할 단위 – 문장]
- 한 출력 요소는 사용자가 한 번에 읽을 수 있는 **하나의 문장**을 담도록 합니다.
- 일반적으로 문장은 다음과 같은 기호를 기준으로 나눕니다.
  - 마침표/물음표/느낌표: `.`, `?`, `!`, `.`(영문), `…` 등
  - 한국어의 종결 표현(예: "합니다.", "됩니다.", "입니다.", "않습니다." 등) 뒤의 마침표
- 단, 아래 원칙을 지킵니다.
  - 줄바꿈이 있어도, 문장 중간에 불필요하게 끊기지 않는다면 **하나의 문장으로 유지**해도 됩니다.
  - 문장이 너무 길어도 **내용을 자르기 위해 임의로 요약/삭제하지 마십시오.** 오직 문장 경계에서만 자릅니다.

[레이아웃/리스트 처리]
- 불릿/번호 리스트가 있는 경우:
  - 각 항목(한 줄/한 문단)이 완결된 문장이라면 **각 항목을 하나의 요소**로 둡니다.
  - 한 항목 안에 여러 문장이 있으면, 가능한 한 **원문 문장 부호 기준**으로 여러 요소로 나눕니다.
- 표나 구조화된 텍스트가 있어도:
  - 내용을 재구성/합치기/풀어서 설명하지 말고,
  - 원문에서 보이는 순서를 따라 문장 경계만 기준으로 자릅니다.

[전처리 규칙]
- 이 단계에서는 **전처리를 최대한 하지 않습니다.**
  - HTML 태그, angle bracket(< >), 특수문자 등이 있어도 삭제하거나 바꾸지 말고 그대로 둡니다.
  - 다만 JSON이 깨지지 않도록 필요한 경우에만 이스케이프(\\\" , \\\\) 만 적용합니다.
- 의미 없는 장식용 특수기호(예: "****", "------")도 **입력에 있으면 그대로 남겨둡니다.**
  - 별도의 정리/삭제를 하지 않습니다.

[품질 규칙]
- 문장 순서는 **입력 순서 그대로** 유지합니다.
- 어떤 부분도 빠지지 않도록, 원문 전체가 문장 리스트로 덮이도록 분할합니다.
- 의미를 바꾸는 재구성/요약/축약/정렬 변경은 절대 하지 마십시오.

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
