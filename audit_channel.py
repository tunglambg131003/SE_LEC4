"""Lab 4: decorate a channel without changing its delivery behavior."""
from service import NotificationChannel


class AuditedChannel:
    def __init__(self, channel: NotificationChannel):
        self._channel = channel
        self.events: list[str] = []

    def send(self, recipient: str, message: str) -> None:
        self._channel.send(recipient, message)
        self.events.append('notification.accepted')
