from Classes.staff_class import Staff

class Receptionist(Staff):
    def __init__(self, username, email, password, role, staff_type, staff_ID, salary, staff_info):
        super().__init__(username, email, password, role, staff_type, staff_ID, salary, staff_info)

if __name__ == "__main__":
    receptionist = Receptionist("John Doe", "john.doe@example.com", "password123", "receptionist", "Receptionist", "R001", 50000, "Receptionist of Mathematics")
    print(receptionist.username)
    print(receptionist.email)
    print(receptionist.password)
    print(receptionist.role)
    print(receptionist.staff_type)
    print(receptionist.staff_ID)
    print(receptionist.salary)
