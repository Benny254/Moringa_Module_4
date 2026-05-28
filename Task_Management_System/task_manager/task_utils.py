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


def mark_task_as_complete(tasks, task_number):

    if 0 <= task_number < len(tasks):

        tasks[task_number]["completed"] = True

        print("Task marked as complete!")

    else:
        print("Invalid task number.")


def view_pending_tasks(tasks):

    pending_tasks = []

    for task in tasks:

        if task["completed"] is False:
            pending_tasks.append(task)

    if len(pending_tasks) == 0:
        print("No pending tasks.")
        return

    for task in pending_tasks:

        print(f"""
Title: {task['title']}
Description: {task['description']}
Due Date: {task['due_date']}
""")


def calculate_progress(tasks):

    if len(tasks) == 0:
        return 0

    completed = 0

    for task in tasks:

        if task["completed"]:
            completed += 1

    progress = (completed / len(tasks)) * 100

    return progress