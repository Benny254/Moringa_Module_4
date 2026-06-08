class Project:
    _id_counter = 1

    def __init__(self, title, description, due_date, user_id):
        self.id = Project._id_counter
        Project._id_counter += 1

        self.title = title
        self.description = description
        self.due_date = due_date
        self.user_id = user_id
        self.tasks = []

    def add_task(self, task_id):
        self.tasks.append(task_id)

    def __repr__(self):
        return f"Project(id={self.id}, title={self.title}, due={self.due_date})"