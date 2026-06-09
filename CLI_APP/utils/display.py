from __future__ import annotations
from typing import List

from rich.console import Console
from rich.table import Table
from rich import box
from rich.text import Text

from models.user import User
from models.project import Project
from models.task import Task
from utils.helpers import truncate

console = Console()


def display_users(users: List[User]):
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return
    table = Table(title="Users", box=box.ROUNDED, highlight=True)
    table.add_column("ID", style="dim", width=4)
    table.add_column("Name", style="bold cyan")
    table.add_column("Email", style="green")
    table.add_column("Role", style="magenta")
    table.add_column("Projects", justify="right")
    for u in users:
        table.add_row(str(u.id), u.name, u.email, u.role, str(len(u.projects)))
    console.print(table)


def display_projects(projects: List[Project], title: str = "Projects"):
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return
    table = Table(title=title, box=box.ROUNDED, highlight=True)
    table.add_column("ID", style="dim", width=4)
    table.add_column("Title", style="bold cyan")
    table.add_column("Description")
    table.add_column("Due Date", style="yellow")
    table.add_column("Progress", justify="right")
    for p in projects:
        table.add_row(str(p.id), p.title, truncate(p.description, 35),
                      p.due_date or "—", p.completion_rate())
    console.print(table)


def display_tasks(tasks: List[Task], project_title: str = ""):
    header = f"Tasks — {project_title}" if project_title else "Tasks"
    if not tasks:
        console.print(f"[yellow]No tasks in {project_title or 'project'}.[/yellow]")
        return
    table = Table(title=header, box=box.ROUNDED, highlight=True)
    table.add_column("ID", style="dim", width=4)
    table.add_column("Title", style="bold cyan")
    table.add_column("Assigned To", style="green")
    table.add_column("Status")
    for t in tasks:
        status_text = (Text("✅ complete", style="bold green")
                       if t.status == "complete" else Text("🔲 pending", style="yellow"))
        table.add_row(str(t.id), t.title, t.assigned_to or "—", status_text)
    console.print(table)


def success(msg: str):
    console.print(f"[bold green]✔ {msg}[/bold green]")

def error(msg: str):
    console.print(f"[bold red]✖ {msg}[/bold red]")

def info(msg: str):
    console.print(f"[bold blue]ℹ {msg}[/bold blue]")