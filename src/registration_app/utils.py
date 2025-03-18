"""Miscellaneous utils."""


def empty_string_to_none(s: str) -> str | None:
    if len(s.strip()) < 1:
        return None
    else:
        return s
