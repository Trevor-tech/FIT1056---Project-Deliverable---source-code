from Classes.course_class import Course

class Enrollment(Course):
    def __init__(self, course_ID, course_name, description, credits, enrolment_date):
        super().__init__(course_ID, course_name, description, credits)
        self.enrolment_date = enrolment_date

    def enroll_unit(self, unit_ID, unit_name):
        if unit_ID not in self.enrolled_units:
            self.enrolled_units.append((unit_ID, unit_name))
            print(f"Unit {unit_name} (ID: {unit_ID}) enrolled successfully.")
        else:
            print(f"Unit {unit_name} (ID: {unit_ID}) is already enrolled.")

    def get_enrolment_status(self):
        print("Enrolled Units:")
        for unit in self.enrolled_units:
            print(f"Unit ID: {unit[0]}, Unit Name: {unit[1]}")


    
if __name__ == "__main__":
    enrollment = Enrollment("C001", "Mathematics", "Introduction to Mathematics", "3", "2024-01-01")
    print(enrollment.course_ID)
    print(enrollment.course_name)
    print(enrollment.description)
    print(enrollment.credits)
    print(enrollment.enrolment_date)

 


