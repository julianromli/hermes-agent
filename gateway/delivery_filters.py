"""Delivery filters for suppressing noisy replies in group chats."""

from __future__ import annotations

import re
from typing import Optional

SILENT_MARKER = "[SILENT]"
_SILENT_MARKER_RE = re.compile(re.escape(SILENT_MARKER), re.IGNORECASE)


def is_silent_agent_response(text: Optional[str]) -> bool:
    """Return True when agent output should not be delivered."""
    if text is None:
        return True
    stripped = str(text).strip()
    if not stripped:
        return True
    if _SILENT_MARKER_RE.fullmatch(stripped):
        return True
    remainder = _SILENT_MARKER_RE.sub("", stripped).strip()
    if not remainder and SILENT_MARKER.upper() in stripped.upper():
        return True
    return False


def should_suppress_group_command_reply(
    chat_type: Optional[str],
    *,
    supports_message_delete: bool,
    suppress_in_groups: bool = True,
) -> bool:
    """Suppress slash-command acknowledgments in groups without message delete."""
    if not suppress_in_groups:
        return False
    if (chat_type or "dm").lower() not in ("group", "channel"):
        return False
    return not supports_message_delete


def should_suppress_group_agent_reply(
    chat_type: Optional[str],
    text: Optional[str],
    *,
    supports_message_delete: bool,
) -> bool:
    """Suppress empty/[SILENT] agent replies in public group chats."""
    if (chat_type or "dm").lower() not in ("group", "channel"):
        return False
    return is_silent_agent_response(text)
