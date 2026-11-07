from types import SimpleNamespace

import pytest

from rounds.tutor import extract_text


def block(type, text=None):
    return SimpleNamespace(type=type, text=text)


def test_extract_text_skips_thinking_block():
    response = SimpleNamespace(content=[block("thinking"), block("text", "Hello")])
    assert extract_text(response) == "Hello"


def test_extract_text_without_thinking_block():
    response = SimpleNamespace(content=[block("text", "Hello")])
    assert extract_text(response) == "Hello"


def test_extract_text_joins_multiple_text_blocks():
    response = SimpleNamespace(content=[block("text", "One"), block("thinking"), block("text", "Two")])
    assert extract_text(response) == "One\n\nTwo"


def test_extract_text_no_text_block_raises():
    response = SimpleNamespace(content=[block("thinking")])
    with pytest.raises(ValueError):
        extract_text(response)