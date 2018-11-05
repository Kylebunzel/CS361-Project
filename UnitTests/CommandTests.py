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
        self.environment.database.create_account("root", "root", "administrator")

    def test_get_user_exists(self):
        cmd = ConcreteCommand(self.environment)
        self.assertIsNotNone(cmd.get_user("root"))

    def test_get_user_doesnt_exist(self):
        cmd = ConcreteCommand(self.environment)
        self.assertIsNone(cmd.get_user("nonexistent"))
