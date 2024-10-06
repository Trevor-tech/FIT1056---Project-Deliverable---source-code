from Classes.course_class import Course

class Enrollment(Course):
    def __init__(self, course_ID, course_name, description, credits, enrolment_date):
        super().__init__(course_ID, course_name, description, credits)
        self.enrolment_date = enrolment_date
    
    def get_enrolment_status(self):
        pass

if __name__ == "__main__":
    enrollment = Enrollment("C001", "Mathematics", "Introduction to Mathematics", "3", "2024-01-01")
    print(enrollment.course_ID)
    print(enrollment.course_name)
    print(enrollment.description)
    print(enrollment.credits)
    print(enrollment.enrolment_date)

