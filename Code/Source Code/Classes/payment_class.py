from receptionist_class import Receptionist

class Payment(Receptionist):
    def __init__(self, username, email, password, role, staff_type, staff_ID, salary, staff_info):
        super().__init__(username, email, password, role, staff_type, staff_ID, salary, staff_info)