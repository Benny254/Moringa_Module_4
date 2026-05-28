from datetime import datetime


def validate_task_title(title):
    if not title.strip():
        raise ValueError(...)
    return True


def validate_task_description(description):
    if not description.strip():
        raise ValueError(...)
    if len(description) > 500:
        raise ValueError(...)
    return True


def validate_due_date(due_date):
    if not due_date.strip():
        raise ValueError(...)
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError(...)
    return True