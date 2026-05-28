from datetime import datetime


def validate_task_title(title):
    if not title.strip():
        raise ValueError("Task title cannot be empty.")


def validate_task_description(description):
    if not description.strip():
        raise ValueError("Task description cannot be empty.")

    if len(description) > 500:
        raise ValueError("Task description cannot exceed 500 characters.")


def validate_due_date(due_date):
    if not due_date.strip():
        raise ValueError("Due date cannot be empty.")

    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")