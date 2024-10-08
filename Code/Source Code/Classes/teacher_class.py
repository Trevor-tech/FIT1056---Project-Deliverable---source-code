import os
# Check if can get data from data folder.
print("Files in data directory:", os.listdir("../data"))
# Use an absolute path to the data directory
data_directory = os.path.abspath("../data")
from classes.staff_class import Staff

class Teacher(Staff):

    @staticmethod
    def authenticate(input_username_or_email, input_password):
        """
        Method to authenticate a Teacher user.

        Parameter(s):
        - input_username_or_email: str
        - input_password: str

        Returns:
        - an instance of Teacher corresponding to the username or email if successful,
          None otherwise
        """
        recept_path = os.path.join("../data/teachers.txt")   
        if os.path.exists(recept_path):
            with open(recept_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                # Sequence unpacking: 
                # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
                username, email, password, role, teacher_ID, salary, staff_info = line.strip("\n").split(",")
                
                if input_username_or_email == username or input_username_or_email == email:
                    if input_password == password:
                        return Teacher(username, email, password, role, teacher_ID, salary, staff_info)
                    else:
                        return None # or return, or break
        else:
            print(f"Please check subdirectory and file {recept_path} exists.")
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