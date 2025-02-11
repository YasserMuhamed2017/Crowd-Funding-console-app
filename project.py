import re
import hashlib
from datetime import datetime
import pickle

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
    
    with open("f.txt", "a") as f:
        f.writelines(f"First: {first_name}, Last: {last_name}, Email: {email}, password: {hashing(password)}, Phone: {mobile_phone}\n")
    
        
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
    
    with open("f.txt", "r") as f:
        
        for line in f.readlines():
            parts = line.strip().split(', ')
            data = {}
            for part in parts:
                key, value = part.split(': ')
                data[key.strip()] = value.strip()
            
            if email == data['Email'] and hashing(password) == data['password']:
                print(f"You successfully logged in. Welcome {data['First']}!")
                while True:
                    file = open("projects.txt", 'ab')
                    print("################################################ Project ##################################")
                    print("0- Create a Project:\n1- View all projects:\n2- Edit your own project\n3- Delete your own project:\n4- Search for a project:\n5- Exit")
                    try:
                        option = int(input("Enter your option:\n"))
                    except ValueError as v:
                        print(v)
                        exit()

                    if option == 0:
                        title = input("Enter title of your project:\n")
                        details = input("Enter Details of your project:\n")
                        total_target = input("Enter Total Target in EGP:\n")
                        start_date = input("Enter start date in this format yyyy-mm-dd:\n")
                        end_date = input("Enter end date in this format yyyy-mm-dd:\n")
                        p = Project(title, details, total_target, start_date, end_date, data['Phone'])
                        pickle.dump(p, file)
                    elif option == 1:
                        Project.view_projects()
                    elif option == 2:
                        file = open('projects.txt', 'rb')
                        i = 0
                        try:
                            project_index = int(input("Enter the project number you want to edit:\n"))
                        except ValueError as v:
                            print(v)
                            exit()
                        
                        while True:
                            project = pickle.load(file)
                            if i == project_index - 1:
                                break
                            i += 1
                          
                        if 0 < project_index <= i + 1:
                            project.edit_project(project_index - 1, data['Phone'])
                            
                        else:
                            print("\nNo available projects to be edited with this number.\n")
                        file.close()

                    elif option == 3:
                        file = open("projects.txt", "rb")
                        i = 0
                        try:
                            project_index = int(input("Enter the number of project you want to delete:\n"))
                        except ValueError as v:
                            print(v)
                            exit()

                        while True:
                            project = pickle.load(file)
                            if i == project_index - 1:
                                break
                            i += 1
                          
                        if 0 <= project_index <= i + 1:
                            project.delete_project(project_index, data['Phone'])
                        else:
                            print("\nNo available projects to be deleted with this number.\n")

                        file.close()

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
        if self.validate(start_date) and self.validate(end_date):
            print("Date is in the correct format.")
        else:
            print("Date is not in the correct format.")
            return
        # Save Project Data in your project.txt file.
        self.save_project()

    
    def validate(self, date):
        try:
            date_to_check = datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError as v:
            return False

    ##################### Save Project in A File ##############################################################
    def save_project(self):
        with open("project.txt", "a") as f:
            f.writelines(f"Title: {self.title}, Details: {self.details}, Total Target: {self.total_target}, Start Date: {self.start_date}, End Date: {self.end_date}, Phone Number: {self.phone}\n")
            print("Project is created.")
            self.write_lines()
    
    def write_lines(self):
        with open("project.txt", "r") as infile, open("x.txt", "w") as outfile:
            for index, line in enumerate(infile, start=1):
                outfile.write(f"{index}- {line}")
    ############################## View All Projects #############################################################
    @staticmethod
    def view_projects():
        with open("project.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                print(line)
            if len(lines) == 0:
                print("No Projects to view. File Projects is empty.")
    
    ############################# Edit Your own Project in A File ########################
    def edit_project(self, project_index, phone):
        with open("project.txt", "r") as f:
            lines = f.readlines()
            for index, line in enumerate(lines):
                parts = line.split(',')
                data = {}
                for part in parts:
                    key, value = part.split(': ')
                    data[key.strip()] = value.strip()
                if self.phone == phone:
                    title = input("Enter title of your project:\n")
                    details = input("Enter Details of your project:\n")
                    total_target = input("Enter Total Target in EGP:\n")
                    start_date = input("Enter start date in this format yyyy-mm-dd:\n")
                    end_date = input("Enter end date in this format yyyy-mm-dd:\n")
                    if self.validate(start_date) and self.validate(end_date):
                        print("Date is in the correct format.")
                    else:
                        print("Date is not in the correct format.")
                        return
                    new_content = f"Title: {title}, Details: {details}, Total Target: {total_target}, Start Date: {start_date}, End Date: {end_date}, Phone Number: {self.phone}"
                    lines[project_index] = new_content + '\n'
                    with open("project.txt", 'w') as file:
                        file.writelines(lines)
                    return
            print("You don't have permission to edit this project.")

    ############################################# Delete A Project #######################################################
    def delete_project(self, index, phone):
        with open("project.txt", "r") as f:
            lines = f.readlines()
            lst = []
            if 0 <= index <= len(lines):
                for idx, line in enumerate(lines):
                    parts = line.split(',')
                    data = {}
                    for part in parts:
                        key, value = part.split(': ')
                        data[key.strip()] = value.strip()
                        
                    lst.append(data)
                for id, item in enumerate(lst):
                    if id == index - 1:
                        if phone == item['Phone Number']:
                            lines.pop(index - 1)
                            with open("project.txt", "w") as file:
                                file.writelines(lines)
                            print(f"Project {index} has been deleted successfully.")
                            break
                        else:
                            print("You don't have permission to delete this project.")
            else:
                print(f"Error: Index {index} is out of range. The file has {len(lines)} lines.")

    ######################################## Search for a Specific Project with a Start Date #########################
    @staticmethod 
    def search(date):
        with open("project.txt", "r") as f:
            lines = f.readlines()
            lst = []
            for idx, line in enumerate(lines):
                parts = line.split(',')
                data = {}
                for part in parts:
                    key, value = part.split(': ')
                    data[key.strip()] = value.strip()
                lst.append(data)
            count = 0
            print()
            for item in lst:
                if item['Start Date'] == date:
                    count += 1
                    for key, value in item.items():
                        print(f"{key}: {value}")
                    print()
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