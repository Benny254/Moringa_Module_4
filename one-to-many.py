class Student:
    all_students = []
    def __init__(self, name):
        self.name = name
        self.teacher = None
        Student.all_students.append(self)

    @property
    def teacher(self):
        return self._teacher

    @teacher.setter
    def teacher(self, new_teacher):
        if not isinstance(new_teacher, Teacher) and new_teacher is not None:
            raise ValueError("teacher must be an instance of Teacher or None")
        self._teacher = new_teacher 

class Teacher:
    def __init__(self, name):
        self.name = name
        self.students = ""

    def add_student(self, student):
        if not isinstance(student, Student):
            raise ValueError("student must be an instance of Student")
        self.students += student.name + " "

student1 = Student("Alice")
student2 = Student("Bob")
teacher = Teacher("Smith")
teacher.add_student(student1)
teacher.add_student(student2)
student1.teacher = teacher
student2.teacher = teacher

print(student1.teacher.name)
print(student2.teacher.name)
print(teacher.students)