from classes.receptionist_class import Receptionist

class Payment(Receptionist):
    def __init__(self, username, email, password, role, staff_type, staff_ID, salary, staff_info):
        super().__init__(username, email, password, role, staff_type, staff_ID, salary, staff_info)

if __name__ == "__main__":  
    payment = Payment("John Doe", "john.doe@example.com", "password123", "payment", "Payment", "P001", 50000, "Payment of Mathematics")
    print(payment.username)
    print(payment.email)
    print(payment.password)
    print(payment.role)
    print(payment.staff_type)
    print(payment.staff_ID)
    print(payment.salary)
    print(payment.staff_info)
