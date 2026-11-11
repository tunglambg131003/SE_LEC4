"""Starter for Labs 1 and 3: review ordering and exception boundaries."""
import logging
from collections.abc import Mapping
from dataclasses import replace
from typing import Protocol

from models import Task, Assignee, NotificationError

logger = logging.getLogger(__name__)


class TaskRepository(Protocol):
    def get(self, task_id: str) -> Task: ...

    def save(self, task: Task) -> None:
        """Return after commit; SaveError means no persisted change."""
        ...


class NotificationChannel(Protocol):
    def send(self, recipient: str, message: str) -> None: ...


class TaskService:
    def __init__(self, repository: TaskRepository,
                 channels: Mapping[str, NotificationChannel]):
        self._repository = repository
        self._channels = dict(channels)

    def assign_task(self, task_id: str, assignee: Assignee) -> Task:
        channel = self._channels[assignee.preferred_channel]
        task = self._repository.get(task_id)
        assigned = replace(task, assignee_id=assignee.id)
        # Review this interaction against R1-R4 before accepting the design.
        self._repository.save(assigned)
        try:
            channel.send(assignee.contact,
                         f'You were assigned: {assigned.title}')
        except NotificationError:
            logger.warning('notification failed for task %s', assigned.id)
        return assigned
