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

from rounds.tutor import build_messages


def test_build_messages_appends_user_turn_without_changing_history():
    history = [
        {"role": "user", "content": "Start the session."},
        {"role": "assistant", "content": "What causes a cotton-wool spot?"},
    ]
    results = [
        (1, "Content 1", 17, 17, "Title 1", 0.03),
    ]

    messages = build_messages(history, "Maybe the axons swell?", results)

    assert len(messages) == 3
    assert messages[-1]["role"] == "user"
    assert '<source title="Title 1" pages="17">' in messages[-1]["content"]
    assert "<student_message>\nMaybe the axons swell?\n</student_message>" in messages[-1]["content"]
    assert len(history) == 2