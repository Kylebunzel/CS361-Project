from unittest import TestCase
from Command import Command
from TextFileInterface import TextFileInterface
from Environment import Environment


# concrete base class of abstract Command to allow testing
class ConcreteCommand(Command):
    def action(self, args):
        pass


class CommandTests(TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.environment.database.clear_database()
        self.cmd = ConcreteCommand(self.environment)

    # User Test cases
    def test_get_user_exists(self):
        self.environment.database.create_account("root", "root", "administrator")
        self.assertIsNotNone(self.cmd.get_user("root"))

    def test_get_user_doesnt_exist(self):
        self.assertIsNone(self.cmd.get_user("nonexistent"))

    # Course Test cases
    def test_get_course_exists(self):
        self.environment.database.create_course("123", "test_course")
        self.assertIsNotNone(self.cmd.course_exists("123"))

    def test_get_course_doesnt_exist(self):
        self.assertIsNotNone(self.cmd.course_exists("000"))

    def test_get_course_assigned(self):
        self.environment.database.create_account("teacher", "root", "instructor")
        self.environment.database.create_course("123", "test_course")
        self.environment.database.set_course_assignment("123", "teacher")
        self.assertTrue(self.cmd.course_assigned("123"))

    def test_get_course_not_assigned(self):
        self.assertFalse(self.cmd.course_assigned("000"))

    def test_get_lab_exists(self):
        self.environment.database.create_course("123", "test_course")
        self.environment.database.create_lab("123", "001")
        self.assertTrue(self.cmd.lab_exists("123", "001"))

    def test_get_lab_doesnt_exist(self):
        self.assertFalse(self.cmd.lab_exists("123", "1231231"))

    def test_get_lab_assigned(self):
        self.environment.database.create_account("ta", "pass", "TA")
        self.environment.database.create_course("123", "test_course")
        self.environment.database.create_lab("123", "001")
        self.environment.database.set_lab_assignment("123", "001", "ta")
        self.assertTrue(self.cmd.lab_assigned("123", "001"))

    def test_get_lab_not_assigned(self):
        self.environment.database.create_course("234", "test_course2")
        self.environment.database.create_lab("234", "000")
        self.assertFalse(self.cmd.lab_assigned("234", "000"))

    def test_valid_role_admin(self):
        self.assertTrue(self.cmd.is_valid_role("administrator"))

    def test_valid_role_supervisor(self):
        self.assertTrue(self.cmd.is_valid_role("supervisor"))

    def test_valid_role_instructor(self):
        self.assertTrue(self.cmd.is_valid_role("instructor"))

    def test_valid_role_TA(self):
        self.assertTrue(self.cmd.is_valid_role("TA"))

    def test_invalid_role(self):
        self.assertFalse(self.cmd.is_valid_role("invalid"))




