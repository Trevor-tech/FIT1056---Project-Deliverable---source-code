from Classes.course_class import Course

class Certificate(Course):
    def __init__(self, course_ID, course_name, credits):
        super().__init__(course_ID, course_name, credits)

if __name__ == "__main__":
    certificate = Certificate("C001", "Mathematics", "3")
    print(certificate.course_ID)
    print(certificate.course_name)
    print(certificate.credits)


