
from Classes.staff_class import Staff

class Teacher(Staff):
    def __init__(self, username, email, password, role, staff_ID, salary, staff_info, teacher_ID):
        super().__init__(username, email, password, role, staff_ID, salary, staff_info)

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