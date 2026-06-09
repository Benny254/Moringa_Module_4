from models.person import Person

class Student(Person):
    """A student who can register for courses."""
    
    def __init__(self, student_id, name, email, phone_number):
        super().__init__(name, email, phone_number)
        self._student_id = student_id

    @property
    def student_id(self):
        return self._student_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def phone_number(self):
        return self._phone_number

    def display(self):
        print(f" Student ID: {self._student_id}")
        print(f" Name: {self._name}")
        print(f" Email: {self._email}")
        print(f" Phone: {self._phone_number}")

    def to_dict(self):
        return {
            "student_id": self._student_id,
            "name": self._name,
            "email": self._email,
            "phone_number": self._phone_number
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            email=data["email"],
            phone_number=data["phone_number"]
        )
    
    def __str__(self):
        return f"Student(id={self._student_id}, name={self._name}, email={self._email})"