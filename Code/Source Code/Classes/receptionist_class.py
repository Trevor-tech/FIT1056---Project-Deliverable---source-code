import os
from classes.staff_class import Staff
from classes.teacher_class import Teacher
from classes.student_class import Student

class Receptionist(Staff):
    
    @staticmethod
    def authenticate(input_username_or_email, input_password):
        """
        Method to authenticate a Receptionist user.

        Parameter(s):
        - input_username_or_email: str
        - input_password: str

        Returns:
        - an instance of Receptionist corresponding to the username or email if successful,
          None otherwise
        """
        recept_path = os.path.join("../data/receptionist.txt")
        if os.path.exists(recept_path):
            with open(recept_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                # Sequence unpacking: 
                # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
                username, email, password, role, recept_id, salary, staff_info = line.strip("\n").split(",")
                
                if input_username_or_email == username or input_username_or_email == email:
                    if input_password == password:
                        return Receptionist(username, email, password, role, recept_id, salary, staff_info)
                    else:
                        return None # or return, or break
        else:
            print(f"Please check subdirectory and file {recept_path} exists.")
            
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