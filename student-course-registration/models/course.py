class Course:
    def __init__(self, course_id, course_name, trainer, capacity):
        self._course_id = course_id
        self._course_name = course_name
        self._trainer = trainer
        self._capacity = capacity

    @property
    def course_id(self):
        return self._course_id

    @property
    def course_name(self):
        return self._course_name

    @property
    def trainer(self):
        return self._trainer

    @property
    def capacity(self):
        return self._capacity

    def display(self):
        print(f" Course ID  : {self._course_id}")
        print(f" Name       : {self._course_name}")
        print(f" Trainer    : {self._trainer}")
        print(f" Capacity   : {self._capacity}")

    def to_dict(self):
        return {
            "course_id": self._course_id,
            "course_name": self._course_name,
            "trainer": self._trainer,
            "capacity": self._capacity
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            course_id=data["course_id"],
            course_name=data["course_name"],
            trainer=data["trainer"],
            capacity=data["capacity"]
        )