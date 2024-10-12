import os
import sys
from classes.staff_class import Staff
from classes.teacher_class import Teacher
from classes.student_class import Student

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Navigate up to the Source Code directory
source_code_dir = os.path.dirname(os.path.dirname(current_file_path))

# Add the Source Code directory to the Python path
sys.path.insert(0, source_code_dir)

# Construct the path to the data directory
data_dir = os.path.join(source_code_dir, 'data')

class Receptionist(Staff):
    
    @staticmethod
    def authenticate(input_username, input_password):
        """
    Method to authenticate a Receptionist user.

    Parameter(s):
    - input_username: str
    - input_password: str

    Returns:
    - True if authentication is successful, False otherwise
    """
        receptionists_path = os.path.join(data_dir, 'receptionists.txt')
        if os.path.exists(receptionists_path):
            with open(receptionists_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
                for line in lines:
                    username, email, password, role, recept_ID, salary, staff_info = [item.strip() for item in line.strip("\n").split(",")]
                    
                    print(f"Checking: {username}, Input: {input_username}")  # Debug print
            
                    if input_username == username:
                        if input_password == password:
                            return Receptionist(username, email, password, role, recept_ID, salary, staff_info)
                        else:
                            return False
        # If we've gone through all lines and haven't returned yet, the username wasn't found
                print(f"Username {input_username} not found in file")  # Debug print
                return False
        else:
            print(f"Please check that the file {receptionists_path} exists.")
            return False
            
    def __init__(self, username, email, password, role, recept_id, salary, staff_info):
        super().__init__(role, recept_id, salary, staff_info)
        self.username = username
        self.email = email
        self.password = password
        self.import_all_data()
    
    def import_all_data(self):
        """
        Import all data necesseary for latter.
        """
        self.import_teachers_data()
        self.import_student_data()
    
    def import_teachers_data(self):
        """
        Import teachers' data.

        Returns:
        Bool -  True if import successfully, 
                false otherwise
        """
        self.teachers = []
        teachers_path = "./Data/teachers.txt"
        if os.path.exists(teachers_path):
            with open(teachers_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                # Sequence unpacking
                # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
                username, email, password, role, recept_id, salary, staff_info = line.strip("\n").split(",")
                teacher_obj = Teacher(username, email, password, role, recept_id, salary, staff_info)
                self.teachers.append(teacher_obj)
        else:
            print(f"Please check the subdirectory and file exists for {teachers_path}.")

    def import_students_data(self):
        """
        Import students' data.

        Returns:
        Bool -  True if import successfully, 
                false otherwise
        """
        self.students = []
        students_path = "./data/pst4_students.txt"
        if os.path.exists(students_path):
            with open(students_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
                for line in lines:
                    username, email, password, student_id = line.strip("\n").split(",")
                    student_obj = Student(username, email, password, student_id)
                    self.students.append(student_obj)
        else:
            print(f"Please check the subdirectory and file exists for {students_path}.")

if __name__ == "__main__":
    receptionist = Receptionist("John Doe", "john.doe@example.com", "password123", "Receptionist", "R001", 50000, "Receptionist of Mathematics")
    print(receptionist.username)
    print(receptionist.email)
    print(receptionist.password)
    print(receptionist.role)
    print(receptionist.staff_ID)
    print(receptionist.salary)
    pass