import unittest
from TextFileInterface import TextFileInterface
from Components.LabCommands import CreateLab, AssignLab, ViewLabs
from Environment import Environment
from User import User


class CreateLabUnitTests(unittest.TestCase):

    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi, DEBUG=True)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")
        self.environment.database.create_course("361", "SoftwareEngineering")

    def test_create_lab_correct_args(self):
        self.environment.user = User("root", "administrator")

        create_command = CreateLab(self.environment)
        course_number = "361"
        lab_number = "801"
        response = create_command.action(["create_lab", course_number, lab_number])

        self.assertTrue(create_command.lab_exists(course_number, lab_number))
        self.assertEqual(response, "Lab created.")

    def test_create_lab_wrong_num_args(self):
        self.environment.user = User("root", "administrator")

        create_command = CreateLab(self.environment)
        course_number = "361"
        lab_number = "801"
        response = create_command.action(["create_lab", course_number])

        self.assertFalse(create_command.lab_exists(course_number, lab_number))
        self.assertEqual(response, "Error creating lab.")

    def test_create_lab_no_permissions(self):
        self.environment.user = User("root", "TA")

        create_command = CreateLab(self.environment)
        course_number = "361"
        lab_number = "801"
        response = create_command.action(["create_lab", course_number, lab_number])

        self.assertFalse(create_command.lab_exists(course_number, lab_number))
        self.assertEqual(response, "Error creating lab.")

    def test_create_lab_not_logged_in(self):
        create_command = CreateLab(self.environment)
        course_number = "361"
        lab_number = "801"
        response = create_command.action(["create_lab", course_number, lab_number])

        self.assertFalse(create_command.lab_exists(course_number, lab_number))
        self.assertEqual(response, "Error creating lab.")

    def test_create_lab_already_exists(self):
        self.environment.user = User("root", "administrator")
        course_number = "361"
        lab_number = "801"
        self.environment.database.create_lab(course_number, lab_number)

        create_command = CreateLab(self.environment)
        response = create_command.action(["create_lab", course_number, lab_number])

        self.assertEqual(response, "Error creating lab.")

    def test_create_lab_course_doesnt_exist(self):
        self.environment.user = User("root", "administrator")
        course_number = "3000"
        lab_number = "801"
        create_command = CreateLab(self.environment)
        response = create_command.action(["create_lab", course_number, lab_number])

        self.assertFalse(create_command.lab_exists(course_number, lab_number))
        self.assertEqual(response, "Error creating lab.")


class AssignLabUnitTests(unittest.TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi, DEBUG=True)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")
        self.environment.database.create_course("361", "SoftwareEngineering")
        self.environment.database.create_lab("361", "801")
        self.environment.database.create_account("apoorv", "password", "TA")

    def test_assign_lab_correct_args_and_permissions(self):
        self.environment.user = User("jayson", "instructor")

        course_number = "361"
        lab_number = "801"
        assign_command = AssignLab(self.environment)
        response = assign_command.action(["assign_lab", course_number, lab_number, "apoorv"])

        self.assertTrue(assign_command.lab_assigned(course_number, lab_number))
        self.assertEqual(response, "Assigned to lab.")

    def test_assign_lab_no_permissions(self):
        self.environment.user = User("apoorv", "TA")

        course_number = "361"
        lab_number = "801"
        assign_command = AssignLab(self.environment)
        response = assign_command.action(["assign_lab", course_number, lab_number, "apoorv"])

        self.assertFalse(assign_command.lab_assigned(course_number, lab_number))
        self.assertEqual(response, "Error assigning to lab.")

    def test_assign_lab_not_logged_in(self):
        course_number = "361"
        lab_number = "801"
        assign_command = AssignLab(self.environment)
        response = assign_command.action(["assign_lab", course_number, lab_number, "apoorv"])

        self.assertFalse(assign_command.lab_assigned(course_number, lab_number))
        self.assertEqual(response, "Error assigning to lab.")

    def test_assign_lab_wrong_num_args(self):
        self.environment.user = User("root", "administrator")

        course_number = "361"
        lab_number = "801"
        assign_command = AssignLab(self.environment)
        response = assign_command.action(["assign_lab", course_number, lab_number])

        self.assertFalse(assign_command.lab_assigned(course_number, lab_number))
        self.assertEqual(response, "Error assigning to lab.")

    def test_assign_lab_that_doesnt_exist(self):
        self.environment.user = User("root", "administrator")

        course_number = "361"
        lab_number = "888"
        assign_command = AssignLab(self.environment)
        response = assign_command.action(["assign_lab", course_number, lab_number, "apoorv"])

        self.assertFalse(assign_command.lab_assigned(course_number, lab_number))
        self.assertEqual(response, "Error assigning to lab.")

    def test_assign_lab_that_already_assigned(self):
        self.environment.user = User("root", "administrator")

        course_number = "361"
        lab_number = "801"

        assign_command = AssignLab(self.environment)
        self.environment.database.set_lab_assignment(course_number, lab_number, "apoorv")
        self.assertTrue(assign_command.lab_assigned(course_number, lab_number))

        response = assign_command.action(["assign_lab", course_number, lab_number, "apoorv"])

        self.assertEqual(response, "Error assigning to lab.")

    def test_assign_lab_to_nonexistant_user(self):
        self.environment.user = User("root", "administrator")

        course_number = "361"
        lab_number = "801"
        assign_command = AssignLab(self.environment)
        response = assign_command.action(["assign_lab", course_number, lab_number, "IDontExist"])

        self.assertFalse(assign_command.lab_assigned(course_number, lab_number))
        self.assertEqual(response, "Error assigning to lab.")

    def test_assign_lab_to_not_a_ta(self):
        self.environment.user = User("root", "administrator")
        self.environment.database.create_account("jayson", "password", "instructor")

        course_number = "361"
        lab_number = "801"
        assign_command = AssignLab(self.environment)
        response = assign_command.action(["assign_lab", course_number, lab_number, "jayson"])

        self.assertFalse(assign_command.lab_assigned(course_number, lab_number))
        self.assertEqual(response, "Error assigning to lab.")


class ViewLabsUnitTests(unittest.TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi, DEBUG=True)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")

        self.environment.database.create_course("361", "SoftwareEngineering")
        self.environment.database.create_lab("361", "801")
        self.environment.database.create_lab("361", "802")
        self.environment.database.create_lab("361", "803")

        self.environment.database.create_account("apoorv", "password", "TA")

        self.environment.database.set_lab_assignment("361", "802", "apoorv")

    def test_view_labs_not_logged_in(self):
        view_command = ViewLabs(self.environment)
        response = view_command.action(["view_labs"])

        self.assertEqual(response, "Error viewing labs.")

    def test_view_labs_wrong_num_args(self):
        self.environment.user = User("root", "administrator")
        view_command = ViewLabs(self.environment)
        response = view_command.action(["view_labs", "extraBogusArg"])

        self.assertEqual(response, "Error viewing labs.")

    # really dumb test - any role can view labs
    def test_view_labs_no_permissions(self):
        self.environment.user = User("bogusUser", "bogusRole")
        view_command = ViewLabs(self.environment)
        response = view_command.action(["view_labs"])

        self.assertEqual(response, "Error viewing labs.")

    def test_view_labs_correct(self):
        self.environment.user = User("root", "administrator")
        view_command = ViewLabs(self.environment)
        response = view_command.action(["view_labs"])

        self.assertEqual(response,  "361 801\n" +
                                    "361 802 apoorv\n" +
                                    "361 803\n")
