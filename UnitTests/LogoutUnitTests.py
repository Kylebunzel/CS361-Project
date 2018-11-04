from unittest import TestCase
from Components.Logout import Logout
from TextFileInterface import TextFileInterface
from Environment import Environment


class LogoutUnitTests(TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")

    def test_successful_logout(self):
        self.environment.database.set_logged_in("root")
        logout = Logout(self.environment)
        user = logout.action(["logout"])
        self.assertIsNone(self.environment.user)

    def test_not_logged_on(self):
        logout = Logout(self.environment)
        user = logout.action(["logout"])
        self.assertIsNone(self.environment.user)

    def test_extra_args(self):
        self.environment.database.set_logged_in("root")
        logout = Logout(self.environment)
        logout.action(["logout", "foo"])
        self.assertIsNone(self.environment.user)
