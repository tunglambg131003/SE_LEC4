"""Provided domain values and errors. No edits needed."""
from dataclasses import dataclass

class SaveError(Exception):
    """The assignment was not committed."""

class NotificationError(Exception):
    """The notification was not accepted."""

@dataclass(frozen=True)
class Task:
    id: str
    title: str
    assignee_id: str | None = None

@dataclass(frozen=True)
class Assignee:
    id: str
    preferred_channel: str
    contact: str
