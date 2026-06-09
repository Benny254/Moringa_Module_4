class Person:
    """Abstract base representing any person in the system."""
    
    def __init__(self, name, email, phone_number):
        self._name = name
        self._email = email
        self._phone_number = phone_number

    def __repr__(self):
        return f"Person(name={self._name!r}, email={self._email!r}, phone_number={self._phone_number!r})"