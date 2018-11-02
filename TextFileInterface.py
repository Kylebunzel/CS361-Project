import DataInterface
import hashlib


class TextFileInterface(DataInterface.DataInterface):
    def __init__(self):
        self.account_filename = "account.txt"
        self.login_filename = "login.txt"
        self.course_filename = "course.txt"
        self.course_assignment_filename = "course_assignments.txt"
        self.lab_filename = "lab.txt"
        self.lab_assignment_filename = "lab_assignments.txt"

    def create_account(self, account_name, password, role):
        hash = hashlib.new("md5")
        hash.update(f"{password}".encode("ascii"))
        hashed_password = hash.hexdigest()
        account_file = open(self.account_filename, "a")
        account_file.write(f"{account_name}:{hashed_password}:{role}\n")
        account_file.close()

    def delete_account(self, account_name):
        account_file = open(self.account_filename, "r")
        lines = []
        for line in account_file:
            if line.split(":")[0] != account_name:
                lines.append(line)
        account_file.close()

        account_file = open(self.account_filename, "w")
        account_file.writelines(lines)
        account_file.close()

    def update_account(self, account_name, password, role):
        self.delete_account(account_name)
        self.create_account(account_name, password, role)

    def get_accounts(self):
        accounts = []
        account_file = open(self.account_filename, "r")
        lines = account_file.readlines()
        account_file.close()
        for line in lines:
            fields = line.split(":")
            accounts.append({"name": fields[0], "password": fields[1], "role": fields[2].rstrip()})
        return accounts

    def get_logged_in(self):
        login_file = open(self.login_filename, "r")
        logged_in_user = login_file.readline().rstrip()
        login_file.close()
        return logged_in_user

    def set_logged_in(self, account_name):
        login_file = open(self.login_filename, "w")
        login_file.write(f"{account_name}\n")
        login_file.close()

    def set_logged_out(self):
        login_file = open(self.login_filename, "w")
        login_file.close()

    def create_course(self, course_number, course_name,):
        course_file = open(self.course_filename, "a")
        course_file.write(f"{course_number}:{course_name}\n")
        course_file.close()

    def get_courses(self):
        courses = []
        course_file = open(self.course_filename, "r")
        lines = course_file.readlines()
        course_file.close()
        for line in lines:
            fields = line.split(":")
            courses.append({"number": fields[0], "name": fields[1].rstrip()})
        return courses

    def set_course_assignment(self, course_number, instructor_name):
        course_assignment_file = open(self.course_assignment_filename, "a")
        course_assignment_file.write(f"{course_number}:{instructor_name}\n")
        course_assignment_file.close()

    def get_labs(self):
        labs = []
        lab_file = open(self.lab_filename, "r")
        lines = lab_file.readlines()
        lab_file.close()
        for line in lines:
            fields = line.split(":")
            labs.append({"course_number": fields[0], "lab_number": fields[1], "ta_name": fields[2].rstrip()})
        return labs

    def set_lab_assignment(self, course_number, lab_number, ta_name):
        lab_file = open(self.lab_filename, "a")
        lab_file.write(f"{course_number}:{lab_number}:{ta_name}\n")
        lab_file.close()

