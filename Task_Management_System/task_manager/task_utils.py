# task_manager/task_utils.py

from task_manager.validation import (
    validate_task_title,
    validate_task_description,
    validate_due_date
)


def add_task(tasks, title, description, due_date):
    if (
        validate_task_title(title)
        and validate_task_description(description)
        and validate_due_date(due_date)
    ):

        task = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": False
        }

        tasks.append(task)
        print("Task added successfully!")

    else:
        print("Task was not added.")


def mark_task_as_complete(tasks, task_number):
    if 0 <= task_number < len(tasks):
        tasks[task_number]["completed"] = True
        print("Task marked as complete!")
    else:
        print("Invalid task number.")


def view_pending_tasks(tasks):
    pending_tasks = [task for task in tasks if not task["completed"]]

    if not pending_tasks:
        print("No pending tasks.")
        return

    print("\nPending Tasks:")
    for index, task in enumerate(pending_tasks, start=1):
        print(f"""
Task {index}
Title: {task['title']}
Description: {task['description']}
Due Date: {task['due_date']}
Completed: {task['completed']}
""")


def calculate_progress(tasks):
    if len(tasks) == 0:
        return 0

    completed_tasks = len(
        [task for task in tasks if task["completed"]]
    )

    progress = (completed_tasks / len(tasks)) * 100
    return progress