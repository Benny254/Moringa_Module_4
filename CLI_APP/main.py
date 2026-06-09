#!/usr/bin/env python3
"""
Project Tracker CLI
===================
Usage:
    python main.py <command> [options]

Run `python main.py --help` or `python main.py <command> --help` for details.
"""

import argparse
import sys

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import save_users, load_users, find_user_by_email, find_user_by_id
from utils.helpers import validate_date
from utils.display import (
    display_users, display_projects, display_tasks,
    success, error, info, console,
)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _get_user(users, identifier: str):
    if identifier.isdigit():
        u = find_user_by_id(users, int(identifier))
    else:
        u = find_user_by_email(users, identifier)
    if not u:
        error(f"User not found: {identifier!r}")
        sys.exit(1)
    return u


def _get_project(user, project_id: str):
    if not project_id.isdigit():
        error("Project ID must be an integer.")
        sys.exit(1)
    p = user.get_project_by_id(int(project_id))
    if not p:
        error(f"Project {project_id} not found for user {user.email}.")
        sys.exit(1)
    return p


def _get_task(project, task_id: str):
    if not task_id.isdigit():
        error("Task ID must be an integer.")
        sys.exit(1)
    t = project.get_task_by_id(int(task_id))
    if not t:
        error(f"Task {task_id} not found in project '{project.title}'.")
        sys.exit(1)
    return t


# ── Command handlers ─────────────────────────────────────────────────────────

def cmd_add_user(args, users):
    existing = find_user_by_email(users, args.email)
    if existing:
        error(f"A user with email {args.email!r} already exists.")
        sys.exit(1)
    try:
        user = User(name=args.name, email=args.email, role=args.role)
    except ValueError as exc:
        error(str(exc))
        sys.exit(1)
    users.append(user)
    save_users(users)
    success(f"User created: {user}")


def cmd_list_users(args, users):
    display_users(users)


def cmd_delete_user(args, users):
    user = _get_user(users, args.user)
    users.remove(user)
    save_users(users)
    success(f"Deleted user: {user.name} <{user.email}>")


def cmd_add_project(args, users):
    user = _get_user(users, args.user)
    due = None
    if args.due_date:
        try:
            due = validate_date(args.due_date)
        except ValueError as exc:
            error(str(exc))
            sys.exit(1)
    proj = Project(
        title=args.title,
        description=args.description or "",
        due_date=due,
        owner_email=user.email,
    )
    user.add_project(proj)
    save_users(users)
    success(f"Project '{proj.title}' (ID {proj.id}) added to {user.name}.")


def cmd_list_projects(args, users):
    user = _get_user(users, args.user)
    display_projects(user.projects, title=f"Projects — {user.name}")


def cmd_edit_project(args, users):
    user = _get_user(users, args.user)
    proj = _get_project(user, args.project_id)
    if args.title:
        proj.title = args.title
    if args.description is not None:
        proj.description = args.description
    if args.due_date:
        try:
            proj.due_date = validate_date(args.due_date)
        except ValueError as exc:
            error(str(exc))
            sys.exit(1)
    save_users(users)
    success(f"Project updated: {proj}")


def cmd_delete_project(args, users):
    user = _get_user(users, args.user)
    removed = user.remove_project(int(args.project_id))
    if not removed:
        error(f"Project {args.project_id} not found.")
        sys.exit(1)
    save_users(users)
    success(f"Deleted project {args.project_id} from {user.name}.")


def cmd_add_task(args, users):
    user = _get_user(users, args.user)
    proj = _get_project(user, args.project_id)
    assignee = args.assign_to or user.email
    task = Task(title=args.title, assigned_to=assignee)
    proj.add_task(task)
    save_users(users)
    success(f"Task '{task.title}' (ID {task.id}) added to project '{proj.title}'.")


def cmd_list_tasks(args, users):
    user = _get_user(users, args.user)
    proj = _get_project(user, args.project_id)
    display_tasks(proj.tasks, project_title=proj.title)


def cmd_complete_task(args, users):
    user = _get_user(users, args.user)
    proj = _get_project(user, args.project_id)
    task = _get_task(proj, args.task_id)
    task.complete()
    save_users(users)
    success(f"Task '{task.title}' marked as complete.")


def cmd_reopen_task(args, users):
    user = _get_user(users, args.user)
    proj = _get_project(user, args.project_id)
    task = _get_task(proj, args.task_id)
    task.reopen()
    save_users(users)
    success(f"Task '{task.title}' re-opened.")


def cmd_delete_task(args, users):
    user = _get_user(users, args.user)
    proj = _get_project(user, args.project_id)
    removed = proj.remove_task(int(args.task_id))
    if not removed:
        error(f"Task {args.task_id} not found.")
        sys.exit(1)
    save_users(users)
    success(f"Deleted task {args.task_id}.")


def cmd_search(args, users):
    kw = args.keyword.lower()
    found_projects = []
    for u in users:
        for p in u.projects:
            if kw in p.title.lower() or kw in p.description.lower():
                found_projects.append((u, p))
    if not found_projects:
        info(f"No projects matched '{args.keyword}'.")
        return
    for u, p in found_projects:
        console.print(f"\n[bold]Owner:[/bold] {u.name} <{u.email}>")
        display_projects([p])
        if args.include_tasks:
            display_tasks(p.tasks, project_title=p.title)


def cmd_summary(args, users):
    display_users(users)


# ── Argument parser ──────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tracker",
        description="Multi-user Project Tracker CLI",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    p_add_user = sub.add_parser("add-user", help="Create a new user.")
    p_add_user.add_argument("name", help="Full name")
    p_add_user.add_argument("email", help="Email address")
    p_add_user.add_argument("--role", choices=["developer", "admin", "viewer"],
                            default="developer", help="User role (default: developer)")

    sub.add_parser("list-users", help="List all users.")

    p_del_user = sub.add_parser("delete-user", help="Delete a user.")
    p_del_user.add_argument("user", help="User email or ID")

    p_add_proj = sub.add_parser("add-project", help="Add a project to a user.")
    p_add_proj.add_argument("user", help="User email or ID")
    p_add_proj.add_argument("title", help="Project title")
    p_add_proj.add_argument("--description", "-d", default="", help="Short description")
    p_add_proj.add_argument("--due-date", help="Due date YYYY-MM-DD")

    p_list_proj = sub.add_parser("list-projects", help="List a user's projects.")
    p_list_proj.add_argument("user", help="User email or ID")

    p_edit_proj = sub.add_parser("edit-project", help="Edit project fields.")
    p_edit_proj.add_argument("user", help="User email or ID")
    p_edit_proj.add_argument("project_id", help="Project ID")
    p_edit_proj.add_argument("--title", help="New title")
    p_edit_proj.add_argument("--description", help="New description")
    p_edit_proj.add_argument("--due-date", help="New due date YYYY-MM-DD")

    p_del_proj = sub.add_parser("delete-project", help="Delete a project.")
    p_del_proj.add_argument("user", help="User email or ID")
    p_del_proj.add_argument("project_id", help="Project ID")

    p_add_task = sub.add_parser("add-task", help="Add a task to a project.")
    p_add_task.add_argument("user", help="User email or ID")
    p_add_task.add_argument("project_id", help="Project ID")
    p_add_task.add_argument("title", help="Task title")
    p_add_task.add_argument("--assign-to", help="Assignee email (defaults to project owner)")

    p_list_tasks = sub.add_parser("list-tasks", help="List tasks in a project.")
    p_list_tasks.add_argument("user", help="User email or ID")
    p_list_tasks.add_argument("project_id", help="Project ID")

    p_complete = sub.add_parser("complete-task", help="Mark a task complete.")
    p_complete.add_argument("user", help="User email or ID")
    p_complete.add_argument("project_id", help="Project ID")
    p_complete.add_argument("task_id", help="Task ID")

    p_reopen = sub.add_parser("reopen-task", help="Re-open a completed task.")
    p_reopen.add_argument("user", help="User email or ID")
    p_reopen.add_argument("project_id", help="Project ID")
    p_reopen.add_argument("task_id", help="Task ID")

    p_del_task = sub.add_parser("delete-task", help="Delete a task.")
    p_del_task.add_argument("user", help="User email or ID")
    p_del_task.add_argument("project_id", help="Project ID")
    p_del_task.add_argument("task_id", help="Task ID")

    p_search = sub.add_parser("search", help="Search projects by keyword.")
    p_search.add_argument("keyword", help="Keyword to search for")
    p_search.add_argument("--include-tasks", action="store_true",
                          help="Also show tasks for matched projects")

    sub.add_parser("summary", help="Show summary of all users.")

    return parser


COMMANDS = {
    "add-user": cmd_add_user,
    "list-users": cmd_list_users,
    "delete-user": cmd_delete_user,
    "add-project": cmd_add_project,
    "list-projects": cmd_list_projects,
    "edit-project": cmd_edit_project,
    "delete-project": cmd_delete_project,
    "add-task": cmd_add_task,
    "list-tasks": cmd_list_tasks,
    "complete-task": cmd_complete_task,
    "reopen-task": cmd_reopen_task,
    "delete-task": cmd_delete_task,
    "search": cmd_search,
    "summary": cmd_summary,
}

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    users = load_users()
    handler = COMMANDS.get(args.command)
    if handler:
        handler(args, users)
    else:
        parser.print_help()