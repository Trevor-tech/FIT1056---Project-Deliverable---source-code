import os
from classes.user_class import User

class Staff(User):
    
    @staticmethod
    def authenticate(input_username, input_password):
        from classes.receptionist_class import Receptionist
        from classes.teacher_class import Teacher

        receptionist = Receptionist.authenticate(input_username, input_password)
        if receptionist:
            return receptionist
        teacher = Teacher.authenticate(input_username, input_password)
        if teacher:
            return teacher
        return None

    def __init__(self, username, email, password, role, staff_ID, salary, staff_info):
        super().__init__(username, email, password)
        self.role = role
        self.staff_ID = staff_ID
        self.salary = salary
        self.staff_info = staff_info
    
    def calculate_salary(self):
        pass

    def performance_analysis(self):
        pass

    def manage_students(self):
        pass

    def manage_course(self):
        pass

if __name__ == "__main__":
    staff = Staff("John Doe", "john.doe@example.com", "password123", "Teacher", "S001", 50000, "Teacher of Mathematics")
    print(staff.username)
    print(staff.email)
    print(staff.password)
    print(staff.role)
    print(staff.staff_ID)
    print(staff.salary)
    print(staff.staff_info)
