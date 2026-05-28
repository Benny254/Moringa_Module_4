# main.py

from task_manager.task_utils import (
    add_task,
    mark_task_as_complete,
    view_pending_tasks,
    calculate_progress
)

tasks = []


def display_menu():
    print("""
====== TASK MANAGEMENT SYSTEM ======

1. Add Task
2. Mark Task as Complete
3. View Pending Tasks
4. Track Progress
5. Exit

===================================
""")


while True:
    display_menu()

    choice = input("Enter your choice: ")

    if choice == "1":
        title = input("Enter task title: ")
        description = input("Enter task description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")

        add_task(tasks, title, description, due_date)

    elif choice == "2":

        if not tasks:
            print("No tasks available.")
            continue

        print("\nAll Tasks:")
        for index, task in enumerate(tasks):
            print(f"{index}. {task['title']} - Completed: {task['completed']}")

        try:
            task_number = int(
                input("Enter task number to mark as complete: ")
            )

            mark_task_as_complete(tasks, task_number)

        except ValueError:
            print("Please enter a valid number.")

    elif choice == "3":
        view_pending_tasks(tasks)

    elif choice == "4":
        progress = calculate_progress(tasks)
        print(f"Progress: {progress:.2f}% completed")

    elif choice == "5":
        print("Exiting Task Management System...")
        break

    else:
        print("Invalid choice. Please try again.")