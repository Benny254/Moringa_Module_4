class User:
    _id_counter = 1

    def __init__(self, name, email):
        self.id = User._id_counter
        User._id_counter += 1

        self.name = name
        self.email = email
        self.projects = []

    def add_project(self, project_id):
        self.projects.append(project_id)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"