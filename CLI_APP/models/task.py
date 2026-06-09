from __future__ import annotations
from typing import Optional


class Task:
    """Represents a single task within a project."""

    _id_counter: int = 1

    def __init__(self, title: str, assigned_to: Optional[str] = None,
                 status: str = "pending", task_id: Optional[int] = None):
        if task_id is not None:
            self._id = task_id
            if task_id >= Task._id_counter:
                Task._id_counter = task_id + 1
        else:
            self._id = Task._id_counter
            Task._id_counter += 1

        self.title = title
        self._status = status
        self._assigned_to = assigned_to

    @property
    def id(self) -> int:
        return self._id

    @property
    def status(self) -> str:
        return self._status

    @property
    def assigned_to(self) -> Optional[str]:
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value: Optional[str]):
        self._assigned_to = value

    def complete(self):
        self._status = "complete"

    def reopen(self):
        self._status = "pending"

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "title": self.title,
            "status": self._status,
            "assigned_to": self._assigned_to,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(
            title=data["title"],
            assigned_to=data.get("assigned_to"),
            status=data.get("status", "pending"),
            task_id=data.get("id"),
        )

    def __str__(self) -> str:
        assignee = self._assigned_to or "unassigned"
        icon = "✅" if self._status == "complete" else "🔲"
        return f"  {icon} [{self._id}] {self.title}  (assigned: {assignee})"

    def __repr__(self) -> str:
        return f"Task(id={self._id}, title={self.title!r}, status={self._status!r})"