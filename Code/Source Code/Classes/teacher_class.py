import os
import sys
from classes.staff_class import Staff

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Navigate up to the Source Code directory
source_code_dir = os.path.dirname(os.path.dirname(current_file_path))

# Add the Source Code directory to the Python path
sys.path.insert(0, source_code_dir)

# Construct the path to the data directory
data_dir = os.path.join(source_code_dir, 'data')

class Teacher(Staff):

    @staticmethod
    def authenticate(input_username, input_password):
        """
    Method to authenticate a Teacher user.

    Parameter(s):
    - input_username: str
    - input_password: str

    Returns:
    - True if authentication is successful, False otherwise
    """
        teachers_path = os.path.join(data_dir, 'teachers.txt')
        if os.path.exists(teachers_path):
            with open(teachers_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
                for line in lines:
                    username, email, password, role, recept_ID, salary, staff_info = [item.strip() for item in line.strip("\n").split(",")]
                    
                    print(f"Checking: {username}, Input: {input_username}")  # Debug print
            
                    if input_username == username:
                        if input_password == password:
                            return Teacher(username, email, password, role, recept_ID, salary, staff_info)
                        else:
                            return False
        # If we've gone through all lines and haven't returned yet, the username wasn't found
                print(f"Username {input_username} not found in file")  # Debug print
                return False
        else:
            print(f"Please check that the file {teachers_path} exists.")
            return False
            
    def __init__(self, username, email, password, role, teacher_ID, salary, staff_info):
        super().__init__(username, email, password, role, teacher_ID, salary, staff_info)

    def grade_assignment(self):
        pass

    def create_assignment(self):
        pass

if __name__ == "__main__":
    teacher = Teacher("John Doe", "john.doe@example.com", "password123", "teacher", "T001", 50000, "Teacher of Mathematics", "T001")
    print(teacher.username)
    print(teacher.email)
    print(teacher.password)
    print(teacher.role)
    print(teacher.staff_ID)
    print(teacher.salary)
    print(teacher.staff_info)
    print(teacher.teacher_ID)