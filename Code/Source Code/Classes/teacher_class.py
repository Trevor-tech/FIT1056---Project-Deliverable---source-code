
from staff_class import Staff

class Teacher(Staff):
    def __init__(self, username, email, password, role, staff_ID, salary, staff_info, teacher_ID):
        super().__init__(username, email, password, role, staff_ID, salary, staff_info)

    def grade_assignment(self):
        pass

    def create_assignment(self):
        pass