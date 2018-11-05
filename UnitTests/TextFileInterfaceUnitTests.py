import unittest
import hashlib
from TextFileInterface import TextFileInterface


class TextFileInterfaceUnitTests(unittest.TestCase):

    @staticmethod
    def hashed_password(password):
        h = hashlib.new("md5")
        h.update(f"{password}".encode("ascii"))
        return h.hexdigest()

    def setUp(self):
        self.tfi = TextFileInterface(
            relative_directory="../../CS361-Project/TextDB/")

    def test_constructor(self):
        self.assertIsNotNone(self.tfi.account_filename)
        self.assertIsNotNone(self.tfi.login_filename)
        self.assertIsNotNone(self.tfi.course_filename)
        self.assertIsNotNone(self.tfi.course_assignment_filename)
        self.assertIsNotNone(self.tfi.lab_filename)
        self.assertIsNotNone(self.tfi.lab_assignment_filename)

    def test_clear_database(self):
        self.tfi.create_account("account", "pass", "role")
        self.tfi.create_course("1", "course")
        self.tfi.create_lab("1", "801")
        self.tfi.set_course_assignment("1", "jayson")
        self.tfi.set_lab_assignment("1", "801", "apoorv")

        self.tfi.clear_database()

        dbfiles = [self.tfi.account_filename,
                   self.tfi.course_filename,
                   self.tfi.course_assignment_filename,
                   self.tfi.login_filename,
                   self.tfi.lab_filename,
                   self.tfi.lab_assignment_filename
                   ]
        for file in dbfiles:
            fin = open(file, "r")
            lines = fin.readlines()
            fin.close()

            self.assertEqual(lines, [])

    def test_create_account(self):
        password = "pass"
        self.tfi.create_account("account", password, "role")

        account_file = open(self.tfi.account_filename, "r")
        lines = account_file.readlines()
        account_file.close()

        self.assertEqual(lines, ["account:" + self.hashed_password(password) + ":role\n"])

    def test_delete_account(self):
        self.tfi.create_account("account", "pass", "role")
        self.tfi.delete_account("account")

        account_file = open(self.tfi.account_filename, "r")
        lines = account_file.readlines()
        account_file.close()

        self.assertEqual(lines, [])

    def test_update_account(self):
        password = "newpass"
        self.tfi.create_account("account", "pass", "role")
        self.tfi.update_account("account", password, "newrole")

        account_file = open(self.tfi.account_filename, "r")
        lines = account_file.readlines()
        account_file.close()

        self.assertEqual(lines, ["account:"+self.hashed_password(password)+":newrole\n"])


    def test_get_accounts(self):
        password1 = "pass"
        password2 = "pass2"

        self.tfi.create_account("account", password1, "role")
        self.tfi.create_account("account2", password2, "role2")

        accounts = self.tfi.get_accounts()

        self.assertEqual(accounts, [{"name":"account", "password":self.hashed_password(password1), "role":"role"},
                                    {"name":"account2","password":self.hashed_password(password2), "role":"role2"}])



