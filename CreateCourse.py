import Command


class CreateCourse(Command.Command):
    def __init__(self):
        pass

    """
        args is a list containing the following:
            ["create_Course", name, number]
    """
    def action(self, args):
        print("Create Course command entered.")
        """
            Creates a course with specified name and number.
        """
