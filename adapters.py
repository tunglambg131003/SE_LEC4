"""Provided offline adapters. No database, network or edits needed."""
from dataclasses import replace
from models import Task, SaveError, NotificationError

class InMemoryRepository:
    def __init__(self, tasks, *, fail_save=False, trace=None):
        self._tasks = {task.id: replace(task) for task in tasks}
        self.fail_save = fail_save
        self.trace = trace if trace is not None else []

    def get(self, task_id: str) -> Task:
        self.trace.append('get')
        return replace(self._tasks[task_id])

    def save(self, task: Task) -> None:
        """Success models a committed write; failure changes no stored state."""
        self.trace.append('save')
        if self.fail_save:
            raise SaveError('simulated save failure')
        self._tasks[task.id] = replace(task)

    def persisted(self, task_id: str) -> Task:
        return replace(self._tasks[task_id])

class RecordingChannel:
    def __init__(self, *, fail=False, trace=None):
        self.sent = []
        self.attempts = 0
        self.fail = fail
        self.trace = trace if trace is not None else []

    def send(self, recipient: str, message: str) -> None:
        self.trace.append('send')
        self.attempts += 1
        if self.fail:
            raise NotificationError('simulated notification failure')
        self.sent.append((recipient, message))
