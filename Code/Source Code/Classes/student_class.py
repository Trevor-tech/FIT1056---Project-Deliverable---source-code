import os
import sys
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
        recept_path = os.path.join("../data/students.txt") 
        if os.path.exists(recept_path):
            with open(recept_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                # Sequence unpacking: 
                # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
                username, email, password, student_ID = line.strip("\n").split(",")
                
                if input_username_or_email == username or input_username_or_email == email:
                    if input_password == password:
                        return Student(username, email, password, student_ID)
                    else:
                        return None
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


if __name__ == "__main__":      
    student = Student("John Doe", "john.doe@example.com", "password123", "S001")
    print(student.username)
    print(student.email)
    print(student.password)
    print(student.student_ID)

    # Test authentication
    authenticated_student = Student.authenticate("John Doe", "password123")
    if authenticated_student:
        print("Authentication successful")
        print(f"Authenticated student ID: {authenticated_student.student_ID}")
    else:
        print("Authentication failed")
