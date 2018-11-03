import Login
import Logout
import AccountCommands
import TextFileInterface
import CourseCommands

class UI(object):
    # dictionary matching strings to commands
    database = TextFileInterface.TextFileInterface()

    commands = {
        "login": Login.Login(database),
        "logout": Logout.Logout(database),
        "create_account": AccountCommands.CreateAccount(database),
        "delete_account": AccountCommands.DeleteAccount(database),
        "create_course": CourseCommands.CreateCourse(database),
        "assign_course": CourseCommands.AssignCourse(database)
    }

    def command(self, string, user):
        # parse input into a list, splitting by strings
        args = self.parse_commands(string)

        # get valid inputs that map to commands
        valid_args = self.commands.keys()

        # if command is valid initiate its action
        if args[0] in valid_args:
            return self.commands[args[0]].action(args, user)
        else:
            print("Invalid Command")

    # input: command of type string
    # return: list of command separated by spaces
    @staticmethod
    def parse_commands(command):
        return command.split()
