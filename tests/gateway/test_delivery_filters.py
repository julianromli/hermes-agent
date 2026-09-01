"""Tests for gateway.delivery_filters group/silent suppression."""

import pytest

from gateway.delivery_filters import (
    SILENT_MARKER,
    is_silent_agent_response,
    should_suppress_group_agent_reply,
    should_suppress_group_command_reply,
)


@pytest.mark.parametrize(
    "text,expected",
    [
        ("", True),
        ("   ", True),
        (None, True),
        (SILENT_MARKER, True),
        ("[silent]", True),
        ("No active task to stop.", False),
        ("Here is your summary.", False),
    ],
)
def test_is_silent_agent_response(text, expected):
    assert is_silent_agent_response(text) is expected


def test_should_suppress_group_command_reply_dm():
    assert should_suppress_group_command_reply(
        "dm", supports_message_delete=False
    ) is False


def test_should_suppress_group_command_reply_whatsapp_group():
    assert should_suppress_group_command_reply(
        "group", supports_message_delete=False
    ) is True


def test_should_suppress_group_command_reply_telegram_group():
    assert should_suppress_group_command_reply(
        "group", supports_message_delete=True
    ) is False


def test_should_suppress_group_agent_reply_silent():
    assert should_suppress_group_agent_reply(
        "group", SILENT_MARKER, supports_message_delete=False
    ) is True


def test_should_suppress_group_agent_reply_normal():
    assert should_suppress_group_agent_reply(
        "group", "Hello group", supports_message_delete=False
    ) is False
