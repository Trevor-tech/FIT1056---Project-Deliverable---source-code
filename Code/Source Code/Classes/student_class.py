import os
import sys

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Navigate up to the Source Code directory
source_code_dir = os.path.dirname(os.path.dirname(current_file_path))

# Add the Source Code directory to the Python path
sys.path.insert(0, source_code_dir)

# Construct the path to the data directory
data_dir = os.path.join(source_code_dir, 'data')

class Student:
    @staticmethod
    def authenticate(input_username, input_password):
        students_path = os.path.join(data_dir, 'students.txt')
        if os.path.exists(students_path):
            with open(students_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                username, password, unit_code, enrollment_date, unit_credit = [item.strip() for item in line.strip("\n").split(",")]
                
                print(f"Checking: {username}, Input: {input_username}")  # Debug print
        
                if input_username == username:
                    if input_password == password:
                        return Student(username, password, unit_code, enrollment_date, unit_credit)
            print(f"Username {input_username} not found in file")  # Debug print
            return None
        else:
            print(f"Please check that the file {students_path} exists.")
            return None

    def __init__(self, username, password, student_ID, unit_code, enrollment_date, unit_credit):
        self.username = username
        self.password = password
        self.student_ID = student_ID
        self.unit_code = unit_code
        self.enrollment_date = enrollment_date
        self.unit_credit = unit_credit

    def submit_assignment(self):
        pass

    def view_feedback(self):
        pass

if __name__ == "__main__":
    pass