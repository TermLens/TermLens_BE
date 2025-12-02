import json
import re
from typing import Any


_CODE_BLOCK_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)
_INVALID_ESCAPE_RE = re.compile(r'(?<!\\)\\(?!["\\/bfnrtu])')


def _strip_code_block(text: str) -> str:
    """코드블록(`````, ```json````) 안에 JSON이 있으면 그 내용만 추출한다."""
    match = _CODE_BLOCK_RE.search(text)
    if match:
        return match.group(1)
    return text


def _find_json_fragment(text: str) -> str:
    """첫 번째 JSON 조각을 균형 맞는 괄호 기준으로 잘라낸다."""
    obj_start = text.find("{")
    arr_start = text.find("[")
    starts = [(i, ch) for i, ch in ((obj_start, "{"), (arr_start, "[")) if i != -1]
    if not starts:
        raise ValueError("JSON 시작 구분자를 찾지 못했습니다.")

    start_idx, start_char = min(starts, key=lambda x: x[0])
    closing_map = {"{": "}", "[": "]"}
    stack = []
    in_string = False
    escaped = False
    end_idx = None

    for idx in range(start_idx, len(text)):
        ch = text[idx]

        if in_string:
            if escaped:
                escaped = False
                continue
            if ch == "\\":
                escaped = True
                continue
            if ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue

        if ch in "{[":
            stack.append(ch)
            continue

        if ch in "}]":
            if not stack:
                continue
            opener = stack.pop()
            if closing_map[opener] != ch:
                # 괄호 종류가 맞지 않으면 무시하고 계속 탐색
                continue
            if not stack:
                end_idx = idx
                break

    fragment = text[start_idx : end_idx + 1 if end_idx is not None else len(text)]
    if stack:
        # 닫히지 않은 괄호를 보정
        missing = "".join(closing_map[ch] for ch in reversed(stack))
        fragment += missing

    return fragment


def _escape_invalid_backslashes(text: str) -> str:
    """잘못된 역슬래시 시퀀스를 이스케이프해 JSON 파싱 오류를 줄인다."""
    return _INVALID_ESCAPE_RE.sub(r"\\\\", text)


def extract_json_fragment(text: str) -> Any:
    """
    LLM 응답에서 첫 번째 JSON 조각(객체 또는 배열)을 추출해 파싱한다.
    - 코드블록(`````, ```json````) 제거
    - 괄호 균형을 맞추어 닫힘 기호가 빠진 경우 보정
    - 잘못된 역슬래시 시퀀스를 보정
    """
    if text is None:
        raise ValueError("LLM 응답이 비어 있어 JSON을 찾지 못했습니다.")

    cleaned = _strip_code_block(text.strip())
    fragment = _find_json_fragment(cleaned)

    last_error = None
    for candidate in (fragment, _escape_invalid_backslashes(fragment)):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as err:
            last_error = err
            continue
    
    print("CLEANED:", cleaned)
    print("FRAGMENT:", fragment)
    print("FRAGMENT repr:", repr(fragment))
    print("Failed JSON text:", text) # 디버깅용 출력
    raise ValueError(f"JSON 파싱에 실패했습니다: {last_error}")