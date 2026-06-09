import sys, os, tempfile, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from models.user import User
from models.project import Project
from models.task import Task
from utils.helpers import validate_date, truncate


class TestPerson(unittest.TestCase):
    def test_email_validation(self):
        u = User("Alice", "alice@example.com")
        with self.assertRaises(ValueError):
            u.email = "not-an-email"

    def test_name_setter(self):
        u = User("Alice", "alice@example.com")
        u.name = "  Bob  "
        self.assertEqual(u.name, "Bob")

    def test_empty_name_raises(self):
        u = User("Alice", "alice@example.com")
        with self.assertRaises(ValueError):
            u.name = "   "


class TestTask(unittest.TestCase):
    def test_complete(self):
        t = Task("Write tests")
        t.complete()
        self.assertEqual(t.status, "complete")

    def test_reopen(self):
        t = Task("Write tests")
        t.complete()
        t.reopen()
        self.assertEqual(t.status, "pending")

    def test_serialise_roundtrip(self):
        t = Task("Deploy app", assigned_to="dev@example.com")
        t2 = Task.from_dict(t.to_dict())
        self.assertEqual(t.title, t2.title)
        self.assertEqual(t.assigned_to, t2.assigned_to)


class TestProject(unittest.TestCase):
    def test_add_and_retrieve_task(self):
        p = Project("Alpha")
        t = Task("Task one")
        p.add_task(t)
        self.assertEqual(p.get_task_by_id(t.id), t)

    def test_completion_rate(self):
        p = Project("Gamma")
        t1, t2 = Task("T1"), Task("T2")
        p.add_task(t1); p.add_task(t2)
        t1.complete()
        self.assertEqual(p.completion_rate(), "1/2 complete")

    def test_serialise_roundtrip(self):
        p = Project("Delta", description="desc", due_date="2025-12-31")
        p.add_task(Task("Write docs"))
        p2 = Project.from_dict(p.to_dict())
        self.assertEqual(p.title, p2.title)
        self.assertEqual(len(p2.tasks), 1)


class TestUser(unittest.TestCase):
    def test_role_validation(self):
        u = User("Dave", "dave@example.com")
        with self.assertRaises(ValueError):
            u.role = "superuser"

    def test_serialise_roundtrip(self):
        u = User("Eve", "eve@example.com", role="admin")
        p = Project("Eve's Project", owner_email=u.email)
        p.add_task(Task("Task A"))
        u.add_project(p)
        u2 = User.from_dict(u.to_dict())
        self.assertEqual(u.email, u2.email)
        self.assertEqual(len(u2.projects[0].tasks), 1)


class TestHelpers(unittest.TestCase):
    def test_validate_date_ok(self):
        self.assertEqual(validate_date("2025-06-15"), "2025-06-15")

    def test_validate_date_bad_format(self):
        with self.assertRaises(ValueError):
            validate_date("15/06/2025")

    def test_truncate(self):
        self.assertEqual(truncate("Hello world", width=5), "Hell…")


class TestStorage(unittest.TestCase):
    def test_save_and_load(self):
        import utils.storage as storage
        original = storage.USERS_FILE
        with tempfile.TemporaryDirectory() as tmpdir:
            storage.USERS_FILE = os.path.join(tmpdir, "users.json")
            users = [User("Frank", "frank@example.com")]
            storage.save_users(users)
            loaded = storage.load_users()
            self.assertEqual(loaded[0].name, "Frank")
            storage.USERS_FILE = original

    def test_load_missing_file(self):
        import utils.storage as storage
        original = storage.USERS_FILE
        storage.USERS_FILE = "/tmp/nonexistent_tracker.json"
        self.assertEqual(storage.load_users(), [])
        storage.USERS_FILE = original


if __name__ == "__main__":
    unittest.main(verbosity=2)