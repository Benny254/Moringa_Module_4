from __future__ import annotations
from typing import List, Optional
from models.task import Task


class Project:
    """A project owned by a user, containing many tasks."""

    _id_counter: int = 1

    def __init__(self, title: str, description: str = "", due_date: Optional[str] = None,
                 owner_email: Optional[str] = None, project_id: Optional[int] = None):
        if project_id is not None:
            self._id = project_id
            if project_id >= Project._id_counter:
                Project._id_counter = project_id + 1
        else:
            self._id = Project._id_counter
            Project._id_counter += 1

        self._title = title
        self._description = description
        self._due_date = due_date
        self._owner_email = owner_email
        self._tasks: List[Task] = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def due_date(self) -> Optional[str]:
        return self._due_date

    @due_date.setter
    def due_date(self, value: Optional[str]):
        self._due_date = value

    @property
    def owner_email(self) -> Optional[str]:
        return self._owner_email

    @property
    def tasks(self) -> List[Task]:
        return list(self._tasks)

    def add_task(self, task: Task):
        self._tasks.append(task)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for t in self._tasks:
            if t.id == task_id:
                return t
        return None

    def remove_task(self, task_id: int) -> bool:
        original = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        return len(self._tasks) < original

    def completion_rate(self) -> str:
        if not self._tasks:
            return "No tasks"
        done = sum(1 for t in self._tasks if t.status == "complete")
        return f"{done}/{len(self._tasks)} complete"

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "owner_email": self._owner_email,
            "tasks": [t.to_dict() for t in self._tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        proj = cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date"),
            owner_email=data.get("owner_email"),
            project_id=data.get("id"),
        )
        for td in data.get("tasks", []):
            proj.add_task(Task.from_dict(td))
        return proj

    def __str__(self) -> str:
        due = f"  due: {self._due_date}" if self._due_date else ""
        return f"[{self._id}] {self._title}{due}  ({self.completion_rate()})"

    def __repr__(self) -> str:
        return f"Project(id={self._id}, title={self._title!r})"