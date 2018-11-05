from unittest import TestCase
from Components.Login import Login
from TextFileInterface import TextFileInterface
from Environment import Environment
from User import User


class LoginUnitTests(TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")

    def test_not_enough_args(self):
        login = Login(self.environment)
        login.action(["login", "testuser"])
        self.assertIsNone(self.environment.user)

    def test_too_many_args(self):
        login = Login(self.environment)
        login.action(["login", "testuser", "1234", "foo"])
        self.assertIsNone(self.environment.user)

    def test_already_logged_in(self):
        self.environment.user = User("someone_else", "supervisor")

        self.environment.database.create_account("testuser", "1234", "supervisor")
        login = Login(self.environment)
        response = login.action(["login", "testuser", "1234"])

        self.assertEqual(response, "Error logging in.")
        self.assertIsNotNone(self.environment.user)

    def test_wrong_username(self):
        self.environment.database.create_account("testuser", "1234", "supervisor")
        login = Login(self.environment)
        login.action(["login", "testuse", "1234"])
        self.assertIsNone(self.environment.user)

    def test_wrong_password(self):
        self.environment.database.create_account("testuser", "1234", "supervisor")
        login = Login(self.environment)
        login.action(["login", "testuser", "4321"])
        self.assertIsNone(self.environment.user)

    def test_wrong_both(self):
        self.environment.database.create_account("testuser", "1234", "supervisor")
        login = Login(self.environment)
        login.action(["login", "testuse", "123"])
        self.assertIsNone(self.environment.user)

    def test_all_correct(self):
        self.environment.database.create_account("testuser", "1234", "supervisor")
        login = Login(self.environment)
        login.action(["login", "testuser", "1234"])
        self.assertIsNotNone(self.environment.user)
