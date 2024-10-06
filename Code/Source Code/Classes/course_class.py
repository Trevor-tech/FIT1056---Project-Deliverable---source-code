class Course:
    def __init__(self, course_ID, course_name, description, credits):
        self.__course_ID = course_ID
        self.course_name = course_name
        self.description = description
        self.credits = credits
    
    def enrol_student(self):
        pass 

    def assign_teacher(self):
        pass

    def add_asssignment(self):
        pass

if __name__ == "__main__":
    course = Course("C001", "Mathematics", "Introduction to Mathematics", "3")
    print(course.course_ID)
    print(course.course_name)
    print(course.description)
    print(course.credits)


