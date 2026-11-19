"""Keep measured transcript ranges relative to the containing result text."""

from __future__ import annotations

from collections.abc import Mapping


def needs_join_space(left: str, right: str) -> bool:
    """Separate independent word-delimited windows, but not Chinese or Japanese ones.

    Chinese and Japanese text takes no space between windows. Korean separates
    words with spaces, so Hangul syllables join like Latin text.
    """
    if left.isspace() or right.isspace():
        return False
    return not any("\u2e80" <= character <= "\ua4cf" for character in (left, right))


def join_separator(transcript: str, following: str) -> str:
    """Return the separator to put before a later window's text: ``" "`` or ``""``.

    ``transcript`` is the text so far and ``following`` is the next window's text.
    Standard ASR joins segment texts with no separator (spec TR.1), so the first
    non-empty segment of each later window starts with this separator itself.
    """
    if transcript and following and needs_join_space(transcript[-1], following[0]):
        return " "
    return ""


def shift_source_offsets(extra: Mapping, offset: int) -> dict:
    """Copy extra fields, moving known character offsets into the merged text.

    Only the plugin's exact source ranges change. Measured times and raw model
    evidence keep their own documented timelines and coordinates.
    """
    result = dict(extra)
    for key in ("source_start", "source_end"):
        if key in result:
            value = result[key]
            if type(value) is not int or value < 0:
                raise ValueError(f"{key} must be a non-negative character offset")
            result[key] = value + offset
    return result
