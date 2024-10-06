from Classes.user_class import User

class Staff(User):
    def __init__(self, username, email, password, role, staff_type, staff_ID, salary, staff_info):
        super().__init__(username, email, password, role)
        self.staff_type = staff_type
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
