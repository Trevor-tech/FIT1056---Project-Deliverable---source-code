import os
from classes.user_class import User

class Student(User):
    
    @staticmethod
    def authenticate(input_username_or_email, input_password):
        """
        Method to authenticate a Student user.

        Parameter(s):
        - input_username_or_email: str
        - input_password: str

        Returns:
        - an instance of Student corresponding to the username or email if successful,
          None otherwise
        """
        recept_path = "./Data/students.txt"
        if os.path.exists(recept_path):
            with open(recept_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                # Sequence unpacking: 
                # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
                username, email, password, role, recept_id, salary, staff_info = line.strip("\n").split(",")
                
                if input_username_or_email == username or email:
                    if input_password == password:
                        return Student(username, email, password, role, recept_id, salary, staff_info)
                    else:
                        return None # or return, or break
        else:
            print(f"Please check subdirectory and file {recept_path} exists.")
        pass
    def __init__(self, username, email, password, student_ID):
        super().__init__(username, email, password)
        self.student_ID = student_ID

    def submit_assignment(self):
        pass

    def view_feedback(self):
        pass

'''
if __name__ == "__main__":      
    student = Student("John Doe", "john.doe@example.com", "password123", "S001")
    print(student.username)
    print(student.email)
    print(student.password)
    print(student.student_ID)
'''