from task_utils import (
    add_task,
    mark_task_as_complete,
    view_pending_tasks,
    calculate_progress
)

tasks = []

while True:
    print("1. Add Task")
    print("2. Mark Task as Complete")
    print("3. View Pending Tasks")
    print("4. Track Progress")
    print("5. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        title = input("Enter title: ")
        description = input("Enter description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")
        add_task(tasks, title, description, due_date)

    elif choice == "2":
        for i, task in enumerate(tasks):
            print(f"{i}. {task['title']} - Completed: {task['completed']}")

        try:
            num = int(input("Enter task number to mark as complete: "))
            mark_task_as_complete(tasks, num)
        except ValueError:
            print("Invalid task number.")

    elif choice == "3":
        view_pending_tasks(tasks)

    elif choice == "4":
        print(calculate_progress(tasks))

    elif choice == "5":
        break

    else:
        print("Invalid choice.")