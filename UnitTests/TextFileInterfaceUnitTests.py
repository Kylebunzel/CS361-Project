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
            relative_directory="TestDB/")
        self.tfi.clear_database()

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

    def test_get_set_logged_in(self):
        self.tfi.set_logged_in("account")

        response = self.tfi.get_logged_in()

        self.assertEqual(response, "account")

    def test_set_logged_in_set_logged_out(self):
        self.tfi.set_logged_in("account")

        response = self.tfi.get_logged_in()
        self.assertEqual(response, "account")

        self.tfi.set_logged_out()

        response = self.tfi.get_logged_in()
        self.assertEqual(response, "")

    def test_create_course_get_courses(self):
        self.tfi.create_course("361", "CompSci361")

        response = self.tfi.get_courses()

        self.assertEqual(response, [{"course_name":"CompSci361", "course_number":"361"}])

    def test_create_course_assignments_get_courses_assignments(self):
        self.tfi.set_course_assignment("361", "jayson")

        response = self.tfi.get_course_assignments()

        self.assertEqual(response, [{"instructor_name":"jayson", "course_number":"361"}])

    def test_create_lab_get_labs(self):
        self.tfi.create_lab("361", "801")

        response = self.tfi.get_labs()

        self.assertEqual(response, [{"course_number":"361", "lab_number":"801"}])

    def test_create_lab_assignment_get_lab_assignments(self):
        self.tfi.set_lab_assignment("361", "801", "apoorv")

        response = self.tfi.get_lab_assignments()

        self.assertEqual(response, [{"course_number":"361", "lab_number":"801", "ta_name":"apoorv"}])
