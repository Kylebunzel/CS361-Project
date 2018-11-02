class CreateAccount:
    """
        args is a list containing the following:
            ["create_account", username, password, role]
    """
    def action(self, args, user):
        if user is None:
            print("You must be logged in to perform this action.")
            return None

        print("Create account command entered.")
