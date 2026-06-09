import json
import os

from models.student import Student
from models.course import Course

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")
REGISTRATIONS_FILE = os.path.join(DATA_DIR, "registrations.json")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _input(prompt):
    """Safe input() wrapper — returns empty string on EOF/interrupt."""
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return ""


class SchoolSystem:

    def __init__(self):
        self.students = []
        self.courses = []
        self.registrations = []

    # ── internal lookups ─────────────────────────────────────────────────────

    def _find_student(self, student_id):
        for s in self.students:
            if s.student_id.lower() == student_id.lower():
                return s
        return None

    def _find_course(self, course_id):
        for c in self.courses:
            if c.course_id.lower() == course_id.lower():
                return c
        return None

    def _registered_students_in(self, course_id):
        return [r["student_id"] for r in self.registrations
                if r["course_id"].lower() == course_id.lower()]

    def _registered_courses_for(self, student_id):
        return [r["course_id"] for r in self.registrations
                if r["student_id"].lower() == student_id.lower()]

    # ── validation ────────────────────────────────────────────────────────────

    @staticmethod
    def _validate_email(email):
        return "@" in email and "." in email.split("@")[-1]

    # ── student management ────────────────────────────────────────────────────

    def add_student(self):
        print("\n--- Add Student ---")

        student_id = _input("  Student ID : ")
        if not student_id:
            print("  [!] Student ID cannot be empty.")
            return
        if self._find_student(student_id):
            print(f"  [!] A student with ID '{student_id}' already exists.")
            return

        name = _input("  Name       : ")
        if not name:
            print("  [!] Name cannot be empty.")
            return

        email = _input("  Email      : ")
        if not self._validate_email(email):
            print("  [!] Invalid email address. Must contain '@' and a domain.")
            return

        phone = _input("  Phone      : ")
        if not phone:
            print("  [!] Phone number cannot be empty.")
            return

        self.students.append(Student(student_id, name, email, phone))
        print(f"  [✔] Student {name} added successfully.")

    def view_students(self):
        print("\n--- All Students ---")
        if not self.students:
            print("  No students found.")
            return
        for i, s in enumerate(self.students, 1):
            print(f"\n  Student #{i}")
            s.display()

    def search_student(self):
        print("\n--- Search Student ---")
        query = _input("  Enter Student ID or Name: ").lower()
        if not query:
            print("  [!] Search term cannot be empty.")
            return
        results = [
            s for s in self.students
            if query in s.student_id.lower() or query in s.name.lower()
        ]
        if not results:
            print("  No matching students found.")
            return
        for s in results:
            print()
            s.display()

    # ── course management ─────────────────────────────────────────────────────

    def add_course(self):
        print("\n--- Add Course ---")

        course_id = _input("  Course ID  : ")
        if not course_id:
            print("  [!] Course ID cannot be empty.")
            return
        if self._find_course(course_id):
            print(f"  [!] A course with ID '{course_id}' already exists.")
            return

        course_name = _input("  Course Name: ")
        if not course_name:
            print("  [!] Course name cannot be empty.")
            return

        trainer = _input("  Trainer    : ")
        if not trainer:
            print("  [!] Trainer name cannot be empty.")
            return

        capacity_raw = _input("  Capacity   : ")
        try:
            capacity = int(capacity_raw)
            if capacity <= 0:
                raise ValueError
        except ValueError:
            print("  [!] Capacity must be a positive whole number (e.g. 5).")
            return

        self.courses.append(Course(course_id, course_name, trainer, capacity))
        print(f"  [✔] Course '{course_name}' added successfully.")

    def view_courses(self):
        print("\n--- All Courses ---")
        if not self.courses:
            print("  No courses found.")
            return
        for i, c in enumerate(self.courses, 1):
            enrolled = len(self._registered_students_in(c.course_id))
            slots = c.capacity - enrolled
            print(f"\n  Course #{i}")
            c.display()
            print(f"  Enrolled   : {enrolled}  |  Available slots: {slots}")

    # ── registration management ───────────────────────────────────────────────

    def register_student(self):
        print("\n--- Register Student to Course ---")

        student_id = _input("  Student ID : ")
        if not student_id:
            print("  [!] Student ID cannot be empty.")
            return
        student = self._find_student(student_id)
        if not student:
            print(f"  [!] No student found with ID '{student_id}'.")
            return

        course_id = _input("  Course ID  : ")
        if not course_id:
            print("  [!] Course ID cannot be empty.")
            return
        course = self._find_course(course_id)
        if not course:
            print(f"  [!] No course found with ID '{course_id}'.")
            return

        already = [c.lower() for c in self._registered_courses_for(student_id)]
        if course_id.lower() in already:
            print(f"  [!] {student.name} is already registered for this course.")
            return

        enrolled = len(self._registered_students_in(course_id))
        if enrolled >= course.capacity:
            print("  [!] Registration failed. This course is already full.")
            return

        self.registrations.append({
            "student_id": student.student_id,
            "course_id": course.course_id,
        })
        print(f"  [✔] {student.name} successfully registered for {course.course_name}.")

    def view_students_in_course(self):
        print("\n--- Students in a Course ---")
        course_id = _input("  Course ID: ")
        if not course_id:
            print("  [!] Course ID cannot be empty.")
            return
        course = self._find_course(course_id)
        if not course:
            print(f"  [!] No course found with ID '{course_id}'.")
            return
        student_ids = self._registered_students_in(course_id)
        if not student_ids:
            print(f"  No students registered in '{course.course_name}' yet.")
            return
        print(f"\n  Students in '{course.course_name}':")
        for sid in student_ids:
            s = self._find_student(sid)
            if s:
                print(f"    - [{s.student_id}]  {s.name}  |  {s.email}  |  {s.phone_number}")

    def view_courses_for_student(self):
        print("\n--- Courses for a Student ---")
        student_id = _input("  Student ID: ")
        if not student_id:
            print("  [!] Student ID cannot be empty.")
            return
        student = self._find_student(student_id)
        if not student:
            print(f"  [!] No student found with ID '{student_id}'.")
            return
        course_ids = self._registered_courses_for(student_id)
        if not course_ids:
            print(f"  {student.name} has not registered for any courses yet.")
            return
        print(f"\n  Courses registered by {student.name}:")
        for cid in course_ids:
            c = self._find_course(cid)
            if c:
                print(f"    - [{c.course_id}]  {c.course_name}  |  Trainer: {c.trainer}")

    # ── file I/O ──────────────────────────────────────────────────────────────

    def save_data(self):
        _ensure_data_dir()
        try:
            with open(STUDENTS_FILE, "w") as f:
                json.dump([s.to_dict() for s in self.students], f, indent=2)
            with open(COURSES_FILE, "w") as f:
                json.dump([c.to_dict() for c in self.courses], f, indent=2)
            with open(REGISTRATIONS_FILE, "w") as f:
                json.dump(self.registrations, f, indent=2)
            print("  [✔] Data saved successfully.")
        except PermissionError:
            print("  [!] Permission denied — could not write to data folder.")
        except Exception as e:
            print(f"  [!] Error saving data: {e}")

    def load_data(self):
        _ensure_data_dir()
        try:
            if os.path.exists(STUDENTS_FILE):
                with open(STUDENTS_FILE, "r") as f:
                    self.students = [Student.from_dict(d) for d in json.load(f)]
            if os.path.exists(COURSES_FILE):
                with open(COURSES_FILE, "r") as f:
                    self.courses = [Course.from_dict(d) for d in json.load(f)]
            if os.path.exists(REGISTRATIONS_FILE):
                with open(REGISTRATIONS_FILE, "r") as f:
                    self.registrations = json.load(f)
            print("  [✔] Data loaded successfully.")
        except json.JSONDecodeError:
            print("  [!] Data file is corrupted. Starting with empty data.")
        except KeyError as e:
            print(f"  [!] Missing field in data file: {e}. Starting fresh.")
        except Exception as e:
            print(f"  [!] Unexpected error loading data: {e}")