from user_class import User

class Student(User):
    def __init__(self, username, email, password, student_ID):
        super().__init__(username, email, password)
        self.__student_ID = student_ID

    def submit_assignment(self):
        pass

    def view_feedback(self):
        pass


