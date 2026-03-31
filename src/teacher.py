from __future__ import annotations

from collections import Counter
from typing import Any, Iterable, Sequence

DEFAULT_TEACHER_NAMES: tuple[str, ...] = ("강경미",)
TEACHER_STATE = "IGNORE"

_OCR_NAME_CORRECTIONS = {
    "류데림": "류혜림",
}


def normalize_person_name(text: str | None) -> str:
    """OCR/패널 전반에서 공통으로 쓰는 이름 정규화."""
    if text is None:
        return ""
    normalized = "".join(
        ch for ch in str(text).strip().replace(" ", "") if "가" <= ch <= "힣"
    )
    return _OCR_NAME_CORRECTIONS.get(normalized, normalized)


def resolve_teacher_names(
    teacher_names: Sequence[str] | None = None,
) -> list[str]:
    names = teacher_names or DEFAULT_TEACHER_NAMES
    resolved = [normalize_person_name(name) for name in names]
    return [name for name in resolved if name]


def is_teacher_name(
    name: str | None,
    teacher_names: Sequence[str] | None = None,
) -> bool:
    normalized_name = normalize_person_name(name)
    if not normalized_name:
        return False

    for teacher_name in resolve_teacher_names(teacher_names):
        if teacher_name and (
            teacher_name in normalized_name or normalized_name in teacher_name
        ):
            return True
    return False


def student_slots(slots: Iterable[Any]) -> list[Any]:
    return [slot for slot in slots if not bool(getattr(slot, "is_teacher", False))]


def best_voted_name(name_votes: Sequence[str] | None = None) -> str:
    normalized_votes = [normalize_person_name(name) for name in (name_votes or [])]
    filtered_votes = [name for name in normalized_votes if name]
    if not filtered_votes:
        return ""
    return Counter(filtered_votes).most_common(1)[0][0]


def resolve_display_name(
    preferred_name: str | None,
    slot_id: int | None,
    *,
    name_votes: Sequence[str] | None = None,
    fallback_prefix: str = "학생",
) -> str:
    normalized_name = normalize_person_name(preferred_name)
    if normalized_name:
        return normalized_name

    voted_name = best_voted_name(name_votes)
    if voted_name:
        return voted_name

    if slot_id is None:
        return fallback_prefix
    return f"{fallback_prefix} {slot_id}"
