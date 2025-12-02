import json
import html
import re
from typing import List, Optional, Tuple

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
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ ]*\n[ ]*", "\n", text)
    return text.strip()


def _is_korean_text(text: str) -> bool:
    hangul = len(re.findall(r"[가-힣]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    if hangul == 0 and latin == 0:
        return True
    if hangul == 0:
        return False
    if latin == 0:
        return True
    return hangul / (hangul + latin) >= 0.3


def _next_significant_char(text: str, start: int) -> Tuple[Optional[str], int]:
    idx = start
    while idx < len(text):
        ch = text[idx]
        if ch in " \t\r\f\v":
            idx += 1
            continue
        if ch in '")]}\u201d\u2019':
            idx += 1
            continue
        return ch, idx
    return None, len(text)


def _prev_significant_char(text: str, start: int) -> Tuple[Optional[str], int]:
    idx = start
    while idx >= 0:
        ch = text[idx]
        if ch.isspace():
            idx -= 1
            continue
        return ch, idx
    return None, -1


_BULLET_PATTERN = re.compile(
    r"^\s*(?:[\-\*\u2022\u2023\u25E6\u25AA\u25CF\u00B7\u25B6\u25B8\u25C0\u25C2\u25BA\u25C6\u25C7\u25A0\u25A1\u2605\u203B]"
    r"|\d+[.)]|[A-Za-z가-힣][.)])\s+"
)

_SF_EXCEPTION_SUFFIXES = {
    "no",
    "vol",
    "p",
    "pp",
    "page",
    "al",
    "ed",
    "eds",
    "항",
    "조",
    "호",
    "절",
    "권",
    "쪽",
}

_TITLE_ABBREVIATIONS = {"mr", "mrs", "ms", "dr", "prof", "sr", "jr"}
_COMMON_ABBREVIATIONS = {
    "e.g",
    "i.e",
    "etc",
    "cf",
    "ca",
    "vs",
    "fig",
    "eq",
    "dept",
    "inc",
    "ltd",
    "co",
    "corp",
    "st",
}


def _is_decimal(text: str, idx: int) -> bool:
    prev_ch, _ = _prev_significant_char(text, idx - 1)
    next_ch, _ = _next_significant_char(text, idx + 1)
    return bool(prev_ch and next_ch and prev_ch.isdigit() and next_ch.isdigit())


def _is_ellipsis(text: str, idx: int) -> bool:
    next_ch = text[idx + 1] if idx + 1 < len(text) else ""
    return next_ch == "."


def _extract_token_before(text: str, idx: int) -> str:
    window_start = max(0, idx - 15)
    snippet = text[window_start : idx + 1]
    match = re.search(r"([A-Za-z가-힣0-9㈜]+)[.?!…]*$", snippet)
    if not match:
        return ""
    return match.group(1)


def _is_abbreviation(text: str, idx: int, language: str, next_char: Optional[str]) -> bool:
    raw_token = _extract_token_before(text, idx).strip(".")
    token = raw_token.lower()
    if not token:
        return False

    # U.S.A. 혹은 단일 대문자 약어 연속 처리
    if len(raw_token) == 1 and raw_token.isalpha() and raw_token.isupper():
        if idx + 2 < len(text) and text[idx + 2] == ".":
            return True

    if token.endswith(tuple(_SF_EXCEPTION_SUFFIXES)):
        return True

    if token in _TITLE_ABBREVIATIONS:
        return True

    if token in _COMMON_ABBREVIATIONS:
        if next_char and next_char.islower():
            return True
    if token in {"p", "pp", "no", "vol", "page"}:
        if next_char and (next_char.isdigit() or next_char in {" ", "\u00a0"}):
            return True

    if language == "ko" and token in {"㈜", "주식회사"}:
        return True

    return False


def _looks_like_bullet_start(text: str, start: int) -> bool:
    return bool(_BULLET_PATTERN.match(text[start:]))


def _should_split_on_newline(text: str, idx: int) -> bool:
    if idx + 1 < len(text) and text[idx + 1] == "\n":
        return True
    return _looks_like_bullet_start(text, idx + 1)


def _should_split_on_punctuation(text: str, idx: int, language: str) -> bool:
    ch = text[idx]
    if ch not in {".", "?", "!", "…", "。", "！", "？"}:
        return False

    if ch == "." and _is_decimal(text, idx):
        return False

    if ch == "." and _is_ellipsis(text, idx):
        return False

    next_ch, _ = _next_significant_char(text, idx + 1)
    if _is_abbreviation(text, idx, language, next_ch):
        return False

    # `?` 혹은 `!` 뒤에 오는 마침표 대비
    if ch in {"?", "!"} and next_ch == ".":
        return True

    # 다음에 오는 유의미 문자가 없거나, 문장 시작 형태라면 분할
    if next_ch is None:
        return True

    if next_ch == "\n":
        return True

    if _looks_like_bullet_start(text, idx + 1):
        return True

    if language == "ko":
        return bool(re.match(r"[가-힣0-9A-Z\"'“‘(]", next_ch))
    return bool(re.match(r"[A-Z0-9\"'“‘(]", next_ch))


def _split_by_rules(text: str, language: str) -> List[str]:
    sentences: List[str] = []
    buffer: List[str] = []
    length = len(text)

    for idx, ch in enumerate(text):
        buffer.append(ch)

        split = False
        if ch == "\n":
            split = _should_split_on_newline(text, idx)
        elif _should_split_on_punctuation(text, idx, language):
            split = True

        if split:
            sentence = "".join(buffer).strip()
            if sentence:
                sentences.append(sentence)
            buffer = []

    tail = "".join(buffer).strip()
    if tail:
        sentences.append(tail)
    return sentences


def split_sentences_block(block: str, client: Optional[LLMClient] = None) -> List[str]:
    """
    약관 블록을 규칙 기반으로 문장 단위 분리한다. (LLM 비사용)
    """
    print(f"원본 블록 길이: {len(block)}")
    block = _normalize_block(block)
    print(f"정규화된 블록 길이: {len(block)}")
    if not block:
        return []

    language = "ko" if _is_korean_text(block) else "en"
    sentences = _split_by_rules(block, language)
    # print("rule-base 분리 후 문장들:")
    # print(sentences)
    return sentences
