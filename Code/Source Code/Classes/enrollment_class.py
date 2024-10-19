from classes.course_class import Course

class Enrollment(Course):
    def __init__(self, course_ID, student_ID, last_name, first_name, enrolment_date, credit):
        super().__init__(course_ID, f"{last_name} {first_name}")
        self.student_ID = student_ID
        self.last_name = last_name
        self.first_name = first_name
        self.enrolment_date = enrolment_date
        self.credit = credit

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
    enrollment = Enrollment("C001", "123456789012", "Doe", "John", "2024-01-01", "6")
    print(enrollment.course_ID)
    print(enrollment.student_ID)
    print(enrollment.last_name)
    print(enrollment.first_name)
    print(enrollment.enrolment_date)
    print(enrollment.credit)
