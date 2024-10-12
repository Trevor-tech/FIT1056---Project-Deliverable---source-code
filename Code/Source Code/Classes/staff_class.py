import os
from classes.user_class import User

class Staff(User):
    
    @staticmethod
    def authenticate(input_username, input_password):
        # Import here so that circular import error is avoided between staff_class.py and receptionist_class.py.
        from classes.receptionist_class import Receptionist
        from classes.teacher_class import Teacher

        if Receptionist.authenticate(input_username, input_password):
            return True
        elif Teacher.authenticate(input_username, input_password):
            return True
        else:
            return False
        pass

    def __init__(self, username, email, password, role, staff_ID, salary, staff_info):
        super().__init__(username, email, password, role)
        self.staff_ID = staff_ID
        self.__salary = salary
        self.__staff_info = staff_info
    
    def calculate_salary(self):
        pass

    def performance_analysis(self):
        pass

    def manage_students(self):
        pass

    def manage_course(self):
        pass

if __name__ == "__main__":
    staff = Staff("John Doe", "john.doe@example.com", "password123", "staff", "Teacher", "S001", 50000, "Teacher of Mathematics")
    print(staff.username)
    print(staff.email)
    print(staff.password)
    print(staff.role)
    print(staff.staff_type)
    print(staff.staff_ID)
    print(staff.salary)
    print(staff.staff_info)
    pass
