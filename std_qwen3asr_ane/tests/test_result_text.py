import pytest

from std_qwen3asr_ane.result_text import join_separator


@pytest.mark.parametrize(
    ("transcript", "following", "separator"),
    [
        ("hello world", "again", " "),
        ("오늘은", "날씨가 좋아요.", " "),
        ("今天", "天气很好", ""),
        ("こんにちは", "世界", ""),
        ("hello", "你好", ""),
        ("hello ", "again", ""),
        ("hello", " again", ""),
        ("", "again", ""),
        ("hello", "", ""),
    ],
)
def test_join_separator_spaces_word_delimited_windows_only(transcript, following, separator):
    assert join_separator(transcript, following) == separator
