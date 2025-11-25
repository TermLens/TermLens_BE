import re
from typing import List

import kss
import spacy
from spacy.lang.en import English

_nlp_en = None


def _get_english_model():
    """
    Load an English sentence tokenizer. Falls back to a lightweight sentencizer
    if the full en_core_web_sm model is unavailable.
    """
    global _nlp_en
    if _nlp_en is not None:
        return _nlp_en

    try:
        _nlp_en = spacy.load("en_core_web_sm")
    except Exception:
        # Fallback to a minimal pipeline to avoid import errors in environments
        # without the prebuilt model.
        _nlp_en = English()
        if "sentencizer" not in _nlp_en.pipe_names:
            _nlp_en.add_pipe("sentencizer")

    return _nlp_en


def is_korean(text: str) -> bool:
    hangul_cnt = len(re.findall(r"[가-힣]", text))
    return hangul_cnt / max(len(text), 1) > 0.3


def split_sentences_block(block: str) -> List[str]:
    """
    Split a block of text into sentences using KSS for Korean and spaCy for English.
    """
    block = block.strip()
    if not block:
        return []

    if is_korean(block):
        sents = kss.split_sentences(block)
        return [s.strip() for s in sents if s.strip()]

    nlp_en = _get_english_model()
    doc = nlp_en(block)
    return [s.text.strip() for s in doc.sents if s.text.strip()]
