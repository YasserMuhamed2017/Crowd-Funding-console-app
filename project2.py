import re
import hashlib
from datetime import datetime
import csv
############################################# Registration Function ###############################################
def register():
    print("################################################ Authentication System ######################################")
    print("################################################ Registration ###############################################")
    
    first_name = input("Enter your First Name\n")
    last_name = input("Enter your Last Name\n")
    email = input("Enter your Email\n")
    if validate_email(email) is None:
        print("Error: you entered a wrong email.")
        return
    
    mobile_phone = input("Enter your Mobile Number\n")
    if validate_mobile_phone(mobile_phone) is None:
        print("Error: you entered a wrong phone number.")
        return
    
    password = input("Enter your password\n")
    if not validate_password(password):
        print("Error: Your password must be 8 characters at least.")
        return
    
    confirmed_password = input("Confirm your Password\n")
    if not validate_password(password):
        print("Error: Your password must be 8 characters at least.")
        return

    if validate(password, confirmed_password):
        print("Password match")
    else:
        print("Password not match")
        return
    
    with open("login.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([first_name, last_name, email, password, mobile_phone])
    
        
# Hashing Function     
def hashing(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Validation (Password Match)
def validate(password, confirmed_password):
    pattern =  r"^.[^\s]{8,}$"
    if re.match(pattern, password) and re.match(pattern, confirmed_password):
        hashed_password = hashing(password)
        confirmed_hashed_password = hashing(confirmed_password)

        if hashed_password == confirmed_hashed_password:
            return True
        else:
            return False

    elif (len(pattern) < 8):
        print("Password must be at least 8 characters.")
    elif " " in password:
        print("Your Password contains a space.")
    elif " " in confirmed_password:
        print("Your Password contains a space.")

# Validation (Phone)
def validate_mobile_phone(mobile_phone):
    pattern = r"^01[0-2, 5]\d{8}$"
    return re.fullmatch(pattern, mobile_phone)

# Validation (Email)
def validate_email(email):
    pattern = r"^[a-zA-Z0-9]+@[a-z]+\.com$"
    return re.match(pattern, email)

# Validation (Password)
def validate_password(password):
    pattern =  r"^.[^\s]{8,}$"
    return re.match(pattern, password)


###################################################### Login Function #################################################
def login():
    print("################################################ Authentication System ######################################")
    print("################################################ Login ######################################################")
    email = input("Enter your email:\n")
    if not validate_email(email):
        print("Error: you entered a wrong email.")
        return
    
    password = input("Enter your password:\n")
    if not validate_password(password):
        print("Error: Your password must be 8 characters at least.")
        return
    
    with open("login.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if email == row[2] and password == row[3]:
                phone = row[4]
                print(f"You successfully logged in. Welcome {row[0]}!")
                while True:
                    print("################################################ Project ##################################")
                    print("0- Create a Project:\n1- View all projects:\n2- Edit your own project\n3- Delete your own project:\n4- Search for a project:\n5- Exit")

                    try:
                        option = int(input("Enter your option:\n"))
                    except ValueError as v:
                        print("You entered a value that's not allowed to enter.")
                        break
                        
                    if option == 0:
                        title = input("Enter title of your project:\n")
                        details = input("Enter Details of your project:\n")
                        total_target = input("Enter Total Target in EGP:\n")
                        start_date = input("Enter start date in this format yyyy-mm-dd:\n")
                        end_date = input("Enter end date in this format yyyy-mm-dd:\n")
                        p = Project(title, details, total_target, start_date, end_date, row[4])
                    elif option == 1:
                        Project.view_projects()
                    elif option == 2:
                        with open("project.csv", "r") as file:
                            rows = []
                            reader = csv.reader(file)
                            project_index = int(input("Enter the project number you want to edit:\n"))
                            rows = list(reader)
                            length = len(rows)
                            for idx, row in enumerate(rows):
                                try:
                                    if project_index == idx:
                                        Project.edit_project(project_index, phone, row[5])
                                        break
                                except ValueError as v:
                                    print("You entered a value that's not allowed to enter.")
                                    break
                            if length < project_index:
                                print("\nNo available projects to be edited with this number.\n")
                    elif option == 3:
                        with open("project.csv", "r") as file:
                            rows = []
                            reader = csv.reader(file)
                            project_index = int(input("Enter the project number you want to delete:\n"))
                            rows = list(csv.reader(file))
                            length = len(rows)
                            for idx, row in enumerate(rows):
                                try:
                                    if project_index == idx:
                                        Project.delete_project(project_index, phone, row[5])
                                        break
                                except ValueError as v:
                                    print("You entered a value that's not allowed to enter.")
                                    return
                            if length < project_index:
                                print("No available projects to be deleted with this number.\n")
                                
                    elif option == 4:
                        date = input("Enter Start Date to search for a project:\n")
                        Project.search(date)
                    elif option == 5:
                        exit()
                    else:
                        print("Invalid option. Please try again.")           
        print("Your creditionals are not correct. Please, try again.")

###################################### Class Object For Project #############################################
class Project():
    def __init__(self, title, details, total_target, start_date, end_date, phone):
        self.phone = phone
        self.title = title
        self.details = details
        self.total_target = total_target
        self.start_date = start_date
        self.end_date = end_date

        # Validate date format.
        if self.validate_date(start_date) and self.validate_date(end_date):
            print("Date is in the correct format.")
        else:
            print("Date is not in the correct format.")
            return
        # Save Project Data in your project.txt file.
        self.save_project()

    
    def validate_date(self, date):
        try:
            date_to_check = datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError as v:
            return False
        
    @classmethod
    def validate(cls, date):
        try:
            date_to_check = datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError as v:
            return False

    ##################### Save Project in A File ##############################################################
    def save_project(self):
        with open("project.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([self.title, self.details, self.total_target, self.start_date, self.end_date, self.phone])
            print("Project is created.")
            
    ############################## View All Projects #############################################################
    @staticmethod
    def view_projects():
        with open("project.csv", "r") as file:
            reader = list(csv.reader(file)) 
            if len(reader) != 0:
                print("------------------------ View Projects ---------------")
            for idx, row in enumerate(reader):
                if idx != 0:
                    print(str(idx) + "- Title: " + row[0], end=", ")
                    print("Details: " + row[1], end=", ")
                    print("Total Target: " + row[2], end=", ")
                    print("Start Date: " + row[3], end=", ")
                    print("End Date: " + row[4], end=", ")
                    print("Phone Number: " + row[5])
                    print("--------------------------------------------------------")
            if len(reader) == 0:
                print("No Projects to view. File Projects is empty.")
    
    ############################# Edit Your own Project in A File ########################
    @classmethod
    def edit_project(cls, project_index, phone_owner, project_owner_phone):
        with open("project.csv", "r") as file:
                rows = []
                reader = csv.reader(file)
                rows = list(reader)
                for idx, row in enumerate(rows):
                    if phone_owner == project_owner_phone and idx == project_index:
                        title = input("Enter title of your project:\n")
                        details = input("Enter Details of your project:\n")
                        total_target = input("Enter Total Target in EGP:\n")
                        start_date = input("Enter start date in this format yyyy-mm-dd:\n")
                        end_date = input("Enter end date in this format yyyy-mm-dd:\n")
                        if cls.validate(start_date) and cls.validate(end_date):
                            print("Date is in the correct format.")
                        else:
                            print("Date is not in the correct format.")
                            return
                        row[0] = title
                        row[1] = details 
                        row[2] = total_target
                        row[3] = start_date
                        row[4] = end_date
                        row[5] = phone_owner
                        with open("project.csv", 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerows(rows)
                            print("Project is finally edited.")
                            return
                print("You don't have permission to edit this project.")

    ############################################# Delete A Project #######################################################
    @classmethod
    def delete_project(cls, project_index, phone_owner, project_owner_phone):
        with open("project.csv", "r") as file:
            rows = []
            reader = csv.reader(file)
            rows = list(reader)
            for idx, row in enumerate(rows):
                if phone_owner == project_owner_phone and idx == project_index:
                    rows.pop(idx)
                    with open("project.csv", 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)
                        print("Project is finally deleted.")
                        return
            print("You don't have permission to delete this project.")
            return
    ######################################## Search for a Specific Project with a Start Date #########################
    @staticmethod 
    def search(date):
        with open("project.csv", "r") as file:
            rows = []
            reader = csv.reader(file)
            rows = list(reader)
            count = 0
            for idx, row in enumerate(rows):
                if row[3] == date:
                    count += 1
                    print("-----------------------------------------------------------------------------------------")
                    print("Title: " + row[0], end=", ")
                    print("Details: " + row[1], end=", ")
                    print("Total Target: " + row[2], end=", ")
                    print("Start Date: " + row[3], end=", ")
                    print("End Date: " + row[4], end=", ")
                    print("Phone Number: " + row[5])
                    
            if count == 0:
                print("No projects with the specified date.")

while True:
    print("################################################ Full Project###############################################")
    print("1- Registeration\n2- Login\n3- Exit")
    try:
        option = int(input("Enter your option:\n"))
    except ValueError as v:
        print(v)
        break
    if option == 1:
        register()
    elif option == 2:
        login()
    elif option == 3:
        exit()
    else:
        print("Invalid option. Please try again.")