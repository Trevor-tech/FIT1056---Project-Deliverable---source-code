from Classes.staff_class import Staff

class Receptionist(Staff):
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
        recept_path = "./Data/receptionist.txt"
        if os.path.exists(recept_path):
            with open(recept_path, "r", encoding="utf8") as rf:
                lines = rf.readlines()
            for line in lines:
                # Sequence unpacking: 
                # https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences
                recept_id, first_name, last_name, contact_num, username, email, password = line.strip("\n").split(",")
                
                if input_username_or_email == username or email:
                    if input_password == password:
                        return ReceptionistUser(recept_id, first_name, last_name, contact_num, input_username, input_password)
                    else:
                        return None # or return, or break
        else:
            print(f"Please check subdirectory and file {recept_path} exists.")
            
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
    pass
