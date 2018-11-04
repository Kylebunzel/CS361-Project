import unittest
from TextFileInterface import TextFileInterface
from Components.AccountCommands import CreateAccount, DeleteAccount, ViewAccounts
from Environment import Environment
from User import User


class CreateAccountUnitTests(unittest.TestCase):

    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi, DEBUG=True)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")

    def test_create_account_correct_args(self):
        self.environment.user = User("root", "administrator")
        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertIsNotNone(create_account.get_user(user_name))
        self.assertEqual(response, "Account created.")

    def test_create_account_no_permissions(self):
        self.environment.user = User("ta_acct", "TA")

        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertIsNone(create_account.get_user(user_name))
        self.assertEqual(response, "Error creating account.")

    def test_create_account_not_logged_in(self):
        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertIsNone(create_account.get_user(user_name))
        self.assertEqual(response, "Error creating account.")

    def test_create_account_account_exists(self):
        self.environment.user = User("root", "administrator")
        user_name = "new_user"
        self.environment.database.create_account(user_name, "password", "TA")

        create_account = CreateAccount(self.environment)
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertEqual(response, "Error creating account.")


class DeleteAccountUnitTests(unittest.TestCase):

    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi, DEBUG=True)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")

    def test_delete_account_correct_args(self):
        self.environment.user = User("root", "administrator")
        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action(["delete_account", user_name])

        self.assertEqual(response, "Account deleted.")
        self.assertIsNone(delete_command.get_user(user_name))

    def test_delete_account_that_doesnt_exist(self):
        self.environment.user = User("root", "administrator")
        user_name = "nonexisting_account"

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action(["delete_account", user_name])

        self.assertEqual(response, "Error deleting account.")

    def test_delete_account_no_permissions(self):
        self.environment.user = User("TA_user", "TA")

        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action(["delete_account", user_name])

        self.assertEqual(response, "Error deleting account.")
        self.assertIsNotNone(delete_command.get_user(user_name))

    def test_delete_account_no_args(self):
        self.environment.user = User("root", "administrator")
        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action(["delete_account"])

        self.assertEqual(response, "Error deleting account.")
        self.assertIsNotNone(delete_command.get_user(user_name))


class ViewAccountsUnitTests(unittest.TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi, DEBUG=True)
        self.environment.database.clear_database()

    def test_view_accounts_none_in_database(self):
        self.environment.user = User("root", "administrator")
        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])

        self.assertEqual(response, "")

    def test_view_accounts_3_valid_in_database(self):
        self.environment.user = User("root", "administrator")
        self.environment.database.create_account("InstructorUser", "password", "instructor")
        self.environment.database.create_account("AdministratorUser", "password", "administrator")
        self.environment.database.create_account("SupervisorUser", "password", "supervisor")

        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])

        self.assertEqual(response,  "InstructorUser instructor\n" +
                                    "AdministratorUser administrator\n" +
                                    "SupervisorUser supervisor\n")

    def test_view_accounts_not_logged_in(self):
        self.environment.database.create_account("InstructorUser", "password", "instructor")
        self.environment.database.create_account("AdministratorUser", "password", "administrator")
        self.environment.database.create_account("SupervisorUser", "password", "supervisor")

        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])
        self.assertEqual(response, "Error viewing accounts.")
