class Task:
    _id_counter = 1

    def __init__(self, title, assigned_to=None):
        self.id = Task._id_counter
        Task._id_counter += 1

        self.title = title
        self.status = "pending"
        self.assigned_to = assigned_to

    def complete(self):
        self.status = "completed"

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, status={self.status})"