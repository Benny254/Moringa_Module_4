import argparse
from rich import print

from models.user import User
from models.project import Project
from models.task import Task

from utils.storage import load_data, save_data


# ---------------- Load existing data ---------------- #
users = []
projects = []
tasks = []


def load_existing_data():
    global users, projects, tasks

    users_data = load_data("users.json")
    projects_data = load_data("projects.json")
    tasks_data = load_data("tasks.json")

    # rebuild objects (simple reconstruction)
    for u in users_data:
        user = User(u["name"], u["email"])
        user.id = u["id"]
        user.projects = u.get("projects", [])
        users.append(user)

    for p in projects_data:
        project = Project(p["title"], p["description"], p["due_date"], p["user_id"])
        project.id = p["id"]
        project.tasks = p.get("tasks", [])
        projects.append(project)

    for t in tasks_data:
        task = Task(t["title"], t.get("assigned_to"))
        task.id = t["id"]
        task.status = t.get("status", "pending")
        tasks.append(task)


# ---------------- CLI Functions ---------------- #

def add_user(args):
    user = User(args.name, args.email)
    users.append(user)

    save_data("users.json", [u.__dict__ for u in users])
    print(f"[green]User created:[/green] {user}")


def list_users(args):
    for u in users:
        print(u)


def add_project(args):
    project = Project(args.title, args.description, args.due_date, args.user_id)
    projects.append(project)

    for u in users:
        if u.id == args.user_id:
            u.add_project(project.id)

    save_data("projects.json", [p.__dict__ for p in projects])
    print(f"[blue]Project added:[/blue] {project}")


def add_task(args):
    task = Task(args.title, args.assigned_to)
    tasks.append(task)

    for p in projects:
        if p.id == args.project_id:
            p.add_task(task.id)

    save_data("tasks.json", [t.__dict__ for t in tasks])
    print(f"[yellow]Task added:[/yellow] {task}")


def complete_task(args):
    for t in tasks:
        if t.id == args.task_id:
            t.complete()
            save_data("tasks.json", [t.__dict__ for t in tasks])
            print(f"[green]Task completed:[/green] {t}")
            return

    print("[red]Task not found[/red]")


def list_projects(args):
    for p in projects:
        print(p)


# ---------------- CLI Setup ---------------- #

def main():
    load_existing_data()

    parser = argparse.ArgumentParser(description="Project Tracker CLI")
    subparsers = parser.add_subparsers()

    # Add User
    user_parser = subparsers.add_parser("add-user")
    user_parser.add_argument("--name", required=True)
    user_parser.add_argument("--email", required=True)
    user_parser.set_defaults(func=add_user)

    # List Users
    list_user_parser = subparsers.add_parser("list-users")
    list_user_parser.set_defaults(func=list_users)

    # Add Project
    project_parser = subparsers.add_parser("add-project")
    project_parser.add_argument("--title", required=True)
    project_parser.add_argument("--description", required=True)
    project_parser.add_argument("--due_date", required=True)
    project_parser.add_argument("--user_id", type=int, required=True)
    project_parser.set_defaults(func=add_project)

    # Add Task
    task_parser = subparsers.add_parser("add-task")
    task_parser.add_argument("--title", required=True)
    task_parser.add_argument("--project_id", type=int, required=True)
    task_parser.add_argument("--assigned_to", required=False)
    task_parser.set_defaults(func=add_task)

    # Complete Task
    complete_parser = subparsers.add_parser("complete-task")
    complete_parser.add_argument("--task_id", type=int, required=True)
    complete_parser.set_defaults(func=complete_task)

    # List Projects
    list_proj = subparsers.add_parser("list-projects")
    list_proj.set_defaults(func=list_projects)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()