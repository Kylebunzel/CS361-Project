import unittest


class CreateCourseTests(unittest.TestCase):
    def setUp(self):
        self.ui = UI()

    def test_command_create_course_supervisor(self):
        """
            @jkuniqh
            The only ones able to create a course are the supervisor and the administrator

            When create_course command is entered, it expects two arguments (for now, maybe later we can add more details):
             - class number
             - class name
            The response is a string, either:
             - If Successful: "Created course."
             - If Failure: "Error creating course."
        """
        # Create a supervisor account and log in as part of the setup
        self.ui.command("create_account userSupervisor userPassword supervisor")
        self.ui.command("login userSupervisor userPassword")

        # Command: "create_course 361 SystemsProgramming", expect success
        self.assertEquals(self.ui.command("create_course 361 SystemsProgramming"), "Created course.")

    def test_command_create_course_administrator(self):
        self.ui.command("create_account userAdministrator userPassword administrator")
        self.ui.command("login userAdministrator userPassword")
        self.assertEquals(self.ui.command("create_course 361 SystemsProgramming"), "Created course.")

    def test_command_create_course_instructor(self):
        self.ui.command("create_account userInstructor userPassword instructor")
        self.ui.command("login userInstructor userPassword")
        self.assertEquals(self.ui.command("create_course 361 SystemsProgramming"),
                          "Error creating course.")

    def test_command_create_course_TA(self):
        self.ui.command("create_account userTA userPassword ta")
        self.ui.command("login userInstructor userPassword")
        self.assertEquals(self.ui.command("create_course 361 SystemsProgramming"),
                          "Error creating course.")

    def test_command_create_course_format(self):
        # Command: "create_course", expect error, not enough arguments
        self.ui.command("create_account userSupervisor userPassword supervisor")
        self.ui.command("login userSupervisor userPassword")
        self.assertEquals(self.ui.command("create_course"), "Error creating course.")
        self.assertEquals(self.ui.command("create_course 361"), "Error creating course.")
        self.assertEquals(self.ui.command("create_course SystemProgramming"), "Error creating course.")
        self.assertEquals(self.ui.command("create_course SystemsProgramming 361"), "Erro creating course.")


    def test_command_create_course_duplicate(self):
        self.ui.command("create_account userSupervisor userPassword supervisor")
        self.ui.command("login userSupervisor userPassword")
        self.assertEquals(self.ui.command("create_course 361 SystemsProgramming"), "Created course.")
        self.assertEquals(self.ui.command("create_course 361 SystemsProgramming"), "Error creating course.")
