from user_class import User

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