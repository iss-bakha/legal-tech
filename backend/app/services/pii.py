"""Маскировка персональных данных до отправки текста в LLM.

Сейчас: ИИН/БИН, телефоны РК, e-mail, номера удостоверений, банковские карты и IBAN.
TODO: ФИО и адреса (нужен NER-модуль или правила по словарям).
"""

import re
from dataclasses import dataclass, field

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("IBAN", re.compile(r"\bKZ\d{2}[A-Z0-9]{16}\b", re.IGNORECASE)),
    ("CARD", re.compile(r"\b(?:\d{4}[ -]?){3}\d{4}\b")),
    ("ИИН", re.compile(r"(?<!\d)\d{12}(?!\d)")),
    (
        "ТЕЛЕФОН",
        re.compile(r"(?<!\d)(?:\+7|8)[\s(-]*7\d{2}[\s)-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}(?!\d)"),
    ),
    ("УДОСТОВЕРЕНИЕ", re.compile(r"(?<!\d)\d{9}(?!\d)")),
]


@dataclass
class MaskResult:
    text: str
    # метка -> исходное значение; хранится только у нас, в LLM не уходит
    mapping: dict[str, str] = field(default_factory=dict)


def mask_pii(text: str) -> MaskResult:
    mapping: dict[str, str] = {}
    counters: dict[str, int] = {}
    seen: dict[str, str] = {}

    for label, pattern in _PATTERNS:

        def repl(m: re.Match[str], label: str = label) -> str:
            value = m.group(0)
            if value in seen:
                return seen[value]
            counters[label] = counters.get(label, 0) + 1
            tag = f"[{label}_{counters[label]}]"
            seen[value] = tag
            mapping[tag] = value
            return tag

        text = pattern.sub(repl, text)

    return MaskResult(text=text, mapping=mapping)


def unmask(text: str, mapping: dict[str, str]) -> str:
    for tag, value in mapping.items():
        text = text.replace(tag, value)
    return text
