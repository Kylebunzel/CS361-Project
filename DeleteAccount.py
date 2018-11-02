class DeleteAccount:
    def __init__(self):
        pass

    """
        args is a list containing the following:
            ["delete_account", username]
    """
    def action(self, args, user):
        if user is None:
            "Print you must be logged in to perform this action."
            return None

        print("Delete Account command entered")
