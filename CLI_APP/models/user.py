from __future__ import annotations
from typing import List, Optional
from models.person import Person
from models.project import Project


class User(Person):
    """A registered user who can own projects."""

    _id_counter: int = 1

    def __init__(self, name: str, email: str, user_id: Optional[int] = None, role: str = "developer"):
        super().__init__(name, email)
        if user_id is not None:
            self._id = user_id
            if user_id >= User._id_counter:
                User._id_counter = user_id + 1
        else:
            self._id = User._id_counter
            User._id_counter += 1

        self._role = role
        self._projects: List[Project] = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def role(self) -> str:
        return self._role

    @role.setter
    def role(self, value: str):
        allowed = {"developer", "admin", "viewer"}
        if value not in allowed:
            raise ValueError(f"Role must be one of {allowed}")
        self._role = value

    @property
    def projects(self) -> List[Project]:
        return list(self._projects)

    def add_project(self, project: Project):
        self._projects.append(project)

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        for p in self._projects:
            if p.id == project_id:
                return p
        return None

    def remove_project(self, project_id: int) -> bool:
        original = len(self._projects)
        self._projects = [p for p in self._projects if p.id != project_id]
        return len(self._projects) < original

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "email": self._email,
            "role": self._role,
            "projects": [p.to_dict() for p in self._projects],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(
            name=data["name"],
            email=data["email"],
            user_id=data.get("id"),
            role=data.get("role", "developer"),
        )
        for pd in data.get("projects", []):
            user.add_project(Project.from_dict(pd))
        return user

    def __str__(self) -> str:
        return (f"[{self._id}] {self._name}  <{self._email}>  "
                f"role={self._role}  projects={len(self._projects)}")

    def __repr__(self) -> str:
        return f"User(id={self._id}, name={self._name!r}, email={self._email!r})"