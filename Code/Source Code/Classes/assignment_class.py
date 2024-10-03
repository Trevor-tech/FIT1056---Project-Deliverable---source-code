from course_class import Course

class Assignment(Course):
    def __init__(self, course_ID, course_name, assignment_ID, title, due_date):
        super().__init__(course_ID, course_name)
        self.__assignment_ID = assignment_ID
        self.title = title
        self.due_date = due_date
    
    def get_status(self):
        pass

    def submit(self):
        pass