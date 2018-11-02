import UI
import TextFileInterface
# create an instance of the UI
ui = UI.UI()

TextFileInterface.TextFileInterface().create_account("tyler", "a", "supervisor")
# create a user to determine if someone is logged onto the system
# if CurrentUser is none: no one is logged on
# if CurrentUser is not None, someone is logged on.
currentUser = None

# set application to running
running = True
while running:
    s = input("Enter a command: ")

    # stop and quit application
    if s == "q":
        running = False
    else:
        # take input and attempt to change into a command
        currentUser = ui.command(s, currentUser)

print("Program has been terminated.")

