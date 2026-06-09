#!/usr/bin/env python3
"""
Student Course Registration System
Entry point — runs the interactive menu.
"""

from services.school_system import SchoolSystem


MENU = """
===== Student Course Registration System =====

  1.  Add Student
  2.  View Students
  3.  Search Student
  4.  Add Course
  5.  View Courses
  6.  Register Student to Course
  7.  View Students in a Course
  8.  View Courses for a Student
  9.  Save Data
  10. Load Data
  0.  Exit

Choose an option: """


ACTIONS = {
    "1":  "add_student",
    "2":  "view_students",
    "3":  "search_student",
    "4":  "add_course",
    "5":  "view_courses",
    "6":  "register_student",
    "7":  "view_students_in_course",
    "8":  "view_courses_for_student",
    "9":  "save_data",
    "10": "load_data",
}


def main():
    system = SchoolSystem()

    print("\n  Loading saved data...")
    system.load_data()

    while True:
        try:
            choice = input(MENU).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Saving data before exit...")
            system.save_data()
            print("  Goodbye!\n")
            break

        if choice == "0":
            print("\n  Saving data before exit...")
            system.save_data()
            print("  Goodbye!\n")
            break

        action = ACTIONS.get(choice)
        if not action:
            print("  [!] Invalid option. Please enter a number between 0 and 10.")
            continue

        # Every menu action is wrapped — nothing can crash the app
        try:
            getattr(system, action)()
        except KeyboardInterrupt:
            print("\n  [!] Action cancelled. Returning to menu.")
        except Exception as e:
            print(f"  [!] An unexpected error occurred: {e}")
            print("  Returning to menu...")


if __name__ == "__main__":
    main()