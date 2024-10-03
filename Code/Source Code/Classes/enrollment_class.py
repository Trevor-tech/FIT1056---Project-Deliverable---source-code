from course_class import Course

class Enrollment(Course):
    def __init__(self, course_ID, course_name, description, credits, enrolment_date):
        super().__init__(course_ID, course_name, description, credits)
        self.enrolment_date = enrolment_date
    
    def get_enrolment_status(self):
        pass