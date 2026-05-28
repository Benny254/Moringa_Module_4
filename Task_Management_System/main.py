from task_utils import (
    add_task,
    mark_task_as_complete,
    view_pending_tasks,
    calculate_progress
)

tasks = []


def menu():

    print("\nTask Management System")
    print("1. Add Task")
    print("2. Mark Task as Complete")
    print("3. View Pending Tasks")
    print("4. Track Progress")
    print("5. Exit")


while True:

    menu()

    choice = input("Enter choice: ")

    if choice == "1":

        title = input("Enter title: ")
        description = input("Enter description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")

        add_task(tasks, title, description, due_date)

    elif choice == "2":

        if len(tasks) == 0:
            print("No tasks available.")
            continue

        for index, task in enumerate(tasks, start=1):
            print(f"{index}: {task['title']}")

        try:

            task_number = int(input("Enter task number: "))

            mark_task_as_complete(tasks, task_number)

        except ValueError:
            print("Invalid input.")

    elif choice == "3":

        view_pending_tasks(tasks)

    elif choice == "4":

        progress = calculate_progress(tasks)

        print(f"Progress: {progress:.2f}%")

    elif choice == "5":

        print("Goodbye!")

        break

    else:

        print("Invalid choice.")