import TextFileInterface
import User
import hashlib

class Login:

    def __init__(self, database):
        self.database = database

    """
        args is a list containing the following:
            ["login", <username>, <password>]
    """
    def action(self, args, user):
        if user is not None:
            print("Someone else is logged in.")
            return user

        user_list = self.database.get_accounts()

        account = {}

        for i in user_list:
            if i["name"] == args[1]:
                account = i

        if len(account) == 0:
            print("Username or Password is Incorrect")
            return user

        hash = hashlib.new("md5")
        entered_password = args[2].rstrip()
        hash.update(f"{entered_password}".encode("ascii"))
        hashed_password = hash.hexdigest()

        if account["password"] != hashed_password:
            print("User name or Password is Incorrect")
            return None

        self.database.set_logged_in(account["name"])
        print("Logged in successfully")
        return User.User(account["name"], account["role"])
