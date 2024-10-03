from course_class import Course

class Certificate(Course):
    def __init__(self, course_ID, course_name, credits):
        super().__init__(course_ID, course_name, credits)